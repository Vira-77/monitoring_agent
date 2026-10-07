from dash import dcc

def create_memory_total_graph(memory_data_used, memory_data_free):
    try:
        free_ram = float(memory_data_free.get('value', 0))
        used_ram = float(memory_data_used.get('value', 0))
        total_ram = free_ram + used_ram
        memory_percentage = (used_ram / total_ram) * 100 if total_ram > 0 else 0

        return dcc.Graph(
            id='memory-chart_total',
            figure={
                'data': [{
                    'type': 'indicator',
                    'mode': 'gauge+number+delta',
                    'value': memory_percentage,
                    'number': {
                        'suffix': '%',
                        'font': {'size': 36, 'family': 'Arial Bold'},
                        'valueformat': '.1f'
                    },
                    'title': {
                        'text': f'Memory Usage<br><span style="font-size:1em">{used_ram:.1f}GB / {total_ram:.1f}GB</span>',
                        'font': {'size': 18, 'family': 'Arial', 'color': '#2c3e50'}
                    },
                    'gauge': {
                        'axis': {
                            'range': [0, 100],
                            'tickwidth': 1,
                            'tickcolor': '#2c3e50',
                            'ticksuffix': '%',
                            'showgrid': True
                        },
                        'bar': {
                            'color': 'rgba(231, 76, 60, 0.8)',
                            'thickness': 0.6
                        },
                        'bgcolor': 'white',
                        'borderwidth': 2,
                        'bordercolor': '#34495e',
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(46, 204, 113, 0.15)'},
                            {'range': [50, 75], 'color': 'rgba(241, 196, 15, 0.15)'},
                            {'range': [75, 100], 'color': 'rgba(231, 76, 60, 0.15)'}
                        ],
                        'threshold': {
                            'line': {'color': '#e74c3c', 'width': 4},
                            'thickness': 0.8,
                            'value': 90
                        }
                    }
                }],
                'layout': {
                    'autosize': True,
                    'margin': {'t': 10, 'b': 10, 'l': 10, 'r': 10},
                    'paper_bgcolor': 'white',
                    'font': {'color': '#2c3e50', 'family': 'Arial'},
                    'transition': {
                        'duration': 500,
                        'easing': 'cubic-in-out'
                    }
                }
            },
            config={
                'displayModeBar': False,
                'responsive': True
            },
            style={
                'height': '100%',
                'width': '100%'
            }
        )
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error: {e}")
        return dcc.Graph(
            id='memory-chart_total',
            style={'height': '100%', 'width': '100%'}
        )