import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

st.sidebar.header("Dashboard Controls")
option = st.sidebar.selectbox("Select a category:", ["Overview", "Data", "Visualization"])

day_df = pd.read_csv("Dashboard/day_data_clean.csv")
hour_df = pd.read_csv("Dashboard/hour_data_clean.csv")
hourly_rentals = hour_df.groupby("hr")['cnt'].sum()

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
    st.write("### Select Aggregation Type")
    agg_option = st.radio("Choose aggregation type:", ["Daily Average", "Weekly Average", "3-Month Average"])
    
    if agg_option == "Daily Average":
        day_df['agg_avg'] = day_df['cnt']
        day_df['label'] = [f"Day {i+1}" for i in range(len(day_df))]
    elif agg_option == "Weekly Average":
        day_df['agg_avg'] = day_df['cnt'].rolling(7).mean()
        day_df['label'] = [f"Week {i//7 + 1}" for i in range(len(day_df))]
    elif agg_option == "3-Month Average":
        day_df['agg_avg'] = day_df['cnt'].rolling(90).mean()
        day_df['label'] = [f"Month {i//30 + 1}" for i in range(len(day_df))]
    
    # Line Chart
    st.write(f"### {agg_option} Rentals")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(day_df['dteday'], day_df['agg_avg'], color='red')
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=9, maxticks=9))
    ax.set_xticklabels(day_df['label'][::len(day_df)//9], rotation=30, ha='right')
    ax.set_xlabel('Time Period', size=12)
    ax.set_ylabel('User', size=12)
    ax.set_title(f'{agg_option} Rentals')
    st.pyplot(fig)
    
    # Bar Chart
    st.write("### Bike Rentals by Hour")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hourly_rentals.index, hourly_rentals.values, color="skyblue", edgecolor="black")
    ax.set_xlabel("Hour of the Day", fontsize=10)
    ax.set_ylabel("Total Rentals", fontsize=10)
    ax.set_title("Bike Rentals by Hour", fontsize=12)
    ax.set_xticks(range(0, 24))  
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)