import streamlit as st
import pandas as pd

st.title("Let's explore session state and callback functions")

if "type" not in st.session_state or 'kind_of_column' not in st.session_state:
    st.session_state['kind_of_column']='Categorical'

df = pd.read_csv('C:/Users/User/Desktop/2017_Yellow_Taxi_Trip_Data.csv')

df = df[['passenger_count', 'trip_distance', 'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount']]
#st.write("Filtered DataFrame:", df)
st.bar_chart(df.set_index('fare_amount'))

st.write(st.session_state)

types = {'Categorical':['PULocationID', 'DOLocationID', 'payment_type'], 'Numerical':['passenger_count', 'trip_distance', 'fare_amount']}

def handle_click_wo_button():
    st.session_state.type=st.session_state.kind_of_column

kind_of_column = st.radio("What kind of analysis", ['Categorical', 'Numerical'], on_change=handle_click_wo_button, key='kind_of_column')
column = st.selectbox('Select a column', types[st.session_state['type']])

if st.session_state['type']=='Categorical':
    dist = pd.DataFrame(df[column].value_counts()).head(20)
    st.bar_chart(dist)
else:
    st.table(df[column].describe())