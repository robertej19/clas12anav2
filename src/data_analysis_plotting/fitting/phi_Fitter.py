# 1.) Necessary imports.    
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import argparse
import sys 
import pandas as pd
from matplotlib.patches import Rectangle

from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker
from src.data_analysis_plotting.plot_makers import make_histos

from icecream import ic

# 2.) Define fit function.
def fit_function(phi,A,B,C):
    #A + B*np.cos(2*phi) +C*np.cos(phi)
    rads = phi*np.pi/180
    #return (A * np.exp(-x/beta) + B * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))
    #A = T+L, B=TT, C=LT
    #A = black, B=blue, C=red
    return A + B*np.cos(2*rads) + C*np.cos(rads)

#print(fit_function(45,1,0,1))

def getPhiFit_prebinned(phi_bins,bin_counts,phi_title,plot_dir,args):
    ic.disable()
    if args.v:
        ic.enable() 

    xmin = 0
    xmax = 360
    #print("fitting {}".format(phi_title))
    
    phi_vals = bin_counts
    data_entries = bin_counts
    bins = phi_bins

    data_errors = np.sqrt(data_entries)
    data_errors = [1/err if err>0 else err+1 for err in data_errors]
    
    ic(data_entries)
    ic(data_errors)

    #print(data_entries)

    #ic.enable()
    ic(data_entries)
    if (max(data_entries) == 0):
        #print("No data in this plot, saving and returning 0")

        plt.text(150, 0, "No Data")
        #print("No data")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        bar1 = ax.bar(binscenters, data_entries, width=bins[1] - bins[0], color='navy', label='Histogram entries')

        #plt.hist(phi_vals, bins =np.linspace(0, 360, 20), range=[0,360])# cmap = plt.cm.nipy_spectral)

        plot_title = plot_dir + phi_title+".png"
        plt.savefig(plot_title)
        plt.close()
        #print("plot saved to {}".format(plot_title))
        
        return ["nofit","nofit","nofit","nofit"]
    else:
        ic(bins)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        ic(binscenters)
        # 5.) Fit the function to the histogram data.
        popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=data_entries, p0=[2.0, 2, 0.3],
                    sigma=data_errors, absolute_sigma=True)
        #print(popt) #popt contains the values for A, B, C

        a_err = np.sqrt(pcov[0][0])
        b_err = np.sqrt(pcov[1][1])
        c_err = np.sqrt(pcov[2][2])

        a,b,c = popt[0],popt[1],popt[2]
        #ic(a_err,b_err,c_err)
        #ic.disable()
        
        # 6.)
        # Generate enough x values to make the curves look smooth.
       
        fit_y_data_1 = fit_function(binscenters, *popt)

        ic(fit_y_data_1)

        

        chisq0 = stats.chisquare(f_obs=data_entries, f_exp=fit_y_data_1)
        chisq = stats.chisquare(f_obs=np.array(data_entries, dtype=np.float64), f_exp=np.array(fit_y_data_1, dtype=np.float64))

        sums=[]
        for ind,val in enumerate(fit_y_data_1):
            diff2 = (data_entries[ind]-val)**2
            s1 = diff2/val
            sums.append(s1)

        manchisq = np.sum(sums)

        ###ic.enable()
        if chisq0[0]<0:
            ic(manchisq)
            ic(chisq0[0])
        if not (chisq0[0] == chisq[0]):
            print("ERROR MISMATCH")
            print(chisq0[0])
            print(chisq[0])
            print(manchisq)

        ic.disable()

        p = chisq[1]
        chisq = chisq[0]

        ic(chisq)
        ic(p)


        xspace = np.linspace(0, xmax, 1000)
        fit_y_data = fit_function(xspace, *popt)

        ##ic.enable()
        ic(fit_y_data)
        
        y_manual = []
        for ind, val in enumerate(xspace):
            ic(val,a,b,c)
            y_one = fit_function(val,a,b,c)
            ic(y_one)
            y_manual.append(y_one)


        
        #7
        # Plot the histogram and the fitted function.

        fig = plt.figure()
        ax = fig.add_subplot(111)
        

        bar1 = ax.bar(binscenters, data_entries, width=bins[1] - bins[0], color='navy', label='Histogram entries')
        fit1, = ax.plot(xspace, fit_y_data, color='darkorange', linewidth=2.5, label='Fitted function')

        # Make the plot nicer.
        plt.xlim(xmin,xmax)
        #plt.ylim(0,5)
        plt.xlabel(r'phi')
        plt.ylabel(r'Number of entries')

        plot_title = plot_dir + phi_title+".png"
        plt.title(phi_title)
        #plt.legend(loc='best')

        fit_params = "A: {:2.2f} +/- {:2.2f}\n B:{:2.2f} +/- {:2.2f}\n C:{:2.2f} +/- {:2.2f}\n Chi:{:2.2f} \n p:{:2.2f}".format(a,a_err,b,b_err,c,c_err,chisq,p)

        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        ax.legend([bar1, fit1, extra], ("Data","A+Bcos(2Phi)+Ccos(Phi)",fit_params))

        #plt.text(120, max(data_entries)/1.3, fit_params)

        
        plt.savefig(plot_title)
        #plt.show()
        plt.close()
        #print("plot saved to {}".format(plot_title))

        return popt, pcov, chisq, p

