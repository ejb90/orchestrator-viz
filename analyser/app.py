from dash import dcc, Dash, html, dash_table, Input, Output, State, ctx
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine
import dash_bootstrap_components as dbc

import database


app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])


def load_data():
    engine = create_engine(database.DB_ADDRESS)
    df = pd.read_sql_table("results", con=engine)
    df = df.drop("result", axis=1)
    df = df.drop("step", axis=1)
    return df


def calculate_summary(df):
    """"""
    # Calculate summary stats for numeric columns
    stats = {
        "min": df.min(numeric_only=True),
        "max": df.max(numeric_only=True),
        "mean": df.mean(numeric_only=True),
        "std": df.std(numeric_only=True),
    }

    # Create a summary DataFrame from these stats
    summary_df = pd.DataFrame(stats).T  # transpose so rows are stats

    # For non-numeric columns, fill with empty strings
    for col in df.columns:
        if col not in summary_df.columns:
            summary_df[col] = ""

    # Reorder columns to match original df
    summary_df = summary_df[df.columns]

    # Add a label column for the summary rows — put label in first column
    label_col = df.columns[0]
    summary_df[label_col] = summary_df.index

    return summary_df


def build_preable():
    """"""
    preamble = dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            f"This dashboard displays the stored results of all outputs in {database.DATABASE}",
                            className="lead",
                        ),
                        html.P(
                            "Use the filters and sort headers to explore the data.",
                            className="lead",
                        ),
                        html.P(
                            "You can download the filtered view using the buttons below.",
                            className="lead",
                        ),
                    ]
                ),
                width=12,
            )
        ],
        className="mb-3",
    )
    return preamble


def build_download_buttons():
    download_buttons = dbc.Row(
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
        className="mb-4",
    )
    return download_buttons


def build_table(df):
    """"""
    style_cell_conditional = []
    for col in df.columns:
        style_cell_conditional.append(
            {
                "if": {"column_id": col},
                "width": "12em",
                "minWidth": "12em",
                "maxWidth": "12em",
                "wordBreak": "break-word",
            }
        )
        if pd.api.types.is_float_dtype(df[col]):
            style_cell_conditional.append(
                {
                    "if": {"column_id": col},
                    "textAlign": "right"
                } 
            )
    style_cell_conditional.append(
        {
            "if": {"column_id": "path"},
            "width": "30em",
            "minWidth": "30em",
            "maxWidth": "30em",
            "wordBreak": "break-word",
        }
    )
    style_cell_conditional.append(
        {
            "if": {"column_id": "datetime"},
            "width": "18em",
            "minWidth": "18em",
            "maxWidth": "18em",
            "wordBreak": "break-word",
        }
    )
    style_cell_conditional.append(
        {
            "if": {"column_id": "version"},
            "width": "10em",
            "minWidth": "10em",
            "maxWidth": "10em",
            "wordBreak": "break-word",
        }
    )        

    main_table = dbc.Row(
        [
            dbc.Col(
                dash_table.DataTable(
                    id="main-table",
                    data=df.to_dict("records"),
                    sort_action="native",
                    # page_size=10,
                    filter_action="native",
                    columns=[
                        {
                            "name": col,
                            "id": col,
                            "hideable": True,
                            "type": "numeric",
                            "format": dash_table.Format.Format(
                                precision=6, scheme=dash_table.Format.Scheme.fixed
                            ),
                        }
                        if pd.api.types.is_float_dtype(df[col])
                        else {"name": col, "id": col, "hideable": True}
                        for col in df.columns
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "whiteSpace": "normal",
                        "height": "auto",
                        "maxWidth": "300px",
                    },
                    style_cell_conditional=style_cell_conditional,
                    style_header={
                        "fontWeight": "bold",
                        "whiteSpace": "normal",
                    },
                )
            )
        ]
    )

    summary_table = dbc.Row(
        [
            dbc.Col(
                dash_table.DataTable(
                    id="summary-table",
                    sort_action="none",
                    filter_action="none",
                    hidden_columns=[],
                    editable=False,
                    columns=[
                        {
                            "name": col,
                            "id": col,
                            "hideable": True,
                            "type": "numeric",
                            "format": dash_table.Format.Format(
                                precision=6, scheme=dash_table.Format.Scheme.fixed
                            ),
                        }
                        if pd.api.types.is_float_dtype(df[col])
                        else {"name": col, "id": col, "hideable": True}
                        for col in df.columns
                    ],
                    style_table={"overflowX": "auto"},
                    style_header={"display": "none"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "whiteSpace": "normal",
                        "height": "auto",
                        "maxWidth": "300px",
                    },
                    style_cell_conditional=style_cell_conditional,
                )
            )
        ],
        className="mb-4",
    )

    return main_table, summary_table


