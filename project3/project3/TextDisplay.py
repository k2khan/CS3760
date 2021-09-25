from State import *
from Map import *

class TextDisplay:
  def __init__(self, gameMap):
    self._map = gameMap
    
  def draw(self, state):
    print()
    print('Turn:', state._turn)
    print('Score:', state.getScore())
    print('Scared time remaining:', state._scaredTurnsLeft)
    print()
    for row, line in enumerate(self._map._map):
      for col, char in enumerate(line):
        if self._map.onMap((row,col)):
          if (row,col) == state._playerLocation:
            print('P', end='')
          elif (row,col) in state._ghostPositions:
            print('G', end='')
          elif (row,col) in state._pellets:
            print('.', end='')
          elif (row,col) in state._powerUps:
            print('O', end='')
          else:
            print(' ', end='')
        else:
          print('#', end='')
      print()
    print()
