import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

# Load API key from configuration file
load_dotenv()
api_key = os.getenv("EIA_API_KEY")

def build_url(route):
    return f"https://api.eia.gov/v2/{route}?api_key={api_key}"

gas_route = "natural-gas/pri/sum/data"
electricity_route = "electricity/retail-sales/data"

gas_url = build_url(gas_route)
electricity_url = build_url(electricity_route)

# Make sure all required variables are listed here

def build_headers(data):
    return {
        "X-Params": json.dumps(data),
    }

gas_data = {
    "frequency": "monthly",
    "data": ["value"],
    "facets": {"process": ["PIN"]},
    "start": "2020-01",
    "end": "2023-12",
    "sort": [{"column": "period", "direction": "asc"}],
    "offset": 0,
    "length": 5000
}


electricity_data = {
    "frequency": "monthly",
    "data": ["price"],
    "facets": {"sectorid": ["ALL"]},
    "start": "2020-01",
    "end": "2023-12",
    "sort": [{"column": "period", "direction": "asc"}],
    "offset": 0,
    "length": 5000
}

gas_headers = build_headers(gas_data)
electricity_headers = build_headers(electricity_data)

# Request the data
gas_response = requests.get(gas_url, headers=gas_headers).json()
gas = pd.json_normalize(gas_response["response"]["data"])

electricity_response = requests.get(electricity_url, headers=electricity_headers).json()
electricity = pd.json_normalize(electricity_response["response"]["data"])

# Data processing into DataFrames

gas_data = {
    "period": pd.to_datetime(gas["period"], format="%Y-%m"),
    "value $/MCF": pd.to_numeric(gas["value"]),
}

electricity_data = {
    "period": pd.to_datetime(electricity["period"], format="%Y-%m"),
    "price ¢/kWh": pd.to_numeric(electricity["price"]),
}

gas_df = pd.DataFrame(data = gas_data)
electricity_df = pd.DataFrame(data = electricity_data)

# Grouping data by period and calculating mean

gas_mean_price = gas_df.groupby("period").mean()
gas_mean_price.to_csv("../data/processed/gas_prices.csv", index = True)

electricity_mean_price = electricity_df.groupby("period").mean()
electricity_mean_price.to_csv("../data/processed/electricity_prices.csv", index = True)