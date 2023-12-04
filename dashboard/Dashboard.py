import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from streamlit_extras.app_logo import add_logo 
from utils import add_ispu_legend_to_graph

add_logo('dashboard/logo.png', height=220)

### Initial DataFrame import
df = pd.read_csv('dashboard/data/all_station_df_daily.csv')
df = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime', axis=1)
min_date = df.head(1).index.date[0]
max_date = df.tail(1).index.date[0]
station_names = df['station'].unique()

### Header
st.title('Kualitas Udara Harian (Jangka 30 Hari)')

### Filter
left_column, right_column = st.columns(2)
station = left_column.selectbox('Stasiun', station_names)
starting_date = right_column.date_input('Tanggal Awal', value=min_date, min_value=min_date, max_value=max_date)
ending_date = starting_date + timedelta(days=30)

### DataFrame filter
df_station = df[df['station'] == station]
df_date_filtered = df_station[
  (df_station.index.date >= starting_date )
  & (df_station.index.date <= ending_date)
]

### Graph
fig = px.line(df_date_filtered,
    y='ispu',
    labels={'ispu': 'ISPU', 'datetime': 'Tanggal'},
    title=f'ISPU Per Hari Stasiun {station}, {starting_date} - {ending_date}',
)
add_ispu_legend_to_graph(fig, df_date_filtered['ispu'].max())
st.plotly_chart(
  fig
)
