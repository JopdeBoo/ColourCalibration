import numpy as np
import csv
import matplotlib.pyplot as plt
import colour.models as cm
import skimage.color as sc
import linConversions as conv

SMALL_SIZE = 10*2                                        
MEDIUM_SIZE = 12*2
BIGGER_SIZE = 14*2

plt.rcParams.update({"text.usetex": True,"font.family": "serif",
                     "font.serif": ["Palatino"]})        # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)                    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)                    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE, direction='in')    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE, direction='in')    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)                    # legend fontsize
plt.rc('figure', figsize='15, 6')                        # size of the figure, used to be '4, 3' in inches

def diffPlot(source_lin, reference_lin, corrected_lin):    
    source_XYZ = conv.lin_to_XYZ(source_lin)
    reference_XYZ = conv.lin_to_XYZ(reference_lin)
    corrected_XYZ = conv.lin_to_XYZ(corrected_lin)
    
    source_Lab = sc.xyz2lab(source_XYZ)
    reference_Lab = sc.xyz2lab(reference_XYZ)
    corrected_Lab = sc.xyz2lab(corrected_XYZ)
    
    dE00_source = sc.deltaE_ciede2000(source_Lab, reference_Lab)
    dE00_corrected = sc.deltaE_ciede2000(corrected_Lab, reference_Lab)
            
    diff_source_XYZ = np.sqrt(np.sum((source_XYZ - reference_XYZ)**2, axis=1))*100
    diff_corrected_XYZ = np.sqrt(np.sum((corrected_XYZ - reference_XYZ)**2, axis=1))*100
    
    diff_source_lin = np.sqrt(np.sum((np.array(source_lin)/255 - np.array(reference_lin)/255)**2, axis=1))*100
    diff_corrected_lin = np.sqrt(np.sum((np.array(corrected_lin)/255 - np.array(reference_lin)/255)**2, axis=1))*100                           
    
    x = np.arange(len(diff_source_XYZ))+1
    width = 0.4
    
    plt.figure()
    source_bar_XYZ = plt.bar(x - width/2, diff_source_XYZ, width, label='Source')
    corrected_bar_XYZ = plt.bar(x + width/2, diff_corrected_XYZ, width, label='Corrected')
    plt.title("Colour distance in XYZ-space")
    plt.xlabel("Patch")
    plt.ylabel("Distance")
    plt.ylim([0,np.max(np.concatenate([diff_source_XYZ,diff_corrected_XYZ]))+5])
    plt.vlines(np.arange(5.5, len(diff_source_XYZ),6),0,140, color="red")
    plt.legend()
    plt.show()
    
    plt.figure()
    source_bar_RGB = plt.bar(x - width/2, diff_source_lin, width, label='Source')
    corrected_bar_RGB = plt.bar(x + width/2, diff_corrected_lin, width, label='Corrected')
    plt.title("Colour distance in RGB-space")
    plt.xlabel("Patch")
    plt.ylabel("Distance")
    plt.ylim([0,np.max(np.concatenate([diff_source_lin,diff_corrected_lin]))+5])
    print()
    plt.vlines(np.arange(5.5, len(diff_source_lin),6),0,140, color="red")
    plt.legend()
    plt.show()
    
    plt.figure()
    source_bar_dE = plt.bar(x - width/2, dE00_source, width, label='Source')
    corrected_bar_dE = plt.bar(x + width/2, dE00_corrected, width, label='Corrected')
    plt.title("Colour difference in dE00")
    plt.xlabel("Patch")
    plt.ylabel("dE00")
    plt.xticks(np.arange(1,30.5,1))
    plt.vlines(np.arange(0.5, len(dE00_corrected)+0.6,6),0,140, color="red")
    plt.ylim([0,np.max(np.concatenate([dE00_source,dE00_corrected]))+5])
    plt.xlim(0.5,30.5)
    plt.legend()
    plt.savefig(r"figures\dE00.pdf")
    plt.show()
    
    source_err_XYZ = np.mean(diff_source_XYZ)
    corrected_err_XYZ =np.mean(diff_corrected_XYZ)
    
    source_err_lin = np.mean(diff_source_lin)
    corrected_err_lin =np.mean(diff_corrected_lin)
    
    dE00_source_avg = np.mean(dE00_source)
    dE00_corrected_avg = np.mean(dE00_corrected)
    return(source_err_XYZ,corrected_err_XYZ, source_err_lin,corrected_err_lin,dE00_source_avg,dE00_corrected_avg)

def diffChart(reference_lin, corrected_lin, source_lin):
    ref_sRGB = conv.lin_to_sRGB(reference_lin)
    cor_sRGB = conv.lin_to_sRGB(corrected_lin)
    sou_sRGB = conv.lin_to_sRGB(source_lin)
    
    colours2 = np.array([ref_sRGB,cor_sRGB])
    colours1 = np.array([ref_sRGB,sou_sRGB])
    
    fig, axs = plt.subplots(nrows=2, sharex=True, figsize=(15,4))
    axs[0].set_title('Colour comparisons')
    axs[0].imshow(colours1)
    axs[0].set_yticks([0,1])
    axs[0].set_yticklabels(["reference","source"])
    
    #axs[1].set_title('blue should be down')
    axs[1].imshow(colours2)
    axs[1].set_yticks([0,1])
    axs[1].set_yticklabels(["reference","corrected"])
    
    plt.xticks(np.arange(0,29.5,1),np.arange(1,30.5,1,dtype=int))
    plt.xlabel("Patch number")
    plt.savefig(r"figures\difference_visualised.pdf")
    plt.show()

