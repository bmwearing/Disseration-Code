# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:34:32 2021

@authors: Ben Wearing, Ned Howarth
"""
#relevant imports
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#plotting parameters
variable = 'freedom from torture' 
#freedom of religion
#gender equality
#freedom from torture

title = 'Freedom from Torture, Spain'
x_axis_title = 'Year'
y_axis_title = 'Fft Rating'

#reading in data into Pandas dataframe
df = pd.read_csv('Spain Data.csv')

#lists for axis value
year = []
var = []

#looping over datafarme
for i in range(0,len(df)):
    #placing each datapoint in list
    year.append(df.iloc[i]['ID_year'])
    var.append(df.iloc[i][variable])
    
#linear regression   
slope, intercept, r_value, p_value, std_err = stats.linregress(year,var) 

#plotting
plt.figure(figsize=(40,20))
plt.scatter(year,var,marker='x',color='black',s = 500,linewidth = 4)
plt.plot(year,slope*np.asarray(year) + intercept,color = 'red',linewidth = 3)
plt.title(title,size = 75,pad = 25 )
plt.xlabel(x_axis_title,size = 50)
plt.ylabel(y_axis_title,size = 50)
plt.xticks(np.asarray(year),rotation = 55,size=30)
plt.yticks(size = 40)
plt.grid()
plt.show()