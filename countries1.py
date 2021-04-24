# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:12:28 2021

@authors: Ben Wearing, Ned Howarth
"""
# relevant imports
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#parameters for tuning plot
ave = False
variable = 'freedom from torture' 
#freedom of religion
#gender equality
#freedom from torture

title = 'Freedom from Torture, Egypt'
x_axis_title = 'Year'
y_axis_title = 'FfT Rating'

country = 'Egypt'

#saving copy of data set
save_copy = False
save_title = str(variable + '.csv')

#converting data set to pandas dataframe
df = pd.read_csv('Final_Data.csv')

#new blank dataframe
df2 = pd.DataFrame(data={})


#for identifying countries, staring with first in dataset
ID = df.iloc[0]['ID_country_code']
#relevant arrays for plotting and to store data over time series, seperated by country
year_array = np.linspace(1975,2019,45)
year = np.empty(50,dtype=object)
year_country = []
var = np.empty(50,dtype=object)
var_country = []
sum_var = np.zeros(45)
ave_array = np.zeros(45)

#looping over countries
for i in range(0,len(df)):
    if df.iloc[i]['ID_country_code'] == ID:
        
        #storing individual country data
        year_country.append(df.iloc[i]['ID_year'])
        var_country.append(df.iloc[i][variable])
        if ave == True:
            
            #summing data over countries for individual year
            for k in range(0,len(year_array)):
                if df.iloc[i]['ID_year'] == year_array[k]:
                    sum_var[k] += df.iloc[i][variable]
                    ave_array[k] += 1 
        
        
    else:
        #analysis for countries trend once data for every year of a country has been stored in lists
        #spearmans rank
        r1,r2 = stats.spearmanr(year_country,var_country)
        #linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(year_country,var_country) 
        #mean values
        mean = np.mean(var_country)
        mean10 = np.mean(var_country[-10:])
        
        #reject/accept status
        if p_value > 0.05:
            x = 'Reject_stat'
        elif slope < 0:
            x = 'Reject_-ve'
        elif r1 < 0.35:
            x = 'Reject_scatter'
        elif mean10 < 0.5 and slope < 0.01:
            x = 'reject_low_val'
        else:
            x = 'Accept'
            
            
       
        #storing countries data in data frame
        df2 = df2.append({'Country_name': df.iloc[i-1]['ID_country_name'],
                          'corelation':r_value,
                          'rank_Coeff':r1,
                          'slope': slope,
                          'std_err':std_err,
                          'intercept': intercept,
                          'p_value':p_value,
                          'mean':mean,
                          'mean_10':mean10,
                          'Reject/Accept':x},ignore_index=True)
        
        #readying the loop the next country in the set
        ID = df.iloc[i]['ID_country_code']
        year[len(df2)-1] = year_country
        var[len(df2)-1] = var_country
        year_country = []
        var_country = []

#saving copy of the individual country data to csv
if save_copy == True:
    df2.to_csv(save_title)

#plotting for avaraged values
if ave == True:
    sum_var = sum_var/ave_array
    slope, intercept, r_value, p_value, std_err = stats.linregress(year[0][:44],sum_var[:44])
    
    plt.figure(figsize=(40,20))
    plt.scatter(year[0][1:45],sum_var[1:45],s=250)
    plt.title(title,size = 75,pad = 25 )
    plt.xlabel(x_axis_title,size = 50)
    plt.ylabel(y_axis_title,size = 50)
    plt.xticks(year_array[1:45],rotation = 55,size=30)
    plt.yticks(size = 40)
    plt.grid()
    plt.show()

    
#plotting for individual country    
C = df2[df2['Country_name']== country].index.values
plt.figure(figsize=(40,20))
plt.scatter(year[C[0]],var[C[0]],marker='x',color='black',s = 500,linewidth = 4)
plt.plot(year[C[0]],df2['slope'][C[0]]*np.asarray(year[C[0]])+df2['intercept'][C[0]],color = 'red',linewidth = 3)
plt.title(title,size = 75,pad = 25 )
plt.xlabel(x_axis_title,size = 50)
plt.ylabel(y_axis_title,size = 50)
plt.xticks(np.asarray(year[C[0]]),rotation = 55,size=30)
plt.yticks(size = 40)
plt.grid()
plt.show()
        
    
    
