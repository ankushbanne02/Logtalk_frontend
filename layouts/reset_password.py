import dash_bootstrap_components as dbc
from dash import html

def reset_password_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Reset Password", className="text-center mb-4"),

                        dbc.Input(
                            id="reset-username",
                            placeholder="Email / Username",
                            type="email",
                            className="mb-3"
                        ),

                        dbc.Input(
                            id="reset-old-password",
                            placeholder="Old Password",
                            type="password",
                            className="mb-3"
                        ),

                        dbc.Input(
                            id="reset-new-password",
                            placeholder="New Password",
                            type="password",
                            className="mb-3"
                        ),

                        dbc.Button(
                            "Update Password",
                            id="reset-password-btn",
                            color="dark",
                            className="w-100"
                        ),

                        html.Div(
                            id="reset-password-msg",
                            className="text-center mt-3"
                        ),

                        html.Hr(),

                        dbc.Button(
                            "Back to Login",
                            href="/login",
                            color="link",
                            className="w-100"
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