def plotPhi_duo(phi_bins,bin_counts_0,bin_counts_1,phi_title,plot_dir,args,saveplot=True):
    ic.disable()
    if args.v:
        ic.enable() 

    xmin = 0
    xmax = 360
    #print("fitting {}".format(phi_title))
    
    data_entries_0 = bin_counts_0
    data_entries_1 = bin_counts_1
    bins = phi_bins

    data_errors_0 = np.sqrt(data_entries_0)
    data_errors_0 = [1/err if err>0 else err+1 for err in data_errors_0]

    data_errors_1 = np.sqrt(data_entries_1)
    data_errors_1 = [1/err if err>0 else err+1 for err in data_errors_1]


    #print(data_entries)

    if (max(data_entries_0) == 0) and(max(data_entries_1) == 0):
        #print("No data in this plot, saving and returning 0")

        plt.text(150, 0, "No Data")
        #print("No data")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        bar1 = ax.bar(binscenters, data_entries_0, width=bins[1] - bins[0], color='navy', label='Histogram entries')

        #plt.hist(phi_vals, bins =np.linspace(0, 360, 20), range=[0,360])# cmap = plt.cm.nipy_spectral)

        plot_title = plot_dir + phi_title+".png"
        if saveplot:
            plt.savefig(plot_title)
            plt.close()
        else:
            plt.show()
            plt.close()

        return ["nofit","nofit","nofit","nofit"]
    else:
        ic(bins)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        ic(binscenters)
        # 5.) Fit the function to the histogram data.
        #popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=data_entries, p0=[2.0, 2, 0.3],
         #           sigma=data_errors, absolute_sigma=True)
        #print(popt) #popt contains the values for A, B, C

        ##a_err = np.sqrt(pcov[0][0])
        ##b_err = np.sqrt(pcov[1][1])
        #c_err = np.sqrt(pcov[2][2])

        #a,b,c = popt[0],popt[1],popt[2]
        #ic(a_err,b_err,c_err)
        #ic.disable()
        
        # 6.)
        # Generate enough x values to make the curves look smooth.
       
        #fit_y_data_1 = fit_function(binscenters, *popt)

        #ic(fit_y_data_1)

        

        #chisq0 = stats.chisquare(f_obs=data_entries, f_exp=fit_y_data_1)
        #chisq = stats.chisquare(f_obs=np.array(data_entries, dtype=np.float64), f_exp=np.array(fit_y_data_1, dtype=np.float64))

        #sums=[]
        #for ind,val in enumerate(fit_y_data_1):
        #    diff2 = (data_entries[ind]-val)**2
        #    s1 = diff2/val
        #    sums.append(s1)

       # manchisq = np.sum(sums)

        ###ic.enable()
        #if chisq0[0]<0:
        #    ic(manchisq)
        #    ic(chisq0[0])
        #if not (chisq0[0] == chisq[0]):
        #    print("ERROR MISMATCH")
        #    print(chisq0[0])
        #    print(chisq[0])
        #    print(manchisq)

        ic.disable()

       # p = chisq[1]
       # chisq = chisq[0]

        ##ic(chisq)
        #ic(p)


        #xspace = np.linspace(0, xmax, 1000)
        #fit_y_data = fit_function(xspace, *popt)

        ##ic.enable()
        #ic(fit_y_data)
        
        #y_manual = []
        #for ind, val in enumerate(xspace):
        #    ic(val,a,b,c)
        #    y_one = fit_function(val,a,b,c)
        #    ic(y_one)
        #    y_manual.append(y_one)


        
        #7
        # Plot the histogram and the fitted function.

        fig = plt.figure()
        ax = fig.add_subplot(111)
        


        highPower = data_entries_0
        lowPower = data_entries_1


        #plt.bar(binscenters, highPower,  
        #        color='b', label='LUND Events')
        #plt.bar(binscenters,  lowPower, color='r', alpha=0.5, label='Sim Events')





        bar0 = ax.bar(binscenters, data_entries_0, width=bins[1] - bins[0], color='red', label='Sim input')
        bar1 = ax.bar(binscenters, data_entries_1, width=bins[1] - bins[0], color='black', label='sim output')
       # fit1, = ax.plot(xspace, fit_y_data, color='darkorange', linewidth=2.5, label='Fitted function')

        # Make the plot nicer.
        plt.xlim(xmin,xmax)
        #plt.ylim(0,5)
        plt.xlabel(r'phi')
        plt.ylabel(r'Number of entries')

        plot_title = plot_dir + phi_title+".png"
        plt.title(phi_title)
        #plt.legend(loc='best')
        plt.legend()


        #fit_params = "A: {:2.2f} +/- {:2.2f}\n B:{:2.2f} +/- {:2.2f}\n C:{:2.2f} +/- {:2.2f}\n Chi:{:2.2f} \n p:{:2.2f}".format(a,a_err,b,b_err,c,c_err,chisq,p)


        #plt.text(120, max(data_entries)/1.3, fit_params)

        
        if saveplot:
            plt.savefig(plot_title)
            plt.close()
        else:
            plt.show()
            plt.close()
        #print("plot saved to {}".format(plot_title))

