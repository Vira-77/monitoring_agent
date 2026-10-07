from dash import html
import dash_bootstrap_components as dbc
from components.cpu_chart import create_cpu_chart
from components.memory_chart import create_memory_total_graph
from components.disk_chart import create_disk_chart
from components.combined_graph import create_combined_graph
from components.log_array import create_detailed_logs_chart
from components.cpu_frequency_graph import create_cpu_frequency_graph
from components.process_table import create_process_table

def create_dashboard_layout(ip_address, hostname):
    return html.Div([
        html.Div([
            html.H1(f"Server Dashboard - {ip_address}", className="text-center mb-4"),
            html.H2(f"Hostname - {hostname}", className="text-center mb-4") if hostname != "Unknown" else None,
            dbc.Button("Back to Home", href='/', color="secondary", className="mb-3")
        ], className="text-center"),
        html.Div(id='dashboard-content', 
                 children=create_empty_dashboard(),
                 style={'height': '160vh'})
    ], className="dashboard-container container")

def create_empty_dashboard():
    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='cpu-container', 
                    children=create_cpu_chart([]),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ), 
                md=8,
                style={'height': '45vh'}
            ),
            dbc.Col(
                html.Div(
                    id='memory-container', 
                    children=create_memory_total_graph({}, {}),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ), 
                md=4,
                style={'height': '45vh'}
            )
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='combined-container', 
                    children=create_combined_graph([], []),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ), 
                md=8,
                style={'height': '45vh'}
            ),
            dbc.Col(
                html.Div(
                    id='disk-container', 
                    children=create_disk_chart({}),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ), 
                md=4,
                style={'height': '45vh'}
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='logs-container',
                    children=create_detailed_logs_chart([]),
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ),
                md=12
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='cpu-frequency-container',
                    children=create_cpu_frequency_graph([], "CPU Name"),
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #ddd'
                    }
                ),
                md=12
            )
        ]),
    ], className="p-4")

def update_dashboard_content(cpu_data, memory_data_used, memory_data_free, disk_data, cpu_historical=None, memory_historical=None, logs_data=None, cpu_frequency_data=None, cpu_name="CPU Name", processes_data=None):
    style_container = {
        'width': '100%',
        'height': '100%', 
        'padding': '10px',
        'border': '1px solid #ddd'
    }
    
    style_col = {'height': '60vh'}

    components = []

    cpu_memory_row = dbc.Row([
        dbc.Col(
            html.Div(
                id='cpu-container', 
                children=create_cpu_chart(cpu_data or []),
                style=style_container
            ), 
            md=8,
            style=style_col
        ),
        dbc.Col(
            html.Div(
                id='memory-container', 
                children=create_memory_total_graph(memory_data_used or {}, memory_data_free or {}),
                style=style_container
            ), 
            md=4,
            style=style_col
        )
    ], className="mb-4")
    components.append(cpu_memory_row)

    combined_disk_row = dbc.Row([
        dbc.Col(
            html.Div(
                id='combined-container', 
                children=create_combined_graph(cpu_historical or [], memory_historical or []),
                style=style_container
            ), 
            md=8,
            style=style_col
        ),
        dbc.Col(
            html.Div(
                id='disk-container', 
                children=create_disk_chart(disk_data or {}),
                style=style_container
            ), 
            md=4,
            style=style_col
        )
    ])
    components.append(combined_disk_row)

    if logs_data:
        components.append(
            dbc.Row([
                dbc.Col(
                    html.Div(
                        id='logs-container',
                        children=create_detailed_logs_chart(logs_data),
                        style=style_container
                    ),
                    md=12
                )
            ])
        )

    if cpu_frequency_data:
        components.append(
            dbc.Row([
                dbc.Col(
                    html.Div(
                        id='cpu-frequency-container',
                        children=create_cpu_frequency_graph(cpu_frequency_data, cpu_name),
                        style=style_container
                    ),
                    md=12
                )
            ])
        )

    if processes_data:
        components.append(
            dbc.Row([
                dbc.Col(
                    html.Div(
                        id='process-table-container',
                        children=create_process_table(processes_data),
                        style=style_container
                    ),
                    md=12
                )
            ])
        )

    return html.Div(components, className="p-4")