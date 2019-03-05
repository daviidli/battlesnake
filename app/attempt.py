import numpy as np
from enum import Enum


class Dir(Enum):
    UP = {"i": 0, "dir": "up", "opposite": "down"}
    DOWN = {"i": 1, "dir": "down", "opposite": "up"}
    LEFT = {"i": 2, "dir": "left", "opposite": "right"}
    RIGHT = {"i": 3, "dir": "right", "opposite": "left"}


class Snake:
    def __init__(self, name, body, width, height, health):
        self.name = name
        self.health = 100
        self.head = body[0]
        self.tail = body[len(body)]
        self.length = len(body)
        self.body_board = np.zeros((width, height))
        self.body_arr = body
        self.is_dead = False

        for b in body:
            self.body_board[b["x"]][b["y"]] = 1

    def load(self, body):
        if len(self.body_arr) == len(body):
            self.body_board[self.tail["x"]][self.tail["y"]] = 0
        self.body_board[body[0]["x"]][body[0]["y"]] = 1

        self.head = body[0]
        self.tail = body[len(body)]
        self.length = len(body)
        self.body_arr = body

    def update(self, body, health):
        if self.is_dead:
            return

        if len(body) == 0 or health == 0:
            self.is_dead = True
            self.body_board *= 0
            self.body_arr = []
            self.length = 0

        self.load(body)


class A:
    def __init__(self, me, height, width, enemies):
        self.height = height
        self.width = width
        self.food_board = None
        self.enemy_board = np.zeros((width, height))
        self.me = Snake("me", me["body"], width, height, 100)
        self.me_board = self.me.body_board
        self.enemies = []

        for e in enemies:
            enemy = Snake(e["name"], e["body"], width, height, 100)
            self.enemies.append(enemy)
            self.enemy_board += enemy

    def update(self, food, enemies, me):
        for i in range(len(enemies)):
            if enemies[i]["name"] == self.enemies[i].name:
                self.enemies[i].update(enemies[i]["body"], enemies[i]["health"])

        self.enemy_board = np.zeros((self.width, self.height))
        for e in self.enemies:
            self.enemy_board += e.body_board

        self.food_board = np.zeros((self.width, self.height))
        for f in food:
            self.food_board[f["x"]][f["y"]] = 1

        self.me.update(me["body"], me["health"])

    def find_facing(self):
        next_body = self.me.body_arr[1]
        if self.me.head["x"] == next_body["x"]:
            if self.me.head["y"] + 1 == next_body["y"]:
                return Dir.UP
            else:
                return Dir.DOWN
        else:
            if self.me.head["x"] + 1 == next_body["x"]:
                return Dir.LEFT
            else:
                return Dir.RIGHT

    def find_direction(self):
        facing = self.find_facing()

        # [up, down, left, right]
        dir_values = [0, 0, 0, 0]

        at_edge_points = 10000
        close_edge_points = 10
        enemy_points = 5
        food_points = -15
        hungry_food_points = -50
        me_points = 5

        head = self.me.head

        if head["x"] == 0:
            dir_values[Dir.LEFT["i"]] += at_edge_points
        if head["x"] == self.width - 1:
            dir_values[Dir.RIGHT["i"]] += at_edge_points
        if head["y"] == 0:
            dir_values[Dir.UP["i"]] += at_edge_points
        if head["y"] == self.width - 1:
            dir_values[Dir.DOWN["i"]] += at_edge_points




