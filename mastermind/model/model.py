import datetime
import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import CheckConstraint

GAME_TABLE = 'game'
USER_TABLE = 'user'
GUESS_TABLE = 'guess'
CODE_TABLE = 'code'
FEEDBACK_TABLE = 'feedback'

Base = declarative_base()


class User(Base):
    """
    Abstraction for a player + user.
    """
    __tablename__ = USER_TABLE
    name = Column(String(32), nullable=False, primary_key=True)
    pass_hash = Column(String(256), nullable=False)


class Code(Base):
    """
    Any color sequence used in the game i.e. the code or a guess.
    Color sequences cannot be of arbitrary length in this version.
    """
    __tablename__ = CODE_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    colors = Column(String(4), nullable=False)
    created = Column(DateTime, onupdate=datetime.datetime.now)


class Feedback(Base):
    """
    The feedback of the codemaster
    """
    __tablename__ = FEEDBACK_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    colors = Column(String(4), nullable=False)
    created = Column(DateTime, onupdate=datetime.datetime.now)


class Guess(Base):
    """
    A complete guess contains a code and its feedback (it represents a move).
    """
    __tablename__ = GUESS_TABLE
    code_id = Column(Integer, ForeignKey(CODE_TABLE + '.id'), primary_key=True)
    code = relationship('Code', foreign_keys=[code_id])
    feedback_id = Column(Integer, ForeignKey(FEEDBACK_TABLE + '.id'), primary_key=True)
    feedback = relationship('Feedback', foreign_keys=[feedback_id])
    game_id = Column(Integer, ForeignKey(GAME_TABLE+'.id'))
    game = relationship("Game", foreign_keys=[game_id])


class Game(Base):
    """
    A mastermind game with its setup, players and moves.
    The score can be calculated with the number of guesses (1 point
    for the codemaker for each guess + an extra point if
    the codebreaker uses all the moves without discovering the code).
    """
    __tablename__ = GAME_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, onupdate=datetime.datetime.now)

    # The players!
    codemaker_id = Column(Integer, ForeignKey(USER_TABLE+'.name'))
    codebreaker_id = Column(Integer, ForeignKey(USER_TABLE + '.name'))
    codemaker = relationship("User", foreign_keys=[codemaker_id])
    codebreaker = relationship("User", foreign_keys=[codebreaker_id])

    # The codes and the moves
    code_id = Column(Integer, ForeignKey(CODE_TABLE + '.id'))
    code = relationship('Code', foreign_keys=[code_id])
    guesses = relationship('Guess', back_populates="game", uselist=True)

    # Setup for the game (8, 10 or 12 moves max) TODO: Add constraint
    max_moves = Column(Integer, default=8)
    __table_args__ = (CheckConstraint('max_moves == 8 or max_moves == 10 or max_moves == 12',
                                      name='correct_nr_moves'), {})
