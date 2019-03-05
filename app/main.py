import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from game import initializeMap
from points import getDir


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#16A085"

    return start_response(color)


def get_facing_dir(head, nn):
    if head["x"] == nn["x"]:
        if head["y"] + 1 == nn["y"]:
            return "up"
        else:
            return "down"
    else:
        if head["x"] + 1 == nn["x"]:
            return "left"
        else:
            return "right"


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    # print(json.dumps(data))

    # directions = ['up', 'down', 'left', 'right']
    # direction = random.choice(directions)

    data_board = data["board"]
    board = initializeMap(data_board["height"], data_board["width"], data_board["food"], data_board["snakes"], data["you"])
    # print(board)

    head = data["you"]["body"][0]
    # print(head)
    mm = getDir(board, head, get_facing_dir(head, data["you"]["body"][1]))

    return move_response(mm)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
