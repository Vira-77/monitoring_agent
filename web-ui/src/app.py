from dash import (
    Dash,
    dcc,
    html,
    callback_context,
    ALL
)
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import asyncio
import time
import re
import urllib.parse
from asyncio import gather

from components.home_page import (
    create_home_page,
    create_server_panel
)
from components.dashboard import (
    create_dashboard_layout,
    update_dashboard_content
)
from utils.api import (
    get_cpu_data,
    get_memory_data_used,
    get_memory_data_free,
    get_disk_data,
    get_cpu_historical,
    get_memory_historical,
    clear_history,
    get_log_data,
    get_cpu_frequency,
    get_cpu_name,
    get_cpu_frequency_historical,
    get_hostname,
    get_top_cpu_processes,
    get_total_errors
)

REFRESH_RATE = 5
SERVERS_DATA_FILE = 'servers_data.json'

def load_servers_data():
    try:
        with open(SERVERS_DATA_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print(f"Warning: Expected list, but got {type(data)}. Returning empty list.")
                return []
    except FileNotFoundError:
        print(f"Warning: {SERVERS_DATA_FILE} not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {SERVERS_DATA_FILE} contains invalid JSON. Returning empty list.")
        return []
    except Exception as e:
        print(f"Error loading servers data: {e}")
        return []

def save_servers_data(data):
    try:
        if not isinstance(data, list):
            raise ValueError("Data to save should be a list")
        with open(SERVERS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved {len(data)} server(s) data.")
    except Exception as e:
        print(f"Error saving servers data: {e}")

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Interval(id='interval-component', interval=REFRESH_RATE * 1000, n_intervals=0),
    html.Div(id='page-content'),
    dcc.Store(id='update-metrics-trigger')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search')]
)
def display_page(pathname, search):
    if pathname == '/':
        servers_data = load_servers_data()
        return create_home_page(servers_data)
    
    elif pathname == '/dashboard':
        if search and 'server=' in search:
            if 'hostname=' in search:
                clear_history()
                params = urllib.parse.parse_qs(search.lstrip('?'))
                ip_address = params.get('server', [''])[0]
                hostname = params.get('hostname', [''])[0]
                return create_dashboard_layout(ip_address, hostname)
        
        return html.Div("No server specified")
    return '404'

@app.callback(
    Output('dashboard-content', 'children'),
    [Input('interval-component', 'n_intervals')],
    [State('url', 'search')]
)
def update_dashboard(n_intervals, search):
    if not search:
        raise PreventUpdate
    
    params = urllib.parse.parse_qs(search.lstrip('?'))
    server_ip = params.get('server', [''])[0]
    
    if not server_ip:
        raise PreventUpdate

    async def fetch_dashboard_data():
        tasks = [
            get_cpu_data(server_ip),
            get_memory_data_used(server_ip),
            get_memory_data_free(server_ip),
            get_disk_data(server_ip),
            get_log_data(server_ip),
            get_cpu_frequency(server_ip),
            get_cpu_name(server_ip),
            get_top_cpu_processes(server_ip)
        ]

        results = await gather(*tasks, return_exceptions=True)

        cpu_data = results[0] if not isinstance(results[0], Exception) else None
        memory_data_used = results[1] if not isinstance(results[1], Exception) else None
        memory_data_free = results[2] if not isinstance(results[2], Exception) else None
        disk_data = results[3] if not isinstance(results[3], Exception) else None
        logs_data = results[4] if not isinstance(results[4], Exception) else None
        cpu_frequency = results[5] if not isinstance(results[5], Exception) else None
        cpu_name = results[6] if not isinstance(results[6], Exception) else {'name': 'Unknown'}
        processes_data = results[7] if not isinstance(results[7], Exception) else []
        print(cpu_frequency)
        

        return update_dashboard_content(
            cpu_data,
            memory_data_used, 
            memory_data_free,
            disk_data,
            get_cpu_historical(),
            get_memory_historical(),
            logs_data,
            get_cpu_frequency_historical(),
            cpu_name.get('name', 'Unknown CPU'),
            processes_data
        )

    return asyncio.run(fetch_dashboard_data())

@app.callback(
    [Output('server-panel', 'children', allow_duplicate=True),
     Output('update-metrics-trigger', 'data')],
    [Input('add-server-button', 'n_clicks'),
     Input({'type': 'remove-button', 'index': ALL}, 'n_clicks')],
    [State('server-input', 'value')],
    prevent_initial_call=True
)
def update_server_list(add_clicks, remove_clicks, server_ip):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    triggered_id = ctx.triggered[0]['prop_id']
    servers_data = load_servers_data()
    
    if 'remove-button' in triggered_id:
        try:
            if isinstance(ctx.triggered_id, dict):
                server_ip_to_remove = ctx.triggered_id['index']
            else:
                pattern = r"{'type': 'remove-button', 'index': '([^']*)'}"
                match = re.search(pattern, triggered_id)
                server_ip_to_remove = match.group(1) if match else None

            if server_ip_to_remove:
                servers_data = [s for s in servers_data if s['ip'] != server_ip_to_remove]
                save_servers_data(servers_data)
                return create_server_panel(servers_data), {'timestamp': time.time(), 'action': 'remove'}

        except Exception as e:
            print(f"Error processing remove button: {e}")
            raise PreventUpdate
    
    if 'add-server-button' in triggered_id and server_ip:
        if not any(s['ip'] == server_ip for s in servers_data):
            new_server = {
                'name': f'Server {len(servers_data) + 1}',
                'ip': server_ip,
                'status': 'offline',
                'cpu_usage': 0,
                'memory_usage': 0,
                'errors': 0
            }
            servers_data.append(new_server)
            save_servers_data(servers_data)
            return create_server_panel(servers_data), {'timestamp': time.time(), 'action': 'add'}

    return create_server_panel(servers_data), {'timestamp': time.time(), 'action': 'none'}

@app.callback(
    Output('server-panel', 'children', allow_duplicate=True),
    [Input('update-metrics-trigger', 'data')],
    prevent_initial_call=True
)
def update_server_metrics(_):
    async def fetch_metrics():
        servers_data = load_servers_data()

        for server in servers_data:

            print(server)
            print(" ")
            print(" ")
            try:
                server_ip = server['ip']
                print("http" not in server_ip)
                if "http" not in server_ip: 
                    server_ip = "http://" + server_ip
                
                hostname_data = await get_hostname(server_ip)
                server['hostname'] = hostname_data.get('hostname', 'Unknown')

                cpu_data = await get_cpu_data(server_ip)
                memory_data_used = await get_memory_data_used(server_ip)
                memory_data_free = await get_memory_data_free(server_ip)
                nbr_errors = await get_total_errors(server_ip)
                
                if cpu_data and isinstance(cpu_data, list) and len(cpu_data) > 0:
                    avg_cpu = sum(float(core['usage']) for core in cpu_data) / len(cpu_data)
                    
                    if isinstance(memory_data_used, dict) and isinstance(memory_data_free, dict):
                        used = float(memory_data_used.get('value', 0))
                        free = float(memory_data_free.get('value', 0))
                        total = used + free
                        memory_usage_percent = (used / total * 100) if total > 0 else 0
                        
                        server['status'] = 'online'
                        server['cpu_usage'] = round(avg_cpu, 2)
                        server['memory_usage'] = round(memory_usage_percent, 2)
                        server['errors'] = nbr_errors
                        continue

                server['status'] = 'offline'
                server['cpu_usage'] = 0
                server['memory_usage'] = 0
                server['errors'] = 0
                print(f"Metrics failed for {server_ip}")

            except Exception as e:
                server['status'] = 'error'
                server['hostname'] = 'Unknown'
                server['cpu_usage'] = 0
                server['memory_usage'] = 0
                server['errors'] += 1
                print(f"Error updating metrics for {server_ip}: {str(e)}")
        
        save_servers_data(servers_data)
        return create_server_panel(servers_data)
    
    return asyncio.run(fetch_metrics())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
