from dash import dcc
import plotly.graph_objs as go

def create_memory_graph(historical_data_memory):
    try:
        traces = []
    
        if historical_data_memory and len(historical_data_memory) > 0:
            x_values = [data['timestamp'] for data in historical_data_memory]
            y_values = [float(data.get('value', 0)) for data in historical_data_memory]

            traces.append(go.Scatter(
                x=x_values,
                y=y_values,
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
            id='memory-chart',
            figure={
                'data': traces,
                'layout': {
                    'title': 'Memory Usage Over Time',
                    'xaxis': {
                        'title': 'Time (Index)',
                        'tickmode': 'linear',
                        'tick0': 1,
                        'dtick': 1
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
        return dcc.Graph(id='memory-graph')
