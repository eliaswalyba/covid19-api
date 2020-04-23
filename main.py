import requests, json, pandas as pd
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from bs4 import BeautifulSoup as BS
from fetcher import get_data, format_df


flask_app = Flask(__name__)
app = Api(
    app = flask_app,
    doc="/covid19/api/v1.0/",
	version = "1.0", 
	title = "COVID19 REST API", 
	description = "All the #COVID19 data you need to create remarkable dashboards or do very detailed analyzes."
)

model = app.model('Name Model', {
    'name': fields.String(
        required = False, 
        description="Name of a country", 
        help="Name cannot be blank."
    )
})

countries_namespace = app.namespace('countries', description='data from all countries or from a specific country')
world_namespace = app.namespace('world', description='worldwide global aggregated data')

@countries_namespace.route(f"/")
class Countries(Resource):
    @app.doc(
        responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
    )
    def get(self):
        countries = get_data()[1]
        return format_df(countries, 'json')

@countries_namespace.route(f"/<name>")
class Country(Resource):
    @app.doc(
        responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
		params={ 'name': 'Specify the name associated with the country' }
    )
    def get(self, name):
        data = get_data()[1]
        filter_rule = data['Country,Other'].str.lower() == name.lower()
        response = format_df(data[filter_rule], 'json')
        return response

@world_namespace.route(f"/")
class World(Resource):
    @app.doc(
        responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
    )
    def get(self):
        data = get_data()[0]
        return format_df(data, 'json')