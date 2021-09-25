import random
from Pente import *

class MyPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    depth = 1
    while self.timeRemaining() > 0:
      if state.getTurn() % 2 == 0:
        (v, m) = self.maxPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      else:
        (v, m) = self.minPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      depth += 1


  def maxPlayer(self, state, depth, alpha, beta):
    if state.gameOver(): 
      return (1 -state.winner(), tuple())
    if depth == 0:
      return (self.heuristic(state),tuple())

    if not self.timeRemaining():
        return (self.heuristic(state), tuple())
    
    actions = state.actions()
      
    best = (-1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v,m) = self.minPlayer(result, depth-1, alpha, beta)
      
      if v > beta:
        return (v, a)
      
      best = max(best, (v,a))
      alpha = max(alpha, v)
        
    return best

  def minPlayer(self, state, depth, alpha, beta):
    if state.gameOver(): 
      return (1 - state.winner(), tuple())
    if depth == 0:
      return (self.heuristic(state),tuple())

    if not self.timeRemaining():
        return (self.heuristic(state), tuple())

    
    actions = state.actions()
       
    best = (1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v, m) = self.maxPlayer(result, depth-1, alpha, beta)
      
      if v < alpha: 
        return (v, a)
      
      best = min(best, (v,a))
      beta = min(beta, v)
      
    return best
    

  def heuristic(self, state):
    score = 0.5
    
    score += state.patternCount(' WWWW ') * 0.5
    score += state.patternCount('WWWW ') * 0.4
    score += state.patternCount('WWW  ') * 0.3
    score += state.patternCount(' WWW ') * 0.3
    score += state.patternCount('WWW ') * 0.2
    score += state.patternCount('WBB ') * 0.1
    score += state.patternCount('W ') * 0.05
    
    score -= state.patternCount(' BBBB ') * 0.5
    score -= state.patternCount('BBBB ') * 0.4
    score -= state.patternCount('BBB  ') * 0.3
    score += state.patternCount(' BBB ') * 0.3
    score -= state.patternCount('BBB ') * 0.2
    score -= state.patternCount('BWW ') * 0.1
    score -= state.patternCount('B ') * 0.05

    return score 
    
