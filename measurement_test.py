# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 15:01:58 2020

@author: jdaza
"""

import pandas as pd
import datetime
import numpy as np
import os 
import sys


def LSL_test_trigger_delay(lsl_file, hw_file, num):

    df1 = pd.read_csv(lsl_file, sep = '\t', header=None)
    df2 = pd.read_csv(hw_file, sep='\t', header=None)
    
    colum_lsl= pd.to_datetime(df1[df1.columns[0]], format = "%Y-%m-%d %H:%M:%S.%f")
    colum_physical= pd.to_datetime(df2[df2.columns[0]], format = "%Y-%m-%d %H:%M:%S.%f")
    
    diff = (colum_physical - colum_lsl).values.astype(float)/1000000
    
   
    #return diff
    return {"max": diff.max(), "min": diff.min(),
            "mean": diff.mean(), "median": np.median(diff),
            "std":diff.std(), "sigma1": diff.mean() + diff.std(),
            "sigma3": diff.mean() + diff.std()*3, "sigma6": diff.mean() + diff.std()*6}


if __name__ == "__main__":

    list_diff = []

    if(len(sys.argv)<2):
        
        print("ERROR: Incorrect use of the script")
        print("Use: python measurement.py test_delay_directory")
        sys.exit() 
        
        
    directory = sys.argv[1]

    
    for i in range(1, 11): 
    
        name_lsl = os.path.join(directory, str(i), "lsl.txt")
        name_hardware  = os.path.join(directory, str(i), "hardware.txt")
           
        list_diff.append(LSL_test_trigger_delay(name_lsl, name_hardware, i))


    df = pd.DataFrame(list_diff)
    
    df.to_csv("results.csv")
    print("Results save on: "+os.getcwd()+'\\results.csv')