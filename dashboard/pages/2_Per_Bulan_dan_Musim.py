import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from streamlit_extras.app_logo import add_logo 
from utils import add_ispu_legend_to_graph

add_logo('dashboard/logo.png', height=220)

### Initial DataFrame import
### Monthly
df_monthly = pd.read_csv('dashboard/data/all_station_df_monthly.csv')
df_monthly = df_monthly.set_index(pd.DatetimeIndex(df_monthly['datetime'])).drop('datetime', axis=1)
min_date = df_monthly.head(1).index.date[0]
max_date = df_monthly.tail(1).index.date[0]
station_names = df_monthly['station'].unique()

### Quarterly
df_quarterly = pd.read_csv('dashboard/data/all_station_df_quarterly.csv')
df_quarterly = df_quarterly.set_index(pd.DatetimeIndex(df_quarterly['datetime'])).drop('datetime', axis=1)

### Header
st.title('Kualitas Udara Per Bulan dan Musim')

### Filter
left_column, right_column = st.columns(2)
station = left_column.selectbox('Stasiun', station_names)
starting_date = right_column.date_input('Tanggal Awal', value=min_date, min_value=min_date, max_value=max_date)
ending_date = starting_date + timedelta(days=365)

### DataFrame filter
### Monthly
df_monthly_station = df_monthly[df_monthly['station'] == station]
df_monthly_date_filtered = df_monthly_station[
  (df_monthly_station.index.date >= starting_date )
  & (df_monthly_station.index.date <= ending_date)
]
### Quarterly
df_quarterly_station = df_quarterly[df_quarterly['station'] == station]


### Graph
### Monthly
st.markdown('## Per Bulan (Jangka 1 Tahun)')
fig_monthly = px.line(df_monthly_date_filtered,
    y='ispu',
    labels={'ispu': 'ISPU', 'datetime': 'Tanggal'},
    title=f'ISPU Per Bulan Stasiun {station}, {starting_date} - {ending_date}',
)
add_ispu_legend_to_graph(fig_monthly, df_monthly_date_filtered['ispu'].max())
st.plotly_chart(
  fig_monthly
)
### Quarterly
st.markdown('## Per Musim')
fig_quarterly = px.line(df_quarterly_station,
    y='ispu',
    labels={'ispu': 'ISPU', 'datetime': 'Tanggal'},
    title=f'ISPU Per Musim Stasiun {station}',
)
add_ispu_legend_to_graph(fig_quarterly, df_quarterly_station['ispu'].max())
st.plotly_chart(
  fig_quarterly
)