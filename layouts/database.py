from dash import html, dash_table
import dash_bootstrap_components as dbc

database_layout = html.Div([


    html.H3("📂 Database Collections", className="mb-4 text-center"),

    dbc.Alert(id="db-alert", is_open=False, dismissable=True, fade=True),

    dash_table.DataTable(
        id="db-table",
        columns=[
            {"name": "Sr", "id": "sr"},
            {"name": "Collection Name", "id": "collection"},
            {"name": "Action", "id": "action"},
        ],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
    ),
])
