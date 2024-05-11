import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Read data from the CSV file
df = pd.read_csv('D:/CSE_student_performances/train.csv')
avg = df['Burn Rate'].median()
n_burnout = df['Burn Rate'].count()
df["Burnout"] = df["Burn Rate"] > avg
default_color1 = 'rgb(196, 240, 197)'
default_color2 = 'rgb(106, 0, 0)'

# fig1
counts = df.groupby(by=["Designation", "Burnout"]).size().reset_index(name="count")
fig1 = px.bar(counts, x="Designation", y="count", color='Burnout', color_discrete_map={
    'true': default_color1,
    'false': default_color2
})
fig1.update_traces(hovertemplate='Seniority Level: %{x}<br>Count: %{y}')
fig1.update_layout(xaxis=dict(
    title="Seniority Level"
), yaxis=dict(
    title="Number Of Employees"
))
##

# fig2
counts = df.groupby(by=["Gender", "Burnout"]).size().reset_index(name="count")
fig2 = px.bar(counts, x='Gender', y='count', color='Burnout', color_discrete_map={
    'true': default_color1,
    'false': default_color2
}, barmode="group")
fig2.update_traces(hovertemplate='Gender: %{x}<br>Count: %{y}')
fig2.update_layout(xaxis=dict(
    title="Gender"
), yaxis=dict(
    title="Number Of Employees"
))

# fig3
fig3 = px.scatter(df, x="Mental Fatigue Score", y="Burn Rate", color='Resource Allocation')

dash.register_page(__name__, path='/dashboard')

layout = html.Div(dbc.Container([
    html.H1('Are Your Employees Burning Out?', style={"margin-top": "20px", "margin-bottom": "30px"}),
    dbc.Stack([
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [html.H4("Number of Burn Out Employees", className="card-title",
                                     style={'font-size': '20px'}),
                             html.H2(n_burnout, style={'font-size': '50px', 'fontColor': '#6A0000'}),
                             html.H4(f'out of {len(df)}', style={'font-size': '15px'})
                             ])
                    )
                ),
                dbc.Col(dbc.Card(
                    dbc.CardBody(
                        [html.H4("Average Burn Out Rate", className="card-title", style={'font-size': '20px'}),
                         html.H2(f'{avg}', style={'font-size': '50px'}),
                         html.H4(f'out of {1}', style={'font-size': '15px'})
                         ])
                )),
                dbc.Col(dbc.Card(
                    dbc.CardImg(src="assets/ab91af9a57fff04a01ba4fd4fc8fb8d4.jpg", top=True,
                                style={'width': '200px', 'height': '160px'})

                ))
            ]
        ),
        dbc.Row([
            # First graph
            dbc.Stack([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [html.H4("Effect of seniority level on Burnout Status", className="card-title"),
                             dcc.Graph(
                                 id='graph1',
                                 figure=fig1
                             )
                             ])
                    )

                ], width=6),

                # Second graph
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [html.H4("Gender-wise Distribution of Burnout Rate", className="card-title"),
                             dcc.Graph(
                                 id='graph2',
                                 figure=fig2
                             )
                             ])
                    )

                ], width={"size": 6, "offset": 0}),

            ], direction="horizontal")

        ]),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [html.H4("Effect of Mental Fatigue Score and Burnout Rate"),
                             dcc.Graph(
                                 id='graph3',
                                 figure=fig3
                             )
                             ], ), style={'width': '1230px', 'align': "center", 'margin-bottom': "30px"}
                    )

                ], width={'size': 12, 'offset': 0}),  # Adjust width to fill the entire row
            ]
            , justify='center', align="center")
    ], gap='4')

]), style={"height": "200vh", }, )
