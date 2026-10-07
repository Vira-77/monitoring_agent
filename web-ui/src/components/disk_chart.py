import json
from dash import dcc
import plotly.graph_objects as go

def create_disk_chart(disk_data):
    try:
        total_gb = 0
        used_gb = 0
        free_gb = 0
        usage_percent = 0.0

        if isinstance(disk_data, list):
            for d in disk_data:
                disk_value_list = json.loads(d["disk_value"])
                
                if d["metric"] == "total":
                    total_gb = sum(float(value) for value in disk_value_list)
                elif d["metric"] == "used":
                    used_gb = sum(float(value) for value in disk_value_list)
                elif d["metric"] == "free":
                    free_gb = sum(float(value) for value in disk_value_list)
                
            usage_percent = (used_gb / total_gb * 100) if total_gb > 0 else 0

        elif isinstance(disk_data, dict):
            usage_percent = float(disk_data.get("percent", 0))

    except (KeyError, ValueError, TypeError) as e:
        total_gb = 0.0
        used_gb = 0.0
        free_gb = 0.0
        usage_percent = 0.0
        print(f"Error: {e}")

    color = ('rgba(46, 204, 113, 0.8)' if usage_percent < 50 else
             'rgba(231, 76, 60, 0.8)' if usage_percent > 80 else
             'rgba(241, 196, 15, 0.8)')

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=usage_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
                'suffix': '%',
                'font': {'size': 36, 'family': 'Arial Bold'},
                'valueformat': '.1f'
        },
        title={
            'text': f"Disk Usage<br><span style='font-size:0.8em'>{used_gb:.1f}GB used / {total_gb:.1f}GB total<br>{free_gb:.1f}GB free</span>",
            'font': {'size': 24}
        },
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(241, 196, 15, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20)
    )   

    return dcc.Graph(
        id='disk-chart',
        figure=fig
    )