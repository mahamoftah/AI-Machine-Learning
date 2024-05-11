from dash import html, register_page  # , callback # If you need callbacks, import it here.
import dash
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc

register_page(
    __name__,
    name='Are Your Employees Burning Out?',
    path='/'
)


def layout():
    layout = (html.Div(
        style={"backgroundImage": "url('assets/im.gif')",'backgroundRepeat': 'no-repeat','backgroundPositionY': '400px',
               'backgroundPositionX': '1000px'},
        id='homeLayout',
        children=[

           dbc.Container(html.Div(
                [
                    dbc.Row(
                        dbc.Col(
                            html.Div("Are Your Employees Burning Out?",
                                     style={"margin-top": "200px", "font-size": "50px",
                                            "font-weight": "bold", }),
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                [
                                    "Understanding what will be the Burn Rate for the employee working in an organization where ",
                                    "work from home is a boon ", html.Br(),"and a bane. How are employees' Burn Rate affected based on various ",
                                    "conditions provided?"],
                                style={"margin-top": "50px", "margin-right": "45px", "font-size": "30px"}
                            ),

                            width={"size": 9}
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.NavLink(
                                dbc.Button("Let's Explore", outline=True, size='lg',
                                           style={"border-color": "#6A0000", }, className="d-grid gap-2 dash-button"
                                           )

                                , href='/model')
                            , style={"margin-top": "50px", "font-size": "30px", "width": "auto"},

                            width={"size": 5}
                        )
                    )], style={"height": "100vh", }, ))
        ]

    ))
    return layout
