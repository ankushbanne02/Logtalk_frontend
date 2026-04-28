import os
import re
import requests
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input, State, no_update
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URI")


def format_markdown_with_headings(text: str):
    return re.sub(r'^\s*#\s+', '# ', text, flags=re.MULTILINE)


def load_plotly_chart(chart_path):
    if not chart_path:
        return None

    full_url = f"{BACKEND_URL}/{chart_path}" if not chart_path.startswith("http") else chart_path

    try:
        if chart_path.lower().endswith(".json"):
            r = requests.get(full_url)
            if r.status_code == 200:
                fig = go.Figure(r.json())
                return dcc.Graph(
                    figure=fig,
                    config={"displayModeBar": False},
                    style={"height": "400px", "marginTop": "8px"}
                )
        elif chart_path.lower().endswith(".html"):
            return html.Iframe(
                src=full_url,
                style={"width": "100%", "height": "600px", "marginTop": "8px"}
            )
        elif chart_path.lower().endswith(".png"):
            return html.Img(
                src=full_url,
                style={"width": "100%", "marginTop": "8px"}
            )
    except Exception as e:
        return html.Div(f"[Chart load error: {e}]", style={"color": "red"})


def format_chat(history):
    chat_bubbles = []

    for entry in history:
        role = entry["role"]
        text = entry.get("text", "")
        chart_path = entry.get("chart_path")

        if role == "user":
            chat_bubbles.append(
                html.Div(
                    html.Div([
                        html.Div(text, className="user-bubble"),
                        html.Img(src="/assets/images/human_logo.png", height="25")
                    ], className="user-message-inner"),
                    className="user-message"
                )
            )
        else:
            bubble_content = []

            if entry.get("flow"):
                bubble_content.append(
                    html.Details([
                        html.Summary("Multi-Agent Flow"),
                        html.Div(entry["flow"])
                    ])
                )

            if text:
                text = re.sub(
                    r"\]\((assets/.*?)\)",
                    lambda m: f"]({BACKEND_URL}/{m.group(1)})",
                    text
                )
                bubble_content.append(
                    dcc.Markdown(
                        format_markdown_with_headings(text),
                        dangerously_allow_html=True
                    )
                )

            if chart_path:
                chart = load_plotly_chart(chart_path)
                if chart:
                    bubble_content.append(chart)

            chat_bubbles.append(
                html.Div([
                    html.Img(src="/assets/images/LogTalk_Logo.png", height="25"),
                    html.Div(bubble_content, className="bot-bubble")
                ], className="bot-message")
            )

    return chat_bubbles


# ---------------- CHATBOT LAYOUT (FIXED) ----------------
chatbot_layout = html.Div([

    # 🔑 SCROLL CONTAINER (RESTORED)
    html.Div(
        html.Div(id="chat-window", className="chat-window"),
        className="chat-scroll-container"
    ),

    # INPUT BAR
    html.Div(
        dbc.InputGroup([
            dbc.Input(
                id="question-input",
                placeholder="Type your question...",
                n_submit=0
            ),
            dbc.Button(
                html.I(className="bi bi-arrow-up"),
                id="run-button"
            )
        ]),
        className="chat-input-bar"
    ),

    dcc.Store(id="chat-history", data=[]),
    dcc.Store(id="process-trigger"),
    dcc.Interval(id="typing-interval", interval=500, disabled=True),
    dcc.Interval(id="welcome-interval", interval=500, max_intervals=1)

], className="chatbot-page")


# ---------------- CALLBACKS ----------------
def register_chatbot_callbacks(app: Dash):

    @app.callback(
        Output("chat-history", "data", allow_duplicate=True),
        Output("chat-window", "children", allow_duplicate=True),
        Input("welcome-interval", "n_intervals"),
        State("chat-history", "data"),
        prevent_initial_call=True
    )
    def show_welcome_message(_, history):
        try:
            r = requests.get(f"{BACKEND_URL}/welcome")
            msg = r.json().get("message", "")
        except:
            msg = "Backend connection failed."

        history = history + [{"role": "bot", "text": msg}]
        return history, format_chat(history)

    @app.callback(
        Output("chat-window", "children", allow_duplicate=True),
        Output("chat-history", "data", allow_duplicate=True),
        Output("question-input", "value"),
        Output("process-trigger", "data"),
        Output("typing-interval", "disabled", allow_duplicate=True),
        Input("run-button", "n_clicks"),
        Input("question-input", "n_submit"),
        State("question-input", "value"),
        State("chat-history", "data"),
        prevent_initial_call=True
    )
    def handle_user_input(_, __, question, history):
        if not question or not question.strip():
            return no_update, no_update, no_update, no_update, True

        history = history + [
            {"role": "user", "text": question.strip()},
            {"role": "bot", "text": "_Analyzing..._"}
        ]

        return format_chat(history), history, "", {"question": question.strip()}, False

    @app.callback(
        Output("chat-history", "data", allow_duplicate=True),
        Output("chat-window", "children", allow_duplicate=True),
        Output("typing-interval", "disabled", allow_duplicate=True),
        Input("process-trigger", "data"),
        State("chat-history", "data"),
        State("auth-token", "data"),   # 🔐 JWT
        prevent_initial_call=True
    )
    def process_and_respond(trigger, history, token):
        if not trigger:
            return no_update, no_update, True

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            r = requests.post(
                f"{BACKEND_URL}/chat",
                json={"user_question": trigger["question"]},
                headers=headers
            )

            if r.status_code == 200:
                data = r.json()
                bot_response = {
                    "role": "bot",
                    "flow": data.get("execution_flow_text"),
                    "text": data.get("summary"),
                    "chart_path": data.get("chart_path")
                }
            elif r.status_code == 401:
                bot_response = {"role": "bot", "text": "🔒 Please login again."}
            else:
                bot_response = {"role": "bot", "text": "⚠️ Server error"}

        except Exception as e:
            bot_response = {"role": "bot", "text": f"⚠️ {e}"}

        history = history[:-1] + [bot_response]
        return history, format_chat(history), True
