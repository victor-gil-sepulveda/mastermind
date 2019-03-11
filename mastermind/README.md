# Mastermind

## Requirements
1. Create game (given a user request)  
2. Return feedback given a code guess  -> or be able to play vs a human player
3. Check game historic (optional, actually is a role of the board not the codemaker)  
4. The code should be production ready  

## Checking required features
A test client is included. Given that the ```mastermind``` project is already
 in your PYTHONPATH, you can start the flask-based service with:

```bash
rm mastermind_local.db ; python -m mastermind.service.main
```
It will be listening at ```localhost:5000```.  

Then you can run the client with:
```bash
rm mastermind_local.db
python -m mastermind.show_required_features
```
And check the results printed in the console.

**About the 4th requirement:** The service uses an sqlite database. As it is using sqlalchemy, the db can
be easily changed by a postgre db, for instance, without any hassle. 

## Notes and criticisms

These are some random thoughts about the decissions taken.

- The client will hold most of the game logic as the API basically 
handles resources.

- To improve scalability, an automatic guess creation procedure should be enqueued
and return an enqueued task (202 accepted). Then we should poll (200) until the resource 
is ready (303 or 404).

- It would be great to have more comments and docstrings, however I tried to do functions
and variable names self-explanatory.
 
- The show_required_features is simulating a client in order to show how the REST 
api can be sed in order to fulfil the requirements. Errors are not handled.

- Depending on the philosophy of resource representation, we could use only resource uris
or resource uris with the data. I have decided to use the first approach but give 
an optional keyword that will expand the resource data.

- The project could be improved a lot by refactoring in order to not repeat so much code.

- Board and Game are modelled as the same entity, they can be modelled as different entities.

- It would come quite handy to create the game with its game code; this avoids the need of 
patching it later. Same for the game_id of a guess.

- Each game has a code, instead of a code relating to a game. As there should
be more guesses than simple codes (or games), we will save some space (
a very small amount of space, but it was funny to make the model a bit more complex!).

- Some missing REST "verbs". 

- Test coverage can be better. "Operation" functions are tested
 by the REST endpoint tests using them.
 
- When using a resource uri as parameter for a REST endpoint, it gets parsed. In order
to get the info, one should access the resource via REST.

- URIs are hardcoded, they could be defined inside each endpoint class.

- Endpoints return raw exceptions as error messages. They should return 
more understandable messages.

- **Sometimes we do not return uris, but ids (like when we are returning the game).
The serialization method should be changed in order to improve this.**

## Dependencies
The project has been coded in python 2.7 and has the following dependencies:  

* flask
* flask_api
* flask_restful
* sqlalchemy
* marshmallow
* webargs
* requests
