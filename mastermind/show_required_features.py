"""
Requirements:

* Create game (given a user request)
* Check game historic (optional, actually is a role of the board not the codemaker)
* Return feedback given a code guess
"""
import json
import random
import requests


def get_complete_endpoint(endpoint):
    complete_endpoint = "http://127.0.0.1:5000/mastermind/v1/{endpoint}".format(endpoint=endpoint)
    return complete_endpoint


if __name__ == "__main__":

    # First prepare the db

    # We create a generic user: mastermind
    # This will be the codemaker when we play against the computer
    mm_user_resp = requests.post(get_complete_endpoint("user"), data=json.dumps({
        "name": "mastermind",
        "pass_hash": "*"
    }))
    mm_user_uri = mm_user_resp.headers["location"]

    # We create one player
    john_user_resp = requests.post(get_complete_endpoint("user"), data=json.dumps({
        "name": "John",
        "pass_hash": "7C9E7C1494B2684AB7C19D6AFF737E460FA9E98D5A234DA1310C97DDF5691834"
    }))
    john_user_uri = john_user_resp.headers["location"]

    # Then we create a game for player vs machine
    game_resp = requests.post(get_complete_endpoint("game"), data=json.dumps({
        "codemaker_uri": mm_user_uri,
        "codebreaker_uri": john_user_uri,
        "max_moves": 8
    }))
    game_uri = game_resp.headers["location"]

    # The user adds a code (in this case the code should be added automatically
    # by the system).
    #***********************************
    # Create game (given a user request)
    #***********************************
    game_code_resp = requests.post(get_complete_endpoint("code"), data=json.dumps({
        "colors": ''.join(random.choice(['1', '2', '3', '4', '_']) for _ in range(4))
    }))
    game_code_uri = game_code_resp.headers["location"]
    #***********************************

    # Then add the code to the game (patching)

    # We can start making some guesses
    for _ in range(8):
        # Create a new guess code
        guess_code_resp = requests.post(get_complete_endpoint("code"), data=json.dumps({
            "colors": ''.join(random.choice(['1', '2', '3', '4', '_']) for _ in range(4))
        }))
        guess_code_uri = guess_code_resp.headers["location"]

        # ***********************************
        # Return feedback given a code guess
        # ***********************************
        # Create the guess itself
        guess_resp = requests.post(get_complete_endpoint("guess"), data=json.dumps({
            "code_uri": guess_code_uri,
            "game_code_uri": game_code_uri
        }))
        guess_uri = guess_resp.headers["location"]
        # ***********************************

        # Get the ids
        guess_data = json.loads(guess_code_resp.data)
        code_id, feedback_id = guess_data["id"]["code_id"], guess_data["id"]["feedback_id"]

        # Patch with the game uri. TODO: Option to create with known game_id
        guess_uri = "/guess?code_id={code_id}&feedback_id={feedback_id}".format(
            code_id=code_id,
            feedback_id=feedback_id
        )
        guess_resp = requests.patch(get_complete_endpoint(guess_uri), data=json.dumps({
            "game_uri": game_uri
        }))

    # ***********************************
    # Check game historic
    # ***********************************
    # Get the game, print the board (we can use the extend option in order to get all the data of guesses).
    game_resp = requests.get(get_complete_endpoint(game_uri))
    # Print the resources
    guesses = json.loads(game_resp.data)["guesses"]
    for guess_uri in guesses:
        print guess_uri
        # Get the guess, expand the resources inside
        board_guess_resp = requests.patch(get_complete_endpoint(guess_uri+"&expand_resources=true"), data=json.dumps({
            "game_uri": game_uri
        }))
        print json.loads(board_guess_resp.data)
