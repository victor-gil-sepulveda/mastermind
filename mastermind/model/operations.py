from mastermind.model.model import Game, User, Code


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
    return session, code_id


def create_game(session, codemaker_uri, codebreaker_uri, max_moves):
    """
    Creates a new game in the database.
    """

    # Get codemaker and codebreaker ids, in this case we prefer
    # to parse the string. We can instead do a couple of get requests
    # instead
    codemaker_id = int(codemaker_uri.split("/")[-1])
    codebreaker_id = int(codebreaker_uri.split("/")[-1])

    # Perform the db job
    game = Game(codemaker_id=codemaker_id, codebreaker_id=codebreaker_id, max_moves=max_moves)
    session.add(game)
    session.flush()
    game_id = game.id
    session.commit()

    # And return the id
    return session, game_id

