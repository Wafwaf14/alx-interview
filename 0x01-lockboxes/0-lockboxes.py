#!/usr/bin/python3
"""Lockboxes Interview question"""


def canUnlockAll(boxes):
    """Takes a list of lists
    Returns true if all boxes can be opened else false"""
    n = len(boxes)
    unlocked = [False] * n
    unlocked[0] = True

    for i in range(n):
        if unlocked[i]:
            for key in boxes[i]:
                if key < n:
                    unlocked[key] = True

    return all(unlocked)
