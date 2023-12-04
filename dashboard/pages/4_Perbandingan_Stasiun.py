import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from streamlit_extras.app_logo import add_logo 
from utils import add_ispu_legend_to_graph

add_logo('dashboard/logo.png', height=220)

### DataFrame initial import
df = pd.read_csv('dashboard/data/all_stations_ispu.csv')
df = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime', axis=1)
min_date = df.head(1).index.date[0]
max_date = df.tail(1).index.date[0]

### Header
st.title('Perbandingan Kualitas Udara: Rata-rata, Terbaik dan Terburuk')

### Filter
left_column, right_column = st.columns(2)
starting_date = left_column.date_input('Tanggal Awal', value=min_date, min_value=min_date, max_value=max_date)
days = right_column.slider('Jangka (Hari)', min_value=30, max_value=180, value=60)
ending_date = starting_date + timedelta(days=days) 
st.write(ending_date)


### DataFrame filter
df_date_filtered = df[
  (df.index.date >= starting_date )
  & (df.index.date <= ending_date )
]

### Graph
### Comparison
st.markdown('## Perbandingan')
all_stastions_ispu_line = px.line(df_date_filtered,
  labels={'datetime': 'Tanggal', 'value': 'ISPU', 'variable': 'Stasiun'},
  title='Perbandingan ISPU'
)
add_ispu_legend_to_graph(all_stastions_ispu_line, df_date_filtered.max().max())
st.plotly_chart(
  all_stastions_ispu_line
)
### Average
st.markdown('## Rata-rata')
all_stations_ispu_avg_bar = px.bar(df_date_filtered.mean().sort_values(),
  orientation='h',
  labels={'index': 'Stasiun', 'value': 'ISPU'},
  title='ISPU Rata-rata'
)
all_stations_ispu_avg_bar.update_layout(showlegend=False)
st.plotly_chart(
  all_stations_ispu_avg_bar
)

### Best 
st.markdown('## Kualitas Udara Terbaik')
all_stations_ispu_min_bar = px.bar(df_date_filtered.min().sort_values(ascending=False),
  orientation='h',
  labels={'index': 'Stasiun', 'value': 'ISPU'},
  title='ISPU Terendah'
)
all_stations_ispu_min_bar.update_layout(showlegend=False)
st.plotly_chart(
  all_stations_ispu_min_bar
)

### Worst
st.markdown('## Kualitas Udara Terburuk')
all_stations_ispu_max_bar = px.bar(df_date_filtered.max().sort_values(),
  orientation='h',
  labels={'index': 'Stasiun', 'value': 'ISPU'},
  title='ISPU Tertinggi'
)
all_stations_ispu_max_bar.update_layout(showlegend=False)
st.plotly_chart(
  all_stations_ispu_max_bar
)

