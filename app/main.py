import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from attempt import Snake, A


game = None
turn = -1

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

    global game
    game = A(
        data["you"],
        data["board"]["height"],
        data["board"]["width"],
        data["board"]["snakes"],
        data["board"]["food"]
    )
    # print(json.dumps(data))

    color = "#e74c3c"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    # print(json.dumps(data))
    global turn
    turn += 1
    print(turn)
    global game
    game.update(data["board"]["food"], data["board"]["snakes"], data["you"])
    d = game.find_direction()

    # directions = ['up', 'down', 'left', 'right']
    # direction = random.choice(directions)

    return move_response(d)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

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
