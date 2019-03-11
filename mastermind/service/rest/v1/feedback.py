from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from mastermind.model.operations import create_feedback, get_feedback_data
from mastermind.model.sessionsingleton import DbSessionHolder


class Feedback(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new code, that will be added to a guess or a game.
        """

        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            feedback_id = create_feedback(session,
                                          json_data["colors"])
            json_data["id"] = feedback_id
            response = make_response(jsonify(json_data),
                                     status.HTTP_201_CREATED)
            response.headers["location"] = "/feedback/{feedback_id}".format(feedback_id=feedback_id)
            response.autocorrect_location_header = False
            return response

        except KeyError, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            session.rollback() # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, feedback_id):
        """
        Obtains a feedback from the database.
        """
        session = DbSessionHolder().get_session()

        try:
            feedback_json = get_feedback_data(session, feedback_id)
            response = make_response(jsonify(feedback_json),
                                     status.HTTP_201_CREATED)
            return response

        except (KeyError, IntegrityError), e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)


