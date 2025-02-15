# OTE Algorithms

This folder contains sub-projects implementing [OTE SDK](../ote_sdk) Task interfaces for different algorithms.
Every sub-project is fully indepedent from each other, and each of them has its own dependencies and `init_venv.sh` script to initialize virtual environment.

## Anomaly Classification

| ID                               | Name  | Complexity (GFlops) | Model size (MB) | Path                                               |
| -------------------------------- | ----- | ------------------- | --------------- | -------------------------------------------------- |
| ote_anomaly_classification_padim | PADIM | 3.9                 | 168.4           | anomaly/configs/classification/padim/template.yaml |
| ote_anomaly_classification_stfpm | STFPM | 5.6                 | 21.1            | anomaly/configs/classification/stfpm/template.yaml |

## Anomaly Detection

| ID                          | Name  | Complexity (GFlops) | Model size (MB) | Path                                          |
| --------------------------- | ----- | ------------------- | --------------- | --------------------------------------------- |
| ote_anomaly_detection_padim | PADIM | 3.9                 | 168.4           | anomaly/configs/detection/padim/template.yaml |
| ote_anomaly_detection_stfpm | STFPM | 5.6                 | 21.1            | anomaly/configs/detection/stfpm/template.yaml |

## Anomaly Segmentation

| ID                             | Name  | Complexity (GFlops) | Model size (MB) | Path                                             |
| ------------------------------ | ----- | ------------------- | --------------- | ------------------------------------------------ |
| ote_anomaly_segmentation_padim | PADIM | 3.9                 | 168.4           | anomaly/configs/segmentation/padim/template.yaml |
| ote_anomaly_segmentation_stfpm | STFPM | 5.6                 | 21.1            | anomaly/configs/segmentation/stfpm/template.yaml |

## Image Classification

| ID                                                | Name                  | Complexity (GFlops) | Model size (MB) | Path                                                                                           |
| ------------------------------------------------- | --------------------- | ------------------- | --------------- | ---------------------------------------------------------------------------------------------- |
| Custom_Image_Classification_MobileNet-V3-large-1x | MobileNet-V3-large-1x | 0.44                | 4.29            | model-preparation-algorithm/configs/classification/mobilenet_v3_large_1_cls_incr/template.yaml |
| Custom_Image_Classification_EfficinetNet-B0       | EfficientNet-B0       | 0.81                | 4.09            | model-preparation-algorithm/configs/classification/efficientnet_b0_cls_incr/template.yaml      |
| Custom_Image_Classification_EfficientNet-V2-S     | EfficientNet-V2-S     | 5.76                | 20.23           | model-preparation-algorithm/configs/classification/efficientnet_v2_s_cls_incr/template.yaml    |

## Object Detection

| ID                                | Name  | Complexity (GFlops) | Model size (MB) | Path                                                                                  |
| --------------------------------- | ----- | ------------------- | --------------- | ------------------------------------------------------------------------------------- |
| Custom_Object_Detection_YOLOX     | YOLOX | 6.5                 | 20.4            | model-preparation-algorithm/configs/detection/cspdarknet_yolox_cls_incr/template.yaml |
| Custom_Object_Detection_Gen3_SSD  | SSD   | 9.4                 | 7.6             | model-preparation-algorithm/configs/detection/mobilenetv2_ssd_cls_incr/template.yaml  |
| Custom_Object_Detection_Gen3_ATSS | ATSS  | 20.6                | 9.1             | model-preparation-algorithm/configs/detection/mobilenetv2_atss_cls_incr/template.yaml |

## Instance Segmentation (Object Counting)

| ID                                                             | Name                     | Complexity (GFlops) | Model size (MB) | Path                                                                                             |
| -------------------------------------------------------------- | ------------------------ | ------------------- | --------------- | ------------------------------------------------------------------------------------------------ |
| Custom_Counting_Instance_Segmentation_MaskRCNN_EfficientNetB2B | MaskRCNN-EfficientNetB2B | 68.48               | 13.27           | model-preparation-algorithm/configs/instance-segmentation/efficientnetb2b_maskrcnn/template.yaml |
| Custom_Counting_Instance_Segmentation_MaskRCNN_ResNet50        | MaskRCNN-ResNet50        | 533.8               | 177.9           | model-preparation-algorithm/configs/instance-segmentation/resnet50_maskrcnn/template.yaml        |

## Rotated Object Detection

| ID                                                                          | Name                     | Complexity (GFlops) | Model size (MB) | Path                                                                                         |
| --------------------------------------------------------------------------- | ------------------------ | ------------------- | --------------- | -------------------------------------------------------------------------------------------- |
| Custom_Rotated_Detection_via_Instance_Segmentation_MaskRCNN_EfficientNetB2B | MaskRCNN-EfficientNetB2B | 68.48               | 13.27           | model-preparation-algorithm/configs/rotated-detection/efficientnetb2b_maskrcnn/template.yaml |
| Custom_Rotated_Detection_via_Instance_Segmentation_MaskRCNN_ResNet50        | MaskRCNN-ResNet50        | 533.8               | 177.9           | model-preparation-algorithm/configs/rotated-detection/resnet50_maskrcnn/template.yaml        |

## Semantic Segmentation

| ID                                                  | Name               | Complexity (GFlops) | Model size (MB) | Path                                                                                  |
| --------------------------------------------------- | ------------------ | ------------------- | --------------- | ------------------------------------------------------------------------------------- |
| Custom_Semantic_Segmentation_Lite-HRNet-s-mod2_OCR  | Lite-HRNet-s-mod2  | 1.82                | 3.5             | model-preparation-algorithm/configs/segmentation/ocr-lite-hrnet-s-mod2/template.yaml  |
| Custom_Semantic_Segmentation_Lite-HRNet-18_OCR      | Lite-HRNet-18      | 3.45                | 4.5             | model-preparation-algorithm/configs/segmentation/ocr-lite-hrnet-18/template.yaml      |
| Custom_Semantic_Segmentation_Lite-HRNet-18-mod2_OCR | Lite-HRNet-18-mod2 | 3.63                | 4.8             | model-preparation-algorithm/configs/segmentation/ocr-lite-hrnet-18-mod2/template.yaml |
| Custom_Semantic_Segmentation_Lite-HRNet-x-mod3_OCR  | Lite-HRNet-x-mod3  | 13.97               | 6.4             | model-preparation-algorithm/configs/segmentation/ocr-lite-hrnet-x-mod3/template.yaml  |
