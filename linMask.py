import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import csv
import linConversions as conv

def sRGB_to_lin(rgb):
    # Converts array or list of sRGB values to linear RGB values
    rgb = np.array(rgb)/255
    linear = np.where(rgb<=0.04045, rgb/12.92, ((rgb+0.055)/1.055)**(2.4))
    return((linear*255).astype(np.uint8))

def createMasks(n_vertical_swatches, n_horizontal_swatches, rotation,
                left, top, right, bottom, swatch_width, vertical_start, 
                horizontal_start, vertical_steps, horizontal_steps, img_path, lin):
    
    # Create mask to extract colour data from each square of colour checker
    image = Image.open(img_path)
    
    # Only linearise image if image is not already linearised
    if lin == 1:
        lin_image = sRGB_to_lin(np.array(image))
    else:
        lin_image = np.array(image)
        
    # Rotate and crop image to make positioning of swatches easier
    image2 = Image.Image.rotate(Image.fromarray(lin_image), rotation)
    width, height = image2.size
    image2 = image2.crop((left,top,width - right,height - bottom))
    image2 = np.array(image2)
    
    masks = []          # Separate masks for each square
    lin = []            # List of average linear RGB values of each square
    
    for i in range(n_vertical_swatches):
        for j in range(n_horizontal_swatches):
            
            # Creation square masks with equal spacing
            mask = np.zeros(image2.shape, dtype=np.uint8)
            mask = cv2.rectangle(mask, (horizontal_start+horizontal_steps*j,
                                        vertical_start+vertical_steps*i),
                                 (horizontal_start+horizontal_steps*j+swatch_width,
                                  vertical_start+vertical_steps*i+swatch_width),
                                 (255,255,255), -1) 
            masks.append(mask)
            
            # Creating images where only a square is visible and taking the 
            # average R, G and B values of all different squares
            swatch = cv2.bitwise_and(image2, mask) 
            values = swatch[np.where((mask==(255,255,255)).all(axis=2))]
            meanlin = [np.average(values[:,0]),np.average(values[:,1]),
                       np.average(values[:,2])]
            lin.append(meanlin)
    
    # Converting the linear RGB data to XYZ data
    XYZ = conv.lin_to_XYZ(lin) 
    
    #Combining masks to get overview for calibration       
    combined_mask = np.zeros(image2.shape, dtype=np.uint8)
    for mask in masks:
        combined_mask += mask
    anti_mask = cv2.bitwise_not(combined_mask)
    overview = cv2.bitwise_and(image2, anti_mask)
    #overview = np.where(overview==(0,0,0), (255,255,255),overview)
    
    plt.figure()
    plt.title("Overview of masks")
    plt.imshow(overview)
    plt.axhline(0.5*image2.shape[0])
    plt.show()
    return(lin,XYZ,lin_image)

def writeCSVs(RGB, XYZ, XYZ_csv, RGB_csv):
    RGB_w = open(RGB_csv, 'w', newline="\n")
    writer_RGB = csv.writer(RGB_w)
    writer_RGB.writerow(["R","G","B"])
    for row in RGB:
        writer_RGB.writerow(row)
    RGB_w.close()  
    
    XYZ_w = open(XYZ_csv, 'w', newline="\n")
    writer_XYZ = csv.writer(XYZ_w)
    writer_XYZ.writerow(["X","Y","Z"])
    for row in XYZ:
        writer_XYZ.writerow(row)
    XYZ_w.close()        

    
    
    
    