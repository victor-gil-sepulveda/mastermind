from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from mastermind.model.operations import create_user
from mastermind.model.sessionsingleton import DbSessionHolder


class User(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new user/player.

        Ex:
        curl -i -X POST -H "Content-Type: application/json" --data '{"name":"susan", "pass_hash":"1111"}' http://127.0.0.1:5000/mastermind/v1/user
        """

        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            create_user(session,
                        json_data["name"],
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
            session.rollback()
            return make_response(jsonify({"error": "The name of the user is already taken :( "}),
                                 status.HTTP_409_CONFLICT)
        except Exception, e:
            session.rollback() # jsut in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)