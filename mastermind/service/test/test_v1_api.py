import unittest
from flask.app import Flask
import json
from mastermind.model.sessionsingleton import DbSessionHolder
from mastermind.service.rest.api import setup_rest_api, API_PREFIX, gen_resource_url
import mastermind.service.rest.v1 as v1
from flask_api import status
import random
import string

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

        self.assertEqual(status.HTTP_201_CREATED, parse_status(response.status))
        # this is the first one introduced and has id = 1
        self.assertEqual("/feedback/1", response.location)
        self.assertDictEqual({"id": 1, "colors": "____"}, json.loads(response.data))

    def test_guess_creation(self):
        # repeated code ahead
        endpoint = gen_resource_url(API_PREFIX, v1, "code")
        code_response = self.client().post(endpoint, data=json.dumps({
            "colors": "____"
        }))

        endpoint = gen_resource_url(API_PREFIX, v1, "feedback")
        fb_response = self.client().post(endpoint, data=json.dumps({
            "colors": "XXXX"
        }))

        endpoint = gen_resource_url(API_PREFIX, v1, "guess")
        response = self.client().post(endpoint, data=json.dumps({
            "code_uri": code_response.location,
            "feedback_uri": fb_response.location
        }))

        expected = {
            "code_uri": "/code/1",
            "feedback_uri": "/feedback/1",
            "id": {
                "code_id": 1,
                "feedback_id": 1
            }
        }
        self.assertEqual("/guess?code_id=1&feedback_id=1", response.location)
        self.assertDictEqual(expected, json.loads(response.data))

    def test_guess_auto_creation(self):
        endpoint = gen_resource_url(API_PREFIX, v1, "code")
        game_code_response = self.client().post(endpoint, data=json.dumps({
            "colors": "1234"
        }))
        code_response = self.client().post(endpoint, data=json.dumps({
            "colors": "4___"
        }))

        endpoint = gen_resource_url(API_PREFIX, v1, "guess")
        response = self.client().post(endpoint, data=json.dumps({
            "code_uri": code_response.location,
            "game_code_uri": game_code_response.location
        }))

        # Get the colors of the feedback
        feedback_id = json.loads(response.data)["id"]["feedback_id"]
        endpoint = gen_resource_url(API_PREFIX, v1, "feedback/{feedback_id}".format(feedback_id=feedback_id))
        response = self.client().get(endpoint)
        self.assertEqual("1___", json.loads(response.data)["colors"])

    def create_a_game(self):
        # Create the players
        endpoint = gen_resource_url(API_PREFIX, v1, "user")
        susan_response = self.client().post(endpoint, data=json.dumps({
            "name": "susan",
            "pass_hash": "111111"
        }))
        john_response = self.client().post(endpoint, data=json.dumps({
            "name": "john",
            "pass_hash": "22222"
        }))

        # Create the game with default max_moves
        endpoint = gen_resource_url(API_PREFIX, v1, "game")
        response = self.client().post(endpoint, data=json.dumps({
            "codemaker_uri": susan_response.location,
            "codebreaker_uri": john_response.location
        }))
        return susan_response, john_response, response

    def test_game_creation(self):
        susan_response, john_response, response = self.create_a_game()

        expected = {
            "id": 1,
            "codebreaker_uri": "/user/john",
            "codemaker_uri": "/user/susan",
            "max_moves": 8
        }

        self.assertEqual("/game/1", response.location)
        self.assertDictEqual(expected, json.loads(response.data))

        # Defining max_moves ...
        endpoint = gen_resource_url(API_PREFIX, v1, "game")
        response = self.client().post(endpoint, data=json.dumps({
            "codemaker_uri": susan_response.location,
            "codebreaker_uri": john_response.location,
            "max_moves": 10
        }))
        self.assertEqual(10, json.loads(response.data)["max_moves"])

        # Incorrect max_moves must return a bad request
        response = self.client().post(endpoint, data=json.dumps({
            "codemaker_uri": susan_response.location,
            "codebreaker_uri": john_response.location,
            "max_moves": 33
        }))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, parse_status(response.status))

    def test_patch_game_code(self):
        susan_response, john_response, game_response = self.create_a_game()

        code_endpoint = gen_resource_url(API_PREFIX, v1, "code")
        code_response = self.client().post(code_endpoint, data=json.dumps({
            "colors": ''.join(random.choice(string.lowercase) for _ in range(4))
        }))
        game_endpoint = gen_resource_url(API_PREFIX, v1, game_response.location[1:])
        new_game_response = self.client().patch(game_endpoint, data=json.dumps({
            "game_code_uri": code_response.location
        }))
        self.assertEqual('code/1', json.loads(new_game_response.data)["code"])

    def create_random_guess(self):
        # repeated code ahead
        # Create the code
        endpoint = gen_resource_url(API_PREFIX, v1, "code")
        code_response = self.client().post(endpoint, data=json.dumps({
            "colors": ''.join(random.choice(string.lowercase) for _ in range(4))
        }))

        # Create the feedback
        endpoint = gen_resource_url(API_PREFIX, v1, "feedback")
        fb_response = self.client().post(endpoint, data=json.dumps({
            "colors": ''.join(random.choice(string.lowercase) for _ in range(4))
        }))

        # And now create the guess!
        endpoint = gen_resource_url(API_PREFIX, v1, "guess")
        self.client().post(endpoint, data=json.dumps({
            "code_uri": code_response.location,
            "feedback_uri": fb_response.location
        }))

        return int(json.loads(code_response.data)["id"]), int(json.loads(fb_response.data)["id"])

    def test_get_guess(self):
        code_id, feedback_id = self.create_random_guess()
        endpoint = gen_resource_url(API_PREFIX, v1, "guess?code_id={code_id}&feedback_id={feedback_id}&expand_resources=false".format(
            code_id=code_id,
            feedback_id=feedback_id
        ))

        response = self.client().get(endpoint)
        expected = {
            "code": "code/1",
            "feedback": "feedback/1",
            "game": None
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_patch_guess(self):
        susan_response, john_response, game_response = self.create_a_game()
        game_id = json.loads(game_response.data)["id"]
        code_id, feedback_id = self.create_random_guess()
        endpoint = gen_resource_url(API_PREFIX, v1, "guess?code_id={code_id}&feedback_id={feedback_id}&expand_resources=false".format(
            code_id=code_id,
            feedback_id=feedback_id
        ))
        response = self.client().patch(endpoint, data=json.dumps({
            "game_id": game_id
        }))
        self.assertTrue("game" in json.loads(response.data))
        self.assertEqual("game/1", json.loads(response.data)["game"])

    def add_random_guess_to_game(self, game_id):
        code_id, feedback_id = self.create_random_guess()

        # Finally add the guess to the game
        endpoint = gen_resource_url(API_PREFIX, v1, "guess?code_id={code_id}&feedback_id={feedback_id}".format(
            code_id=code_id,
            feedback_id=feedback_id
        ))
        self.client().patch(endpoint, data=json.dumps({
            "game_id": game_id
        }))

    def test_get_game(self):
        susan_response, john_response, game_response = self.create_a_game()
        endpoint = gen_resource_url(API_PREFIX, v1, game_response.location[1:]) # remove the first "/" from location
        response = self.client().get(endpoint)
        expected = {
            "code": None,
            "codebreaker": "john",
            "codemaker": "susan",
            "guesses": [],
            "id": 1,
            "max_moves": 8
        }
        json_response = json.loads(response.data)
        game_id = json.loads(response.data)["id"]
        del json_response["created"] # The creation date will be always different to the golden data one
        self.assertDictEqual(expected, json_response)

        # If the game does not exist we get an error
        endpoint = gen_resource_url(API_PREFIX, v1, "game/-1")
        response = self.client().get(endpoint)
        self.assertEqual(status.HTTP_404_NOT_FOUND, parse_status(response.status))

        # If the game has some guesses and code, we also get them
        for _ in range(5):
            self.add_random_guess_to_game(game_id)
        endpoint = gen_resource_url(API_PREFIX, v1, game_response.location[1:])  # remove the first "/" from location
        response = self.client().get(endpoint)
        expected = {
            "id": 1,
            "code": None,
            "max_moves": 8,
            "codebreaker": "john",
            "codemaker": "susan",
            "guesses": [
                "/guess?code_id=1&feedback_id=1",
                "/guess?code_id=2&feedback_id=2",
                "/guess?code_id=3&feedback_id=3",
                "/guess?code_id=4&feedback_id=4",
                "/guess?code_id=5&feedback_id=5"]
        }

        json_response = json.loads(response.data)
        del json_response["created"]
        self.assertDictEqual(expected, json_response)


if __name__ == "__main__":
    unittest.main()
