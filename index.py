from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app, server
from apps import daily, yearly, home, monthly

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/apps/daily':
        return daily.layout
    elif pathname == '/apps/monthly':
        return monthly.layout
    elif pathname == '/apps/yearly':
        return yearly.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
