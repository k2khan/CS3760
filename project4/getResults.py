import sys
import os

white = 0
black = 0
with open('result.txt') as f:
    for line in f:
        if "White" in line:
            white += 1
        if "Black" in line:
            black += 1

print("White: ", white, "Black: ", black)
