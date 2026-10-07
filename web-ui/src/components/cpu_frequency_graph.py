from dash import dcc
import plotly.graph_objs as go

def create_cpu_frequency_graph(frequency_data, cpu_name):
    try:
        traces = []
    
        if frequency_data and len(frequency_data) > 0:
            x_values = [data['timestamp'] for data in frequency_data]
            y_values = [float(data.get('frequency', 0)) for data in frequency_data]

            traces.append(go.Scatter(
                x=x_values,
                y=y_values,
                name='CPU Frequency',
                mode='lines',
                line=dict(
                    color='#3498db',
                    width=3
                )
            ))

        return dcc.Graph(
            id='cpu-frequency-chart',
            figure={
                'data': traces,
                'layout': {
                    'title': f'CPU Frequency Over Time - {cpu_name}',
                    'xaxis': {
                        'title': 'Time',
                        'tickformat': '%H:%M:%S',
                    },
                    'yaxis': {
                        'title': 'Frequency (MHz)',
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
        print("Error creating CPU frequency graph")
        print(f"Error: {e}")
        return dcc.Graph(id='cpu-frequency-chart')