import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Function to load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Dashboard title
st.title("Data insights dashboard for interim submission")

# Loading data from multiple CSV files
data_files = ["data/benin_clean.csv", "data/sierraleone_clean.csv", "data/togo_clean.csv"]
data = pd.concat([load_data(file) for file in data_files], ignore_index=True)

# Dropping any leading or trailing whitespaces from column names
data.columns = data.columns.str.strip()

# Displaying dataset summary
st.subheader("Dataset Overview")
st.write(data.head())

# Boxplot of Global Horizontal Irradiance (GHI)
if 'GHI' in data.columns:
    st.subheader("Boxplot of GHI")
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data['GHI'])
    st.pyplot(plt)
else:
    st.warning("The dataset does not contain a 'GHI' column.")

# Ensuring 'Comments' column exists
if 'Comments' in data.columns:
    st.subheader("Sample Comments in Data")
    st.write(data['Comments'].dropna().head(10))

# Button for refreshing data
if st.button("Refresh Data"):
    st.rerun()