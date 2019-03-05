import numpy as np
import random


def getDir(board, head, facing):
    up = 0
    down = 0
    left = 0
    right = 0

    surround = 4
    edge_points = 10
    enemy_points = 5
    food_points = -15
    me_points = 10

    if head["x"] == 0:
        left += 50000
    if head["x"] == len(board) - 1:
        right += 50000
    if head["y"] == 0:
        up += 50000
    if head["y"] == len(board) - 1:
        down += 50000

    if facing == "up":
        up += (len(board) - head["y"]) * edge_points
        down += 50000
    elif facing == "down":
        up += 50000
        down += head["y"] * edge_points
    elif facing == "left":
        right += 50000
        left += (len(board) - head["x"]) * edge_points
    elif facing == "right":
        left += 50000
        right += head["x"] * edge_points

    for i in range(surround, head["y"]):
        for j in range(head["x"] - surround, head["x"] + surround):
            if i >= len(board) or j >= len(board) or i < 0 or j < 0:
                continue
            if board[i][j] == 2:
                up += food_points
            elif board[i][j] == 3:
                up += enemy_points
            elif board[i][j] == 1:
                up += me_points

    for i in range(head["y"] - surround, head["y"] + surround):
        for j in range(surround, head["x"]):
            if i >= len(board) or j >= len(board) or i < 0 or j < 0:
                continue
            if board[i][j] == 2:
                left += food_points
            elif board[i][j] == 3:
                left += enemy_points
            elif board[i][j] == 1:
                left += me_points

    for i in range(head["y"] - surround, head["y"] + surround):
        for j in range(head["x"], surround):
            if i >= len(board) or j >= len(board) or i < 0 or j < 0:
                continue
            if board[i][j] == 2:
                right += food_points
            elif board[i][j] == 3:
                right += enemy_points
            elif board[i][j] == 1:
                right += me_points

    for i in range(head["y"], head["y"] + surround):
        for j in range(head["x"] - surround, head["x"] + surround):
            if i >= len(board) or j >= len(board) or i < 0 or j < 0:
                continue
            if board[i][j] == 2:
                down += food_points
            elif board[i][j] == 3:
                down += enemy_points
            elif board[i][j] == 1:
                down += me_points
    #
    # print(up)
    # print(down)
    # print(left)
    # print(right)

    minv = min(up, down, left, right)
    if up == minv:
        return "up"
    elif down == minv:
        return "down"
    elif left == minv:
        return "left"
    elif right == minv:
        return "right"
    else:
        directions = list({"up", "down", "left", "right"} - set(facing))
        return random.choice(directions)


# def close_quarters(board, head, facing):
#     for i in range(head["y"] - 1, head["y"] + 1):
#         for j in range(head["x"] - 1, head["x"] + 1):


