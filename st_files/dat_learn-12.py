import streamlit as st
import pandas as pd

def callback():
    st.session_state.my_slider
    st.session_state.my_checkbox
with st.form(key="my_form"):
    slider_input = st.slider("my_slider", 0, 15, 5, key="my_slider")
    checkbox_input = st.checkbox("selection", key="my_checkbox")
    submit_button = st.form_submit_button("Submit", on_click=callback)


