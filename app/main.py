import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

# dashboard title
st.title("Data Insights Dashboard")

# Load data from multiple CSV files
data_files = ["data/benin_clean.csv", "data/sierraleone_clean.csv", "data/togo_clean.csv"]
data = pd.concat([load_data(file) for file in data_files], ignore_index=True)

# Widget for country selection
countries = data['Country'].unique()
selected_country = st.selectbox("Select a Country", countries)

# Filter data based on selected country
country_data = data[data['Country'] == selected_country]

# Boxplot of Global Horizontal Irradiance (GHI)
st.subheader("Boxplot of GHI")
plt.figure(figsize=(10, 5))
sns.boxplot(x=country_data['GHI'])
st.pyplot(plt)

# Top regions table
st.subheader("Top Regions by GHI")
top_regions = country_data.groupby('Region')['GHI'].mean().nlargest(10).reset_index()
st.write(top_regions)

# Button for refreshing data
if st.button("Refresh Data"):
    st.experimental_rerun()