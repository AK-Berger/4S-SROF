
#importing libraries
import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image
import PIL
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array


# Define the DepthToSpace layer
class DepthToSpace(layers.Layer):
    def __init__(self, upscale_factor, **kwargs):
        super(DepthToSpace, self).__init__(**kwargs)
        self.upscale_factor = upscale_factor

    def call(self, inputs):
        return tf.nn.depth_to_space(inputs, self.upscale_factor)

# Build the model architecture and load the trained weights
def model_architecture(weight_address):
    # Initial values
    upscale_factor = 3
    channels = 1
    conv_args = {
        "activation": "relu",
        "kernel_initializer": "Orthogonal",
        "padding": "same",
    }
    # Model structure
    inputs = keras.Input(shape=(None, None, channels))
    x = layers.Conv2D(64, 5, **conv_args)(inputs)
    x = layers.Conv2D(64, 3, **conv_args)(x)
    x = layers.Conv2D(32, 3, **conv_args)(x)
    x = layers.Conv2D(channels * (upscale_factor ** 2), 3, **conv_args)(x)
    outputs = DepthToSpace(upscale_factor=upscale_factor)(x)
    
    # Load model
    model = keras.Model(inputs, outputs)
    model.load_weights(weight_address)
    
    return model

# Optimize model prediction with @tf.function
@tf.function
def predict(input_tensor, model):
    return model(input_tensor, training=False)

# Upscale the image using the optimized model and OpenCV
def upscale_image(model, img):
    # img is expected to be a NumPy array in RGB format
    # Convert image to YCrCb color space
    img_y_cr_cb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(img_y_cr_cb)

    # Normalize Y channel
    y = y_channel.astype("float32") / 255.0
    input_tensor = np.expand_dims(y, axis=0)  # Add batch dimension
    input_tensor = np.expand_dims(input_tensor, axis=-1)  # Add channel dimension

    # Model prediction
    input_tensor_tf = tf.convert_to_tensor(input_tensor)
    out = predict(input_tensor_tf, model)
    out_img_y = out[0, :, :, 0].numpy()  # Remove batch and channel dimensions
    out_img_y = (out_img_y * 255.0).clip(0, 255).astype("uint8")

    # Resize Cr and Cb channels to match the upscaled Y channel size
    height, width = out_img_y.shape
    cr_resized = cv2.resize(cr_channel, (width, height), interpolation=cv2.INTER_CUBIC)
    cb_resized = cv2.resize(cb_channel, (width, height), interpolation=cv2.INTER_CUBIC)

    # Merge channels and convert back to RGB color space
    out_img_y_cr_cb = cv2.merge([out_img_y, cr_resized, cb_resized])
    out_img_rgb = cv2.cvtColor(out_img_y_cr_cb, cv2.COLOR_YCrCb2RGB)

    # Apply Gaussian Blur
    out_img_rgb = cv2.GaussianBlur(out_img_rgb, (3, 3), 0)

    return out_img_rgb

#edge detection using canny and removing extra detected pixels
def edge_extraction_canny( upscaled_image, canny_v1=100, canny_v2=200):

    j_list_left=[]
    i_list_left=[]
    upscaled_image_canny=cv2.Canny(np.array(upscaled_image),canny_v1,canny_v2)
    #finding the external left side pixels
    for j in range(upscaled_image_canny.shape[0]-1,0,-1):
        for i in range(0,upscaled_image_canny.shape[1]):
            if upscaled_image_canny[j,i]!=0:
                j_list_left.append(j)
                i_list_left.append(i)
                break
    i_list_left=np.array(i_list_left)
    j_list_left=np.array(j_list_left)
    #finding the external right side pixels
    j_list_right=[]
    i_list_right=[]
    for j in range(upscaled_image_canny.shape[0]-1,0,-1):
        for i in range(upscaled_image_canny.shape[1]-1,0,-1):
            if upscaled_image_canny[j,i]!=0:
                j_list_right.append(j)
                i_list_right.append(i)
                break
    i_list_right=np.array(i_list_right)
    j_list_right=np.array(j_list_right)
    #finding the external up side pixels
    j_list_up=[]
    i_list_up=[]
    for i in range(upscaled_image_canny.shape[1]):
        for j in range(upscaled_image_canny.shape[0]):
            if upscaled_image_canny[j,i]!=0:
                j_list_up.append(j)
                i_list_up.append(i)
                break
    j_list_up=np.array(j_list_up)
    j_list_up=np.array(j_list_up)
    #merging all the external pixels   
    i_list= list(i_list_left) + list(i_list_right) + list(i_list_up)
    j_list= list(j_list_left) + list(j_list_right) + list(j_list_up)
    #delete duplicates
    i_list,j_list=list(zip(*list(set(zip(i_list,j_list)))))

    j_list=max(j_list)-j_list

    return(i_list,j_list)

#edge detection using a simple threshold to detect objects and removing extra detected pixels
def edge_extraction(upscaled_image, thr=40):

    j_list_left=[]
    i_list_left=[]
    upscaled_image=cv2.cvtColor(np.array(upscaled_image),cv2.COLOR_BGR2GRAY)
    #finding the external left side pixels
    for j in range(upscaled_image.shape[0]-1,0,-1):
        for i in range(0,upscaled_image.shape[1]):
            if upscaled_image[j,i]>thr:
                j_list_left.append(j)
                i_list_left.append(i)
                break
    i_list_left=np.array(i_list_left)
    j_list_left=np.array(j_list_left)
    #finding the external right side pixels
    j_list_right=[]
    i_list_right=[]
    for j in range(upscaled_image.shape[0]-1,0,-1):
        for i in range(upscaled_image.shape[1]-1,0,-1):
            if upscaled_image[j,i]>thr:
                j_list_right.append(j)
                i_list_right.append(i)
                break
    i_list_right=np.array(i_list_right)
    j_list_right=np.array(j_list_right)
    #finding the external up side pixels
    j_list_up=[]
    i_list_up=[]
    for i in range(upscaled_image.shape[1]):
        for j in range(upscaled_image.shape[0]):
            if upscaled_image[j,i]>thr:
                j_list_up.append(j)
                i_list_up.append(i)
                break
    j_list_up=np.array(j_list_up)
    j_list_up=np.array(j_list_up)
    #merging all the external pixels 
    i_list= list(i_list_left) + list(i_list_right) + list(i_list_up)
    j_list= list(j_list_left) + list(j_list_right) + list(j_list_up)
    #delete duplicates
    i_list,j_list=list(zip(*list(set(zip(i_list,j_list)))))

    j_list=max(j_list)-j_list

    return(i_list,j_list)

