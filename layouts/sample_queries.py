import dash_bootstrap_components as dbc
from dash import html

SAMPLE_QUESTIONS = [
    {
        "category": "Throughput",
        "questions": [
            "What was the total throughput yesterday?",
            "Show me throughput per hour for the last 24 hours.",
            "Compare throughput between this week and last week.",
        ],
    },
    {
        "category": "Volume & Dimensions",
        "questions": [
            "How many parcels were over the volume limit today?",
            "Show the distribution of parcel volumes for the last shift.",
            "Which destinations received the largest parcels yesterday?",
        ],
    },
    {
        "category": "Barcode Reads",
        "questions": [
            "What is the barcode no-read rate for today?",
            "Show me the top 5 reasons for barcode read failures.",
            "Trend of 'Data OK' vs 'No read' over the last 7 days.",
        ],
    },
    {
        "category": "Sort Performance",
        "questions": [
            "How many parcels failed to divert today?",
            "Show me destinations that were full most often this week.",
            "What was the rate of 'Good sort' vs error states yesterday?",
        ],
    },
]


def _category_card(category: str, questions: list[str]) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(category, className="mb-3"),
                html.Ul(
                    [html.Li(q, className="mb-2") for q in questions],
                    className="mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )


sample_queries_layout = dbc.Container(
    [
        html.H3("Sample Queries", className="mt-4 mb-2 text-center"),
        html.P(
            "A few example questions you can ask LogTalk to get started.",
            className="text-center text-muted mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    _category_card(item["category"], item["questions"]),
                    md=6,
                    className="mb-4",
                )
                for item in SAMPLE_QUESTIONS
            ]
        ),
        html.Div(
            dbc.Button(
                "Back to LogTalk",
                href="/",
                color="dark",
                className="mt-2",
            ),
            className="text-center",
        ),
    ],
    className="py-4",
)
