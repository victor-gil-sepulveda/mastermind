import datetime
import enum

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


class SequenceRole(enum.IntEnum):
    CODE = 0
    GUESS = 1


class ColorSequence(Base):
    """
    Any color sequence used in the game i.e. the code, or a guess
    """
    __tablename__ = CSEQ_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    colors = Column(String(4), nullable=False)
    feedback = Column(String(4), nullable=True)
    created = Column(DateTime, onupdate=datetime.datetime.now)
    game_id = Column(Integer, ForeignKey(GAME_TABLE+'.id'))
    game = relationship("Game", foreign_keys=[game_id], uselist=True)
    role = Column(Enum(SequenceRole), nullable=False)


class Game(Base):
    """
    A mastermind game
    """
    __tablename__ = GAME_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    max_turns = Column(Integer, default=8)
    codemaker_id = Column(Integer, ForeignKey(USER_TABLE+'.name'))
    codebreaker_id = Column(Integer, ForeignKey(USER_TABLE + '.name'))
    codemaker = relationship("User", foreign_keys=[codemaker_id])
    codebreaker = relationship("User", foreign_keys=[codebreaker_id])
    created = Column(DateTime, onupdate=datetime.datetime.now)
    sequences = relationship('ColorSequence', back_populates="game", uselist=True)
