from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from mastermind.model.model import Base


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class DbSessionHolder(Singleton):
    """
    Keeps a copy of the session maker of sqlalchemy to be used when needed.
    """
    def __init__(self, db_name):
        engine = create_engine('sqlite:///' + db_name)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def get_session(self):
        return self.Session()