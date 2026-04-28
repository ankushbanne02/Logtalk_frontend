import os
import requests
from dash import Input, Output, State, no_update
from requests.exceptions import RequestException

BACKEND_URL = os.getenv("BACKEND_URI")

def register_login_callbacks(app):

    @app.callback(
        Output("auth-token", "data"),
        Output("login-error", "children"),
        Output("url", "pathname", allow_duplicate=True),
        Input("login-btn", "n_clicks"),
        State("login-username", "value"),
        State("login-password", "value"),
        prevent_initial_call=True
    )


    
    def perform_login(n_clicks, username, password):
        
        if not username or not password:
            return no_update, "Please enter username and password", no_update

        try:
            response = requests.post(
                f"{BACKEND_URL}/login",
                json={
                "username": username,
                "password": password
                },
                timeout=5
            )

             #  Success
            if response.status_code == 200:
                token = response.json().get("access_token")
                return token, "", "/"

            #  User not found
            elif response.status_code == 404:
                return None, "User not found", no_update

            #  Incorrect password
            elif response.status_code == 401:
                return None, "Incorrect password", no_update

            #  Other errors
            else:
                return None, response.json().get("detail", "Login failed"), no_update

        except RequestException:
        # Backend down / DNS issue / timeout / connection refused
            return (
                None,
                "Service is currently down. Please contact the Technical team.",
                no_update
                )




    