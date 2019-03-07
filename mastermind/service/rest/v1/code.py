from flask import jsonify, make_response, request
from flask_api import status
from flask_restful import Resource

from mastermind.model.operations import create_code
from mastermind.model.sessionsingleton import DbSessionHolder


class Code(Resource):

    def __init__(self):
        pass

    def post(self):
        """
        Creates a new code, that will be added to a guess or a game.
        """

        json_data = request.get_json(force=True)
        session = DbSessionHolder().get_session()

        try:
            code_id = create_code(session,
                                  json_data["colors"])
            response = make_response(jsonify(json_data),
                                     status.HTTP_201_CREATED)
            response.headers["location"] = "/code/{code_id}".format(code_id=code_id)
            response.autocorrect_location_header = False
            return response

        except KeyError, e:
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            session.rollback() # just in case
            return make_response(jsonify({"error": str(e)}),
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
