from dash import dcc, Dash, html, dash_table, Input, Output, State, ctx
import pandas as pd

from sqlalchemy import create_engine
import dash_bootstrap_components as dbc


DATABASE = "/Users/ellis/Documents/scripts/arboretum/orchestrator/orchestrator.db"

engine = create_engine(f"sqlite:///{DATABASE}")
df = pd.read_sql_table("steps", con=engine)
df = df.drop("step", axis=1)

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(html.H1("Dashboard", className="text-center mb-4"), width=12)]
        ),
        dbc.Row(
            [
                dbc.Col(  
                    html.Div(
                        [
                            html.P(f"This dashboard displays the current status of all steps in {DATABASE}", className="lead"),
                            html.P("Use the filters and sort headers to explore the data.", className="lead"),
                            html.P("You can download the filtered view using the buttons below.", className="lead"),
                        ]
                    ),
                    width=12,
                )
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.ButtonGroup(
                        [
                            dbc.Button("Download CSV", id="btn-csv", color="primary"),
                            dbc.Button("Download JSON", id="btn-json", color="secondary"),
                        ]
                    ),
                    className="mt-3",
                ),
                dcc.Download(id="download"),
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="data-table",
                        data=df.to_dict("records"),
                        sort_action="native",
                        # page_size=10,
                        filter_action="native",
                        columns=[{"name": col, "id": col, "hideable": True} for col in df.columns],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "maxWidth": "300px",
                        },
                        style_header={
                            "fontWeight": "bold",
                            "whiteSpace": "normal",
                        },
                        style_data_conditional=[
                            {
                                "if": {
                                    "filter_query": '{status} = "completed"',
                                    # "column_id": "status",
                                },
                                "backgroundColor": "#d4edda",
                                "color": "#155724",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "unstarted"',
                                    # "column_id": "status",
                                },
                                "backgroundColor": "#e0e0e0",
                                "color": "#424242",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "failed"',
                                    # "column_id": "status",
                                },
                                "backgroundColor": "#f8d7da",
                                "color": "#721c24",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "running"',
                                    # "column_id": "status",
                                },
                                "backgroundColor": "#d0e7ff",
                                "color": "#004085",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "pending"',
                                    # "column_id": "status",
                                },
                                "backgroundColor": "#fff3cd",
                                "color": "#856404",
                            },
                        ],
                    )
                )
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("download", "data"),
    Input("btn-csv", "n_clicks"),
    Input("btn-json", "n_clicks"),
    State("data-table", "derived_virtual_data"),
    prevent_initial_call=True,
)
def download_data(n_csv, n_json, table_data):
    if not table_data:
        return

    triggered_id = ctx.triggered_id

    df_filtered = pd.DataFrame(table_data)

    if triggered_id == "btn-csv":
        return dcc.send_data_frame(df_filtered.to_csv, "orchestrator.csv", index=False)
    elif triggered_id == "btn-json":
        return dict(content=df_filtered.to_json(orient="records", indent=2), filename="orchestrator.json")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
