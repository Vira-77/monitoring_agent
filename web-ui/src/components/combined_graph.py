from dash import dcc
import plotly.graph_objs as go
from datetime import datetime

def create_combined_graph(cpu_historical_data, memory_historical_data):
    try:
        traces = []
        cpu_historical_data = sort_historical_data(cpu_historical_data)
        memory_historical_data = sort_historical_data(memory_historical_data)

        if cpu_historical_data and len(cpu_historical_data) > 0:
            cpu_x_values = [data['timestamp'] for data in cpu_historical_data]
            cpu_y_values = [sum(data['usages']) / len(data['usages']) for data in cpu_historical_data]

            traces.append(go.Scatter(
                x=cpu_x_values,
                y=cpu_y_values,
                name='CPU Average Usage',
                mode='lines',
                line=dict(
                    color='#3498db',
                    width=3
                )
            ))

        if memory_historical_data and len(memory_historical_data) > 0:
            memory_x_values = [data['timestamp'] for data in memory_historical_data]
            memory_y_values = [float(data.get('value', 0)) for data in memory_historical_data]

            traces.append(go.Scatter(
                x=memory_x_values,
                y=memory_y_values,
                name='Memory Usage',
                mode='lines',
                line=dict(
                    color='#2ecc71',
                    width=3
                ),
                fill='tozeroy',
                fillcolor='rgba(46, 204, 113, 0.2)'
            ))

        return dcc.Graph(
            id='combined-chart',
            figure={
                'data': traces,
                'layout': {
                    'title': 'CPU and Memory Usage Over Time',
                    'xaxis': {
                        'title': 'Time',
                        'tickformat': '%H:%M:%S',
                    },
                    'yaxis': {
                        'title': 'Usage (%)',
                        'range': [0, 100],
                    },
                    'height': 400,
                    'margin': {'t': 40, 'b': 50, 'l': 50, 'r': 30},
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'font': {'color': '#2c3e50'}    
                }
            },
            style={'width': '80%', 'margin': 'auto'}
        )
    except (KeyError, ValueError, TypeError) as e:
        print("il y a une erreur")
        print(f"Error: {e}")
        return dcc.Graph(id='combined-chart')
    
def sort_historical_data(data):
    return sorted(data, key=lambda x: datetime.strptime(x['timestamp'], '%H:%M:%S'))