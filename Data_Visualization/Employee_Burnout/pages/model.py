import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import pickle
import numpy as np
import sklearn

with open('D:/CSE_student_performances/pages/model.pkl', 'rb') as file:
    lr_model = pickle.load(file)

dash.register_page(__name__, path='/model')

layout = html.Div(dbc.Container([

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("User Inputs", className="card-title"),
                    html.Div(
                        children=[
                            html.Div(
                                className="padding-top-bot",
                                children=[
                                    html.H6("Gender"),
                                    dbc.Select(id="gender",
                                               options=[{"label": "Female", "value": "Female"},
                                                        {"label": "Male", "value": "Male"}, ]
                                               )
                                ],
                                style={'margin-bottom': '5px'}
                            ),
                            html.Div(
                                className="padding-top-bot",
                                children=[
                                    html.H6("Working From Home Availability"),
                                    dbc.Select(id="wfh",
                                               options=[{"label": "Yes", "value": "Yes"},
                                                        {"label": "No", "value": "No"}, ]
                                               )
                                ],
                            ),
                            html.Div(
                                className="padding-top-bot",
                                children=[
                                    html.H6("Seniority Level"),
                                    dbc.Select(id="level",
                                               options=[{"label": "1", "value": "1"},
                                                        {"label": "2", "value": "2"},
                                                        {"label": "3", "value": "3"},
                                                        {"label": "4", "value": "4"},
                                                        {"label": "5", "value": "5"}, ]
                                               )
                                ],
                            ),
                            html.Div(
                                className="padding-top-bot",
                                children=[
                                    html.H6("Working Hours Per Day"),
                                    dbc.Select(id="hours",
                                               options=[{"label": "1", "value": "1"},
                                                        {"label": "2", "value": "2"},
                                                        {"label": "3", "value": "3"},
                                                        {"label": "4", "value": "4"},
                                                        {"label": "5", "value": "5"},
                                                        {"label": "6", "value": "6"},
                                                        {"label": "7", "value": "7"},
                                                        {"label": "8", "value": "8"},
                                                        {"label": "9", "value": "9"},
                                                        {"label": "10", "value": "10"}, ]
                                               )
                                ],
                            ),
                            html.Div(
                                className="padding-top-bot",
                                children=[
                                    html.H6("Mental Fatigue Score"),
                                    dbc.Input(id="score", type="number", min=0, max=10, step=1,
                                              placeholder='Enter Your Score from 0 to 10'),
                                ],
                                style={'margin-bottom': '10px'},
                            ),
                            html.Div(

                                children=[
                                    dbc.Button('Predict', id='submit', outline=True, size='lg',
                                               style={"border-color": "#6A0000", }, className="d-grid dash-button"
                                               ),

                                ],
                                style={'textAlign': 'center'},
                            ),

                        ],
                    )
                ])
            ])
        ], width=6, style={'margin-top': '30px'}),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("Burning Out Rate Prediction", className="card-title"),
                    dbc.Stack([dbc.Stack([html.Img(src='assets/on1.jpeg', id='img1',
                                                   style={'width': '40%', 'height': '50%',
                                                          }),
                                          html.Img(src='assets/off1.jpeg', id='img2',
                                                   style={'width': '40%', 'height': '50%',
                                                          'margin-left': '100px', 'margin-top': '0px'})],
                                         direction="horizontal")
                                  ,
                               html.H2('Model Output', id='rate', style={'margin-top': '20px'}, ),
                               dbc.Card(dbc.CardBody([html.H2('0.0', id='rate', style={'textAlign': 'center'}),
                                                      html.H4('', id='notice',
                                                              style={'textAlign': 'center',
                                                                     'font-size': '20px'})]),
                                        style={'margin-top': '30px'}, )],
                              gap='3', style={'margin-top': '30px'}, ),
                    dbc.NavLink(
                        dbc.Button([
                            "Analyze Results ",
                            html.I(className="fa fa-arrow-right", style={'margin-left': '5px'})
                            # Font Awesome arrow icon
                        ], id='analyze-results', outline=True, size='lg',
                            style={"border-color": "#6A0000", 'margin-top': '30px'},
                            className="arrow-button")

                        , href='/dashboard'),


                ])
                , style={'height': '720px'}, )
        ], style={'margin-top': '30px'}, )
    ])]), style={"height": "100vh", }, )


# Callback to handle prediction
# Callback to handle prediction
@callback(
    Output(component_id='img1', component_property='src'),
    Output(component_id='img2', component_property='src'),
    Output(component_id='rate', component_property='children'),
    Output(component_id='notice', component_property='children'),
    Input(component_id='submit', component_property='n_clicks'),
    State(component_id='gender', component_property='value'),
    State(component_id='wfh', component_property='value'),
    State(component_id='level', component_property='value'),
    State(component_id='hours', component_property='value'),
    State(component_id='score', component_property='value'),
)
def predict(n_clicks, gender, wft, level, hours, score):
    if n_clicks is None or n_clicks == 0:
        return dash.no_update

    # Mapper for categorical variables
    gender_mapper = {'Female': 0, 'Male': 1}
    wft_mapper = {'No': 0, 'Yes': 1}

    # Prepare input data for prediction
    obs = np.array([int(gender_mapper[gender]), int(wft_mapper[wft]), int(level), int(hours), float(score)]).reshape(1,
                                                                                                                     -1)

    # Make prediction
    rate = round(float(lr_model.predict(obs)[0]), 2)

    # Determine notice text and style based on the predicted rate
    if rate > 0.5:
        src1 = 'assets/on1.jpeg'
        src2 = 'assets/off2.jpeg'
        notice = f'It seems like a lot is going on and you probably get tired quickly'
        notice_style = {'color': '#6A0000', 'font-size': '20px'}  # Red color for high burnout rate
    else:
        src1 = 'assets/on2.jpeg'
        src2 = 'assets/off1.jpeg'
        notice = f'You seem to be managing well and maintaining a healthy work-life balance'
        notice_style = {'color': 'green', 'font-size': '20px'}  # Green color for low burnout rate

    return src1, src2, rate, html.H4(notice, style=notice_style)
