# Mastermind

## Requirements
* Create game (given a user request)  
* Return feedback given a code guess  -> or be able to play vs a human player
* Check game historic (optional, actually is a role of the board not the codemaker)  
* The code should be production ready  

## Notes and critics

### Model
The client will hold most of the logic.

To improve scalability, an automatic guess creation procedure should be enqueued
and return an enqueued task (202 accepted). Then we should poll (200) until the resource 
is ready (303 or 404).

It would be great to have more comments and docstrings, however I tried to do functions
and variable names self-explanatory.
 
The show_required_features is simulating a client in order to show how the REST 
api can be sed in order to fulfil the requirements. Errors are not handled.

Depending on the philosophy of resource representation, we could use only resource uris
or resource uris with the data. I have decided to use the first approach but give 
an optional keyword that will expand the resource data.

Requires a lot of refactoring in order to not repeat so much code.

Board and Game are modelled as the same entity.

It would come quite handy to create the game with its code, avoids patching. Same for 
the game_id of a guess.

Each game has a code, instead of a code relating to a game. As there should
be more guesses than simple codes (or games), we will save some space (
a very small amount of space, but it was funny to make the model a bit more complex!).

Make optional: adding game id to guess.

Some missing REST "verbs". Test coverage can be better. "Operation" functions are tested
 by the REST endpoint tests using them.
 
When using a resource uri as parameter for a REST endpoint, it gets parsed. In order
to get the info, one should access the resource via REST.

URIs are hardcoded, they can be part of a class.

### Errors
Endpoints return raw exceptions as error messages. They should return 
more understandable messages.

### Dependencies

flask
flask_api
flask_restful
sqlalchemy
marshmallow
webargs
requests
