import inspect
import json
import os
import unittest
import os.path
import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import mastermind.model.test as test_module
from mastermind.model.model import Base, User, Game, Code, Guess, Feedback
from mastermind.model.schemas import UserSchema, GameSchema


class TestModel(unittest.TestCase):
    TEST_DB = 'test_mm_model.db'

    @classmethod
    def setUpClass(cls):
        # get test data folder
        cls.data_folder = os.path.join(os.path.dirname(inspect.getfile(test_module)), "data")

    def setUp(self):
        # Populate the DB
        if os.path.exists(TestModel.TEST_DB):
            os.remove(TestModel.TEST_DB)
        engine = create_engine('sqlite:///'+TestModel.TEST_DB)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        ## Users
        john = User(name="john", pass_hash="96D9632F363564CC3032521409CF22A852F2032EEC099ED5967C0D000CEC607A")
        susan = User(name="susan", pass_hash="B78469618FB15871B9508DEFD1FF70014747C1F918E4185425C5F2BBEA2A4E5D")

        ## A game
        test_game = Game(codemaker=susan, codebreaker=john, max_moves=8,
                         code=Code(colors="1134", created=datetime.datetime.strptime('24052010', "%d%m%Y").date()),
                         guesses=[Guess(code=Code(colors="2324", created=datetime.datetime.strptime('24052010', "%d%m%Y").date()),
                                        feedback=Feedback(colors="1___", created=datetime.datetime.strptime('24052010', "%d%m%Y").date())),
                                  Guess(code=Code(colors="1233", created=datetime.datetime.strptime('24052010', "%d%m%Y").date()),
                                        feedback=Feedback(colors="22__", created=datetime.datetime.strptime('24052010', "%d%m%Y").date()))],
                         created=datetime.datetime.strptime('24052010', "%d%m%Y").date())

        ## Some lines for the game
        session.add_all([
            john, susan,
            test_game
        ])

        session.commit()

        self.session = session

    def test_model_loaded(self):
        data = []

        user_schema = UserSchema()
        for b in self.session.query(User).all():
            data.append(user_schema.dump(b).data)

        game_schema = GameSchema()
        for g in self.session.query(Game).all():
            data.append(game_schema.dump(g).data)

        # fp = open(os.path.join(self.data_folder, "loaded_data.json"), "w")
        # json.dump(data, fp=fp, indent=4, sort_keys=True)

        fp = open(os.path.join(self.data_folder, "loaded_data.json"), "r")
        expected = json.load(fp)
        self.maxDiff = None
        self.assertItemsEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
