import os
import unittest
from flask.app import Flask
import json
from mastermind.model.sessionsingleton import DbSessionHolder
from mastermind.service.rest.api import setup_rest_api, API_PREFIX, gen_resource_url
import mastermind.service.rest.v1 as v1
from flask_api import status

from mastermind.service.rest.tools import parse_status


class TestV1API(unittest.TestCase):

    REST_TEST_DB = "mastermind_rest_api_test.db"

    def setUp(self):
        app = Flask(__name__)
        app.testing = True
        app.config["TESTING"] = True

        setup_rest_api(app)
        self.client = app.test_client

        # Init db
        if os.path.exists(TestV1API.REST_TEST_DB):
            os.remove(TestV1API.REST_TEST_DB)
        DbSessionHolder(TestV1API.REST_TEST_DB)

    def test_user_created(self):
        endpoint = gen_resource_url(API_PREFIX, v1, "user")

        # Adding a user returns 200 and the user
        response = self.client().post(endpoint, data=json.dumps({
            "name": "susan",
            "pass_hash": "1111"
        }))

        self.assertEqual(status.HTTP_201_CREATED, parse_status(response.status))
        self.assertEqual("/user/susan", response.location)
        self.assertDictEqual({"name": "susan", "pass_hash": "1111"}, json.loads(response.data))

if __name__ == "__main__":
    unittest.main()
