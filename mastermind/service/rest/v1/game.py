from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from mastermind.model.operations import create_game
from mastermind.model.sessionsingleton import DbSessionHolder


class Game(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a game. This is a fast operation and returns 201 directly.

        Ex:
        curl -X POST -H "Content-Type: application/json" --data '{"codemaker_uri":"sth/1", "codebreaker_uri":"sth/2", "max_moves": 3}' http://127.0.0.1:5000/mastermind/v1/game
        """
        json_data = request.get_json(force=True)

        session = DbSessionHolder().get_session()
        try:
            game_id = create_game(session,
                                  json_data["codemaker_uri"],
                                  json_data["codebreaker_uri"],
                                  int(json_data["max_moves"]))
            json_data["id"] = game_id

            response = make_response(jsonify(json_data),
                                     status.HTTP_201_CREATED)
            response.headers["location"] = "/game/{id}".format(id=game_id)
            response.autocorrect_location_header = False
            return response

        except (ValueError, KeyError, IntegrityError), e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

