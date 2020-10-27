import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State


df = pd.read_csv('politics.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Election 2020', style={
                'textAlign': 'center'}), width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='choro', figure={}, config={
                'displayModeBar': False}), xs=12, sm=12, md=12, lg=12, xl=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar', figure={}, config={
                'displayModeBar': False}), xs=12, sm=12, md=12, lg=12, xl=12)
    ])
], className='container')


@app.callback(
    [Output('choro', 'figure'),
     Output('bar', 'figure')],
    [Input('choro', 'clickData')]
)
def update(clicked):

    if clicked:
        if df.loc[df['state'] == clicked['points'][0]['location'], 'party'].values[0] == 'democrat':
            df.loc[df['state'] == clicked['points'][0]['location'], 'party'] = 'republican'
        elif df.loc[df['state'] == clicked['points'][0]['location'], 'party'].values[0] == 'republican':
            df.loc[df['state'] == clicked['points'][0]['location'], 'party'] = 'unsure'
        else:
            df.loc[df['state'] == clicked['points'][0]['location'], 'party'] = 'democrat'
        

    fig_map = px.choropleth(
        df,
        locations='state',
        hover_name='state',
        hover_data=['electoral votes'],
        locationmode='USA-states',
        color='party',
        scope='usa',
        color_discrete_map={'democrat': '#5768AC',
                            'republican': '#FA5A50', 'unsure': '#dddddd'}
    )
    fig_map.update_layout(showlegend=False)
    # fig_map.update_traces(hovertemplate='<b>%{locations}%</b><extra></extra>')

    dff = df[df['party'] != 'unsure']

    fig_hist = px.histogram(dff, y='party', x='electoral votes', color='party', range_x=[
                            0, 350], color_discrete_map={'democrat': '#5768AC', 'republican': '#FA5A50'})
    fig_hist.update_layout(showlegend=False, shapes=[
        dict(type='line', xref='paper', x0=0.77,
             x1=0.77, yref='y', y0=-0.5, y1=1.5)
    ])
    fig_hist.add_annotation(y=0.5, x=280, showarrow=False, text='270 to Win')

    return fig_map, fig_hist


if __name__ == "__main__":
    app.run_server(debug=True)
