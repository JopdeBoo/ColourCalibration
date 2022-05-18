import linMask as m
import linCC as CC
import linDiffPlots as dP


if __name__ == "__main__":
    # Put in file names:
    # Image with colour checker
    img_path = r"img\src1.jpg" 
    # csv files in which data from image for squares of checker will be stored             
    source_XYZ_csv = r"data\src1XYZ.csv"       
    source_lin_csv = r"data\src1RGB.csv" 
    # csv files in which data from corrected image for squares of checker will
    # be stored             
    corrected_XYZ_csv = r"data\src1CorXYZ.csv"
    corrected_lin_csv = r"data\src1CorRGB.csv"
    # csv with reference sRGB data of colours on checker
    reference_csv_RGB = r"data\reference_RGB.csv"
    # Image files in which the corrected images are saved
    corrected_img_lin = r"img\src1Corlin.jpg"
    corrected_img_sRGB = r"img\src1CorsRGB.jpg"
    # map of images to be corrected
    map_path = r"img\tobecorrected"
    corrected_directory = r"img\tobecorrected\corrected"
    
    
    # Fill in the shape of the colour checker
    n_vertical_swatches = 5
    n_horizontal_swatches = 6
    total = n_vertical_swatches * n_horizontal_swatches

    # Use the horizontal line in the figure to line up the checker horizontally
    rotation = -1

    # It is optional to crop the image if positioning the mask is too difficult,
    # because the colour checker is small in the image
    left = 900
    top = 1600
    right = 800
    bottom = 1200

    # Choose the width of the mask squares to fit inside the squares of the checker
    swatch_width = 130

    # Choose the position of the top left mask, using the pixel count on the axes
    vertical_start = 140
    horizontal_start = 20

    # choose the vertical and horizontal steps so that each black mask is inside one
    # of the squares on the colour checker
    vertical_steps = 210
    horizontal_steps = 210
    
    write_csv = 0
    correct = 1
    compare = 1
    batch = 0
    
    # Choose number of correction terms out of: 
    # [3, 5, 7, 8, 10, 11, 14, 16, 17, 19, 20, 22]
    correction_terms = 20
    
# ============================================================================#
    lin = 1
    source_lin, source_XYZ, image_lin = m.createMasks(n_vertical_swatches,
                n_horizontal_swatches, rotation, left, top, right, bottom,
                swatch_width, vertical_start, horizontal_start, vertical_steps,
                horizontal_steps, img_path, lin)
    
    if write_csv == 1:
        m.writeCSVs(source_lin, source_XYZ, source_XYZ_csv, source_lin_csv)
    
    if correct == 1:
        corrected, reference_lin, CCM = CC.ColourCorrect(image_lin, corrected_img_lin,
                            corrected_img_sRGB, source_lin, reference_csv_RGB,
                            correction_terms)
        
        if compare == 1: 
            lin = 0
            corrected_lin, corrected_XYZ, cor_image_lin = m.createMasks(
                n_vertical_swatches, n_horizontal_swatches, rotation, left, 
                top, right, bottom, swatch_width, vertical_start, 
                horizontal_start, vertical_steps,horizontal_steps, 
                corrected_img_lin, lin)
            if write_csv == 1:
                m.writeCSVs(corrected_lin, corrected_XYZ, corrected_XYZ_csv,
                               corrected_lin_csv)
            source_err_XYZ,corrected_err_XYZ, source_err_lin,\
            corrected_err_lin, dE00_source, dE00_corrected = dP.diffPlot(source_lin,
                                                reference_lin, corrected_lin)
            
            dP.diffChart(reference_lin, corrected_lin, source_lin)
            
            print(f"Average error in XYZ values for source image is {source_err_XYZ:.3f}%")
            print(f"Average error in XYZ values for corrected image is {corrected_err_XYZ:.3f}%")
            print(f"Average error in RGB values for source image is {source_err_lin:.3f}%")
            print(f"Average error in RGB values for corrected image is {corrected_err_lin:.3f}%")
            print(f"Average dE00 for source image is {dE00_source:.3f}")
            print(f"Average dE00 for corrected image is {dE00_corrected:.3f}")
            
    if batch == 1:
        CC.BatchCorrect(map_path, source_lin, reference_csv_RGB, correction_terms,
                        corrected_directory)
        
    
    
    
    