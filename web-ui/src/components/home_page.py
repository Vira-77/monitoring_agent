from dash import html
import dash_bootstrap_components as dbc

def create_home_page(servers_data):
    return html.Div([
        html.H1("Server Monitor", className="text-center mb-4"),
        html.Div([
            dbc.Input(id='server-input', placeholder='Enter server IP...', className='mb-2'),
            dbc.Button('Add New Server', id='add-server-button', color='primary', className='mb-4')
        ], className="text-center"),
        html.Div(id='server-panel', children=create_server_panel(servers_data), className="table-responsive")
    ], className="container")

def create_server_panel(servers_data=None):
    if not servers_data:
        servers_data = []
        
    return html.Div([
        html.Table(
            id='server-table',
            children=[
                html.Thead(
                    html.Tr([
                        html.Th('Server Name'),
                        html.Th('Hostname'),
                        html.Th('IP Address'),
                        html.Th('Status'),
                        html.Th('CPU Usage'),
                        html.Th('Memory Usage'),
                        html.Th('Errors'),
                        html.Th('Actions')
                    ])
                ),
                html.Tbody(id='server-table-body', children=create_server_rows(servers_data))
            ],
            className='table table-bordered table-striped table-hover table-sm'
        )
    ])

def create_server_row(server):
    if not isinstance(server, dict):
        print(f"Invalid server data type: {type(server)}")
        return html.Tr([html.Td("Invalid server data", colSpan=8)])
        
    return html.Tr([
        html.Td(server.get('name', f"Server {server.get('ip', 'Unknown')}")),
        html.Td(server.get('hostname', 'Unknown')), 
        html.Td(server.get('ip', 'N/A')),
        html.Td(create_status_badge(server.get('status', 'offline'))),
        html.Td(f"{server.get('cpu_usage', 0)}%"),
        html.Td(f"{server.get('memory_usage', 0)}%"),
        html.Td(dbc.Badge(str(server.get('errors', 0)), color="warning")),
        html.Td(create_action_buttons(server.get('ip', ''), server.get('hostname', '')))
    ])

def create_server_rows(servers_data):
    if not servers_data:
        return [html.Tr([
            html.Td(
                "No servers found. Click 'Add New Server' to begin monitoring.",
                colSpan=7,
                className="text-center text-muted"
            )
        ])]
    
    if isinstance(servers_data, list):
        try:
            return [create_server_row(server) for server in servers_data]
        except Exception as e:
            print(f"Error creating server rows: {e}")
            return [html.Tr([html.Td("Error loading server data", colSpan=7)])]
    else:
        return [html.Tr([html.Td("Invalid server data format", colSpan=7)])]

def create_status_badge(status):
    return dbc.Badge(
        "Online" if status == 'online' else "Offline",
        color="success" if status == 'online' else "danger"
    )

def create_action_buttons(server_ip, hostname):
    if not server_ip:
        return html.Div("No actions available")
    
    return html.Div([
        dbc.Button(
            "Monitor",
            id={'type': 'monitor-button', 'index': server_ip},
            href=f"/dashboard?server={server_ip}&hostname={hostname}",
            color="primary",
            size="sm",
            className="me-2",
            n_clicks=0
        ),
        dbc.Button(
            "Remove",
            id={'type': 'remove-button', 'index': server_ip},
            color="danger",
            size="sm"
        )
    ])