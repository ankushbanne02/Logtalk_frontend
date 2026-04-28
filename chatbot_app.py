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

from layouts.sample_queries import sample_queries_layout

UPLOAD_LOG_URL = "https://logtalk-log-uploader.mangoocean-41604236.westeurope.azurecontainerapps.io/"

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
    dcc.Store(id="chat-history", storage_type="memory", data=[]),
    dcc.Store(id="auth-expired-chat", data=0),
    dcc.Store(id="auth-expired-db-load", data=0),
    dcc.Store(id="auth-expired-db-delete", data=0),

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
                            "Upload Log",
                            href=UPLOAD_LOG_URL,
                            target="_blank",
                            external_link=True,
                            className="text-white",
                            id="upload-log-link",
                        ),

                        dbc.NavLink(
                            "Sample Queries",
                            href="/sample-queries",
                            className="text-white",
                            id="sample-queries-link",
                        ),

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
    elif pathname == "/sample-queries":
        return sample_queries_layout

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
    Output("upload-log-link", "style"),
    Output("sample-queries-link", "style"),
    Output("login-btn-nav", "style"),
    Output("logout-btn", "style"),
    Input("url", "pathname"),
    State("auth-token", "data")
)
def update_navbar(pathname, token):

    hidden = {"display": "none"}
    shown_link = {"display": "block"}

    # On login page → hide everything
    if pathname == "/login":
        return hidden, hidden, hidden, hidden, hidden

    # Logged in → show nav links + logout, hide login button
    if token:
        return shown_link, shown_link, shown_link, hidden, shown_link

    # Not logged in → only login button is visible
    return hidden, hidden, hidden, shown_link, hidden



@app.callback(
    Output("auth-token", "clear_data"),
    Output("url", "pathname", allow_duplicate=True),  #  FIX
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    return True, "/login"


# --- Central handler: when any callback signals an expired/invalid token,
#     clear the stored token and bounce the user to /login. Each data
#     callback owns its own counter store, so they don't need
#     allow_duplicate / prevent_initial_call on their own outputs.
@app.callback(
    Output("auth-token", "clear_data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("auth-expired-chat", "data"),
    Input("auth-expired-db-load", "data"),
    Input("auth-expired-db-delete", "data"),
    prevent_initial_call=True,
)
def handle_auth_expired(chat_sig, db_load_sig, db_delete_sig):
    if not (chat_sig or db_load_sig or db_delete_sig):
        return no_update, no_update
    return True, "/login"

# ---------------- REGISTER CALLBACKS ----------------
register_login_callbacks(app)
register_reset_callbacks(app)
register_chatbot_callbacks(app)
register_database_callbacks(app)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
