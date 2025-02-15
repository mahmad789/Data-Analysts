import pandas as pd 
import streamlit as st
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time




st.set_page_config(page_title='Data Dashborad', layout='wide')

st.sidebar.header('Upload Your File')
upload_file = st.sidebar.file_uploader("Choose a  File " , type=['csv','xlsx','json'])


if upload_file is not None:
    if upload_file.name.endswith('.csv'):
        data = pd.read_csv(upload_file)
    elif upload_file.name.endswith('.xlsx'):
        data = pd.read_excel(upload_file)
    elif upload_file.name.endswith('.json'):
        data = pd.read_json(upload_file)
    else:
        st.error('unsupported file format')


    st.title('Machine Learning Data')
    st.subheader('Data Overview')

    st.write(data.head(3))
    st.subheader('Columns Details', divider='rainbow')

    col1,col2 = st.columns(2)

    with col1:
        st.subheader('Data Types',divider='grey')
        st.write(data.dtypes)
    with col2:
        st.subheader('Missing Values', divider='grey')
        missing_values = data.isnull().sum()
        missing_percentage = (missing_values / len(data)) * 100
        missing_df = pd.DataFrame({
            'Missing Values': missing_values,
            'Percentage (%)': missing_percentage
        })
        st.write(missing_df)
    st.write(f'The total null values is {data.isnull().sum().sum()}')
    st.write(f'The percentage of total null values is {(data.isnull().sum().sum()/data.size)*100}')
    st.subheader('Data Summary')
    st.write(data.describe())

    st.subheader('Missing Value Heat Map')
    fig,ax = plt.subplots(figsize=(10,5))
    sb.heatmap(data.isnull(),ax=ax,cbar=False)
    st.pyplot(fig)


    st.subheader('Data Distribution')
    cols = data.select_dtypes(include=['int64','float64']).columns

    if len(cols) > 0:
        selected_col = st.selectbox("Select a column for distribution",cols)
        fig = px.histogram(data, x=selected_col, nbins=30, title=f"Distribution of {selected_col}")
        st.plotly_chart(fig)
    else:
        st.warning("No numeric columns found!")
    st.subheader("Correlation Heatmap")
        

    numeric_df = data.select_dtypes(include=['number'])
    if len(numeric_df.columns) > 1:
        fig, ax = plt.subplots(figsize=(8, 5))
        sb.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric columns for correlation analysis.")
    
    st.subheader('Categorical Data')
    ct = data.select_dtypes(include='object').columns


    if len(ct) > 0:
        selected_cat = st.selectbox("Select a categorical column", ct)
        fig = px.bar(data[selected_cat].value_counts(), title=f"Count of {selected_cat}")
        st.plotly_chart(fig)
    else:
        st.warning("No categorical columns found!")

