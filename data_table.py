import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc


df = pd.read_csv('internet_cleaned.csv')
jdf = df[df['year'] == 2019]

df['id'] = df['iso_alpha3']
df.set_index('id', inplace=True, drop=False)

app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {'name': i, 'id': i, 'deletable': True,
                'selectable': True, 'hideable': True}
            if i == 'iso_alpha3' or i == 'year' or i == 'id'
            else {'name': i, 'id': i, 'deletable': True, 'selectable': True}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action='native',
        sort_action='native',
        column_selectable='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=6,
        style_cell={
            'minWidth': 95,
            'maxWidth': 95,
            'width': 95
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),

    html.Br(),
    html.Br(),

    html.Div(id='bar-container'),

    html.Div(id='choromap-container'),
], className='container')


@app.callback(
    Output('bar-container', 'children'),
    [Input('datatable-interactivity', 'derived_virtual_data'),
     Input('datatable-interactivity', 'derived_virtual_selected_rows'),
     Input('datatable-interactivity', 'derived_virtual_selected_row_ids'),
     Input('datatable-interactivity', 'selected_rows'),
     Input('datatable-interactivity', 'derived_virtual_indices'),
     Input('datatable-interactivity', 'derived_virtual_row_ids'),
     Input('datatable-interactivity', 'active_cell'),
     Input('datatable-interactivity', 'selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows, rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    dff = pd.DataFrame(all_rows_data)
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9' for i in range(len(dff))]

    if 'country' in dff and 'did online course' in dff:
        return [
            dcc.Graph(id='bar-chart',
                figure=px.bar(
                    data_frame=dff,
                    x='country',
                    y='did online course',
                    labels={'did online course': '% of Pop took online course'}
                ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                .update_traces(marker_color=colors, hovertemplate='<b>%{y}%</b><extra></extra>')
            )
        ]


@app.callback(
    Output('choromap-container', 'children'),
    [Input('datatable-interactivity', 'derived_virtual_data'),
     Input('datatable-interactivity', 'derived_virtual_selected_row_ids')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    borders = [5 if i in slctd_row_indices else 1 for i in range(len(dff))]

    if 'iso_alpha3' in dff and 'internet daily' in dff and 'country' in dff:
        return [
            dcc.Graph(id='choropleth',
                style={'height': 700},
                figure=px.choropleth(
                    data_frame=dff,
                    locations='iso_alpha3',
                    scope='europe',
                    color='internet daily',
                    title='% of Pop that Uses Internet Daily',
                    template='plotly_dark',
                    hover_data=['country', 'internet daily']
                ).update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}" + "%")
            )
        ]


if __name__ == "__main__":
    app.run_server(debug=True)
