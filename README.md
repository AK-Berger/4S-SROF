# Deep Learning to Analyze Sliding Drops ([Cite Us](#citation))

The **4S-SROF toolkit** is designed to solve existing challenges in analyzing the sliding motion of drops on tilted plates. It enables researchers to conduct detailed studies by considering a wide range of variables and their correlations.

Key features include:
- **Super-Resolution Enhancement**: The toolkit enlarges images by an up-scale ratio of 3 using a super-resolution model trained on a dataset of 14,000 sliding drop images.
- **Comprehensive Analysis**: Extracts various criteria from the super-resolution images to provide precise insights into drop behavior.
- **Optimized Contact Angle Measurement**: Contact angles are measured using an optimized polynomial method, as described in the accompanying manuscript.

The 4S-SROF toolkit streamlines complex image processing tasks, empowering researchers with high-quality data for in-depth analysis.

![graphical abstract](https://user-images.githubusercontent.com/57271994/194614949-8736973c-4df3-4449-9a21-bc2423405648.png)

---
# Data Information

## Tutorial

- **File:** `tutorial.ipynb`

    This tutorial contains examples and outputs explaining how the toolkit works step-by-step. It is designed to help researchers understand each step and its parameters. A comprehensive example is provided at the end, demonstrating the extraction of all criteria from a high-speed camera video.

---

## Drop Profile Video

- **File:** `drop_profile.mp4`

    This video illustrates a sliding drop on a sample with a defect in the middle:

    - The **first drop** in the upper part of the video is the real drop image after preprocessing. Key preprocessing steps include:
      - Calculating the tilt angle and aligning frames horizontally.
      - Removing noise and background.
      - Detecting the drop position (marked by red lines).
    - The **second drop** (larger image) represents the drop after applying a super-resolution model.
    - Below that, the **drop contour** is extracted, and parameters such as contact angles (CAs), drop height, and drop length are displayed.
    - On the left, four plots analyze how the drop slides over a defected sample.

[Preview the video on GitHub](https://github.com/AK-Berger/4S-SROF/assets/57271994/4130c91c-193a-4bf9-b08d-e2df878f88bf)

---

## ESPCN Super-Resolution Model Weights

- **File:** `SuperRes_weights.h5`

    This file contains the weights for the modified ESPCN super-resolution model, trained on 14,000 sliding drop images.

---

## Python Files

The following `.py` files are included in the toolkit and provide functions for related image processing tasks:

- `angle_detection.py`
- `baseline_detection.py`
- `criteria_definition.py`
- `edge_superres.py`
- `tools.py`
- `visualization.py`

These scripts are essential for researchers working with this toolkit.

---

## Dataset

- **Description:** The dataset contains 14,000 sliding drop images used to train the modified super-resolution model.
- **Access:** [Download the dataset](https://www.kaggle.com/datasets/sajjdeus/4s-srof)

---

## Samples

- **Description:** The `samples` folder contains two sliding drop examples. Pre-run outputs are included in `tutorial.ipynb`. 
- **Usage:** 
  - To re-run the tutorial, add the `samples` folder to your working directory.
  - Alternatively, replace the video frames with your own dataset.

---
# Libraries and Versions

Below is a list of the libraries and their corresponding versions used in this project:

| Library      | Version | Link                                                 |
|--------------|---------|------------------------------------------------------|
| TensorFlow   | 2.5.0   | [tensorflow](https://pypi.org/project/tensorflow/)   |
| Keras        | 2.9.0   | [keras](https://pypi.org/project/keras/)             |
| OpenCV (cv2) | 4.5.4   | [opencv-python](https://pypi.org/project/opencv-python/) |
| SciPy        | 1.7.1   | [scipy](https://pypi.org/project/scipy/)             |
| Pillow (PIL) | 8.4.0   | [Pillow](https://pypi.org/project/Pillow/)           |
| NumPy        | 1.20.3  | [numpy](https://pypi.org/project/numpy/)             |
| Pandas       | 1.3.4   | [pandas](https://pypi.org/project/pandas/)           |
| Matplotlib   | 3.4.3   | [matplotlib](https://pypi.org/project/matplotlib/)   |
| Natsort      | 8.4.0   | [natsort](https://pypi.org/project/natsort/)         |

Each library name links to its official PyPI page for more details.


---
# Citation

If you find **"Deep Learning to Analyze Sliding Drops"** useful for your research, please consider citing the paper using the following information:

<div style="position: relative;">
  <pre>
    <code>
@article{shumaly2023deep,
  title={Deep learning to analyze sliding drops},
  author={Shumaly, Sajjad and Darvish, Fahimeh and Li, Xiaomei and Saal, Alexander and Hinduja, Chirag and Steffen, Werner and Kukharenko, Oleksandra and Butt, Hans-J{\"u}rgen and Berger, R{\"u}diger},
  journal={Langmuir},
  volume={39},
  number={3},
  pages={1111--1122},
  year={2023},
  publisher={ACS Publications}
}
    </code>
  </pre>
  <button onclick="copyText(this)" style="position: absolute; top: 0; right: 0;"></button>
</div>





---
