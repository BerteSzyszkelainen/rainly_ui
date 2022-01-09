from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app, server
from apps import rainfall, humidity, home, temperature, pressure, wind, analysis

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/apps/rainfall':
        return rainfall.layout
    elif pathname == '/apps/temperature':
        return temperature.layout
    elif pathname == '/apps/humidity':
        return humidity.layout
    elif pathname == '/apps/pressure':
        return pressure.layout
    elif pathname == '/apps/wind':
        return wind.layout
    elif pathname == '/apps/analysis':
        return analysis.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
