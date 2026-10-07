from dash import dcc
import plotly.graph_objs as go
import numpy as np

def create_cpu_graph(historical_data):
    traces = []
    
    if historical_data and len(historical_data) > 0:
        x_values = [data['timestamp'] for data in historical_data]
        
        y_values = [np.mean(data['usages']) for data in historical_data]
        
        traces.append(go.Scatter(
            x=x_values,
            y=y_values,
            name='Average CPU Usage',
            mode='lines',
            line=dict(
                color='#2ecc71',
                width=3
            ),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.2)'
        ))

    return dcc.Graph(
        id='cpu-time-graph',
        figure={
            'data': traces,
            'layout': {
                'title': 'Average CPU Usage Over Time',
                'yaxis': {
                    'range': [0, 100],
                    'title': 'Average Usage (%)'
                },
                'xaxis': {
                    'title': 'Time'
                },
                'height': 400,
                'margin': {'t': 40, 'b': 50, 'l': 50, 'r': 30},
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'font': {'color': '#2c3e50'},
                'showlegend': True,
                'legend': {'orientation': 'h'}
            }
        }
    )