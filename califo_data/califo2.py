import streamlit as st 
import pandas as pd 
from sklearn.datasets import fetch_california_housing 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import ssl, certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())



## Page layout
## Page expands to full width
st.set_page_config(page_title='The Machine Learning App for Streamlit', layout='wide', page_icon="random")
st.image("https://th.bing.com/th/id/R.a1d475075bd59c35ce4db0d99b54f44d?rik=mUDMHc3EY%2bYdJQ&riu=http%3a%2f%2fmedia.architecturaldigest.com%2fphotos%2f56abe0b945b074d074914ae1%2fmaster%2fpass%2fcalifornia-homes-03.jpg&ehk=zvWEvCgVPFWcJCrMxFPGeT8CnNOVn%2bOD%2fmKC4DcORQ8%3d&risl=1&pid=ImgRaw&r=0", caption="Architectural Digest", use_container_width=True)

# Function to build and train the model 
def build_model(df): 
    X = df.drop(columns=['Target']) 
    y = df['Target'] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_size) 
    model = RandomForestRegressor( 
        n_estimators=parameter_n_estimators, 
        random_state=parameter_random_state,
        max_features=parameter_max_features,
        criterion=parameter_criterion,
        min_samples_split=parameter_min_samples_split,
        min_samples_leaf=parameter_min_samples_leaf,
        bootstrap=parameter_bootstrap,
        oob_score=parameter_oob_score,
        n_jobs=parameter_n_jobs
    )    
    model.fit(X_train, y_train)
    st.session_state.model = model
    st.session_state.model_trained = True
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    st.session_state.model_r2_score = r2 # Save the R² score in session state
    
# Function for user input features
def user_input_features():
    MedInc = st.number_input('Median Income', min_value=0.0, step=0.1)
    HouseAge = st.number_input('House Age', min_value=0, step=1)
    AveRooms = st.number_input('Average Rooms', min_value=0.0, step=0.1)
    AveBedrms = st.number_input('Average Bedrooms', min_value=0.0, step=0.1)
    Population = st.number_input('Population', min_value=0, step=1)
    AveOccup = st.number_input('Average Occupancy', min_value=0.0, step=0.1)
    Latitude = st.number_input('Latitude', min_value=0.0, step=0.01)
    Longitude = st.number_input('Longitude', min_value=-150.0, step=0.01)

    data = { 
        'MedInc': MedInc, 
        'HouseAge': HouseAge, 
        'AveRooms': AveRooms, 
        'AveBedrms': AveBedrms, 
        'Population': Population, 
        'AveOccup': AveOccup, 
        'Latitude': Latitude, 
        'Longitude': Longitude 
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Sidebar - Specify parameter setting
st.sidebar.header("Please define parameters before loading dataset!!!")
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 10, 5)

with st.sidebar.subheader('2.1. Learning Parameters'):
    parameter_n_estimators = st.sidebar.slider('Number of estimators (n_estimators)', 0, 1000, 100, 100)
    parameter_max_features = st.sidebar.radio('Max features (max_features)', options=['sqrt', 'log2'])
    parameter_min_samples_split = st.sidebar.slider('minimum number of samples required to split an internal node (min_samples_split)',1, 10, 2, 1)
    parameter_min_samples_leaf = st.sidebar.slider('minimum number of samples required to split an internal node (min_samples_leaf)', 1, 10, 2, 1)

with st.sidebar.subheader('2.2. General Parameters' ):
    parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
    parameter_criterion = st.sidebar.selectbox('Performance measure (criterion)', options=['absolute_error', 'friedman_mse', 'squared_error', 'poisson'])
    parameter_bootstrap = st.sidebar.select_slider('Bootsrap samples when building trees(bootsrap)', options=[True, False])
    parameter_oob_score = st.sidebar.select_slider('Whether to out-of-bag samples to estimate the R^2 on unseen data=oob_score', options=[True, False])
    parameter_n_jobs = st.sidebar.select_slider(' Number of jobs to run in parallel', options=[1, -1])

st.subheader('1. Dataset')

if st.button('Press to use Example Dataset'):
    califo = fetch_california_housing()
    # The fetch_california_housing() function from sklearn.datasets returns a dictionary-like object called a Bunch, 
    # which contains the data in a structured format. This Bunch object includes attributes like data, target, 
    # feature_names, etc.
    df = pd.DataFrame(califo.data, columns=califo.feature_names)
    df['Target'] = califo.target
    st.session_state['df'] = df
    st.session_state['shape'] = df.shape

    st.markdown('The fetch_california_housing is used as the example.')
    #Since the st.markdown line is within the block that only runs when the button is pressed, the message will appear after clicking the button and will remain visible in the Streamlit app until the app layout changes
    build_model(df)

# Ensure model is trained before allowing predictions
if 'model' in st.session_state and st.session_state.model_trained:
   # Always show the dataset head if available
   if 'df' and 'shape' in st.session_state:
       st.write(st.session_state['df'].head())
       st.write(f"Training Set : {st.session_state['shape']}")
       st.write(f"Model trained with R² score: {st.session_state.model_r2_score:.2f}")
    # Subheader for predictions
   st.subheader('2. Make Predictions')
   st.info('Specify input features for prediction:')
   input_df = user_input_features()
   st.write("User Input Features:")
   st.dataframe(input_df)

   # Button to make prediction 
   if st.button('Predict'):
       prediction = st.session_state.model.predict(input_df)
       st.subheader('Prediction')
       st.write(f'Predicted Target: {prediction[0]:.2f}')
else:
    st.warning('Model is not trained yet. Please press the button above to train the model using the example dataset.')
    