import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship

GAME_TABLE = 'game'
USER_TABLE = 'user'
CSEQ_TABLE = 'colorsequence'

Base = declarative_base()


class User(Base):
    """
    Abstraction for a player
    """
    __tablename__ = USER_TABLE
    name = Column(String(32), nullable=False, primary_key=True)
    pass_hash = Column(String(256), nullable=False)


class ColorSequence(Base):
    """
    Any color sequence used in the game i.e. the code, or a guess
    """
    __tablename__ = CSEQ_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    colors = Column(String(4), nullable=False)
    feedback = Column(String(4), nullable=True)
    game_id = Column(Integer, ForeignKey(GAME_TABLE+'.id'))
    created = Column(DateTime, onupdate=datetime.datetime.now)


class Game(Base):
    """
    A mastermind game
    """
    __tablename__ = GAME_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    max_turns = Column(Integer, default=8)
    codemaker_id = Column(Integer, ForeignKey(USER_TABLE+'.id'))
    codebreaker_id = Column(Integer, ForeignKey(USER_TABLE + '.id'))
    codemaker = relationship("User", foreign_keys=[codemaker_id])
    codebreaker = relationship("User", foreign_keys=[codebreaker_id])
    created = Column(DateTime, onupdate=datetime.datetime.now)
    code_id = Column(Integer, ForeignKey(CSEQ_TABLE + '.id'))
    code = relationship("ColorSequence", foreign_keys=[code_id])
    guesses = relationship('ColorSequence', backref='game', lazy='dynamic')