def build_plot_x_vs_y_per_zval_forall_aval(df, xval, yval, zval, aval):
    """"""
    df = df[df['name'] == aval]

    fig = px.line(df, x=xval, y=yval, color=zval, markers=True,
              title=f"{yval.title()} vs {xval.title()} by {zval.title()}")

    figure = dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=fig)),
        ],
        className="mb-4",
    )

    return figure


def build_webapp(df):
    """"""
    header = dbc.Row(
        [dbc.Col(html.H1("Results Dashboard", className="text-center mb-4"), width=12)]
    )

    preamble = build_preable()
    download_buttons = build_download_buttons()
    main_table, summary_table = build_table(df)
    runtime_vs_version_plot_mesh =  build_plot_x_vs_y_per_zval_forall_aval(df, "version", "runtime", "model", "mesh")
    runtime_vs_version_plot_simulate =  build_plot_x_vs_y_per_zval_forall_aval(df, "version", "runtime", "model", "simulate")

    # main_table = dbc.Collapse(main_table, id="collapse-summary", is_open=True)

    app.layout = dbc.Container(
        [
            header,
            preamble,
            download_buttons,
            main_table,
            summary_table,
            runtime_vs_version_plot_mesh,
            runtime_vs_version_plot_simulate,
        ],
        fluid=True,
    )


@app.callback(
    Output("download", "data"),
    Input("btn-csv", "n_clicks"),
    Input("btn-json", "n_clicks"),
    State("main-table", "derived_virtual_data"),
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
        return dict(
            content=df_filtered.to_json(orient="records", indent=2),
            filename="orchestrator.json",
        )


@app.callback(
    Output("summary-table", "data"), Input("main-table", "derived_virtual_data")
)
def update_summary(filtered_data):
    if not filtered_data:
        return []

    df_filtered = pd.DataFrame(filtered_data)

    stats = {
        "min": df_filtered.min(numeric_only=True),
        "max": df_filtered.max(numeric_only=True),
        "mean": df_filtered.mean(numeric_only=True),
        "std": df_filtered.std(numeric_only=True),
    }

    summary_df = pd.DataFrame(stats).T  # rows are min, max, mean, std
    summary_df.insert(0, df_filtered.columns[0], summary_df.index)  # add label

    # Fill non-numeric cols with empty strings
    for col in df_filtered.columns:
        if col not in summary_df.columns:
            summary_df[col] = ""

    # Reorder columns to match
    summary_df = summary_df[df_filtered.columns]

    return summary_df.to_dict("records")


@app.callback(
    Output("summary-table", "hidden_columns"),
    Input("main-table", "hidden_columns"),
)
def sync_hidden_columns(hidden_cols):
    # Just pass the list of hidden column IDs from main to summary
    return hidden_cols or []


@app.callback(
    Output("collapse-summary", "is_open"),
    Input("btn-toggle-summary", "n_clicks"),
    State("collapse-summary", "is_open"),
)
def toggle_summary(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Run the app
if __name__ == "__main__":
    df = load_data()
    build_webapp(df)
    app.run(debug=True)
