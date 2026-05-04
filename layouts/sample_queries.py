import dash_bootstrap_components as dbc
from dash import html

CATEGORIES = [
    {
        "icon": "bi-bar-chart-steps",
        "title": "Sort Report",
        "color": "#EF7B13",
        "questions": [
            "Give me sort report of 11 aug 2025",
            "Give me sort report for PLC 1001 on 11 aug 2025",
            "Show me sort report pie chart for 11 aug 2025",
            "Show me sort report for PLC 1001 in pie chart for 11 aug 2025",
        ],
    },
    {
        "icon": "bi-chat-square-dots",
        "title": "Message Count Analysis",
        "color": "#3b82f6",
        "questions": [
            "Give counts of each message of 17 aug 2025",
            "Give counts of each message of 13 may 2025 for PLC 1002",
        ],
    },
    {
        "icon": "bi-speedometer2",
        "title": "Throughput / Capacity Analysis",
        "color": "#10b981",
        "questions": [
            "Share me parcel per hour throughput for 17 aug 2025",
            "Share me parcel per hour throughput for 17 aug 2025 for PLC 1001",
            "Give me the minute in which throughput was highest for 17 aug 2025",
            "Give me the throughput of parcels per 10-minute interval of 17 aug 2025",
        ],
    },
    {
        "icon": "bi-box-seam",
        "title": "Volume Read Analysis",
        "color": "#8b5cf6",
        "questions": [
            "Give me volume read report for 11 aug 2025",
            "Give me volume read report for PLC 1001 on 11 aug 2025",
        ],
    },
    {
        "icon": "bi-upc-scan",
        "title": "Barcode Read Analysis",
        "color": "#ef4444",
        "questions": [
            "Give me barcode read rate report on 17 aug 2025",
            "Give me barcode read rate report for PLC 1001 on 17 aug 2025",
            "Show me barcode read rate pie chart for 11 nov PLC 1001",
        ],
    },
    {
        "icon": "bi-distribute-vertical",
        "title": "Volume Distribution",
        "color": "#f59e0b",
        "questions": [
            "Share the volume distribution for 17 aug 2025",
        ],
    },
]


def _question_item(text: str) -> html.Li:
    return html.Li(
        html.Span(
            [
                html.I(className="bi bi-chat-right-text me-2", style={"fontSize": "0.85rem", "opacity": "0.6"}),
                text,
            ]
        ),
        className="sample-query-item",
    )


def _category_card(cat: dict) -> dbc.Col:
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(
                    html.Div(
                        [
                            html.Div(
                                html.I(className=f"bi {cat['icon']}"),
                                className="sample-icon-circle",
                                style={"background": cat["color"]},
                            ),
                            html.Span(cat["title"], className="sample-card-title"),
                        ],
                        className="d-flex align-items-center gap-3",
                    ),
                    className="sample-card-header",
                    style={"borderLeft": f"4px solid {cat['color']}"},
                ),
                dbc.CardBody(
                    html.Ul(
                        [_question_item(q) for q in cat["questions"]],
                        className="sample-query-list",
                    )
                ),
            ],
            className="sample-card h-100 shadow-sm",
        ),
        md=6,
        className="mb-4",
    )


sample_queries_layout = html.Div(
    [
        # ── Header ──────────────────────────────────────────────────────────
        html.Div(
            [
                html.I(className="bi bi-lightbulb-fill me-2", style={"color": "#EF7B13", "fontSize": "1.6rem"}),
                html.H3("Sample Queries", className="mb-0 d-inline align-middle"),
            ],
            className="d-flex align-items-center justify-content-center mt-4 mb-2",
        ),
        html.P(
            "Copy any of the example questions below and paste them directly into the LogTalk chat.",
            className="text-center text-muted mb-4",
        ),

        # ── Cards grid ──────────────────────────────────────────────────────
        dbc.Container(
            dbc.Row([_category_card(cat) for cat in CATEGORIES]),
            fluid=True,
            className="px-3 px-md-5",
        ),

        # ── Back button ─────────────────────────────────────────────────────
        html.Div(
            dbc.Button(
                [html.I(className="bi bi-arrow-left me-2"), "Back to LogTalk"],
                href="/",
                color="dark",
                outline=True,
                className="mt-2 mb-5",
            ),
            className="text-center",
        ),
    ],
    className="sample-queries-page",
)
