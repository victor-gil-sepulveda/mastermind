from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from mastermind.model.operations import create_guess, add_game_id_to_guess, create_guess_with_auto_feedback, get_guess
from mastermind.model.sessionsingleton import DbSessionHolder
from webargs import fields
from webargs.flaskparser import use_args

patch_args = {
    "code_id": fields.Int(required=True),
    "feedback_id": fields.Int(required=True),
    "expand_resources": fields.Bool(missing=False, required=False)
}

get_args = {
    "code_id": fields.Int(required=True),
    "feedback_id": fields.Int(required=True),
    "expand_resources": fields.Bool(missing=False, required=False)
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
            if "game_code_uri" in json_data:
                code_id, feedback_id = create_guess_with_auto_feedback(session,
                                                                       json_data["code_uri"],
                                                                       json_data["game_code_uri"])
                del json_data["game_code_uri"]
                json_data["feedback_uri"] = "feedback/{feedback_id}".format(feedback_id=feedback_id)
            else:
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
            session.rollback()  # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

    @use_args(patch_args)
    def patch(self, args):
        code_id = int(args["code_id"])
        feedback_id = int(args["feedback_id"])
        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            if "game_id" in json_data:
                new_guess = add_game_id_to_guess(session, code_id, feedback_id, int(json_data["game_id"]), args["expand_resources"])
                response = make_response(jsonify(new_guess), status.HTTP_200_OK)
                response.headers["location"] = "/guess?code_id={code_id}&feedback_id={feedback_id}".format(
                    code_id=code_id,
                    feedback_id=feedback_id)
                response.autocorrect_location_header = False
                return response
        except Exception, e:
            session.rollback() # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

    @use_args(get_args)
    def get(self, args):
        code_id = int(args["code_id"])
        feedback_id = int(args["feedback_id"])

        session = DbSessionHolder().get_session()

        try:
                guess = get_guess(session, code_id, feedback_id, args["expand_resources"])
                response = make_response(jsonify(guess), status.HTTP_200_OK)

                return response

        except IntegrityError, e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_409_CONFLICT)

        except Exception, e:
            session.rollback()  # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

