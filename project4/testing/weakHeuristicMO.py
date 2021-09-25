import random
from Pente import *

class submission2(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
    self._bestMove = {}
  
  def findMove(self, state):
    depth = 1
    while self.timeRemaining():
      if state.getTurn() % 2 == 0:
        (v, m) = self.maxPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      else:
        (v, m) = self.minPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      depth += 1

  def maxPlayer(self, state, depth, alpha, beta):
    if state.gameOver(): 
      if state.winner() == 0:
        return (1 - 1e-6 * state.getTurn(), tuple())
      if state.winner() == 1:
        return (0 + 1e-6 * state.getTurn(), tuple())
    if depth == 0:
      return (self.heuristic(state),tuple())

    actions = self.moveOrdering(state)
    if len(actions) == 0:
      actions = state.actions()
      
    best = (-1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v,m) = self.minPlayer(result, depth-1, alpha, beta)
      
      if v > beta:
        return (v, a)
      
      best = max(best, (v,a))
      alpha = max(alpha, v)
    
    self._bestMove[state] = best[1]
    return best

  def minPlayer(self, state, depth, alpha, beta):
    if state.gameOver(): 
      if state.winner() == 0:
        return (1 - 1e-6 * state.getTurn(), tuple())
      if state.winner() == 1:
        return (0 + 1e-6 * state.getTurn(), tuple())
    if depth == 0:
      return (self.heuristic(state),tuple())
    
    actions = self.moveOrdering(state)
    if len(actions) == 0:
      actions = state.actions()

    best = (1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v, m) = self.maxPlayer(result, depth-1, alpha, beta)
      
      if v < alpha: 
        return (v, a)
      
      best = min(best, (v,a))
      beta = min(beta, v)
    
    self._bestMove[state] = best[1]
    return best
    
  def heuristic(self, state):
    score = 0.5
    
    score += state.patternCount(' WWWW ') * 0.2
    score += state.patternCount('WWWW ') * 0.15
    score += state.patternCount(' WWW ') * 0.15
    score += state.patternCount('WWW  ') * 0.1
    score += state.patternCount('WWW ') * 0.075
    score += state.patternCount('WW ') * 0.05
    score += state.patternCount('W ') * 0.005
    score += state.patternCount('WBB ') * 0.01
    
    score -= state.patternCount(' BBBB ') * 0.2
    score -= state.patternCount('BBBB ') * 0.15
    score -= state.patternCount(' BBB ') * 0.15
    score -= state.patternCount('BBB  ') * 0.1
    score -= state.patternCount('BBB ') * 0.075
    score -= state.patternCount('BB ') * 0.05
    score -= state.patternCount('W ') * 0.005
    score -= state.patternCount('BWW ') * 0.01

    return score 
    
  def moveOrdering(self, state):
    locations = {}
      
    if state.winningMoves():
      return state.winningMoves()


    for l in state.patternLocations('WWWW_'):
      locations[l] = locations.get(l, 0) + 1
    for l in state.patternLocations('WWW_'):
      locations[l] = locations.get(l, 0) + .6
    for l in state.patternLocations('WW_'):
      locations[l] = locations.get(l, 0) + .4
    for l in state.patternLocations('W_'):
      locations[l] = locations.get(l, 0) + .25
    for l in state.patternLocations('WBB_'):
      locations[l] = locations.get(l, 0) + .5
    for l in state.patternLocations('BWW_'):
      locations[l] = locations.get(l, 0) + .5
    for l in state.patternLocations('B_'):
      locations[l] = locations.get(l, 0) + .2

    sortedLocations = []
    for (l, v) in locations.items():
      sortedLocations.append((v, l))
    sortedLocations = sorted(sortedLocations, key=lambda tup: tup[0], reverse = True)
    if len(sortedLocations) > 10:
      sortedLocations = sortedLocations[:10]
    return [l for (v, l) in sortedLocations]
