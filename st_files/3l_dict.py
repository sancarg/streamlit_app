import streamlit as st
import pandas as pd

df = pd.read_csv('C:/Users/User/Desktop/2017_Yellow_Taxi_Trip_Data.csv')
df = df[['passenger_count', 'trip_distance', 'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount']]

# Define types with sub-categories
types = {
    'Categorical': {
        'Location': ['PULocationID', 'DOLocationID'],
        'Payment': ['payment_type']
    },
    'Numerical': {
        'Passenger': ['passenger_count'],
        'Trip': ['trip_distance', 'fare_amount']
    }
}

# Callback function to handle radio button change
def handle_click_wo_button():
    st.session_state['type']   
# we can remove def function and on_change parameter only by using key parameter(for session_state) to get the same result.
# Streamlit automatically manages the session state for widgets like radio buttons, select boxes, and 
# others when you use the key parameter. This means that if a user interacts with the widget, the selected value is 
# stored in st.session_state and can be accessed later in the script.

# Radio button for type of analysis
kind_of_column = st.radio("What kind of analysis", ['Categorical', 'Numerical'], on_change=handle_click_wo_button, key='type')

# Selectbox for sub-category selection
sub_category = st.selectbox('Select a sub-category', list(types[st.session_state['type']].keys()))

# Purpose: This select box allows the user to choose a sub-category (e.g., ‘Location’ or ‘Payment’ under ‘Categorical’, 
# #‘Passenger’ or ‘Trip’ under ‘Numerical’).
# Options: The options are dynamically generated based on the selected type (‘Categorical’ or ‘Numerical’) 
# from the radio button. It lists the keys of the nested dictionary corresponding to the selected type.
# This selectbox select box (sub_category) narrows down the choices to a RELEVANT subset (sub-categories)
# Selectbox for column selection

column = st.selectbox('Select a column', types[st.session_state['type']][sub_category])

# Purpose: This select box allows the user to choose a specific column within the selected sub-category.
# Display data based on selection
# Options: The options are dynamically generated based on the selected sub-category. It lists the columns (values) 
# within the nested dictionary corresponding to the selected sub-category.
# This select box (column) further narrows it down to specific columns within that subset.

# Adding visualization options 
visualization_type = st.selectbox('Select a visualization type', ['Bar Chart', 'Histogram', 'Line Chart']) 

# Displaying data based on selection 
if st.session_state['type'] == 'Categorical': 
    dist = pd.DataFrame(df[column].value_counts()) 
    if visualization_type == 'Bar Chart': 
        st.bar_chart(dist) 
    elif visualization_type == 'Line Chart': 
        st.line_chart(dist) 
else: 
    if visualization_type == 'Histogram': 
        st.hist(df[column]) 
    elif visualization_type == 'Line Chart': 
        st.line_chart(df[column].dropna()) 
    else: st.table(df[column].describe())