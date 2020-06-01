from flask import Blueprint
from flask_restful import Api, Resource, url_for
from flask_restful import reqparse
#custom imports
from flask_restful_swagger import swagger
from .aux_func import stations_summary, precipitation_summary, tobservation_summary, start_date


api_mod = Blueprint('api', __name__)
#api = Api(api_mod)
api = swagger.docs(Api(api_mod), apiVersion='1.0')

class Precipitation(Resource):
    @swagger.operation(
        notes='GET precipitations of last 12 months registries, sorted by stations',
        nickname='get',
        responseMessages=[
            {
                "code": 200,
                "message": "Precipitation of las 12 months retrieved successfuly"
            }
        ]
    )
    def get(self):
        """
        GET precipitations of last 12 months registries, sorted by stations
        """
        last_date = precipitation_summary()
        return last_date

class Station(Resource):
    @swagger.operation(
        notes="GET's Number of stations, Stations sorted by activity in descending order, and most active station",
        nickname='get',
        responseMessages=[
            {
                "code": 200,
                "message": "Detail summary of stations succesfully retreived"
            }
        ]
    )
    def get(self):
        """
        GET's Number of stations, Stations sorted by activity in 
        descending order, and most active station
        """
        station_description = stations_summary()
        return station_description

class Tobs(Resource):
    @swagger.operation(
        notes="GET's temperature observations of last 12 months registries, sorted by stations activity",
        nickname='get',
        responseMessages=[
            {
                "code": 200,
                "message": "Temperature observations of las 12 months retrieved successfuly"
            }
        ]
    )
    def get(self):
        """
        GET's temperature observations of last 12 months registries, sorted by stations activity
        """
        station_description = tobservation_summary()
        return station_description


class Start(Resource):
    @swagger.operation(
        notes="        GET's mximun temperature , minimum temperature and average temperature from start date till actual date",
        nickname='get',
        responseMessages=[
            {
                "code": 200,
                "message": "Temperature stats retreived successfuly"
            }
        ]
    )
    def get(self, *args, **kwargs):
        """
        GET's mximun temperature , minimum temperature and average temperature
        from start date till actual date
        """
        start = kwargs['start']
        no_return_summary = start_date(start)
        return no_return_summary

class StartEnd(Resource):
    @swagger.operation(
        notes=" GET's mximun temperature , minimum temperature and average temperature from start date till actual end date",
        nickname='get',
        responseMessages=[
            {
                "code": 200,
                "message": "Temperature stats retreived successfuly"
            }
        ]
    )
    def get(self, *args, **kwargs):
        """
        GET's mximun temperature , minimum temperature and average temperature
        from start date till actual end date
        """
        start = kwargs['start']
        end = kwargs['end']
        trip_summary = start_date(start, end)
        return trip_summary

api.add_resource(Precipitation, '/precipitation')
api.add_resource(Station, '/stations')
api.add_resource(Tobs, '/tobs')
api.add_resource(Start, '/<start>')
api.add_resource(StartEnd, '/<start>/<end>')
