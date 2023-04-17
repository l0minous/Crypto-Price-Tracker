import requests
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies={}"
CRYPTO_IDS = "bitcoin,ethereum,dogecoin"
CURRENCY = "usd"


def fetch_crypto_prices() -> pd.DataFrame:
    """
    Fetch cryptocurrency prices from the CoinGecko API and return them as a pandas DataFrame.
    
    """
    response = requests.get(COINGECKO_API_URL.format(CRYPTO_IDS, CURRENCY))
    data = response.json()
    return pd.DataFrame(data).T.reset_index().rename(columns={"index": "Crypto Coin", "usd": "Price (USD)"})


def update_dashboard() -> dbc.Table:
    """
    Updating the dashboard by fetching the latest cryptocurrency prices and formatting them as a table.

    """
    x = fetch_crypto_prices()
    table = dbc.Table.from_dataframe(x, striped=True, bordered=True, hover=True)
    return table


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        "href": "style.css",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container(
    [
        html.H1("Cryptocurrency Price Tracker", className="title"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="crypto_table", className="mt-4 card"),
                        html.Div(
                            dbc.Button("Refresh Prices", id="refresh_button", className="btn custom-button"),
                            className="d-grid mt-3",
                        ),
                    ],
                    width=6,
                    className="mx-auto",
                ),
            ],
            className="justify-content-center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("crypto_table", "children"),
    [Input("refresh_button", "n_clicks")],
)
def update_crypto_table(n_clicks: int) -> dbc.Table:
    """
    Update the cryptocurrency table in the dashboard.
    
    where n_clicks is the number of times the refresh button has been clicked.
    
    """
    if n_clicks is None:
        return update_dashboard()
    return update_dashboard()


if __name__ == "__main__":
    app.run_server(debug=True)
