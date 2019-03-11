from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from mastermind.model.operations import create_game, get_game
from mastermind.model.sessionsingleton import DbSessionHolder
from webargs import fields
from flask import request
from webargs.flaskparser import parser

get_args = {
    "expand_resources": fields.Bool(missing=False, required=False)
}


class Game(Resource):
    DEFAULT_MAX_MOVES = 8

    def __init__(self):
        pass

    def post(self):
        """
        Creates a game. This is a fast operation and returns 201 directly.

        Ex:
        curl -i -X POST -H "Content-Type: application/json" --data '{"codemaker_uri":"sth/1", "codebreaker_uri":"sth/2", "max_moves": 3}' http://127.0.0.1:5000/mastermind/v1/game
        """
        json_data = request.get_json(force=True)

        session = DbSessionHolder().get_session()
        # Default value
        if "max_moves" not in json_data:
            json_data["max_moves"] = Game.DEFAULT_MAX_MOVES

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

    def get(self, game_id):
        """
        Obtains a game from the database
        """
        session = DbSessionHolder().get_session()

        args = parser.parse(get_args, request)

        if game_id is None:
            return make_response(jsonify({"error": "You need to specify the game ID."}),
                                 status.HTTP_400_BAD_REQUEST)
        try:
            game_data = get_game(session, game_id, args["expand_resources"])
            if game_data is None:
                return make_response(jsonify({"error": "Game not found."}),
                                     status.HTTP_404_NOT_FOUND)

            return make_response(jsonify(game_data),
                                 status.HTTP_200_OK)

        except Exception, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
