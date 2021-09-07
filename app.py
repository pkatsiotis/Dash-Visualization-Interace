import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.express as px

data = pd.read_csv('avocado.csv')
data.drop('Unnamed: 0', axis=1, inplace=True)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data = data.sort_values(by='Date')
data['Total Volume'] = data['Total Volume'].map(round)


def produce_fig(dataset, xvals, yvals, title, color, tick, hover):
    figure = px.line(dataset, x=xvals, y=yvals)
    figure.update_layout(
        title_text=title,
        title_x=0.5,
        hovermode='x'
    )
    figure.update_xaxes(fixedrange=True)
    figure.update_yaxes(tickprefix=tick, fixedrange=True)
    figure.update_traces(hovertemplate=hover, line_color=color)
    return figure


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children='🥑', className='header-emoji'),
                html.H1(
                    children='Avocado Analytics', className='header-title'
                ),
                html.P(
                    children='Analyze the behavior of avocado prices and the # '
                             'of avocados sold in the US between 2015 and 2018',
                    className='header-description'
                ),
            ],
            className='header',
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children='Region', className='menu-title'),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[
                                {'label': region, 'value': region}
                                for region in data['region'].sort_values().unique()
                            ],
                            value='Albany',
                            clearable=False,
                            className='dropdown'
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children='Type', className='menu-title'),
                        dcc.Dropdown(
                            id='type-filter',
                            options=[
                                {'label': avocado_type, 'value': avocado_type}
                                for avocado_type in data['type'].unique()
                            ],
                            value='organic',
                            clearable=False,
                            searchable=False,
                            className='dropdown'
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children='Date Range', className='menu-title'),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=data['Date'].min().date(),
                            max_date_allowed=data['Date'].max().date(),
                            start_date=data['Date'].min().date(),
                            end_date=data['Date'].max().date()
                        )
                    ]
                )
            ],
            className='menu'
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='price-chart',
                        config={'displayModeBar': False},
                    ),
                    className='card'
                ),
                html.Div(
                    children=dcc.Graph(
                        id='volume-chart',
                        config={'displayModeBar': False},
                    ),
                    className='card'
                ),
            ],
            className='wrapper',
        ),
    ]
)


@app.callback(
    Output('price-chart', 'figure'),
    Output('volume-chart', 'figure'),
    Input('region-filter', 'value'),
    Input('type-filter', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data[(data['region'] == region) & (data['type'] == avocado_type) &
                         (data['Date'] >= start_date) & (data['Date'] <= end_date)]

    price_chart = produce_fig(
        filtered_data,
        'Date',
        'AveragePrice',
        'Average Price of Avocados',
        '#17B897',
        '$',
        '$%{y:.2f}''<extra></extra>'
    )

    volume_chart = produce_fig(
        filtered_data,
        'Date',
        'Total Volume',
        'Avocados Sold',
        '#E12D39',
        None,
        None
    )
    return price_chart, volume_chart


if __name__ == '__main__':
    app.run_server(debug=True)
