from State import *
from Map import *

from cs1graphics import *

class GraphicsDisplay:
  def __init__(self, gameMap, width):
    self._map = gameMap
    
    self._scale = width/self._map.getWidth()
    
    self._canvas = Canvas(width, int(self._scale*(3+self._map.getHeight())))
    self._canvas.setTitle('Catch the Ghosts')
    self._canvas.setBackgroundColor('black')
    
    self._turn = Text('Turn: 0', .75*self._scale)
    self._turn.moveTo(width/2, self._scale/2)
    self._turn.setFontColor('white')
    self._canvas.add(self._turn)
    
    self._score = Text('Score: 0', .75*self._scale)
    self._score.moveTo(width/2, 3*self._scale/2)
    self._score.setFontColor('white')
    self._canvas.add(self._score)
    
    self._scared = Text('Scared time:  0', .75*self._scale)
    self._scared.moveTo(width/2, 5*self._scale/2)
    self._scared.setFontColor('white')
    self._canvas.add(self._scared)
    
    self._player = Circle(.4*self._scale)
    self._player.setFillColor('yellow')
    self._player.setBorderWidth(0)
    self._player.setDepth(-5)
    self._player.moveTo( (self._map.getPlayerLocation()[1]+.5)*self._scale, (self._map.getPlayerLocation()[0]+3.5)*self._scale )
    self._canvas.add(self._player)
    
    for row in range(self._map.getHeight()):
      for col in range(self._map.getWidth()):
        if not self._map.onMap((row,col)):
          s = Square(self._scale)
          s.moveTo( (col+.5)*self._scale, (row+3.5)*self._scale )
          s.setFillColor('cyan')
          s.setBorderWidth(0)
          self._canvas.add(s)
    
    self._ghosts = []
    for ghostId, loc in enumerate(self._map.getGhostLocations()):
      s = Square(.65*self._scale)
      s.rotate(45)
      s.setFillColor(['magenta','red','blue','green'][ghostId])
      s.setBorderWidth(0)
      s.moveTo( (loc[1]+.5)*self._scale, (loc[0]+3.5)*self._scale )
      s.setDepth(-10)
      self._ghosts.append(s)
      self._canvas.add(s)
      
    self._pellets = {}
    for loc in self._map.getPellets():
      c = Circle(.1*self._scale)
      c.setFillColor('white')
      c.moveTo( (loc[1]+.5)*self._scale, (loc[0]+3.5)*self._scale )
      self._pellets[loc] = c
      self._canvas.add(c)
    
    self._powerUps = {}
    for loc in self._map.getPowerups():
      c = Circle(.2*self._scale)
      c.setFillColor('blue')
      c.setBorderWidth(0)
      c.moveTo( (loc[1]+.5)*self._scale, (loc[0]+3.5)*self._scale )
      self._powerUps[loc] = c
      self._canvas.add(c)
    
  def draw(self, state):
    self._turn.setMessage(f'Turn: {state.getTurn()}')
    self._score.setMessage(f'Score: {state.getScore()}')
    self._scared.setMessage(f'Scared time: {state.getScaredTurnsLeft()}')
    
    loc = state.getPlayerPosition()
    self._player.moveTo( (loc[1]+.5)*self._scale, (loc[0]+3.5)*self._scale )
    
    for ghostId, loc in enumerate(state.getGhostPositions()):
      self._ghosts[ghostId].moveTo( (loc[1]+.5)*self._scale, (loc[0]+3.5)*self._scale )
      
    for (k,v) in list(self._pellets.items()):
      if k not in state.getPellets():
        self._canvas.remove(v)
        self._pellets.pop(k)
        
    for (k,v) in list(self._powerUps.items()):
      if k not in state.getPowerUps():
        self._canvas.remove(v)
        self._powerUps.pop(k)
        

