import streamlit as st
import pandas as pd

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

feat_types = {'Categorical':['PULocationID', 'DOLocationID', 'payment_type'], 'Numerical':['passenger_count', 'trip_distance', 'fare_amount']}
column = st.selectbox('Select a column', feat_types[st.session_state['type']])


st.session_state['type'] = st.radio("What kind of analysis", ['Categorical', 'Numerical'])
#Because of session_state, when we select categorical or numerical analysis on radio selection
#list of "select a column" doesn't change. But the graph demonstrates the right result.


#selected_type = st.radio("Select Type", ('Categorical', 'Numerical'))
# Display the corresponding options based on the selected type
#if selected_type:
#    selected_option = st.selectbox(f"Select {selected_type} Option", types[selected_type])
#    st.write(f"You selected: {selected_option}")

if st.session_state['type']=='Categorical':
    dist = pd.DataFrame(df[column].value_counts()).head(20)
    st.bar_chart(dist)
else:
    st.table(df[column].describe())