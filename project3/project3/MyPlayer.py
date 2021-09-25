from Player import *

import random

class MyPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
    
  def findMove(self, state):
    depth = 0
    while self.timeRemaining():
      value, bestMove = self.maxPlayerValue(state, depth)
      self.setMove(bestMove)
      depth += 1
  
  def maxPlayerValue(self, state, depth):
    if self.timeRemaining() == 0:
      return (state.getScore(), 'Stay')
    if depth == 0:
      return (self.heuristic(state), 'Stay')

    best = float('-inf')
    bestMove = ''
    for action in state.actions():
      result = state.result(action)
      v = self.randomPlayerValue(result, depth - 1)
      if v > best:
        best = v
        bestMove = action

    return best, bestMove

  def randomPlayerValue(self, state, depth):
    if self.timeRemaining() == 0:
      return state.getScore()
    if depth == 0:
      return self.heuristic(state)

    average = 0
    for result, prob in state.ghostResultDistribution():
      v = self.maxPlayerValue(result, depth - 1)[0]
      average += prob * v

    return average

  def heuristic(self, state):
    return state.getScore()