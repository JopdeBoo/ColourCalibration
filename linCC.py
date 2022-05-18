import numpy as np
import colour
import cv2
import matplotlib.pyplot as plt
import linConversions as conv
import os
from PIL import Image

def sRGB_to_lin(rgb):
    # Converts array or list of sRGB values to linear RGB values
    rgb = np.array(rgb)/255
    linear = np.where(rgb<=0.04045, rgb/12.92, ((rgb+0.055)/1.055)**(2.4))
    return((linear*255).astype(np.uint8))

def ColourCorrect(image_lin, corrected_img_lin, corrected_img_sRGB, source_lin,
                  reference_RGB, terms):
    
    # Load in reference data and convert to linear RGB
    reference_RGB = np.loadtxt(reference_RGB, delimiter=",",
                               skiprows=1, usecols=(0, 1, 2))
    reference_lin = conv.sRGB_to_lin(reference_RGB)
    
    # Calculating the colour correction matrix and colour correcting the image
    # using the reference and source colour values
    CCM, colour_corrected=colour.characterisation.colour_correction_Cheung2004(
        image_lin, source_lin, reference_lin, terms)
    colour_corrected = colour_corrected.astype(int).clip(0,255)
    
    # Converting the linear images to sRGB
    image_sRGB = conv.lin_to_sRGB(image_lin)
    corrected_sRGB = conv.lin_to_sRGB(colour_corrected)
    
    # Plotting all images
    plt.imshow(image_lin)
    plt.title("Source linear")
    plt.show()
    
    plt.imshow(colour_corrected)
    plt.title("Corrected linear")
    plt.show()
        
    plt.imshow(image_sRGB)
    plt.title("Source sRGB")
    plt.show()
    
    plt.imshow(corrected_sRGB)
    plt.title("Corrected sRGB")
    plt.show()
    
    # Saving corrected images (cv2 works in BGR, so R and B are swapped)
    corrected_img_BGR_lin = colour_corrected[:,:,::-1]
    corrected_img_BGR_sRGB = corrected_sRGB[:,:,::-1]
    cv2.imwrite(corrected_img_lin, corrected_img_BGR_lin)
    cv2.imwrite(corrected_img_sRGB, corrected_img_BGR_sRGB)
    return(colour_corrected, reference_lin, CCM)

def BatchCorrect(map_path, checker_source_lin, checker_reference_sRGB, terms,
                 corrected_dir):
    os.makedirs(corrected_dir)
    for image in sorted(os.listdir(map_path)):
        if image.endswith(".jpg") or image.endswith(".png"):
            image_name = image.replace(".jpg","")
            image_lin = sRGB_to_lin(Image.open(map_path+"/"+image))
            ColourCorrect(image_lin, corrected_dir+"/"+image_name+"_cor_lin.jpg", 
                          corrected_dir+"/"+image_name+"_cor_sRGB.jpg", 
                          checker_source_lin, checker_reference_sRGB, terms)
