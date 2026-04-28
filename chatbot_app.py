import os
import dash
from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc

from chatbot_frontend import chatbot_layout, register_chatbot_callbacks
from layouts.database import database_layout
from layouts.login import login_layout
from callbacks.database_callbacks import register_database_callbacks
from callbacks.login_callbacks import register_login_callbacks


from layouts.reset_password import reset_password_layout
from callbacks.reset_password_callback import register_reset_callbacks

# ---------------- APP INIT ----------------
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
    ],
    suppress_callback_exceptions=True,
)

app.title = "logTalk"
server = app.server

# ---------------- LAYOUT ----------------
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="auth-token", storage_type="local"),

    dbc.Navbar(
        dbc.Container(
            fluid=True,
            children=[
                html.Div(
                    html.Img(src="/assets/images/company_logo.jpeg", height="40px"),
                    className="me-auto"
                ),
                html.Div(
                    html.A(html.Img(src="/assets/images/LogTalk_Logo.png"), href="/"),
                    className="logo-center"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "Database",
                            href="/database",
                            className="text-white",
                            id="page-switch-link"
                        ),

                        dbc.Button(
                            "Login",
                            href="/login",
                            color="dark",
                            size="sm",
                            id="login-btn-nav"
                        ),

                        dbc.Button(
                            "Logout",
                            color="dark",
                            size="sm",
                            id="logout-btn",
                            style={"display": "none"}
                        ),
                    ],
                    className="ms-auto gap-3",
                    navbar=True,
                ),
            ],
        ),
        color="#EF7B13",
        dark=True,
    ),

    html.Div(id="page-content", style={"paddingTop": "56px", "height": "100vh"})
])

# ---------------- ROUTING ----------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("auth-token", "data")
)



def display_page(pathname, token):

    if not token and pathname not in ["/login", "/reset-password"]:
        return dcc.Location(pathname="/login", id="redirect")

    if pathname == "/login":
        return login_layout()
    elif pathname == "/reset-password":
        return reset_password_layout()
    elif pathname == "/database":
        return database_layout

    return chatbot_layout

# ---------------- PAGE SWITCH LINK ----------------
@app.callback(
    Output("page-switch-link", "children"),
    Output("page-switch-link", "href"),
    Input("url", "pathname")
)
def update_page_link(pathname):
    if pathname == "/database":
        return "LogTalk", "/"
    return "Database", "/database"


# ---------------- NAVBAR VISIBILITY ----------------
@app.callback(
    Output("page-switch-link", "style"),
    Output("login-btn-nav", "style"),
    Output("logout-btn", "style"),
    Input("url", "pathname"),
    State("auth-token", "data")
)
def update_navbar(pathname, token):

    # On login page → hide everything
    if pathname == "/login":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}

    # Logged in
    if token:
        return (
            {"display": "block"},
            {"display": "none"},
            {"display": "block"}
        )

    # Not logged in
    return (
        {"display": "none"},
        {"display": "block"},
        {"display": "none"}
    )



@app.callback(
    Output("auth-token", "clear_data"),
    Output("url", "pathname", allow_duplicate=True),  #  FIX
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    return True, "/login"

# ---------------- REGISTER CALLBACKS ----------------
register_login_callbacks(app)
register_reset_callbacks(app)
register_chatbot_callbacks(app)
register_database_callbacks(app)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=False)
