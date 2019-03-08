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
        DbSessionHolder(TestV1API.REST_TEST_DB).reset()

    def test_user_creation(self):
        endpoint = gen_resource_url(API_PREFIX, v1, "user")

        # Adding a new user returns 201
        response = self.client().post(endpoint, data=json.dumps({
            "name": "susan",
            "pass_hash": "1111"
        }))

        self.assertEqual(status.HTTP_201_CREATED, parse_status(response.status))
        self.assertEqual("/user/susan", response.location)
        self.assertDictEqual({"name": "susan", "pass_hash": "1111"}, json.loads(response.data))

        # Adding a user with an already stored username is not allowed
        response = self.client().post(endpoint, data=json.dumps({
            "name": "susan",
            "pass_hash": "213124"
        }))
        self.assertEqual(status.HTTP_409_CONFLICT, parse_status(response.status))

    def test_code_creation(self):
        endpoint = gen_resource_url(API_PREFIX, v1, "code")

        # Adding a new code returns 201
        response = self.client().post(endpoint, data=json.dumps({
            "colors": "____"
        }))

        self.assertEqual(status.HTTP_201_CREATED, parse_status(response.status))
        # this is the first one introduced and has id = 1
        self.assertEqual("/code/1", response.location)
        self.assertDictEqual({"id": 1, "colors": "____"}, json.loads(response.data))

    def test_feedback_creation(self):
        # repeated code ahead
        endpoint = gen_resource_url(API_PREFIX, v1, "feedback")

        # Adding a new code returns 201
        response = self.client().post(endpoint, data=json.dumps({
            "colors": "____"
        }))

        print str(response)
        print response.data
        self.assertEqual(status.HTTP_201_CREATED, parse_status(response.status))
        # this is the first one introduced and has id = 1
        self.assertEqual("/feedback/1", response.location)
        self.assertDictEqual({"id": 1, "colors": "____"}, json.loads(response.data))

if __name__ == "__main__":
    unittest.main()
