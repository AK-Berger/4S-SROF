
# Setup and Usage Guide

This document explains how to configure the environment and run the 4S-SROF analysis workflow.

---

## Step 1: Install Anaconda or Miniconda

The recommended setup for this project is a dedicated Conda environment. Install either:

1. **Anaconda**: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)  
2. **Miniconda**: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

After installation, verify that Conda is available:

```bash
conda --version
```

---

## Step 2: Create the Project Environment

This project is currently aligned with the `srof` environment and tested with Python 3.9.

1. Create the environment:

```bash
conda create -n srof python=3.9
```

2. Activate it:

```bash
conda activate srof
```

3. Confirm the Python version:

```bash
python --version
```

---

## Step 3: Download the GitHub Repository

The code is hosted on GitHub. Follow these steps to download and use it:

1. **Clone or Download the Repository**:  
   - Navigate to the [code repository](https://github.com/shumaly/4S-SROF) and either click on **"Code" > "Download ZIP"** or clone the repository using:
     ```bash
     git clone <repository-url>
     ```

2. **Save the Repository in a Convenient Location**:  
   - Choose any location that is easy for you to access from Jupyter Notebook or your file browser.
   - Keep the project files together so the notebook can access the input data, weights file, and package modules consistently.

---

## Step 4: Install Required Libraries

All required Python packages are maintained in `requirements.txt`. After activating the `srof` environment, install them with:

```bash
pip install -r requirements.txt
```

This approach is preferred over installing individual libraries manually, because it keeps the environment consistent with the tested project setup.

---

## Step 5: Set Up Jupyter Notebook

Jupyter Notebook provides the easiest way to run the analysis workflow interactively.

1. Register the environment as a notebook kernel:

```bash
python -m ipykernel install --user --name=srof --display-name "Python (srof)"
```

2. Launch Jupyter Notebook:

```bash
jupyter notebook
```

---

## Step 6: Open the Code in Jupyter Notebook

1. In the Jupyter interface, navigate to the downloaded repository.

2. Open the file named `analysis_workflow.ipynb`.

3. If prompted, select the `Python (srof)` kernel.

---

## You're All Set!
Now that everything is set up, you can use the code to its full potential. If you encounter any issues or have any questions, feel free to reach out.

---

# How to Use the Code

Follow the steps below to prepare your video frames and use the code effectively:

---

## Step 1: Prepare the Video Frames

1. **Locate the Folder**:  
   Go to the folder containing the exported high-speed camera video frames. Ensure that these frames are in `.tif` format.

2. **Remove Unnecessary Frames**:
   
   - **Keep a "No Droplet" Frame**:  
     Retain only one frame from the beginning where the droplet has not yet entered the video frames. This will serve as the initial "no droplet" reference frame.
   - **Before the Droplet Appears**:
     Remove all video frames that do not contain the droplet until you reach the first frame where the advancing and receding of the droplet are clearly visible (keep the "no droplet" reference frame).
   - **Margins**:  
     Ensure there is a margin of empty space between the droplet and the starting position of the frame. This margin should be approximately one-third of the droplet's length.
   - **After the Droplet Exits**:  
     Remove all video frames where the droplet is no longer in the frame or where the advancing and receding are not clear. Ensure the last frame also has a margin of empty space equivalent to one-third of the droplet's length.
     

## Step 2: Introducing Drop Slope

To prepare for drop slope analysis, follow the steps below:

1. **Create the "slope" Folder**:  
   In the directory containing your video frames, create a new folder and name it `slope` (all lowercase).

2. **Copy Relevant Frames**:  
   Identify the first and last frames that contain the droplet. Copy these frames into the `slope` folder.

3. **Rename the Frames**:  
   - Rename the first frame to `1.tif`.  
   - Rename the last frame to `2.tif`.

4. **Mark the Advancing Point**:  
   - Open `1.tif` and `2.tif` using Microsoft Paint.  
   - Select the **Pen** tool and choose the **red color**.  
   - On each frame, mark a single **red pixel** at the advancing point on the droplet's contact line.  
   - Save the marked images as `1.bmp` and `2.bmp` in the same `slope` folder.

Your `slope` folder should now contain the marked frames `1.bmp` and `2.bmp`, ready for further analysis.

## Step 3: Run the Code

Once you have prepared your video frames and introduced the drop slope, you can start running the code by following these instructions:

1. **Start the Notebook**:  
   Open the Jupyter Notebook file (e.g., `analysis_workflow.ipynb`) in your Jupyter Notebook environment.

2. **Run the First Cell**:  
   - The first cell loads the required libraries and imports the shared workflow helper functions from `srof/analysis_workflow.py`.
   - Simply run the cell by selecting it and pressing `Shift + Enter` (or `Ctrl + Enter`).  
   - This step initializes the environment and sets up the required tools for further analysis.

3. **Set Variables in the Second Cell**:  
   - Locate the second cell, which includes a section titled **"Set Variables"**. Adjust the following variables based on your experiment:
     - **`fps` (Frames Per Second)**:  
       Set this variable to match the frame rate of your high-speed camera. This ensures that the velocity calculations are scaled correctly.
     - **`cm_on_pixel_ratio`**:  
       This variable converts measurements from centimeters to pixels. While it has a default value, you should update it if you’ve changed the camera objective or the experimental setup.
     - **`error_handling_kernel_size`**:  
       This variable sets the kernel size for the `cv2.morphologyEx` function, which removes noise from the data. In a noisy environment, you can increase this value up to `11` to improve noise reduction.

## Step 4: Running the Second Cell

After setting the variables in the second cell, follow these steps:

1. **Execute the Second Cell**:  
   Run the second cell by selecting it and pressing `Shift + Enter` (or `Ctrl + Enter`).  

2. **Folders Created Automatically**:  
   After running the second cell, the program will create two new folders in your video frames directory:  
   - **`SR_edge`**: This folder contains the analyzed frame output for each video frame. These images can help you understand the reasons behind the changes observed in the results.  
   - **`SR_result`**: This folder contains a file named `result.xlsx` with the analyzed features. The workflow still exports the same 9 columns and does not add or remove any columns when saving. For Excel compatibility, the saved file uses these headers:
     - **`Video ID`**: Renamed from `file number`.
     - **`time (s)`**: Time in seconds.
     - **`x_center (cm)`**: X-coordinate of the droplet's center.
     - **`Advancing (degree)`**: Renamed from `adv (degree)`.
     - **`Receding (degree)`**: Renamed from `rec (degree)`.
     - **`Drop length (cm)`**: Renamed from `contact_line_length (cm)`.
     - **`Drop height (cm)`**: Renamed from `y_center (cm)`.
     - **`Velocity (cm/s)`**: Renamed from `velocity (cm/s)`.
     - **`Middle line angle (degree)`**: Renamed from `middle_angle_degree (degree)`.

   The notebook now uses platform-independent path handling, so the same workflow should work on Windows, macOS, and Linux as long as your experiment folders and files are prepared as described.
    

## Important Points

1. **Frame Naming Convention**:  
   - The names of the frames are typically formatted like this:
     ```
     1_50DEG_Glass2_PFOTS_Drop_1_C001H001S0001000155.tif
     ```
   - The last digits of the frame name are used to identify the `file number` variable in the analysis.  
     **Do not change these digits** when capturing videos using the high-speed camera. 
   - Avoid using dots (`.`) in the frame names. Instead, separate parts using underscores (`_`) to ensure compatibility with the code.
   - You can modify other aspects of the frame naming convention as needed.

2. **Droplet in Frame**:  
   - Ensure there is only **one droplet** visible in the video frames throughout the experiment.  
   - If even a few pixels of another droplet appear in the frames, the code might crash or produce incorrect results.
  
3. **Slope Folder**:  
   - If you plan to perform measurements for different droplet numbers or tilt angles **without altering the experimental setup**, you can reuse the `slope` folder created during the first experiment. Simply copy this folder to the new experiment directory, and there is no need to create a new `slope` folder.  
   - However, if the setup is adjusted (e.g., changing the surface or modifying the alignment), the relative angle between the camera and the sample may change. In such cases, you must create a new `slope` folder and generate fresh `.bmp` files to ensure accurate measurements.