def plotPhi_single(phi_bins,bin_counts_0,phi_title,plot_dir,args,saveplot=True):
    ic.disable()
    if args.v:
        ic.enable() 

    xmin = 0
    xmax = 360
    #print("fitting {}".format(phi_title))
    
    data_entries_0 = bin_counts_0
    bins = phi_bins

    data_errors_0 = np.sqrt(data_entries_0)
    data_errors_0 = [1/err if err>0 else err+1 for err in data_errors_0]


    #print(data_entries)

    if (max(data_entries_0) == 0):
        #print("No data in this plot, saving and returning 0")

        plt.text(150, 0, "No Data")
        #print("No data")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        bar1 = ax.bar(binscenters, data_entries_0, width=bins[1] - bins[0], color='navy', label='Histogram entries')

        #plt.hist(phi_vals, bins =np.linspace(0, 360, 20), range=[0,360])# cmap = plt.cm.nipy_spectral)

        plot_title = plot_dir + phi_title+".png"
        if saveplot:
            plt.savefig(plot_title)
            plt.close()
        else:
            plt.show()
            plt.close()

        return ["nofit","nofit","nofit","nofit"]
    else:
        ic(bins)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        ic(binscenters)
        # 5.) Fit the function to the histogram data.
        #popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=data_entries, p0=[2.0, 2, 0.3],
         #           sigma=data_errors, absolute_sigma=True)
        #print(popt) #popt contains the values for A, B, C

        ##a_err = np.sqrt(pcov[0][0])
        ##b_err = np.sqrt(pcov[1][1])
        #c_err = np.sqrt(pcov[2][2])

        #a,b,c = popt[0],popt[1],popt[2]
        #ic(a_err,b_err,c_err)
        #ic.disable()
        
        # 6.)
        # Generate enough x values to make the curves look smooth.
       
        #fit_y_data_1 = fit_function(binscenters, *popt)

        #ic(fit_y_data_1)

        

        #chisq0 = stats.chisquare(f_obs=data_entries, f_exp=fit_y_data_1)
        #chisq = stats.chisquare(f_obs=np.array(data_entries, dtype=np.float64), f_exp=np.array(fit_y_data_1, dtype=np.float64))

        #sums=[]
        #for ind,val in enumerate(fit_y_data_1):
        #    diff2 = (data_entries[ind]-val)**2
        #    s1 = diff2/val
        #    sums.append(s1)

       # manchisq = np.sum(sums)

        ###ic.enable()
        #if chisq0[0]<0:
        #    ic(manchisq)
        #    ic(chisq0[0])
        #if not (chisq0[0] == chisq[0]):
        #    print("ERROR MISMATCH")
        #    print(chisq0[0])
        #    print(chisq[0])
        #    print(manchisq)

        ic.disable()

       # p = chisq[1]
       # chisq = chisq[0]

        ##ic(chisq)
        #ic(p)


        #xspace = np.linspace(0, xmax, 1000)
        #fit_y_data = fit_function(xspace, *popt)

        ##ic.enable()
        #ic(fit_y_data)
        
        #y_manual = []
        #for ind, val in enumerate(xspace):
        #    ic(val,a,b,c)
        #    y_one = fit_function(val,a,b,c)
        #    ic(y_one)
        #    y_manual.append(y_one)


        
        #7
        # Plot the histogram and the fitted function.

        fig = plt.figure()
        ax = fig.add_subplot(111)
        




        #plt.bar(binscenters, highPower,  
        #        color='b', label='LUND Events')
        #plt.bar(binscenters,  lowPower, color='r', alpha=0.5, label='Sim Events')





        bar0 = ax.bar(binscenters, data_entries_0, width=bins[1] - bins[0], color='red', label='Sim input')
       # fit1, = ax.plot(xspace, fit_y_data, color='darkorange', linewidth=2.5, label='Fitted function')

        # Make the plot nicer.
        plt.xlim(xmin,xmax)
        #plt.ylim(0,5)
        plt.xlabel(r'phi')
        plt.ylabel(r'Number of entries')

        plot_title = plot_dir + phi_title+".png"
        plt.title(phi_title)
        #plt.legend(loc='best')
        plt.legend()


        #fit_params = "A: {:2.2f} +/- {:2.2f}\n B:{:2.2f} +/- {:2.2f}\n C:{:2.2f} +/- {:2.2f}\n Chi:{:2.2f} \n p:{:2.2f}".format(a,a_err,b,b_err,c,c_err,chisq,p)


        #plt.text(120, max(data_entries)/1.3, fit_params)

        
        if saveplot:
            plt.savefig(plot_title)
            plt.close()
        else:
            plt.show()
            plt.close()
        #print("plot saved to {}".format(plot_title))


