import streamlit as st
import pandas as pd
import numpy as np

# 1. Using form
with st.form("form1"):
   st.write("Inside the form")
   my_number = st.slider('Pick a number', 1, 10)
   my_color = st.selectbox('Pick a color', ['red','orange','green','blue','violet'])
   my_stuff = st.radio('Pick a stuff', ['ball', 'hat', 'luggage'])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_number)
st.write(my_color)
st.write(my_stuff)

form = st.form("form2")
form.slider("Inside the form")
st.slider("Outside the form")

# Now add a submit button to the form:
form.form_submit_button("Submit")

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")

# 2. Mathematic
if 'sum' not in st.session_state:
    st.session_state.sum = ''

def sum():
    result = st.session_state.a + st.session_state.b
    st.session_state.sum = result

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    st.number_input('a', key = 'a')
    st.number_input('b', key = 'b')
    st.form_submit_button('add', on_click=sum)
    
st.write("kg to lb / lb to kg")

if "kg" not in st.session_state:
    st.session_state.kg = 0
if "lb" not in st.session_state:
    st.session_state.lb = 0

def lb_to_kg():
    st.session_state.kg = st.session_state.lb/2.2046

def kg_to_lb():
    st.session_state.lb = st.session_state.kg*2.2046

col1, buff, col2 = st.columns([2, 1, 2], gap="small")
with col1:
    pounds = st.number_input("Pounds:", key="lb", on_change=lb_to_kg)

with col2:
    kilogram = st.number_input("Kilogram", key="kg", on_change=kg_to_lb)


# 3. Arranging an Appointment
from datetime import time
appointment = st.slider("Schedule your appointment:", value=(time(11, 30), time(12, 45)))
st.write("You're scheduled for:", appointment)

# 4. Arranging Values
values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.write("Values:", values)

# 5. Initialize the checkbox state
if 'show' not in st.session_state:
    st.session_state.show = False
#if 'show' not in st.session_state:
#    st.session_state.show = False

# Checkbox to toggle visibility
st.session_state.show = st.checkbox("Show text input", st.session_state.show)

# Conditionally display the text input
if st.session_state.show:
    text = st.text_input("Enter some text", key="text") #st.session_state.text = st.text_input("Enter some text", st.session_state.text)
    st.write(f"You entered: {st.session_state.text}")

# 6. Initialize the step in session state
if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def reset_steps():
    st.session_state.step = 1

# Step 1
if st.session_state.step == 1:
    st.session_state.name = st.text_input("Enter your name")
    if st.button("Next", on_click=next_step):
        pass

# Step 2
elif st.session_state.step == 2:
    st.session_state.age = st.number_input("Enter your age", min_value=0)
    if st.button("Next", on_click=next_step):
        pass

# Step 3
elif st.session_state.step == 3:
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Age: {st.session_state.age}")
    if st.button("Reset", on_click=reset_steps):
        pass

# 7. st.columns (with left, middle, right)



vertical_alignment = st.selectbox(
    "Vertical alignment", ["top", "center", "bottom"], index=2
)

left, middle, right = st.columns(3, vertical_alignment=vertical_alignment)
left.image("https://static.streamlit.io/examples/cat.jpg", caption="By @phonvanna")

middle.image("https://static.streamlit.io/examples/dog.jpg", caption="By @shotbyrain")

right.image("https://static.streamlit.io/examples/owl.jpg", caption="By @zmachacek")

color = st.color_picker("Pick A Color", "#00f900")
st.write("The current color is", color)

on = st.toggle("Activate feature")

if on:
    st.write("Feature activated!")

df = pd.DataFrame(
    np.random.randn(20, 2) / [22, 48] + [36.76, 34.5],
    columns=["lat", "lon"],
)
# Generate random data
data = np.random.randn(20, 2) / [22, 48] + [36.76, 34.5] 
# [36.76, 34.5] part is lat and lon (ccoordinates) two column list get by np.random.randn(20, 2) divided by [22, 48]

# Create a DataFrame
df = pd.DataFrame(data, columns=["lat", "lon"])
st.table(df.head())

st.map(df)

df = pd.DataFrame(
    {
        "col1": np.random.randn(12) / 50 + 36.76,
        "col2": np.random.randn(12) / 50 + 34.5,
        "col3": np.random.randn(12) * 100,
        "col4": np.random.rand(12, 4).tolist(), # RGBA tuple with the red, green, blue, and alpha components 
        #specified as ints from 0 to 255 or floats from 0.0 to 1.0. 
    }
)

st.map(df, latitude="col1", longitude="col2", size="col3", color="col4")
