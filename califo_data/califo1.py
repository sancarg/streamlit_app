import streamlit as st 
import pandas as pd 
from sklearn.datasets import fetch_california_housing 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor

# Function to build and train the model 
def build_model(df): 
    X = df.drop(columns=['Target']) 
    y = df['Target'] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
    model = RandomForestRegressor() 
    model.fit(X_train, y_train) 
    st.session_state.model = model 
    st.session_state.model_trained = True
    r2_score = model.score(X_test, y_test) 
    st.session_state.model_r2_score = r2_score 
    st.write(f"Model trained with R^2 score: {model.score(X_test, y_test):.2f}")
# Function for user input features
def user_input_features():
    MedInc = st.number_input('Median Income', min_value=0.0, step=0.1)
    HouseAge = st.number_input('House Age', min_value=0, step=1)
    AveRooms = st.number_input('Average Rooms', min_value=0.0, step=0.1)
    AveBedrms = st.number_input('Average Bedrooms', min_value=0.0, step=0.1)
    Population = st.number_input('Population', min_value=0, step=1)
    AveOccup = st.number_input('Average Occupancy', min_value=0.0, step=0.1)
    Latitude = st.number_input('Latitude', min_value=0.0, step=0.0)
    Longitude = st.number_input('Longitude', min_value=-150.0, step=0.01)

    data = { 
        'MedInc': MedInc, 
        'HouseAge': HouseAge, 
        'AveRooms': AveRooms, 
        'AveBedrms': AveBedrms, 
        'Population': Population, 
        'AveOccup': AveOccup, 
        'Latitude': Latitude, 
        'Longitude': Longitude } 
    features = pd.DataFrame(data, index=[0]) 
    return features

st.subheader('1. Dataset')
st.info('Awaiting for CSV file to be uploaded.')

if st.button('Press to use Example Dataset'):
    califo = fetch_california_housing()
    df = pd.DataFrame(califo.data, columns=califo.feature_names)
    df['Target'] = califo.target

    st.markdown('The fetch_california_housing is used as the example.')
    st.write(df.head())
    build_model(df)

# Ensure model is trained before allowing predictions
if 'model' in st.session_state:
   # Always show the dataset head if available
   if 'df' in locals():
       st.write(df.head())
   
   # Subheader for predictions
   st.subheader('2. Make Predictions')
   st.info('Specify input features for prediction:')
   input_df = user_input_features()
   
   # Button to make prediction 
   if st.button('Predict'):
       prediction = st.session_state.model.predict(input_df)
       st.subheader('Prediction')
       st.write(f'Predicted Target: {prediction[0]:.2f}')
else:
    st.warning('Model is not trained yet. Please press the button above to train the model using the example dataset.')

       
    

                               