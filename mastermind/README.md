# Mastermind

## Requirements
* Create game (given a user request)  
* Return feedback given a code guess  
* Check game historic (optional, actually is a role of the board not the codemaker)  
* The code should be production ready  

## Notes and critics

### Model
Board and Game are modelled as the same entity.

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

