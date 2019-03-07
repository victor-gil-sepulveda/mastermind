from mastermind.model.model import Game, User
from mastermind.model.sessionsingleton import DbSessionHolder


def create_user(user_name, user_pass_hash):
    """
    Inserts a new user/player in the DB.
    """
    # Perform the db job
    session = DbSessionHolder().get_session()
    user = User(name=user_name, pass_hash=user_pass_hash)
    session.add(user)
    session.commit()


def create_game(codemaker_uri, codebreaker_uri, max_moves):
    """
    Creates a new game in the database.
    """

    # Get codemaker and codebreaker ids, in this case we prefer
    # to parse the string. We can instead do a couple of get requests
    # instead
    codemaker_id = int(codemaker_uri.split("/")[-1])
    codebreaker_id = int(codebreaker_uri.split("/")[-1])

    # Perform the db job
    session = DbSessionHolder().get_session()
    game = Game(codemaker_id=codemaker_id, codebreaker_id=codebreaker_id, max_moves=max_moves)
    session.add(game)
    session.flush()
    game_id = game.id
    session.commit()

    # And return the id
    return game_id

