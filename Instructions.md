
# Beginner-Friendly Instructions to Set Up and Use the Code
# How to Set Up the Code

Welcome! This guide is designed to help you set up your environment and run the provided code seamlessly. Follow these steps carefully, and you'll be ready to go in no time.

---

## Step 1: Install Python

Before starting, make sure Python is installed on your computer. Follow these steps:

1. **Download Python**:  
   Go to the [official Python website](https://www.python.org/downloads/) and download the latest version for your operating system.

2. **Install Python**:  
   - Run the downloaded installer.
   - Check the box that says **"Add Python to PATH"** before proceeding with the installation.
   - Follow the installation wizard and complete the setup.

3. **Verify Installation**:  
   Open a terminal or command prompt and type:
   ```bash
   python --version
   ```
   If Python is installed correctly, you'll see the installed version number.

---

## Step 2: Install Anaconda

Anaconda is a comprehensive platform that simplifies working with Python and data science tools.

1. **Download Anaconda**:  
   Visit the [Anaconda website](https://www.anaconda.com/products/distribution) and download the latest version for your operating system.

2. **Install Anaconda**:  
   - Run the installer and follow the on-screen instructions.
   - Choose to add Anaconda to your PATH (optional but recommended).

3. **Verify Installation**:  
   Open a terminal (or Anaconda Prompt) and type:
   ```bash
   conda --version
   ```
   You should see the installed version of Conda.

---

## Step 3: Set Up Your Integrated Development Environment (IDE)

To run the code, you need an IDE. We recommend **Jupyter Notebook**, which is included with Anaconda.

### Why Jupyter Notebook?  
Jupyter Notebook is a user-friendly, interactive environment perfect for running Python code and visualizing data.

### Steps to Open Jupyter Notebook:
If you installed Anaconda, you already have Jupyter Notebook installed. You can simply search for "Jupyter Notebook" in your operating system's search bar and open it. Once opened, a web browser will display the Jupyter Notebook dashboard where you can manage and run your notebooks.

---

## Step 4: Download the GitHub Repository

The code is hosted on GitHub. Follow these steps to download and use it:

1. **Clone or Download the Repository**:  
   - Navigate to the [code repository](https://github.com/shumaly/4S-SROF) and either click on **"Code" > "Download ZIP"** or clone the repository using:
     ```bash
     git clone <repository-url>
     ```

2. **Save in an Easy-to-Find Location**:  
   - If you are using Jupyter Notebook, it's best to save the repository in:
     ```
     C:/Users/[your_admin_name]/
     ```
   - This ensures you can quickly access it from the Jupyter Notebook dashboard.

---

## Step 6: Install Required Libraries

This project requires the following libraries and specific versions. Some of these libraries are automatically included when you install Anaconda. The list below clarifies which libraries are pre-installed and which need manual installation.

### Libraries and Versions
Below is a list of the libraries and their corresponding versions used in this project:

| Library       | Version | Link                                      | Pre-installed with Anaconda? |
|---------------|---------|-------------------------------------------|------------------------------|
| TensorFlow    | 2.5.0   | [tensorflow](https://pypi.org/project/tensorflow/) | No                          |
| Keras         | 2.9.0   | [keras](https://pypi.org/project/keras/) | No                          |
| OpenCV (cv2)  | 4.5.4   | [opencv-python](https://pypi.org/project/opencv-python/) | No                          |
| Natsort       | 8.4.0   | [natsort](https://pypi.org/project/natsort/) | No                          |
| SciPy         | 1.7.1   | [scipy](https://pypi.org/project/scipy/) | Yes                         |
| Pillow (PIL)  | 8.4.0   | [Pillow](https://pypi.org/project/Pillow/) | Yes                         |
| NumPy         | 1.20.3  | [numpy](https://pypi.org/project/numpy/) | Yes                         |
| Pandas        | 1.3.4   | [pandas](https://pypi.org/project/pandas/) | Yes                         |
| Matplotlib    | 3.4.3   | [matplotlib](https://pypi.org/project/matplotlib/) | Yes                         |

### How to Install
#### For Libraries Not Pre-installed
1. Open your terminal (or Anaconda Prompt).
2. Install the libraries manually using the following commands:
   ```bash
   pip install tensorflow
   pip install keras
   pip install opencv-python
   pip install natsort

---

## Step 6: Open the Code in Jupyter Notebook

1. Launch Jupyter Notebook:

2. Navigate to the downloaded repository:
   - Go to the directory where you saved the GitHub repository (e.g., `C:/Users/[your_admin_name]/`).
   - Open the file named `Control Panel.ipynb`.

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
   Open the Jupyter Notebook file (e.g., `Control Panel.ipynb`) in your Jupyter Notebook environment.

2. **Run the First Cell**:  
   - The first cell contains the code to load libraries and define necessary functions.
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
   - **`SR_result`**: This folder contains a file named `result.xlsx` with the analyzed features, including the following columns:
     - **`file number`**: The frame number.
     - **`time (s)`**: Time in seconds.
     - **`x_center (cm)`**: X-coordinate of the droplet's center.
     - **`adv (degree)`**: Advancing contact angle in degrees.
     - **`rec (degree)`**: Receding contact angle in degrees.
     - **`contact_line_length (cm)`**: Length of the contact line in centimeters.
     - **`y_center (cm)`**: Y-coordinate of the droplet's center.
     - **`middle_angle_degree (degree)`**: Middle angle of the droplet in degrees.
     - **`velocity (cm/s)`**: Droplet velocity in centimeters per second.
    

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

Adhering to these guidelines will help you avoid potential errors and ensure the analysis runs smoothly.


