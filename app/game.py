import numpy as np


def initializeMap(height, width, food, enemies, me):
    board = np.zeros((height, width))

    for s in enemies:
        for b in s["body"]:
            board[b["x"]][b["y"]] = 3

    for f in food:
        board[f["x"]][f["y"]] = 2

    for m in me["body"]:
        board[m["x"]][m["y"]] = 1

    return board


