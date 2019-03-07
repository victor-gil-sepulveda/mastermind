from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError


class User(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new user/player.
        """
        pass