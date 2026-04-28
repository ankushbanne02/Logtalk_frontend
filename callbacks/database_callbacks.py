from dash import Input, Output, State, no_update
import requests
import os
from dotenv import load_dotenv  

load_dotenv()

api_url = os.getenv("BACKEND_URI")


def register_database_callbacks(app):

    #  Load collections whenever URL = /database
    @app.callback(
        Output("db-table", "data"),
        Output("auth-token", "clear_data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("url", "pathname"),
        State("auth-token", "data"),   # ⬅ read token
        prevent_initial_call=True
    )

    def load_collections(pathname, token):

        if pathname != "/database":
            return no_update, no_update, no_update

        #  add auth header
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            resp = requests.get(
                f"{api_url}/database/collections",
                headers=headers
            )

            # session expired / invalid token → clear token + redirect to login
            if resp.status_code == 401:
                return [], True, "/login"

            collections = resp.json()

        except Exception:
            collections = []

        data = []
        for i, name in enumerate(collections, start=1):
            data.append({"sr": i, "collection": name, "action": "🗑️ Delete"})

        return data, no_update, no_update


    #  Delete collection when clicking in Action column
    @app.callback(
        Output("db-table", "data", allow_duplicate=True),
        Output("db-alert", "children"),
        Output("db-alert", "color"),
        Output("db-alert", "is_open"),
        Output("db-table", "active_cell"),
        Output("auth-token", "clear_data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("db-table", "active_cell"),
        State("db-table", "data"),
        State("auth-token", "data"),   #  read token
        prevent_initial_call=True
    )
    def delete_collection(active_cell, table_data, token):

        if not active_cell or not table_data:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        row = active_cell.get("row")
        col = active_cell.get("column_id")

        if col != "action" or row is None:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        collection_name = table_data[row]["collection"]

        # add auth header
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            resp = requests.delete(
                f"{api_url}/database/collections/{collection_name}",
                headers=headers
            )

            # unauthorized → clear token + redirect to login
            if resp.status_code == 401:
                return (
                    table_data,
                    " Session expired. Please login again.",
                    "danger",
                    True,
                    None,
                    True,
                    "/login",
                )

            # success
            if resp.status_code == 200:

                updated_data = [
                    r for r in table_data if r["collection"] != collection_name
                ]

                # Re-index Sr
                for i, r in enumerate(updated_data, start=1):
                    r["sr"] = i

                return (
                    updated_data,
                    f" Collection '{collection_name}' deleted.",
                    "success",
                    True,
                    None,
                    no_update,
                    no_update,
                )

            #  backend error case
            return (
                table_data,
                f" {resp.json().get('detail', 'Error deleting collection')}",
                "danger",
                True,
                None,
                no_update,
                no_update,
            )

        except Exception as e:
            return (
                table_data,
                f" Backend error: {e}",
                "danger",
                True,
                None,
                no_update,
                no_update,
            )
