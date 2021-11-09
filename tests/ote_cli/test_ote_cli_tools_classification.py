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

import os
from subprocess import run

import pytest

from ote_cli.registry import Registry

from tests.ote_cli.common import get_some_vars, create_venv


args = {
    '--train-ann-file': '',
    '--train-data-roots': 'data/classification/train',
    '--val-ann-file': '',
    '--val-data-roots': 'data/classification/val',
    '--test-ann-files': '',
    '--test-data-roots': 'data/classification/val',
}

root = '/tmp/ote_cli/'
ote_dir = os.getcwd()

templates = Registry('external').filter(task_type='CLASSIFICATION').templates
templates_names = [template['name'] for template in templates]


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_train(template):
    template_dir, work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
    create_venv(algo_backend_dir, work_dir, template_work_dir)
    command_line = ['ote_train',
                    '--train-ann-file',
                    f'{os.path.join(ote_dir, args["--train-ann-file"])}',
                    '--train-data-roots',
                    f'{os.path.join(ote_dir, args["--train-data-roots"])}',
                    '--val-ann-file',
                    f'{os.path.join(ote_dir, args["--val-ann-file"])}',
                    '--val-data-roots',
                    f'{os.path.join(ote_dir, args["--val-data-roots"])}',
                    '--save-weights',
                    f'{template_work_dir}/trained.pth',
                    'params',
                    '--learning_parameters.max_num_epochs',
                    '2',
                    '--learning_parameters.batch_size',
                    '2']
    assert run(command_line, cwd=f'{template_dir}', env={'PATH':f'{work_dir}/venv/bin'}).returncode == 0


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_export(template):
    template_dir, work_dir, template_work_dir, _ = get_some_vars(template, root)
    command_line = ['ote_export',
                    '--labels',
                    'none',
                    '--load-weights',
                    f'{template_work_dir}/trained.pth',
                    f'--save-model-to',
                    f'{template_work_dir}/exported']
    assert run(command_line, cwd=f'{template_dir}', env={'PATH':f'{work_dir}/venv/bin'}).returncode == 0


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_eval(template):
    template_dir, work_dir, template_work_dir, _ = get_some_vars(template, root)
    command_line = ['ote_eval',
                    '--test-ann-file',
                    f'{os.path.join(ote_dir, args["--test-ann-files"])}',
                    '--test-data-roots',
                    f'{os.path.join(ote_dir, args["--test-data-roots"])}',
                    '--load-weights',
                    f'{template_work_dir}/trained.pth']
    assert run(command_line, cwd=f'{template_dir}', env={'PATH':f'{work_dir}/venv/bin'}).returncode == 0
