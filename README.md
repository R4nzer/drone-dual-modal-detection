# Drone-Based Dual-Modal Vehicle Detection

Dual-modal (RGB + Infrared) object detection based on YOLOv5, designed for robust vehicle detection from UAV platforms under challenging lighting and weather conditions.

## Overview

This project extends YOLOv5 with a dual-backbone architecture that fuses RGB and infrared (IR) features for vehicle detection. By leveraging complementary modalities, the model maintains detection accuracy in low-light, fog, and other adverse conditions where RGB-only detectors fail.

**Key features:**
- Dual-backbone feature extraction for RGB and IR inputs
- Mid-level feature fusion via custom `Concat3` module
- Attention-augmented architecture (`attentionuav7.yaml`)
- Data preprocessing pipeline for the [DroneVehicle](https://github.com/VisDrone/DroneVehicle) dataset
- GradCAM visualization support for model interpretability

## Installation

```bash
conda create -n dual-modal python=3.8
conda activate dual-modal
pip install -r requirements.txt
```

## Dataset Preparation

### 1. Convert to Grayscale & Preprocess

```bash
python data/rgb2gray.py
python data/imageprocess.py
python data/xml2txt.py
```

### 2. Generate Train/Val/Test Splits

Place your `images`, `images2` (IR), and `labels` folders under `data/`, then:

```bash
python data/split_train_val.py
python data/voc_label.py
python data/voc_label2.py
```

This generates `train.txt`, `train2.txt`, `val.txt`, `val2.txt`, `test.txt`, `test2.txt`.

### 3. Configure Dataset YAML

Edit `data/dual.yaml` to point to the generated splits:

```yaml
train: data/train.txt
train2: data/train2.txt
val: data/val.txt
val2: data/val2.txt
test: data/test.txt
nc: 4
names: ['car', 'truck', 'bus', 'van']
```

## Training

```bash
python train.py \
  --data data/dual.yaml \
  --cfg models/attentionuav7.yaml \
  --weights weights/yolov5s.pt \
  --batch-size 2 \
  --epochs 50
```

## Inference

```bash
python detect.py \
  --weights weights/dual.pt \
  --source data/test_images \
  --source2 data/test_images2
```

For GradCAM visualization:

```bash
python dualdetectchange.py \
  --weights weights/dual.pt \
  --source data/test_images \
  --source2 data/test_images2
```

## Validation

```bash
python val.py --weights weights/dual.pt --data data/dual.yaml
```

## Model Architecture

The dual-modal architecture uses two separate backbone pathways for RGB and IR inputs, fused at intermediate layers through the `Concat3` module. The model configuration is defined in `models/attentionuav7.yaml`.

| Component | Description |
|-----------|-------------|
| Backbone 1 | Shallow feature extraction (shared early layers) |
| Backbone 2 | Deep dual-pathway processing with feature fusion |
| Head | YOLOv5 detection head |


## Acknowledgements

This project builds upon [YOLOv5](https://github.com/ultralytics/yolov5) by Ultralytics (GPL-3.0). The DroneVehicle dataset is provided by the [VisDrone](https://github.com/VisDrone/DroneVehicle) project.

## License

This project is released under the GPL-3.0 License, inherited from YOLOv5.
