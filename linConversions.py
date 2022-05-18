import numpy as np

def sRGB_to_lin(rgb):
    # Converts array or list of sRGB values to linear RGB values
    rgb = np.array(rgb)/255
    linear = np.where(rgb<=0.04045, rgb/12.92, ((rgb+0.055)/1.055)**(2.4))
    return((linear*255).astype(int))

def lin_to_XYZ(lin):
    # Converts array of linear RGB values to XYZ values
    lin = np.array(lin)/255
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    return(np.transpose(np.matmul(M, np.transpose(lin))))

def lin_to_sRGB(lin):
    # Converts array or list of linear RGB values to sRGB values
    lin = np.array(lin)/255
    rgb = np.where(lin <= 0.0031308, 12.92*lin, (1.055*lin)**(1/2.4)-0.055)
    return((rgb*255).astype(int))

def sRGB_to_XYZ(rgb):
    # Converts array of sRGB values to XYZ values
    rgb = rgb/255
    linear = np.where(rgb<=0.04045, rgb/12.92, ((rgb+0.055)/1.055)**2.4)
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    return(np.transpose(np.matmul(M, np.transpose(linear))))
