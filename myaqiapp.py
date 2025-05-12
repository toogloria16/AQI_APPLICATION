import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
streamlit run /usr/local/lib/python3.11/dist-packages/colab_kernel_launcher.py [ARGUMENTS]
st.set_page_config(layout="wide")
st.title("Air Quality Data Analysis App")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Combined_Stations_with_AQI.csv")
    return df

df = load_data()

st.header("Dataset Overview")
st.write(df.head())

st.subheader("Data Summary")
st.write(df.describe())

st.subheader("Missing Values")
st.write(df.isnull().sum())

# EDA: AQI Distribution
st.header("Exploratory Data Analysis (EDA)")
st.subheader("AQI Distribution by Station")
selected_station = st.selectbox("Select Station", df['station'].unique())
station_df = df[df['station'] == selected_station]

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(station_df['AQI'].dropna(), bins=30, kde=True, ax=ax)
ax.set_title(f"AQI Distribution - {selected_station}")
st.pyplot(fig)

# Yearly Analysis by Station
st.header("Yearly AQI Analysis by Station")

yearly_aqi = df.groupby(['station', 'year'])['AQI'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
for station in yearly_aqi['station'].unique():
    data = yearly_aqi[yearly_aqi['station'] == station]
    ax.plot(data['year'], data['AQI'], label=station)
ax.set_title("Yearly Average AQI by Station")
ax.set_xlabel("Year")
ax.set_ylabel("Average AQI")
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
st.pyplot(fig)

# AQI Summary Table
st.header("AQI Summary by Station")
aqi_summary = df.groupby('station')['AQI'].agg(['mean', 'min', 'max', 'std']).reset_index()
st.dataframe(aqi_summary.style.format({"mean": "{:.2f}", "min": "{:.0f}", "max": "{:.0f}", "std": "{:.2f}"}))

# Additional Interactive Plot
st.subheader("Compare Pollutants Over Time")
pollutant = st.selectbox("Select Pollutant", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
yearly_pollutant = df.groupby(['station', 'year'])[pollutant].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
for station in yearly_pollutant['station'].unique():
    data = yearly_pollutant[yearly_pollutant['station'] == station]
    ax.plot(data['year'], data[pollutant], label=station)
ax.set_title(f"Yearly Average {pollutant} by Station")
ax.set_xlabel("Year")
ax.set_ylabel(f"Average {pollutant}")
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
st.pyplot(fig)

st.write("Developed using Streamlit - Air Quality Analysis Dashboard")
