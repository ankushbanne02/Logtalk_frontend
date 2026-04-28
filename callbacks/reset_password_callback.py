
import os
import requests
from dash import Input, Output, State, no_update
from requests.exceptions import RequestException

BACKEND_URL = os.getenv("BACKEND_URI")


def register_reset_callbacks(app):

    @app.callback(
        Output("reset-password-msg", "children"),
        Output("reset-password-msg", "style"),
        Output("reset-username", "value"),
        Output("reset-old-password", "value"),
        Output("reset-new-password", "value"),
        Input("reset-password-btn", "n_clicks"),
        State("reset-username", "value"),
        State("reset-old-password", "value"),
        State("reset-new-password", "value"),
        prevent_initial_call=True
    )

    
    def reset_password(n, username, old_pwd, new_pwd):

        #  Validation
        if not username or not old_pwd or not new_pwd:
            return (
                "All fields are required",
                {"color": "red", "textAlign": "center"},
                no_update,
                no_update,
                no_update
            )
        

        if old_pwd == new_pwd:
            return (
                "New password must be different from old password",
                {"color": "red", "textAlign": "center"},
                no_update, no_update, no_update
            )

        try:
            response = requests.post(
                f"{BACKEND_URL}/change-password",
                json={
                    "username": username,
                    "old_password": old_pwd,
                    "new_password": new_pwd
                },
                timeout=5
            )

            #  SUCCESS → clear fields
            if response.status_code == 200:
                return (
                    "Password updated successfully. You can now login.",
                    {"color": "green", "textAlign": "center"},
                    None,   #  clear username
                    None,   #  clear old password
                    None    #  clear new password
                )

            #  Errors → keep values
            elif response.status_code == 401:
                return (
                    "Old password is incorrect",
                    {"color": "red", "textAlign": "center"},
                    no_update,
                    no_update,
                    no_update
                )

            elif response.status_code == 404:
                return (
                    "User not found",
                    {"color": "red", "textAlign": "center"},
                    no_update,
                    no_update,
                    no_update
                )
            

            elif response.status_code == 400:
                return (
                    response.json().get("detail", "new password cannot be the same as the old password"),
                    {"color": "red", "textAlign": "center"},
                    no_update,
                    no_update,
                    no_update
                )

            else:
                return (
                    response.json().get("detail", "Reset failed"),
                    {"color": "red", "textAlign": "center"},
                    no_update,
                    no_update,
                    no_update
                )

        except RequestException:
            return (
                "Service is currently down. Please contact the Technical team.",
                {"color": "red", "textAlign": "center"},
                no_update,
                no_update,
                no_update
            )