import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st

st.title("Bike Sharing Data Analysis")
st.subheader("Pertanyaan")
st.write("1. Di musim berapakah pengguna sepeda paling banyak?")
st.write("2. Berapa rata-rata pengguna per harinya?")

df_day = pd.read_csv('data/day.csv')
df_hour = pd.read_csv('data/hour.csv')

# Data Wrangling
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Fill missing values
df_day.fillna(df_day.mean(), inplace=True)
df_hour.fillna(df_hour.mean(), inplace=True)

# Drop duplicates
df_day.drop_duplicates(inplace=True)
df_hour.drop_duplicates(inplace=True)

# Exploratory Data Analysis (EDA)
df_day['season'] = df_day['season'].astype('category')
df_day['mnth'] = df_day['mnth'].astype('category')
df_day['weekday'] = df_day['weekday'].astype('category')
df_day['weathersit'] = df_day['weathersit'].astype('category')

# Analysis: Number of users per season
season_mapping = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}
df_day['season_name'] = df_day['season'].map(season_mapping)
season_counts = df_day.groupby('season_name')['cnt'].sum().reset_index().sort_values('cnt', ascending=False)
st.subheader("Jumlah Pengguna per Musim")
st.bar_chart(season_counts.set_index('season_name'))

# Analysis: Average users per day
weekday_mapping = {
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
}
df_day['weekday_name'] = df_day['weekday'].map(weekday_mapping)
average_users_by_weekday = df_day.groupby('weekday_name')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)
weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
average_users_by_weekday['weekday_name'] = pd.Categorical(average_users_by_weekday['weekday_name'], categories=weekday_order, ordered=True)
average_users_by_weekday = average_users_by_weekday.sort_values('weekday_name')
st.subheader("Rata-rata Pengguna per Hari")
st.bar_chart(average_users_by_weekday.set_index('weekday_name'))

weather_mapping = {
    1: 'Cerah',
    2: 'Mendung',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
df_day['weather_name'] = df_day['weathersit'].map(weather_mapping)

selected_weather = st.selectbox("Pilih Kondisi Cuaca", df_day['weather_name'].unique())
filtered_data = df_day[df_day['weather_name'] == selected_weather]

average_users_by_weather = filtered_data.groupby('weekday_name')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)
average_users_by_weather['weekday_name'] = pd.Categorical(average_users_by_weather['weekday_name'], categories=weekday_order, ordered=True)
average_users_by_weather = average_users_by_weather.sort_values('weekday_name')

st.subheader(f"Rata-rata Pengguna per Hari untuk Cuaca: {selected_weather}")
st.bar_chart(average_users_by_weather.set_index('weekday_name'))

st.subheader("Kesimpulan")
st.write("1. Pada grafik jumlah pengguna per musim, musim gugur memiliki jumlah pengguna paling banyak.")
st.write("2. Pada grafik rata-rata pengguna per hari, pengguna paling banyak pada hari Jum'at.")
