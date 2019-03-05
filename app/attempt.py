import numpy as np
from enum import Enum


class Dir(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


class Snake:
    def __init__(self, name, body, width, height, health):
        self.name = name
        self.health = 100
        self.head = body[0]
        self.tail = body[len(body) - 1]
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
        self.tail = body[len(body) - 1]
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
    def __init__(self, me, height, width, enemies, food):
        self.height = height
        self.width = width
        self.food = food
        self.enemy_board = np.zeros((height, width))
        self.me = Snake("me", me["body"], width, height, 100)
        self.me_board = self.me.body_board
        self.enemies = []
        self.closest_food = self.find_closest_food()

        for e in enemies:
            enemy = Snake(e["name"], e["body"], width, height, 100)
            self.enemies.append(enemy)
            self.enemy_board += enemy.body_board

    def find_closest_food(self):
        x = self.me.head["x"]
        y = self.me.head["y"]

        closest = {"x": self.width, "y": self.height, "n": 100}
        for f in self.food:
            a = abs(f["x"] - x) + abs(f["y"] - y)
            if a < closest["n"]:
                closest["n"] = a
                closest["x"] = f["x"]
                closest["y"] = f["y"]

        return closest

    def update(self, food, enemies, me):
        for i in range(len(enemies)):
            if enemies[i]["name"] == self.enemies[i].name:
                self.enemies[i].update(enemies[i]["body"], enemies[i]["health"])

        self.enemy_board = np.zeros((self.width, self.height))
        for e in self.enemies:
            self.enemy_board += e.body_board

        self.food = food
        self.closest_food = self.find_closest_food()
        print(self.closest_food)

        self.me.update(me["body"], me["health"])

    def find_facing(self):
        next_body = self.me.body_arr[1]
        if self.me.head["x"] == next_body["x"]:
            if self.me.head["y"] + 1 == next_body["y"]:
                return Dir.up
            else:
                return Dir.down
        else:
            if self.me.head["x"] + 1 == next_body["x"]:
                return Dir.left
            else:
                return Dir.right

    def find_direction(self):
        facing = self.find_facing()

        directions = [Dir.up, Dir.down, Dir.left, Dir.right]
        dir_values = [0, 0, 0, 0]

        at_edge_points = 10000
        close_edge_points = 10
        enemy_points = 8
        food_points = -1
        hungry_points = -20
        extra_hungry_points = -300
        opposite_points = 10000

        head = self.me.head
        print(head)

        if head["x"] == 0:
            dir_values[Dir.left.value] += at_edge_points
        if head["x"] == self.width - 1:
            dir_values[Dir.right.value] += at_edge_points
        if head["y"] == 0:
            dir_values[Dir.up.value] += at_edge_points
        if head["y"] == self.height - 1:
            dir_values[Dir.down.value] += at_edge_points

        if facing == Dir.up:
            dir_values[Dir.down.value] += opposite_points
        elif facing == Dir.down:
            dir_values[Dir.up.value] += opposite_points
        elif facing == Dir.left:
            dir_values[Dir.right.value] += opposite_points
        elif facing == Dir.right:
            dir_values[Dir.left.value] += opposite_points

        dir_values[Dir.up.value] += (self.height - self.me.head["y"]) * close_edge_points
        dir_values[Dir.down.value] += self.me.head["y"] * close_edge_points
        dir_values[Dir.left.value] += (self.width - self.me.head["x"]) * close_edge_points
        dir_values[Dir.right.value] += self.me.head["x"] * close_edge_points

        up_mask = self.mask(
            self.me.head["y"],
            self.me.head["x"] + 1,
            self.width - self.me.head["x"] - 1,
            self.height - self.me.head["y"] - 1,
            self.width
        )
        down_mask = np.rot90(self.mask(
            self.height - self.me.head["y"] - 1,
            self.width - self.me.head["x"],
            self.me.head["x"],
            self.me.head["y"],
            self.width
        ), 2)
        left_mask = np.rot90(self.mask(
            self.me.head["x"],
            self.height - self.me.head["y"],
            self.me.head["y"],
            self.width - self.me.head["x"] - 1,
            self.height
        ))
        right_mask = np.rot90(self.mask(
            self.width - self.me.head["x"] - 1,
            self.me.head["y"] + 1,
            self.height - self.me.head["y"] - 1,
            self.me.head["x"],
            self.height
        ), 3)

        dir_values[Dir.up.value] += \
            np.multiply(self.enemy_board, up_mask).sum() * enemy_points
        dir_values[Dir.down.value] += \
            np.multiply(self.enemy_board, down_mask).sum() * enemy_points
        dir_values[Dir.left.value] += \
            np.multiply(self.enemy_board, left_mask).sum() * enemy_points
        dir_values[Dir.right.value] += \
            np.multiply(self.enemy_board, right_mask).sum() * enemy_points

        if self.me.health < 30:
            if self.closest_food["x"] < self.me.head["x"]:
                dir_values[Dir.left.value] += extra_hungry_points
            elif self.closest_food["x"] > self.me.head["x"]:
                dir_values[Dir.right.value] += extra_hungry_points

            if self.closest_food["y"] < self.me.head["y"]:
                dir_values[Dir.up.value] += extra_hungry_points
            elif self.closest_food["y"] > self.me.head["y"]:
                dir_values[Dir.down.value] += extra_hungry_points
        elif self.me.health < 50:
            if self.closest_food["x"] < self.me.head["x"]:
                dir_values[Dir.left.value] += hungry_points
            elif self.closest_food["x"] > self.me.head["x"]:
                dir_values[Dir.right.value] += hungry_points

            if self.closest_food["y"] < self.me.head["y"]:
                dir_values[Dir.up.value] += hungry_points
            elif self.closest_food["y"] > self.me.head["y"]:
                dir_values[Dir.down.value] += hungry_points
        else:
            if self.closest_food["x"] < self.me.head["x"]:
                dir_values[Dir.left.value] += food_points
            elif self.closest_food["x"] > self.me.head["x"]:
                dir_values[Dir.right.value] += food_points

            if self.closest_food["y"] < self.me.head["y"]:
                dir_values[Dir.up.value] += food_points
            elif self.closest_food["y"] > self.me.head["y"]:
                dir_values[Dir.down.value] += food_points

        print(dir_values)
        i = dir_values.index(min(dir_values))
        return directions[i].name

    @staticmethod
    def mask(height, left, right, rest_height, rest_width):
        a = np.triu(np.ones((height, left)), left - (1 + height))
        b = np.fliplr(np.triu(np.ones((height, right)), right - (0 + height)))
        c = np.zeros((rest_height + 1, rest_width))

        return np.concatenate((np.concatenate((a, b), axis=1), c), axis=0)

