from dash import dcc

def create_cpu_chart(cpu_data):
    try:
        cores = [f'Core {d["id"]}' for d in cpu_data]
        usages = [float(d["usage"]) for d in cpu_data]
    except (KeyError, ValueError, TypeError) as e:
        cores = [f'Core {i}' for i in range(16)]
        usages = [0.0] * 16
        print(f"Error: {e}")

    colors = ['#2ecc71' if u < 50 else '#e74c3c' if u > 80 else '#f1c40f' for u in usages]

    return dcc.Graph(
        id='cpu-chart',
        figure={
            'data': [{
                'type': 'bar',
                'x': cores,
                'y': usages,
                'marker': {
                    'color': colors
                },
                'text': [f'{u:.1f}%' for u in usages],
                'textposition': 'auto',
            }],
            'layout': {
                'title': 'CPU Usage per Core',
                'yaxis': {
                    'range': [0, 100],
                    'title': 'Usage (%)'
                },
                'xaxis': {
                    'title': 'CPU Cores'
                },
                'height': 400,
                'margin': {'t': 40, 'b': 50, 'l': 50, 'r': 30},
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'font': {'color': '#2c3e50'}
            }
        }
    )