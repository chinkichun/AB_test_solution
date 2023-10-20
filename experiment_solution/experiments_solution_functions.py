#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pingouin as pg #for t-Test
import os
import scipy.stats
import itertools


# In[2]:


#Get averages of all metrics per test group

def group_averages(df):
    # group the data by the specified group column
    groups = df.groupby('Test Group Id')
    
    # create a new dataframe to store the averages
    averages = pd.DataFrame()
    
    # loop through all columns in the original dataframe
    for col in df.columns:
        # skip the group column
        if col == 'Test Group Id':
            continue
            
        elif col == 'Date':
            continue
            
        elif col == 'Country':
            continue
        
        else:
        # calculate the average for each group
            col_averages = groups[col].mean()

            # add the column to the new dataframe, with the group as the row index
            # averages[col] = col_averages.round(2)
            averages[col]= col_averages.round(2).apply(lambda x: str(x).rstrip('0').rstrip('.') if '.' in str(x) else str(x))
    
    # transpose the new dataframe so that the columns become rows and vice versa
    averages = averages.transpose()
    averages.columns = pd.Index([f"Group {idx}" for idx in averages.columns], name='Test Group Id')
    
    return averages


# In[3]:


#Pivot df for further processing - ftest and ttest

def pivot_df(df):
    # Define the index and column names for the pivoted DataFrames
    index = 'Date'
    columns = 'Test Group Id'
    
    # Create a dictionary to store the pivoted DataFrames
    
    global pivoted_dfs
    pivoted_dfs = {}
    
    # Loop through each column in the original DataFrame
    for col in df.columns:
        
        if col == 'Date':
            continue # also add skip 'country' column here
        
        elif col == 'Country':
            continue
            
        elif col == 'Test Group Id':
            continue
            
        else:
            # Pivot the column as values against the index and columns
            pivoted_col = df.pivot(index=index, columns=columns, values=col)
            pivoted_col = pivoted_col.reset_index()
            # Store the pivoted DataFrame in the dictionary
#             pivoted_dfs[f"pivot_df_{col}"] = pivoted_col
            pivoted_dfs[f"{col}"] = pivoted_col
    
    # Return the dictionary of pivoted DataFrames
    
    
    return pivoted_dfs



# In[4]:


#Define F-Test function.

#comment our irrelevant info


#define F-Test function
def f_test(group1, group2):
    f = np.var(group1, ddof=1)/np.var(group2, ddof=1)
    nun = group1.size-1
    dun = group2.size-1
    p_value = 1-scipy.stats.f.cdf(f, nun, dun)
    
    global p_value_2t
    p_value_2t = p_value*2
    
#     print('F-score is: {} '.format(f))
#     print('2 tailed p-Value is: {} '.format(p_value_2t))
    
    
    global correction
    if p_value_2t <= 0.05:
        correction = True
#         print ('Reject F-test Null hypothesis and assume unequal variance btw samples')
    
    else:
        correction = False
#         print ('Fail to reject F-test Null hypothesis and assume equal variance btw samples')


# In[6]:


#define t_test function 

# make p-val dynamic so that users can select their own value

correction = False

def t_test(gp1, gp2, alternative='two-sided', correction=correction): #other options ['less', 'greater']
    tTest = pg.ttest(gp1, gp2, alternative = alternative, correction = correction)
    
    gp1_average = gp1.mean().round(2)
    gp2_average = gp2.mean().round(2)
    
#     print('gp1 average is: {} '.format(gp1_average))
#     print('gp2 average is: {} '.format(gp2_average))
#     print(tTest)
    
#     global tTest_df
#     tTest_df = tTest
    
    p_val = tTest.at['T-test', 'p-val']
    p_val = p_val.round(4)
    
    print('t-test p_value is: {} '.format(tTest.at['T-test', 'p-val']))

    if p_val < 0.05: #95% confidence level #make this a variable instead of hard coded
        return 'STATISTICAL DIFFERENCE between group {} (mean = {}) and group {} (mean = {}) with p-value of {}'.format(gp1.name, gp1_average, gp2.name, gp2_average, p_val)

    else:
        return 'No statistical difference between group {} (mean = {}) and group {} (mean = {}) with p-value of {}'.format(gp1.name, gp1_average, gp2.name, gp2_average, p_val)
# In[7]:


#Stat test function - combines f_test and t_test

def stat_test(pivoted_dfs):
    
    t_test_results = []
    
    for key in pivoted_dfs.keys():
        df = pivoted_dfs[key]
    
        # Ignore if the "Date" column is present in the current dataframe
        if 'Date' in df.columns:
            cols = [c for c in pivoted_dfs[key].columns if c != 'Date']
        else:
            cols = pivoted_dfs[key].columns

        # Generate all possible pairs of column names
        column_pairs = list(itertools.combinations(cols, 2))

        for pair in column_pairs:
            col1, col2 = pair
#             print(f"Test results for {col1} vs {col2}")
            f_test(df[col1], df[col2])
            t_test_result = t_test(df[col1], df[col2])
            t_test_results.append({'Metric': '{} - group {} vs group {}'.format(key, col1, col2), 
                                   'Result': t_test_result})
    
    global df_results
    df_results = pd.DataFrame(t_test_results)
    df_results.index = df_results.index + 1
    return df_results



# In[ ]:




