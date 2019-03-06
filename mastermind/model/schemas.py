from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from mastermind.model.model import User, Game, Guess, Feedback, Code


class UserSchema(ModelSchema):
    class Meta:
        model = User


class CodeSchema(ModelSchema):
    class Meta:
        model = Code


class FeedbackSchema(ModelSchema):
    class Meta:
        model = Feedback


class GuessSchema(ModelSchema):
    code = fields.Nested("CodeSchema", many=False)
    feedback = fields.Nested("FeedbackSchema", many=False)

    class Meta:
        model = Guess


class GameSchema(ModelSchema):
    code = fields.Nested("CodeSchema", many=False)
    guesses = fields.Nested("GuessSchema", many=True)

    class Meta:
        model = Game
