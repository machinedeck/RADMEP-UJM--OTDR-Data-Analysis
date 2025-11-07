from datetime import datetime
from scipy import stats
from scipy.optimize import curve_fit
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


# define function for getting the wavelength and line data
class wave_data:
    def __init__(self, wavelength, line, directory, wav_only = False, my_analysis = False):
        os.chdir(directory)
        
        self.line = line
        self.wavelength = wavelength
        if wav_only == False:
            self.filenames = [filename for filename in os.listdir() if "Line0{}_{}nm.txt".format(self.line, self.wavelength) in filename]
        else:
            self.filenames = [filename for filename in os.listdir() if "{}nm.txt".format(self.wavelength) in filename]

        if my_analysis == False:
            self.filenames = sorted(self.filenames, key = lambda filename: datetime.strptime(filename[16:35], "%Y-%m-%d_%H-%M-%S"))
            self.skiprows = 13
        else:
            self.filenames = sorted(self.filenames, key = lambda filename: datetime.strptime(filename[5:24], "%Y-%m-%d_%H-%M-%S"))
            self.skiprows = 14
            
        self.times = []
        self.increment = []
    
        # Just for placeholder
        self.time_ref = datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.time_diff_num = 0
        
        for i, filename in enumerate(self.filenames):
            time_raw = np.loadtxt(filename, max_rows = 1, dtype = "str")
    
            dist_diff = float(np.loadtxt(filename, skiprows = 8, max_rows = 1, dtype = "str")[3])
            self.increment.append(dist_diff)

            time = datetime.strptime(time_raw[1] + " " + time_raw[2], "%Y-%m-%d %H:%M:%S")
            
            if i == 0:
                self.times.append(0)
                self.time_ref = time

            else:
                time_diff = time - self.time_ref
                self.time_ref = time
                self.time_diff_num += time_diff.total_seconds() / 60
                self.times.append(self.time_diff_num)

        self.data = np.array([np.loadtxt(file, skiprows = self.skiprows) for file in self.filenames])
        self.distances = [[i * element for i in range(len(file))] for element, file in zip(self.increment, self.data)]


def ria_linear_fit(data, distance, x_min, xarg_start, dist=False, params_only=True):
    if dist == True:
        minarg = np.argwhere(distance == xmin)

    else:
        minarg = x_min

    # optimize
    data1 = data
    data1 = data1.ravel()
    data1 = data1[minarg:]
    data1 = data1[data1 > -10]
    maxarg = np.argmax(data1[xarg_start:])
    data1 = data1[:xarg_start + maxarg]
    
    leng = len(data1) - 1
    val = data1[leng]
    n = 2
    t = val
    
    while t <= val:
        t = data1[leng-1]
        val = data1[leng]
        leng -= 1
    
    new_data = data[minarg : minarg + leng + 1]
    new_dist = distance[minarg : minarg + leng + 1]

    # self.leng = leng
    # self.minarg = minarg

    # linfit = stats.linregress(new_dist, new_data)

    # slope = linfit.slope
    # intercept = linfit.intercept
    # rvalue = linfit.rvalue
    # return slope, intercept, rvalue, minarg + leng + 1   
    # return new_data, new_dist
    # return filenames

    linfit = curve_fit(lambda x, m, b: m * x + b, new_dist, new_data)[0]

    if params_only == True:
        return linfit[0], linfit[1], minarg + leng + 1
    else:
        return new_dist, new_data, linfit, minarg + leng + 1

def line(x, m, b):
    return m * x + b

# def ria_vals(data, distances, xmin, xarg_start):
#     a = 0
#     slopes = []
#     lengs = []
#     intercepts = []
#     for i, (dat, dist) in enumerate(zip(data, distances)):
#         slope, intercept, leng = ria_linear_fit(dat, dist, xmin, xarg_start)
#         # ria_linear_fit(data, distance, x_min, xarg_start, dist=False):
#         # alpha, leng = ria_linear_fit(xmin, i)
#         # slope, intercept = alpha[0], alpha[1]
#         if i == 0:
#             slopes.append(0)
#             a = slope
#         else:
#             slope_ = a - slope
#             slopes.append(abs(slope_))
    
#         lengs.append(leng)
#         intercepts.append(intercept)

#         return slopes, intercepts, lengs
    
    # plt.plot(plt.plot(distance[0][1050: lengs[0]*1e-2, data[0][1050: lengs[0]])
    # plt.plot(distance[0][1050: lengs[0]*1e-2, data[-1][1050: lengs[-1]]))
    
    # plt.plot(time/(60*24), slopes)
    # plt.xlabel("Time, days")
    # plt.ylabel("Absolute Attenuation Difference, dB")
    # plt.show()
    # plt.plot(slopes)