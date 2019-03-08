from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from mastermind.model.operations import create_guess
from mastermind.model.sessionsingleton import DbSessionHolder
from webargs import fields
from webargs.flaskparser import use_args

url_args = {
    "code_id": fields.String(required=True),
    "feedback_id": fields.Int(required=True)
}


class Guess(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new code, that will be added to a guess or a game.
        """

        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            code_id, feedback_id = create_guess(session,
                                                json_data["code_uri"],
                                                json_data["feedback_uri"])
            json_data["id"] = {
                "code_id": code_id,
                "feedback_id": feedback_id
            }

            response = make_response(jsonify(json_data),
                                     status.HTTP_201_CREATED)
            response.headers["location"] = "/guess?code_id={code_id}&feedback_id={feedback_id}".format(
                code_id=code_id,
                feedback_id=feedback_id)
            response.autocorrect_location_header = False
            return response

        except IntegrityError:
            session.rollback()
            return make_response(jsonify({"error": "Code and guess were related elsewhere."}),
                                 status.HTTP_409_CONFLICT)

        except KeyError, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            session.rollback() # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

    @use_args(url_args)
    def patch(self, args):
        code_id = int(args["code_id"])
        feedback_id = int(args["feedback_id"])
        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            if "game_id" in json_data:
                pass

        except Exception, e:
            session.rollback() # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)