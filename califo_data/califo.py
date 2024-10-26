import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
from sklearn.datasets import fetch_california_housing

#-----------------------------------------------#
## Page layout
## Page expands to full width
st.set_page_config(page_title='The Machine Learning App for Streamlit', layout='wide', page_icon="random")
st.image("https://th.bing.com/th/id/R.a1d475075bd59c35ce4db0d99b54f44d?rik=mUDMHc3EY%2bYdJQ&riu=http%3a%2f%2fmedia.architecturaldigest.com%2fphotos%2f56abe0b945b074d074914ae1%2fmaster%2fpass%2fcalifornia-homes-03.jpg&ehk=zvWEvCgVPFWcJCrMxFPGeT8CnNOVn%2bOD%2fmKC4DcORQ8%3d&risl=1&pid=ImgRaw&r=0", caption="Architectural Digest", use_column_width=True)

#-----------------------------------------------#
# Load example data
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = data.target

# Model building
def build_model(df):
    X = df.drop(columns=['Target'])
    y = df['Target']

    st.markdown('**1.2. Data Train-Test Splits**')
    st.write('Training Set')
    st.info(X.shape)
    st.write('Test Set')
    st.info(y.shape)

    st.markdown('**1.3. Variable details**')
    st.write('X variable')
    st.info(list(X.columns))
    st.write('Y variable')
    st.info(y.name, icon="🚨")

    # Data Splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_size)
    rf = RandomForestRegressor(n_estimators=parameter_n_estimators,
                               random_state=parameter_random_state,
                               max_features=parameter_max_features,
                               criterion=parameter_criterion,
                               min_samples_split=parameter_min_samples_split,
                               min_samples_leaf=parameter_min_samples_leaf,
                               bootstrap=parameter_bootstrap,
                               oob_score=parameter_oob_score,
                               n_jobs=parameter_n_jobs)
    rf.fit(X_train, y_train)

    st.subheader('2. Model Performance')
    st.info('Random Forest Model will be used', icon=":forest:")
    st.markdown('**2.1. Training Set**')
    Y_pred_train = rf.predict(X_train)
    st.write('Coefficient of Determination ($R^2$):')
    st.info(r2_score(y_train, Y_pred_train))

    st.write('Error(RMSE or MAE):')
    st.info( root_mean_squared_error(y_train, Y_pred_train))

    st.markdown('**2.2. Test Set**')
    Y_pred_test = rf.predict(X_test)
    st.write('Coefficient of determination ($R^2$):')
    st.info(r2_score(y_test, Y_pred_test))

    st.write('Error(RMSE or MAE):')
    st.info( root_mean_squared_error(y_test, Y_pred_test))

    st.subheader('3. Model Parameters')
    st.write(rf.get_params())

#------------------------------------------------#
st.write("""
         # The Machine Learning App
         
    In this implementation, The RandomForestRegressor() = function is used in this app for building a regression
    model using the **Random Forest** 🌳🌲 algorithm
         
    Try adjusting the hyperparameters!
""")

#------------------------------------------------#
# Sidebar - Collects user input features into dataframe.
                                           
# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Trainin Set)', 10, 90,5)

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

# Main Panel

#Display The Dataset
st.subheader('1. Dataset')
st.table(df.head())
st.info('Awaiting for CSV file to be uploaded.')
if st.button('Press to use Example Dataset'):
    # California Housing Dataset
    califo = fetch_california_housing()
    df = pd.DataFrame(califo.data, columns=califo.feature_names)
    df['Target'] = califo.target

    st.markdown('The fetch_california_housing is used as the example.')
    st.write(df.head())
    build_model(df)


