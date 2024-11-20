import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def get_co2_data(): 
    url = 'https://raw.githubusercontent.com/alanjones2/CO2/master/data/countries_df.csv'
    df = pd.read_csv(url)
    df = df[['Entity', 'Year', 'Code', 'Annual CO₂ emissions']]
    return df

st.title("CO2 Emissions")
# Get the data
df = get_co2_data()

# Create a list of countries
countries = df['Entity'].unique()

# Select one or more countries
selected_countries = st.multiselect("Select Countries", countries, default="United States")
df1 = df.query('Entity in @selected_countries' )

# Draw a chart of CO2 emissions for selected countries
fig = px.line(df1,"Year","Annual CO₂ emissions",color="Entity")
st.plotly_chart(fig, use_container_width=True)



#2 input country but showing only one result at once
countries_all = df['Entity'].unique()
countries_selected = []

input_country = st.text_input("Add a country")
if input_country in countries_all:
    countries_selected.append(input_country)
else:
    st.warning(f"{input_country} is not in the country list")

df1 = df.query('Entity in @countries_selected' )

# Draw a chart of CO2 emissions for selected countries
fig = px.line(df1,"Year","Annual CO₂ emissions",color="Entity")
st.plotly_chart(fig, use_container_width=True)

