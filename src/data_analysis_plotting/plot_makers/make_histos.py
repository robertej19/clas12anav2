
import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os, subprocess
import math
import shutil
from icecream import ic

#This project
from src.utils import data_getter

def plot_2dhist(x_data,y_data,vars,ranges,colorbar=True,
            saveplot=False,pics_dir="none",plot_title="none"):
    
    # Initalize parameters
    x_name = vars[0]
    y_name = vars[1]
    xmin = ranges[0]
    xmax =  ranges[1]
    num_xbins = ranges[5]
    ymin =  ranges[3]
    ymax =  ranges[4]
    num_ybins = ranges[5]
    x_bins = np.linspace(xmin, xmax, num_xbins) 
    y_bins = np.linspace(ymin, ymax, num_ybins) 

    # Creating plot
    fig, ax = plt.subplots(figsize =(10, 7)) 
    ax.set_xlabel(x_name)  
    ax.set_ylabel(y_name)

    plt.hist2d(x_data, y_data, bins =[x_bins, y_bins],
        range=[[xmin,xmax],[ymin,ymax]])# cmap = plt.cm.nipy_spectral) 

    # Adding color bar 
    if colorbar:
        plt.colorbar()

    plt.tight_layout()  


    #Generate plot title
    if plot_title == "none":
        plot_title = '{} vs {}'.format(x_name,y_name)
    
    plt.title(plot_title) 
        

    if saveplot:
        plt.savefig(pics_dir + plot_title+".png")
        plt.close()
    else:
        plt.show()

def plot_1dhist(x_data,vars,ranges,
            saveplot=False,pics_dir="none",plot_title="none"):
    
    # Initalize parameters
    x_name = vars[0]
    xmin = ranges[0]
    xmax =  ranges[1]
    num_xbins = ranges[2]
    x_bins = np.linspace(xmin, xmax, num_xbins) 

    # Creating plot
    fig, ax = plt.subplots(figsize =(10, 7)) 
    ax.set_xlabel(x_name)  
    ax.set_ylabel('counts')  
    


    plt.hist(x_data, bins =x_bins, range=[xmin,xmax])# cmap = plt.cm.nipy_spectral) 
    

    plt.tight_layout()  


    #Generate plot title
    if plot_title == "none":
        plot_title = '{} vs {}'.format(x_name,y_name)
    
    plt.title(plot_title) 
        

    if saveplot:
        plt.savefig(pics_dir + plot_title+".png")
        plt.close()
    else:
        plt.show()



if __name__ == "__main__":
    ranges = [0,1,100,0,300,120]
    variables = ['xB','Phi']
    conditions = "none"
    datafile = "F18In_168_20210129/skims-168.pkl"
    plot_2dhist(datafile,variables,ranges)