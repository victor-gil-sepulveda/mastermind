from mastermind.control.gamemechanics import get_feedback
from mastermind.model.model import Game, User, Code, Feedback, Guess
from mastermind.model.schemas import GameSchema, GuessSchema, FeedbackSchema


def create_user(session, user_name, user_pass_hash):
    """
    Inserts a new user/player in the DB.
    """
    # Perform the db job
    user = User(name=user_name, pass_hash=user_pass_hash)
    session.add(user)
    session.commit()
    return session


def create_code(session, colors):
    code = Code(colors=colors)
    session.add(code)
    session.flush()
    code_id = code.id
    session.commit()
    # And return the id
    return code_id


def create_feedback(session, colors):
    feedback = Feedback(colors=colors)
    session.add(feedback)
    session.flush()
    feedback_id = feedback.id
    session.commit()
    # And return the id
    return feedback_id


def create_guess(session, code_uri, feedback_uri):
    # Again, we can get the ids in a more elegant way but time is money :)
    code_id = int(code_uri.split("/")[-1])
    feedback_id = int(feedback_uri.split("/")[-1])

    # db job
    guess = Guess(code_id=code_id, feedback_id=feedback_id)
    session.add(guess)
    session.commit()

    # return the composite id
    return code_id, feedback_id


def create_guess_with_auto_feedback(session, code_uri, game_code_uri):
    code_id = int(code_uri.split("/")[-1])
    game_code_id = int(game_code_uri.split("/")[-1])
    code = session.query(Code).get(code_id)
    game_code = session.query(Code).get(game_code_id)

    # Create a feedback
    feedback_colors = get_feedback(code=game_code.colors, guess=code.colors)
    feedback_id = create_feedback(session, feedback_colors)

    # db job
    guess = Guess(code_id=code_id, feedback_id=feedback_id)
    session.add(guess)
    session.commit()

    return code_id, feedback_id


def create_game(session, codemaker_uri, codebreaker_uri, max_moves):
    """
    Creates a new game in the database.
    """

    # Get codemaker and codebreaker ids, in this case we prefer
    # to parse the string. We can instead do a couple of get requests
    # instead
    codemaker_id = codemaker_uri.split("/")[-1]
    codebreaker_id = codebreaker_uri.split("/")[-1]

    # Perform the db job
    game = Game(codemaker_id=codemaker_id, codebreaker_id=codebreaker_id, max_moves=max_moves)
    session.add(game)
    session.flush()
    game_id = game.id
    session.commit()

    # And return the id
    return game_id


def get_feedback_data(session, feedback_id):
    feedback = session.query(Feedback).get(feedback_id)
    feedback_schema = FeedbackSchema()
    feedback_json = feedback_schema.dump(feedback).data
    return feedback_json


def get_game_json(game, expand_resources):
    game_schema = GameSchema()
    game_json = game_schema.dump(game).data
    if not expand_resources:
        # Resources are already expanded, we have to get the uris from them
        # we use a TRIVIAL approach here TODO: do it using marshmallow!!!
        if game_json["code"] is not None:
            code_uri = "code/" + str(game_json["code"]["id"])
            game_json["code"] = code_uri

        guess_resources = []
        for json_guess in game_json["guesses"]:
            code_id = json_guess["code"]["id"]
            feedback_id = json_guess["feedback"]["id"]
            guess_resources.append("/guess?code_id={code_id}&feedback_id={feedback_id}".format(
                code_id=code_id,
                feedback_id=feedback_id))
        game_json["guesses"] = guess_resources
    return game_json


def get_game(session, game_id, expand_resources=False):
    game = session.query(Game).get(game_id)
    if game is None:
        return None
    return get_game_json(game, expand_resources)


def get_guess(session, code_id, feedback_id, expand_resources):
    guess = session.query(Guess).get((code_id, feedback_id))
    guess_schema = GuessSchema()
    guess_json = guess_schema.dump(guess).data
    if not expand_resources:
        # Then create the urls TODO: do it using marshmallow!!!
        code_uri = "code/{code_id}".format(code_id=guess_json["code"]["id"])
        guess_json["code"] = code_uri
        feedback_uri = "feedback/{feedback_id}".format(feedback_id=guess_json["feedback"]["id"])
        guess_json["feedback"] = feedback_uri
    return guess_json


def add_game_id_to_guess(session, code_id, feedback_id, game_id, expand_resources=False):
    guess = session.query(Guess).get((code_id, feedback_id))
    guess.game_id = game_id
    session.commit()
    guess_schema = GuessSchema()

    guess_json = guess_schema.dump(guess).data
    # Convert game id to uri
    guess_json["game"] = "game/{game_id}".format(game_id=game_id)
    if not expand_resources:
        # Then create the urls TODO: do it using marshmallow!!!
        code_uri = "code/{code_id}".format(code_id=guess_json["code"]["id"])
        guess_json["code"] = code_uri
        feedback_uri = "feedback/{feedback_id}".format(feedback_id=guess_json["feedback"]["id"])
        guess_json["feedback"] = feedback_uri
    return guess_json


def add_game_code_id_to_guess(session, game_id, game_code_uri, expand_resources):
    game_code_id = int(game_code_uri.split("/")[-1])
    game = session.query(Game).get(game_id)
    game.code_id = game_code_id
    session.commit()
    return get_game_json(game, expand_resources)
