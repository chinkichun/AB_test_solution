import streamlit as st

import pandas as pd
import numpy as np
import pingouin as pg #for t-Test
import os
import scipy.stats
import os
import itertools

from experiments_solution_functions import group_averages, pivot_df, f_test, t_test, stat_test

correction = False  #default correction before f-Test

# Set page title
st.set_page_config(page_title='Statistical Test Solution', layout = 'wide')

# Define a function to read a CSV file and return a DataFrame
def read_csv(file):
    df = pd.read_csv(file)
    return df



def bg_color(result):
    color = '#66ff99' if 'STATISTICAL DIFFERENCE' in result else ''
    return f'background-color: {color}'

# Define the Streamlit app
def main():
    # Set app title
    st.markdown(
        f"<h1 style='text-align: left; color: green;'>A/B Test Solution</h1>",
        unsafe_allow_html=True
    )

    st.markdown('''
        *Upload csv in format*: **:blue[[Test Group id | Group Member | Metric 1 | Metric 2 | Metric n...]]**''')

    # st.title('Statistical Test Solution')
    
    
    # Create a file uploader
    file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    # Add a "Go" button
    if st.button('Run Test'):
        # If the "Go" button is clicked and a file was uploaded, read it into a DataFrame
        if file is not None:
            df = read_csv(file)

            st.subheader('Daily Averages')

            averages = group_averages(df)
            st.write(averages.style.set_table_attributes('style="width: 100%;"'))
            # st.table(averages)

            st.subheader('Test Results')

            pivoted_df = pivot_df(df)
            # Process the DataFrame and display the results
            stat_test_result = stat_test(pivoted_df)
            # st.write(stat_test_result.style.set_table_attributes('style="width: 100%;"'))
            # st.table(stat_test_result)
            st.table(stat_test_result.style.applymap(bg_color, subset=['Result']))




if __name__ == '__main__':
    main()