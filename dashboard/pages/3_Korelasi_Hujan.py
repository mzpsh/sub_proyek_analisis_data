import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from streamlit_extras.app_logo import add_logo 

add_logo('dashboard/logo.png', height=220)

### DataFrame initial import
df = pd.read_csv('dashboard/data/all_station_df_daily.csv')
df = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime', axis=1)
station_names = df['station'].unique()

### Header
st.title('Korelasi Hujan dan Kualitas Udara')

### Filter
station = st.selectbox('Stasiun', station_names)

### DataFrame filter
df_station = df[df['station'] == station]

### Graph
r_number = df_station\
    .drop(['station'], axis=1)\
      .corr()['RAIN']['ispu']
fig = px.scatter(
  df_station,
  title=f'Korelasi Hujan dan ISPU stasiun {station} (r={round(r_number, 2)})',
  x='RAIN', y='ispu',
  labels={'ispu': 'ISPU', 'RAIN': 'Hujan (mm/hari)'},
  trendline_color_override='red',
  trendline="ols",  
)

st.plotly_chart(
  fig
)
