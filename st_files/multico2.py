import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def get_co2_data(): 
    url = 'https://raw.githubusercontent.com/alanjones2/CO2/master/data/countries_df.csv'
    df = pd.read_csv(url)
    df = df[['Entity', 'Year', 'Code', 'Annual CO₂ emissions']]
    return df

if "countries" not in st.session_state:
        st.session_state['countries'] = []
def add_country(c):
    if c not in st.session_state['countries']:
        st.session_state['countries'].append(c)

def remove_country(c):
    if c in st.session_state['countries']:
        st.session_state['countries'].remove(c)

def get_country_list():
    return st.session_state['countries']

st.title("CO2 Emissions")

# Get the data
df = get_co2_data()
#st.table(df.head())

# Create a list of all countries
all_countries = df['Entity'].unique()

country_input = st.text_input("Specifiy a country")

col1, col2 = st.columns(2)
with col1:
    if st.button("Add"):
        if country_input in all_countries:
            add_country(country_input)
        else:
            st.warning(f"{country_input} is not in the country list")
with col2:
    if st.button("Delete"): 
        if country_input in all_countries:
            remove_country(country_input)
        else:
            st.warning(f"{country_input} is not in the country list")

# Draw a chart of CO2 emissions for selected countries
df1 = df.query('Entity in @get_country_list()' )
fig = px.line(df1,"Year","Annual CO₂ emissions",color="Entity")
st.plotly_chart(fig, use_container_width=True)
