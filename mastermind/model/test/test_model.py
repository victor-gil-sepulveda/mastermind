import inspect
import json
import os
import unittest
import os.path
import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from mastermind.model.model import Base, User


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

        ## Some lines for the game

        session.add_all([

        ])

        session.commit()

        self.session = session

    def test_model_loaded(self):
        data = []

        # bank_schema = BankSchema()
        # for b in self.session.query(Bank).all():
        #     data.append(bank_schema.dump(b).data)


if __name__ == '__main__':
    unittest.main()
