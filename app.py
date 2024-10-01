import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

sns.set(style="whitegrid")

# Load the cleaned datasets
df_day = pd.read_csv('data/day_clean.csv')
df_hour = pd.read_csv('data/hour_clean.csv')

# Replace NaN values with 0
df_day.fillna(0, inplace=True)
df_hour.fillna(0, inplace=True)

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Set the title of the dashboard
st.title("Bike Sharing Dashboard")

# Sidebar for user input
st.sidebar.header("User Input Features")
season_options = ['All Seasons'] + df_day['season'].unique().tolist()
weather_options = ['All Weather'] + df_hour['weathersit'].unique().tolist()

season = st.sidebar.selectbox("Select Season", season_options)
weather = st.sidebar.selectbox("Select Weather", weather_options)

# Add date range slider in the sidebar
min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()
date_range = st.sidebar.slider("Select Date Range", min_value=min_date.date(), max_value=max_date.date(), value=(min_date.date(), max_date.date()), format="YYYY-MM-DD")

# Filter the data based on the selected date range, season, and weather
df_day_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(date_range[0])) & 
						 (df_day['dteday'] <= pd.to_datetime(date_range[1]))]

df_hour_filtered = df_hour[(df_hour['dteday'] >= pd.to_datetime(date_range[0])) & 
						   (df_hour['dteday'] <= pd.to_datetime(date_range[1]))]

if season != 'All Seasons':
	df_day_filtered = df_day_filtered[df_day_filtered['season'] == season]
	df_hour_filtered = df_hour_filtered[df_hour_filtered['season'] == season]

if weather != 'All Weather':
	df_day_filtered = df_day_filtered[df_day_filtered['weathersit'] == weather]
	df_hour_filtered = df_hour_filtered[df_hour_filtered['weathersit'] == weather]

# Calculate spotlight numbers
total_rentals = df_day_filtered['cnt'].sum()
average_rentals_per_day = df_day_filtered['cnt'].mean()
max_rentals_in_a_day = df_day_filtered['cnt'].max()

# Display spotlight numbers
st.header("Spotlight Numbers")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{total_rentals:,}")
col2.metric("Average Rentals per Day", f"{average_rentals_per_day:.2f}")
col3.metric("Max Rentals in a Day", f"{max_rentals_in_a_day:,}")

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_day_filtered, x='dteday', y='cnt', color='red')
plt.title('Jumlah Penyewaan Sepeda per Hari ')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Penyewaan')

# Limit the number of xticks and yticks
plt.xticks(rotation=45)
plt.locator_params(axis='x', nbins=10)
plt.locator_params(axis='y', nbins=10)

st.pyplot(plt)

# Create a pivot table with the average count of rentals by weekday and hour
pivot_table = df_hour_filtered.pivot_table(values='cnt', index='weekday', columns='hr', aggfunc='mean')

# Reorder the index to start from Monday
order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
pivot_table = pivot_table.reindex(order)

# Plot the heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table, cmap='coolwarm', annot=False, cbar_kws={'label': 'Rata-Rata Penyewaan'})
plt.title('Heatmap Rata-Rata Penyewaan Sepeda per Hari dan Jam')
plt.xlabel('Jam')
plt.ylabel('Hari')
st.pyplot(plt)
