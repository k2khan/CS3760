import copy
import random

ghostMemory = {}
resultMemory = {}

class State:
  def __init__(self, gameMap):
    self._map = gameMap
    
    self._turn = 0
    self._gameOver = False
    self._gameWon = False
    self._score = 0
    self._scaredTurnsLeft = 0
    
    self._playerLocation = gameMap.getPlayerLocation()
    self._ghostPositions = gameMap.getGhostLocations()
    self._ghostPrevious = [None] * len(self._ghostPositions)
    self._pellets = gameMap.getPellets()
    self._powerUps = gameMap.getPowerups()
    
  def __hash__(self):
    return hash( (self._turn, self._gameOver, self._score, self._scaredTurnsLeft, self._playerLocation, tuple(self._ghostPositions), tuple(self._ghostPrevious), tuple(self._pellets), tuple(self._powerUps)) )
    
  def getScaredTurnsLeft(self):
    return self._scaredTurnsLeft
    
  def getPlayerPosition(self):
    return self._playerLocation
    
  def getGhostPositions(self):
    return self._ghostPositions
    
  def getPellets(self):
    return self._pellets
  
  def getPowerUps(self):
    return self._powerUps
    
  def gameOver(self):
    return self._gameOver
    
  def getScore(self):
    return self._score
    
  def getTurn(self):
    return self._turn
    
  def actions(self):
    actions = ['Stay']
    if self._map.onMap( (self._playerLocation[0] - 1, self._playerLocation[1]) ):
      actions.append('Up')
    if self._map.onMap( (self._playerLocation[0] + 1, self._playerLocation[1]) ):
      actions.append('Down')
    if self._map.onMap( (self._playerLocation[0], self._playerLocation[1] - 1) ):
      actions.append('Left')
    if self._map.onMap( (self._playerLocation[0], self._playerLocation[1] + 1) ):
      actions.append('Right')
      
    random.shuffle(actions)
    return actions
      
  def result(self, action):
    global resultMemory
    
    if self.gameOver():
      return self

    if (self, action) in resultMemory:
      return resultMemory[(self,action)]
    
    newState = copy.deepcopy(self)
    if action == 'Up':
      newState._playerLocation = (newState._playerLocation[0] - 1, newState._playerLocation[1])
    elif action == 'Down':
      newState._playerLocation = (newState._playerLocation[0] + 1, newState._playerLocation[1])
    elif action == 'Left':
      newState._playerLocation = (newState._playerLocation[0], newState._playerLocation[1] - 1)
    elif action == 'Right':
      newState._playerLocation = (newState._playerLocation[0], newState._playerLocation[1] + 1)

    newState._update(True)
    
    resultMemory[(self,action)] = newState
    return newState
    
  def _update(self, playerTurn=False):
    if self._scaredTurnsLeft == 0 and self._playerLocation in self._ghostPositions:
      self._score -= 500
      self._gameOver = True
      return
    elif self._playerLocation in self._ghostPositions:
      self._score += 200
      ghostId = self._ghostPositions.index(self._playerLocation)
      
      self._ghostPositions[ghostId] = self._map.getGhostLocations()[ghostId]
      
    if self._playerLocation in self._pellets:
      self._pellets.remove(self._playerLocation)
      self._score += 10
      
      if len(self._pellets) == 0:
        self._score += 500
        self._gameOver = True
        self._gameWon = True
        return
        
    if self._playerLocation in self._powerUps:
      self._powerUps.remove(self._playerLocation)
      self._scaredTurnsLeft = 40
    elif self._scaredTurnsLeft > 0 and playerTurn:
      self._scaredTurnsLeft -= 1
      
    if not playerTurn:
      self._turn += 1
      if not self.gameOver():
        self._score -= 1
      
      
  def ghostResultDistribution(self):
    global ghostMemory
      
    if self.gameOver():
      return [(self,1.)]
      
    if self in ghostMemory:
      return ghostMemory[self]
    
    distribution = [ (self, 1.0) ]
    
    for ghostId, ghostPosition in enumerate(self._ghostPositions):
      if self._scaredTurnsLeft == 0 or self._scaredTurnsLeft % 2 == ghostId % 2:
        (row, col) = ghostPosition
        options = [ (row-1,col), (row+1,col), (row,col-1), (row,col+1) ]
        options = [ pos for pos in options if self._map.onMap(pos) ]
        
        if len(options) == 2 and self._ghostPrevious[ghostId] is not None and self._scaredTurnsLeft == 0:
          options.remove(self._ghostPrevious[ghostId])

        if self._scaredTurnsLeft == 0:
          options = [ (self._map.mapDistance(pos, self._playerLocation), pos) for pos in options ]
        else:
          options = [ (-self._map.mapDistance(pos, self._playerLocation), pos) for pos in options ]
        minDist = min(options)[0]
        
        options = [ pos for (d,pos) in options if d == minDist ]
               
        newDistribution = []
        for (state, prob) in distribution:
          for pos in options:
            newState = copy.deepcopy(state)
            newState._ghostPrevious[ghostId] = state._ghostPositions[ghostId]
            newState._ghostPositions[ghostId] = pos
            newDistribution.append((newState, prob/len(options)))
        distribution = newDistribution
        
    finalDistribution = []
    for (state, prob) in distribution:
      state._update()
      finalDistribution.append( (state,prob) )
    
    ghostMemory[self] = finalDistribution
    return finalDistribution
      
      

