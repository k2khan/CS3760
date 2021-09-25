from Suguru import *
from cs1graphics import *

class SuguruVisualizer:
  def __init__(self, state, windowSize):
    self._size = state._size
    self._scale = windowSize/self._size[1]
    self._fixed = set()
    for row in range(self._size[0]):
      for col in range(self._size[1]):
        if len(state.getPossibleValues((row,col))) == 1:
          self._fixed.add((row,col))
    self._guesses = set()
    
    self._canvas = Canvas(windowSize, windowSize*self._size[0]//self._size[1])
    self._canvas.setAutoRefresh(False)
    self._canvas.setTitle('Suguru')
    
    # Draw the cells and initial values
    self._textBoxes = {}
    self._optionBoxes = {}
    for row in range(self._size[0]):
      for col in range(self._size[1]):
        s = Square(self._scale)
        s.move((col+.5)*self._scale, (row+.5)*self._scale)
        s.setBorderWidth(.01*self._scale)
        self._canvas.add(s)
        
        t = Text('')
        t.setFontSize(.5*self._scale)
        t.move((col+.5)*self._scale, (row+.5)*self._scale)
        t.setDepth(-5)
        self._canvas.add(t)
        self._textBoxes[(row,col)] = t
        
        t2 = Text('')        
        t2.setFontColor('red')
        t2.setFontSize(.125*self._scale)
        t2.move((col+.5)*self._scale, (row+.75)*self._scale)
        t2.setDepth(-5)
        self._canvas.add(t2)
        self._optionBoxes[(row,col)] = t2
        
        if state._cellLookup[(row,col)] != state._cellLookup.get((row+1,col), -1):
          l = Path()
          l.setBorderWidth(.05*self._scale)
          l.addPoint(Point(col*self._scale, (row+1)*self._scale))
          l.addPoint(Point((col+1)*self._scale, (row+1)*self._scale))
          self._canvas.add(l)
        
        if state._cellLookup[(row,col)] != state._cellLookup.get((row,col+1), -1):
          l = Path()
          l.setBorderWidth(.05*self._scale)
          l.addPoint(Point((col+1)*self._scale, row*self._scale))
          l.addPoint(Point((col+1)*self._scale, (row+1)*self._scale))
          self._canvas.add(l)
  
    self.draw(state)
    
  def draw(self, state):
    for (k,v) in self._textBoxes.items():
      if len(state.getPossibleValues(k)) == 1:
        self._textBoxes[k].setMessage(str(state.getPossibleValues(k)[0]))
        if k in self._fixed:
          self._textBoxes[k].setFontColor('black')
        elif k in self._guesses:
          v.setFontColor('red')
        else:
          v.setFontColor('blue')
      else:
        v.setMessage('')
        
      if len(state.getPossibleValues(k)) > 1:
        m = ''
        for i in range(1,6):
          if i in state.getPossibleValues(k):
            m += str(i)
          else:
            m += ' '
        self._optionBoxes[k].setMessage(m)
      else:        
        self._optionBoxes[k].setMessage('')
      
    self._canvas.refresh()