def getPhiFit(phi_vals,phi_title,plot_dir,args):
    ic.disable()
    if args.v:
        ic.enable() 

    xmin = 0
    xmax = 360
    #print("fitting {}".format(phi_title))
    
    data = phi_vals
    bins_x = np.linspace(xmin, xmax, 20)
    data_entries, bins = np.histogram(data,bins=bins_x)
    data_errors = np.sqrt(data_entries)
    data_errors = [1/err if err>0 else err+1 for err in data_errors]
    
    ic(data_entries)
    ic(data_errors)

    

    if (max(data_entries) == 0):
        #print("No data in this plot, saving and returning 0")

        plt.text(150, 0, "No Data")

        plt.hist(phi_vals, bins =np.linspace(0, 360, 20), range=[0,360])# cmap = plt.cm.nipy_spectral)

        plot_title = plot_dir + phi_title+".png"
        plt.savefig(plot_title)
        plt.close()
        #print("plot saved to {}".format(plot_title))
        
        return ["nofit","nofit","nofit","nofit"]
    else:
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])

        ic(binscenters)
        # 5.) Fit the function to the histogram data.
        popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=data_entries, p0=[2.0, 2, 0.3],
                    sigma=data_errors, absolute_sigma=True)
        #print(popt) #popt contains the values for A, B, C

        a_err = np.sqrt(pcov[0][0])
        b_err = np.sqrt(pcov[1][1])
        c_err = np.sqrt(pcov[2][2])

        a,b,c = popt[0],popt[1],popt[2]
        #ic(a_err,b_err,c_err)
        #ic.disable()
        
        # 6.)
        # Generate enough x values to make the curves look smooth.
       
        fit_y_data_1 = fit_function(binscenters, *popt)

        ic(fit_y_data_1)

        

        chisq0 = stats.chisquare(f_obs=data_entries, f_exp=fit_y_data_1)
        chisq = stats.chisquare(f_obs=np.array(data_entries, dtype=np.float64), f_exp=np.array(fit_y_data_1, dtype=np.float64))

        sums=[]
        for ind,val in enumerate(fit_y_data_1):
            diff2 = (data_entries[ind]-val)**2
            s1 = diff2/val
            sums.append(s1)

        manchisq = np.sum(sums)

        ###ic.enable()
        if chisq0[0]<0:
            ic(manchisq)
            ic(chisq0[0])
        if not (chisq0[0] == chisq[0]):
            print("ERROR MISMATCH")
            print(chisq0[0])
            print(chisq[0])
            print(manchisq)

        ic.disable()

        p = chisq[1]
        chisq = chisq[0]

        ic(chisq)
        ic(p)


        xspace = np.linspace(0, xmax, 1000)
        fit_y_data = fit_function(xspace, *popt)

        ###ic.enable()
        ic(fit_y_data)
        
        y_manual = []
        for ind, val in enumerate(xspace):
            ic(val,a,b,c)
            y_one = fit_function(val,a,b,c)
            ic(y_one)
            y_manual.append(y_one)


        
        #7
        # Plot the histogram and the fitted function.

        fig = plt.figure()
        ax = fig.add_subplot(111)
        

        bar1 = ax.bar(binscenters, data_entries, width=bins[1] - bins[0], color='navy', label='Histogram entries')
        fit1, = ax.plot(xspace, fit_y_data, color='darkorange', linewidth=2.5, label='Fitted function')

        # Make the plot nicer.
        plt.xlim(xmin,xmax)
        plt.ylim(0,300)
        plt.xlabel(r'phi')
        plt.ylabel(r'Number of entries')

        plot_title = plot_dir + phi_title+".png"
        plt.title(phi_title)
        #plt.legend(loc='best')

        fit_params = "A: {:2.2f} +/- {:2.2f}\n B:{:2.2f} +/- {:2.2f}\n C:{:2.2f} +/- {:2.2f}\n Chi:{:2.2f} \n p:{:2.2f}".format(a,a_err,b,b_err,c,c_err,chisq,p)

        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        ax.legend([bar1, fit1, extra], ("Data","A+Bcos(2Phi)+Ccos(Phi)",fit_params))

        #plt.text(120, max(data_entries)/1.3, fit_params)

        
        plt.savefig(plot_title)
        #plt.show()
        plt.close()
        #print("plot saved to {}".format(plot_title))

        return popt, pcov, chisq, p

