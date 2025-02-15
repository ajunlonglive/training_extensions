# Copyright (C) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import cv2
import numpy as np
from typing import Any, Dict, Iterable, Union
from ote_sdk.utils.argument_checks import check_input_parameters_type


try:
    from openvino.model_zoo.model_api.models.classification import Classification
    from openvino.model_zoo.model_api.models.types import BooleanValue, DictValue
    from openvino.model_zoo.model_api.models.utils import pad_image
except ImportError as e:
    import warnings
    warnings.warn("ModelAPI was not found.")


class OteClassification(Classification):
    __model__ = 'ote_classification'

    def __init__(self, model_adapter, configuration=None, preload=False):
        super().__init__(model_adapter, configuration, preload)
        if self.hierarchical:
            logits_range_dict = self.multihead_class_info.get('head_idx_to_logits_range', False)
            if logits_range_dict:  #  json allows only string key, revert to integer.
                self.multihead_class_info['head_idx_to_logits_range'] = {int(k):v for k,v in logits_range_dict.items()}

    @classmethod
    def parameters(cls):
        parameters = super().parameters()
        parameters['resize_type'].update_default_value('standard')
        parameters.update({
            'multilabel': BooleanValue(default_value=False),
            'hierarchical': BooleanValue(default_value=False),
            'multihead_class_info': DictValue(default_value={})
        })

        return parameters

    def _check_io_number(self, inp, outp):
        pass

    def _get_outputs(self):
        layer_name = 'logits'
        for name, meta in self.outputs.items():
            if 'logits' in meta.names:
                layer_name = name
        layer_shape = self.outputs[layer_name].shape

        if len(layer_shape) != 2 and len(layer_shape) != 4:
            raise RuntimeError('The Classification model wrapper supports topologies only with 2D or 4D output')
        if len(layer_shape) == 4 and (layer_shape[2] != 1 or layer_shape[3] != 1):
            raise RuntimeError('The Classification model wrapper supports topologies only with 4D '
                               'output which has last two dimensions of size 1')
        if self.labels:
            if (layer_shape[1] == len(self.labels) + 1):
                self.labels.insert(0, 'other')
                self.logger.warning("\tInserted 'other' label as first.")
            if layer_shape[1] != len(self.labels):
                raise RuntimeError("Model's number of classes and parsed "
                                'labels must match ({} != {})'.format(layer_shape[1], len(self.labels)))
        return layer_name

    @check_input_parameters_type()
    def preprocess(self, image: np.ndarray):
        meta = {'original_shape': image.shape}
        resized_image = self.resize(image, (self.w, self.h))
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR)
        meta.update({'resized_shape': resized_image.shape})
        if self.resize_type == 'fit_to_window':
            resized_image = pad_image(resized_image, (self.w, self.h))
        resized_image = self.input_transform(resized_image)
        resized_image = self._change_layout(resized_image)
        dict_inputs = {self.image_blob_name: resized_image}
        return dict_inputs, meta

    @check_input_parameters_type()
    def postprocess(self, outputs: Dict[str, np.ndarray], metadata: Dict[str, Any]):
        logits = outputs[self.out_layer_name].squeeze()
        if self.multilabel:
            return get_multilabel_predictions(logits)
        if self.hierarchical:
            return get_hierarchical_predictions(logits, self.multihead_class_info)

        return get_multiclass_predictions(logits)

    @check_input_parameters_type()
    def postprocess_aux_outputs(self, outputs: Dict[str, np.ndarray], metadata: Dict[str, Any]):
        saliency_map = outputs['saliency_map'][0]
        repr_vector = outputs['feature_vector'].reshape(-1)

        logits = outputs[self.out_layer_name].squeeze()

        if self.multilabel:
            probs = sigmoid_numpy(logits)
        elif self.hierarchical:
            probs = activate_multihead_output(logits, self.multihead_class_info)
        else:
            probs = softmax_numpy(logits)

        act_score = float(np.max(probs) - np.min(probs))

        return probs, saliency_map, repr_vector, act_score

@check_input_parameters_type()
def sigmoid_numpy(x: np.ndarray):
    return 1. / (1. + np.exp(-1. * x))


@check_input_parameters_type()
def softmax_numpy(x: np.ndarray, eps: float = 1e-9):
    x = np.exp(x)
    inf_ind = np.isinf(x)
    total_infs = np.sum(inf_ind)
    if total_infs > 0:
        x[inf_ind] = 1. / total_infs
        x[~inf_ind] = 0
    else:
        x /= np.sum(x) + eps
    return x


@check_input_parameters_type()
def activate_multihead_output(logits: np.ndarray, multihead_class_info: dict):
    for i in range(multihead_class_info['num_multiclass_heads']):
        logits_begin, logits_end = multihead_class_info['head_idx_to_logits_range'][i]
        logits[logits_begin : logits_end] = softmax_numpy(logits[logits_begin : logits_end])

    if multihead_class_info['num_multilabel_classes']:
        logits_begin, logits_end = multihead_class_info['num_single_label_classes'], -1
        logits[logits_begin : logits_end] = softmax_numpy(logits[logits_begin : logits_end])

    return logits


@check_input_parameters_type()
def get_hierarchical_predictions(logits: np.ndarray, multihead_class_info: dict,
                                 pos_thr: float = 0.5, activate: bool = True):
    predicted_labels = []
    for i in range(multihead_class_info['num_multiclass_heads']):
        logits_begin, logits_end = multihead_class_info['head_idx_to_logits_range'][i]
        head_logits = logits[logits_begin : logits_end]
        if activate:
            head_logits = softmax_numpy(head_logits)
        j = np.argmax(head_logits)
        label_str = multihead_class_info['all_groups'][i][j]
        predicted_labels.append((multihead_class_info['label_to_idx'][label_str], head_logits[j]))

    if multihead_class_info['num_multilabel_classes']:
        logits_begin, logits_end = multihead_class_info['num_single_label_classes'], -1
        head_logits = logits[logits_begin : logits_end]
        if activate:
            head_logits = sigmoid_numpy(head_logits)

        for i in range(head_logits.shape[0]):
            if head_logits[i] > pos_thr:
                label_str = multihead_class_info['all_groups'][multihead_class_info['num_multiclass_heads'] + i][0]
                predicted_labels.append((multihead_class_info['label_to_idx'][label_str], head_logits[i]))

    return predicted_labels


@check_input_parameters_type()
def get_multiclass_predictions(logits: np.ndarray, activate: bool = True):

    index = np.argmax(logits)
    if activate:
        logits = softmax_numpy(logits)
    return [(index, logits[index])]


@check_input_parameters_type()
def get_multilabel_predictions(logits: np.ndarray, pos_thr: float = 0.5, activate: bool = True):
    if activate:
        logits = sigmoid_numpy(logits)
    scores = []
    indices = []
    for i in range(logits.shape[0]):
        if logits[i] > pos_thr:
            indices.append(i)
            scores.append(logits[i])

    return list(zip(indices, scores))
