from dash import html


def create_detailed_logs_chart(log_data):

   filtered_logs = [log for log in log_data if log['status'] > "400" and log['status']!="INFO"]
  

   if not filtered_logs:
       return html.Div([
           html.H1("Detailed Logs (400 Errors Only)", className="text-center my-4"),
           html.P("No 400 logs found.", className="text-center"),
       ])
  
   table_rows = []


   filtered_logs=filtered_logs[-10:]
   
  
   for log in filtered_logs:
       table_rows.append(
           html.Tr([
               html.Td(log["status"]),
               html.Td(log["message"]),
               html.Td(log["error"]),
               html.Td(log["timestamp"]),
               html.Td(log["level"]),
               html.Td(log["logger"]),
               html.Td(log["method"])
           ])
       )
  
   return html.Div([
       html.H1("Detailed Logs (Errors Only)", className="text-center my-4"),
      
       html.Div([
           html.Table([
               html.Thead([
                   html.Tr([
                       html.Th('Status'),
                       html.Th('Message'),
                       html.Th('Error'),
                       html.Th('Timestamp'),
                       html.Th('Level'),
                       html.Th('Logger'),
                       html.Th('Method')
                   ])
               ]),
               html.Tbody(table_rows)
           ], className="table table-bordered table-striped table-hover table-sm"),
       ], className="table-responsive"),
      
   
   ])
   


