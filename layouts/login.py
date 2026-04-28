import dash_bootstrap_components as dbc
from dash import html

def login_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Login", className="text-center mb-4"),

                        dbc.Input(
                            id="login-username",
                            placeholder="Username",
                            className="mb-3"
                        ),

                        dbc.Input(
                            id="login-password",
                            placeholder="Password",
                            type="password",
                            className="mb-3"
                        ),

                        dbc.Button(
                            "Login",
                            id="login-btn",
                            color="dark",
                            className="w-100"
                        ),


                        dbc.Button(
                            "Reset Password",
                            href="/reset-password",
                            color="link",
                            className="w-100 mt-2"
                        ),


                        html.Div(
                            id="login-error",
                            className="text-danger text-center mt-3"
                        )
                    ]),
                    className="shadow"
                ),
                width=4
            ),
            justify="center",
            className="mt-5"
        )
    )
