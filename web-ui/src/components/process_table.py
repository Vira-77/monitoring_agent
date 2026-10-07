from dash import html
import dash_bootstrap_components as dbc

def create_process_table(processes_data):
    if not processes_data:
        return html.Div("No process data available", className="text-center text-muted")
    
    header = html.Thead([
        html.Tr([
            html.Th("Process Name"),
            html.Th("CPU Usage (Mb)"),
            html.Th("RAM Usage (Mb)")
        ])
    ])
    
    rows = []
    for process in processes_data:
        rows.append(html.Tr([
            html.Td(process.get('name', 'Unknown')),
            html.Td(f"{process.get('cpu_consumption', 0):.1f}Mb"),
            html.Td(f"{process.get('ram_consumption', 0):.1f}Mb")
        ]))
    
    return html.Div([
        html.H4("Top Processes", className="text-center mb-3"),
        dbc.Table([
            header,
            html.Tbody(rows)
        ], 
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        className="mb-3")
    ])