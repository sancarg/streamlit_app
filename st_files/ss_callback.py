import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if "type" not in st.session_state:
    st.session_state['type'] = 'Categorical'

# Load data
df = pd.read_csv('C:/Users/User/Desktop/2017_Yellow_Taxi_Trip_Data.csv')
df = df[['passenger_count', 'trip_distance', 'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount']]

# Define types
types = {'Categorical': ['PULocationID', 'DOLocationID', 'payment_type'], 'Numerical': ['passenger_count', 'trip_distance', 'fare_amount']}

# Callback function to handle radio button change
def handle_click_wo_button():
    st.session_state['type']    
       

# Radio button for type of analysis
type_of_column = st.radio("What kind of analysis", ['Categorical', 'Numerical'], on_change=handle_click_wo_button, key='type')

# Selectbox for column selection
column = st.selectbox('Select a column', types[st.session_state['type']])

# Display data based on selection
if st.session_state['type'] == 'Categorical':
    dist = pd.DataFrame(df[column].value_counts()).head(20)
    st.bar_chart(dist)
else:
    # Create subplots for each numerical column
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Plot histograms for each numerical column
    for i, col in enumerate(['passenger_count', 'trip_distance', 'fare_amount']):
        df[col].plot(kind='hist', ax=axes[i], title=col)

    # Display the subplots
    st.pyplot(fig)

# Display session state
#st.write(st.session_state)
