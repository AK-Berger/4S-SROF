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

## Instructions

- **File:** `Instructions.md`  

    This document provides the complete setup and usage guide for the toolkit. It is organized into two main parts: environment setup and workflow execution.

    - **Environment Setup:**  
      Covers Conda installation, creation of the `srof` environment, dependency installation from `requirements.txt`, and Jupyter kernel registration.

    - **Workflow Usage:**  
      Describes how to prepare video frames, create and mark the `slope` folder, run the notebook, configure experiment-specific variables, and interpret the generated outputs.

---
## Analysis Workflow

- **File:** `analysis_workflow.ipynb`  

    This file contains the main executable notebook for the toolkit. It acts as the central workflow, calling package modules and libraries to perform the analysis. The notebook processes the video frames, extracts features, and generates the final `result.xlsx` file containing the analyzed time-series data.

    Shared helper functions used by the notebook now live in `srof/analysis_workflow.py`, which keeps the notebook setup cell cleaner and makes the workflow logic easier to maintain.

---
## Example Output

- **Release file:** `toolkit-output-example.zip`

    A ready-to-check example output package is available in the GitHub release:

    - [Download toolkit-output-example.zip](https://github.com/shumaly/4S-SROF/releases/download/v1.0.0/toolkit-output-example.zip)

    To try it:

    1. Download and extract `toolkit-output-example.zip`.
    2. Put the extracted example folder in the main project folder.
    3. Run `analysis_workflow.ipynb` on the sample input data.
    4. Compare your generated files with the example output folder to confirm the workflow is running correctly.

    This is a simple way for new users to test the toolkit, understand the folder structure, and see the expected output format before working with their own datasets.

---
## PFOTS Sample with a Defect

- **Release/sample data:** `PFOTS sample with a defect`

    This sample contains sliding drop video frames and related analysis assets that you can use as a practical example input for the toolkit.

    Recommended workflow:

    1. Place the sample folder in the main project directory.
    2. Open `analysis_workflow.ipynb`.
    3. Point the notebook to the sample folder and run the workflow.
    4. Review the generated outputs and compare them with the released example output package above.

    This gives users a quick end-to-end test case for learning the pipeline and checking that the toolkit is producing the expected results.

---


## Dataset

- **Description:** The dataset contains 14,000 sliding drop images used to train the modified super-resolution model.
- **Access:** [Download the dataset](https://www.kaggle.com/datasets/sajjdeus/4s-srof)

---

## Python Environment Setup Guide

The project is currently aligned with the `srof` Conda environment and has been tested with Python 3.9.

1. Create a Conda environment:

```sh
conda create -n srof python=3.9
```

2. Activate the environment:

```sh
conda activate srof
```

3. Install the project dependencies:

```sh
pip install -r requirements.txt
```

4. Register the environment as a Jupyter kernel:

```sh
python -m ipykernel install --user --name=srof --display-name "Python (srof)"
```

5. Start Jupyter Notebook:

```sh
jupyter notebook
```

Then open `analysis_workflow.ipynb` and select the `Python (srof)` kernel if needed.

---
## Citation

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
