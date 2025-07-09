from dash import Dash, html, dash_table
import pandas as pd


from sqlalchemy import create_engine
import dash_bootstrap_components as dbc


engine = create_engine(
    "sqlite:////Users/ellis/Documents/scripts/arboretum/orchestrator/orchestrator.db"
)
df = pd.read_sql_table("steps", con=engine)
df = df.drop("step", axis=1)

# Initialize the app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(html.H1("Dashboard", className="text-center mb-4"), width=12)]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        sort_action="native",
                        # page_size=10,
                        filter_action="native",
                        columns=[
                            {"name": col, "id": col, "presentation": "input"}
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
                        style_header={
                            "fontWeight": "bold",
                            "whiteSpace": "normal",
                        },
                        style_data_conditional=[
                            {
                                "if": {
                                    "filter_query": '{status} = "completed"',
                                    "column_id": "status",
                                },
                                "backgroundColor": "#d4edda",
                                "color": "#155724",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "unstarted"',
                                    "column_id": "status",
                                },
                                "backgroundColor": "#e0e0e0",
                                "color": "#424242",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "failed"',
                                    "column_id": "status",
                                },
                                "backgroundColor": "#f8d7da",
                                "color": "#721c24",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "running"',
                                    "column_id": "status",
                                },
                                "backgroundColor": "#d0e7ff",
                                "color": "#004085",
                            },
                            {
                                "if": {
                                    "filter_query": '{status} = "pending"',
                                    "column_id": "status",
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

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
