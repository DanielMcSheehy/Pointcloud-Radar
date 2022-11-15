import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
import time
import psutil
from plotly.subplots import make_subplots
import math
from formant.sdk.cloud.v1 import Client as FormantClient
import plotly.graph_objects as go
import cv2
import plotly.express as px
import time
import plotly.graph_objects as go


stack = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter3d"}, {"type": "barpolar"}]])

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/3d-scatter.csv')


sample_x, sample_y = df['x1'][:100], df['y1'][:100]


c = [math.radians(degree) for degree in [0, 45, 90, 135, 180, 225, 270, 315]]

pointsWithinDegrees = {}

for radian in c:
    pointsWithinDegrees[math.degrees(radian)] = 0
    
result = np.arctan2(np.subtract(1, sample_y), np.subtract(1, sample_x))

for item in result:
    if not np.isnan(item):
        radian = min(c, key=lambda x:abs(x-item))
        pointsWithinDegrees[math.degrees(radian)] = pointsWithinDegrees[math.degrees(radian)] + 1


camera = dict(
    # eye=dict(x=math.sin(angle), y=math.cos(angle), z=0),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=0, y=0, z=0)
)

steps = []
for i in range(0, 180):
    step = dict(
        method="relayout",
        label=str(i*2),
        args=[{"scene.camera.eye": dict(x=math.sin(math.radians(i*2)), y=math.cos(math.radians(i*2)), z=0)}]  # layout attribute
    )
    steps.append(step)
    steps.append(dict(
        method="relayout",
        label=str(i*2),
        args=[{"polar.angularaxis.rotation": 90+ (i*2)}]  # layout attribute
    ))

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Degrees:"},
    pad={"t": 0},
    steps=steps
)]

name = 'Radar point cloud'

print(pointsWithinDegrees)

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter3d"}, {"type": "polar"}]])
fig.add_trace(go.Scatter3d(
    x=df["x1"],
    y=df["y1"],
    z=df["z1"],
    mode='markers',
    marker=dict(
        size=12, 
        opacity=0.9
    )
), row=1, col=1)

fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='15%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[0],
        autocolorscale=True,
    ),
    ), row=1, col=2
)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='10%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[1],
        autocolorscale=True,
    ), 
), row=1, col=2)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='9%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[2],
        autocolorscale=True,
    ), 
), row=1, col=2)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='8%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[3],
        autocolorscale=True,
    ),
), row=1, col=2)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='7%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[4],
        autocolorscale=True,
    ),
), row=1, col=2)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='5%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[5],
        autocolorscale=True,
    ),
), row=1, col=2)
fig.add_trace(go.Barpolar(
    r=list(pointsWithinDegrees.values()),
    name='2%',
    marker=dict(
        color=px.colors.sequential.Plasma_r[6],
        autocolorscale=True,
    ),
), row=1, col=2)

fig.update_layout(
    title='Radar',
    font_size=16,
    legend_font_size=16,
    polar_angularaxis_direction="clockwise",
    plot_bgcolor='rgb(17,17,17)',
    paper_bgcolor ='rgb(10,10,10)',
    colorscale=dict(sequential=px.colors.sequential.Plasma, diverging=px.colors.sequential.Plasma_r),
)

fig.update_layout(template="plotly_dark")

fig.update_layout(scene_camera=camera, scene_dragmode='orbit', title=name, sliders=sliders, scene_xaxis = dict(nticks=1, range=[0,10], showgrid=False),
                     scene_yaxis = dict(nticks=1, range=[0,10], showgrid=False))

st.plotly_chart(fig, use_container_width=True)

