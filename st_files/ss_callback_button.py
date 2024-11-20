import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Let's explore session state and callback functions")

if "number_of_rows" not in st.session_state or "type" not in st.session_state:
    st.session_state["number_of_rows"] =5
    st.session_state['type'] = 'Categorical'
    

df = pd.read_csv('C:/Users/User/Desktop/2017_Yellow_Taxi_Trip_Data.csv')

df = df[['passenger_count', 'trip_distance', 'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount']]
#st.write("Filtered DataFrame:", df)
st.bar_chart(df.set_index('fare_amount'))

increment = st.button('Show more columns ')
if increment:
    st.session_state.number_of_rows += 1

decrement = st.button('Show less columns')
if decrement:
   st.session_state.number_of_rows -= 1 

st.table(df.head(st.session_state['number_of_rows']))


st.write(st.session_state)

types = {'Categorical':['PULocationID', 'DOLocationID', 'payment_type'], 'Numerical':['passenger_count', 'trip_distance', 'fare_amount']}


def handle_click(new_type):
    st.session_state['type'] = new_type

type_of_column = st.radio("Choose Analysis Type", ['Categorical', 'Numerical'])

change = st.button('Change Analysis Type', on_click=handle_click, args = [type_of_column])
column = st.selectbox('Select a column', (types[st.session_state['type']]))

# In place of the preceding code block;
#def handle_click(new_type):
#    st.session_state['type'] = st.session_state['type_of_column']

# type_of_column = st.radio("Choose Analysis Type", ['Categorical', 'Numerical'], key='type_of_column')
#change = st.button('Change Analysis Type', on_click=handle_click)
#column = st.selectbox('Select a column', (types[st.session_state['type']]))

if st.session_state['type']=='Categorical':
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