# 3.) Generate exponential and gaussian data and histograms.

if (__name__ == "__main__"):

    fs = filestruct.fs()

    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    parser.add_argument('-s','--start', type=int, help='hop in point of program',default=1)
    parser.add_argument('-p','--stop', type=int,help='hop out point of program',default=3)
    parser.add_argument('-i','--hist1',help='make q2 vs xb graph',default=False,action="store_true")
    args = parser.parse_args()

    phi_bins = fs.phi_ranges_clas6_14
    bin_counts_0 = [0,0,0,0,40,30,20,0,0,0,0,0,0,0,0,0,0,0,0,0]
    bin_counts_1 = [0,0,0,0,4,20,10,0,0,0,0,0,0,0,0,0,0,0,0,0]



    counted_data_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.data_basename 
    counted_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.binned_lund_pandas+fs.lund_test_run
    counted_pickled_out_name = fs.counted_pickled_out_name
    

    dataframe0 = pd.read_pickle(counted_lund_pandas_dir+counted_pickled_out_name)
    dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)



    ic(dataframe0)
    ic(dataframe1)

    ic(dataframe0["counts"].sum())
    ic(dataframe1["counts"].sum())


    phi0 = dataframe0.query('tmin >= 0.5 & tmin < 0.9 & xBmin >= 0.3 & xBmin < 0.38 & Q2min >= 2.5 & Q2min < 3.0')
    phi1 = dataframe1.query('tmin >= 0.5 & tmin < 0.9 & xBmin >= 0.3 & xBmin < 0.38 & Q2min >= 2.5 & Q2min < 3.0')

    plot_title = "test0"
    plot_out_dir = "test/"

    bin_counts_0 = phi0["counts"].tolist()
    bin_counts_1 = phi1["counts"].tolist()

    ic(bin_counts_0)
    ic(bin_counts_1)

    plotPhi_duo(phi_bins,bin_counts_0,bin_counts_1,plot_title,plot_out_dir,args,saveplot=False)






