import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as BS

def get_data():
    response = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BS(response.content, 'lxml')
    table = soup.select('#main_table_countries_today')[0]
    countries = pd.read_html(str(table))[0]
    world = countries[countries['Country,Other'] == 'World']
    countries.drop(countries.head(1).index, inplace=True)
    countries.drop(countries.tail(1).index, inplace=True)
    return world, countries

def format_df(df, format):
    reponse = None
    if format == 'json':
        str_data = df.to_json(orient='records')
        dict_data = json.loads(str_data)
        response = {"status": "success", "payload": dict_data}
    elif format == 'csv':
        response = df.to_csv()
    elif format == 'tsv':
        response = df.to_csv(sep='\t')
    else:
        response = {
            "status": "error",
            "message": "Unknown response format. Supported formats are : JSON, CSV and TSV."
        }
    return response, 200