from State import *
from Map import *
from TextDisplay import *
from Player import *
from MyPlayer import *

import random

class Pacman:
  def __init__(self, gameMap, maxTurns, timeLimit, player, display):
    self._maxTurns = maxTurns
    self._timeLimit = timeLimit
    
    self._map = gameMap
    self._player = player
    self._display = display
    self._state = State(self._map)
    
  def play(self):
    while self._state._turn < self._maxTurns and not self._state.gameOver():
      if self._display:
        self._display.draw(self._state)

      
      # Have the player move
      self._player.resetTime()
      self._player.findMove(self._state)
      playerMove = self._player.getMove()
      self._state = self._state.result(playerMove)
      #time.sleep(self._timeLimit + time.time() - player._startTime)
            
      # And then the ghosts
      if not self._state.gameOver():
        ghostDist = self._state.ghostResultDistribution()
  
        p = random.random()
        for (k, v) in ghostDist:
          if p < v:
            self._state = k
            break
          else:
            p -= v

            
    if self._display:
      self._display.draw(self._state)
