import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

st.sidebar.header("Dashboard Controls")
option = st.sidebar.selectbox("Select a category:", ["Overview", "Data", "Visualization"])

day_df = pd.read_csv("Dashboard/day_data_clean.csv")
day_df['weekly_avg'] = day_df['cnt'].rolling(7).mean()

hour_df = pd.read_csv("Dashboard/hour_data_clean.csv")
hourly_rentals = hour_df.groupby("hr")["cnt"].sum()

# Main Content
st.title("Simple Streamlit Dashboard")

if option == "Overview":
    st.write("### Overview")
    st.metric("Total Rental Value", day_df["cnt"].sum())

elif option == "Data":
    st.write("### Data Table Day")
    st.dataframe(day_df)
    
    st.write("### Data Table Hour")
    st.dataframe(hour_df)
    
elif option == "Visualization":
    st.write("### Weekly Average Rentals")
    day_df['weekly_avg'] = day_df['cnt'].rolling(7).mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(day_df['dteday'], day_df['weekly_avg'], color='red')
    ax.set_xlabel('Date', size=12)
    ax.set_ylabel('User', size=12)
    ax.set_title('Weekly Average Rentals')
    st.pyplot(fig)
    
    
    st.write("### Bike Rentals by Hour")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hourly_rentals.index, hourly_rentals.values, color="skyblue", edgecolor="black")
    ax.set_xlabel("Hour of the Day", fontsize=10)
    ax.set_ylabel("Total Rentals", fontsize=10)
    ax.set_title("Bike Rentals by Hour", fontsize=12)
    ax.set_xticks(range(0, 24))  
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

