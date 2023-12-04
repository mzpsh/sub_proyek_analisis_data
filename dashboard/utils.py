import plotly.graph_objects as pgo

def add_ispu_legend_to_graph(fig: pgo.Figure, max_ispu: float):
  max_y = max_ispu
  ispu_points = [0, 50, 100, 200, 300, 500]
  colors = ['green', 'blue', 'yellow', 'red', 'black']
  names = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']

  index = 0
  while(max_y > ispu_points[index] and max_y < 500):
    lower_ispu = ispu_points[index]
    upper_ispu = max_y + 50 if lower_ispu >= 300 else ispu_points[index + 1] 
    fig.add_hrect(y0=lower_ispu, y1=upper_ispu, line_width=0, opacity=.15, layer='below',
      name=names[index],
      fillcolor=colors[index],
      showlegend=True,
    )
    index += 1
  pass