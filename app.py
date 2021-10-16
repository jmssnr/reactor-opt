import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from model import OCP

# Specify list of external stylesheets
external_stylesheets = [dbc.themes.COSMO]

# Create dash instance
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# UI elements
# -------------------------------------------------------------------------------

# Modal
with open("about.md", "r") as f:
    about_md = f.read()

modal_overlay = dbc.Modal(
    [
        dbc.ModalBody(html.Div([dcc.Markdown(about_md)], id="about-md")),
        dbc.ModalFooter(dbc.Button("Close", id="about-close")),
    ],
    id="modal",
    size="lg",
)

about_button = (
    dbc.Button(
        "About",
        outline=True,
        color="info",
        id="about-open",
        style={"width": "150px", "margin-right": "15px"},
    ),
)

github_button = (
    dbc.Button(
        "View Code",
        outline=True,
        color="info",
        href="https://github.com/jmssnr/reactor-opt",
        id="gh-link",
        style={"width": "150px"},
    ),
)

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H4(
                                        "Reactor Optimization", style={"color": "white"}
                                    ),
                                    html.H6(
                                        "Single-Shooting Approach",
                                        style={"color": "white"},
                                    ),
                                ],
                                id="app-title",
                            )
                        ],
                        md=True,
                        align="center",
                    )
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.NavbarToggler(id="navbar-toggler"),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(about_button),
                                        dbc.NavItem(github_button),
                                    ],
                                    navbar=True,
                                ),
                                id="navbar-collapse",
                                navbar=True,
                            ),
                        ],
                        md=2,
                    )
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color="dark",
    sticky="top",
)

output_card = dbc.Card(
    [
        dbc.CardHeader("Optimization Results"),
        dbc.CardBody(
            [
                dcc.Loading(
                    dcc.Graph(
                        id="results-graph",
                        config={"displayModeBar": False},
                        style={"height": "400px"},
                    ),
                    type="dot",
                )
            ]
        ),
    ],
    style={"box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px"},
)

input_card = dbc.Card(
    [
        dbc.CardHeader("Parameters"),
        dbc.CardBody(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("Number of Control Intervals"),
                        dbc.Input(
                            id="N-value", value=15, type="number", min=5, max=30, step=1
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Upper Reactor Temperature"),
                        dbc.Input(
                            id="upper-bound-value",
                            value=0.2,
                            type="number",
                            min=0.1,
                            max=0.3,
                            step=0.05,
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Maximum Number of Iterations"),
                        dbc.Input(
                            id="max-iter-value",
                            value=15,
                            type="number",
                            min=5,
                            max=60,
                            step=1,
                        ),
                    ]
                ),
                dbc.Button("Optimize", id="optimize-button", color="primary"),
            ]
        ),
    ],
    style={"box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px"},
)

# Page layout
# -------------------------------------------------------------------------------
app.layout = html.Div(
    [
        header,
        dbc.CardDeck([input_card, output_card], style={"margin": "10px"}),
        modal_overlay,
    ]
)

# Callbacks
# -------------------------------------------------------------------------------


@app.callback(
    Output("results-graph", "figure"),
    [
        Input("optimize-button", "n_clicks"),
        State("N-value", "value"),
        State("upper-bound-value", "value"),
        State("max-iter-value", "value"),
    ],
)
def optimize(click, N, upper_bound, max_iter):
    problem = OCP(N, upper_bound)
    df = problem.solve(max_iter)
    fig = problem.plot(df)
    fig.update_layout(
        xaxis_title="z / -",
        yaxis_title="x, u / -",
        yaxis_range=[-0.2, 1.1],
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )

    return fig


# Modal open/close
@app.callback(
    Output("modal", "is_open"),
    [Input("about-open", "n_clicks"), Input("about-close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
