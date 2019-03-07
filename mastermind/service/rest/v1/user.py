from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from mastermind.model.operations import create_user


class User(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new user/player.
        """

        json_data = request.get_json(force=True)

        try:
            create_user(json_data["name"],
                        json_data["pass_hash"])
            response = make_response(jsonify(json_data),
                                     status.HTTP_201_CREATED)
            response.headers["location"] = "/user/{name}".format(name=json_data["name"])
            response.autocorrect_location_header = False
            return response
        except KeyError, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return make_response(jsonify({"error": "The name of the user is already taken :( "}),
                                 status.HTTP_409_CONFLICT)
        except Exception, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)