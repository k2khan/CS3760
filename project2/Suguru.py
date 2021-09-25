import copy

class Suguru:
  class State:
    def __init__(self, size, cells, known):
      self._size = size
      self._cells = cells # List of cells, each a list of pairs
      self._known = known
      
      self._cellLookup = dict()
      for cellId, cell in enumerate(cells):
        for location in cell:
          self._cellLookup[location] = cellId
      
      for row in range(size[0]):
        for col in range(size[1]):
          if (row,col) not in known:
            self._known[(row,col)] = list(range(1, len(self.getCell(self.getCellId((row,col))))+1))
            
    def setValue(self, location, value):
      self._known[location] = value
      
    def getSize(self):
      return self._size
      
    def getPossibleValues(self, location):
      return self._known[location]
      
    def removePossibleValue(self, location, value):
      self._known[location].remove(value)
      
    def setPossibleValues(self, location, values):
      if isinstance(values,int):
        values = [values]
      self._known[location] = values
      
    def isValueKnown(self, location):
      return len(self._known[location]) == 1
      
    def isInconsistent(self):
      return min([len(v) for v in self._known.values()]) == 0
      
    def getCellId(self, location):
      return self._cellLookup[location]
      
    def getCell(self, cellId):
      return self._cells[cellId]
      
    def cellSize(self, cellId):
      return len(self._cells[cellId])
      
    def isGoal(self):
      return set([ len(x) for x in self._known.values() ]) == set([1])
      
    def __str__(self):
      s = '%02i%02i' % self._size
      for row in range(self._size[0]):
        for col in range(self._size[1]):
          cell = chr(ord('A') + self._cellLookup[(row,col)])
          value = self._known.get((row,col), 0)
          if len(value) == 1:
            value = value[0]
          else:
            value = 0
          s += '%s%d' % (cell, value)
          
      return s
      
      
  def __init__(self, initial):
    self._size = initial._size
    self._initial = initial
    
  def isGoal(self, state):
    return state.isGoal()
    
  def actions(self, state):
    known = state.getKnown().keys()
    actions = []
    for row in range(size[0]):
      for col in range(size[1]):
        for n in range(len(self._cells[self._cellLookup[(row,col)]])):
          actions.append(((row,col), n))
    return actions
    
  def result(self, state, action):
    newState = copy.deepcopy(state)
    newState.setValue(action[0], [action[1]])
    return newState
    
  def getInitial(self):
    return self._initial
    
  def getSize(self):
    return self._initial._size

def suguruFromString(s):
  size = (int(s[:2]),int(s[2:4]))
  numCells = len(set([s[i:i+2] for i in range(4,s.index('-'),3)]))
  cells = []
  known = {}
  for i in range(numCells):
    cells.append([])
  index = 4
  for row in range(size[0]):
    for col in range(size[1]):
      cellId = 26*(ord(s[index]) - ord('A'))+ord(s[index+1]) - ord('A')
      cells[cellId].append((row,col))
      if s[index+2] != '0':
        known[(row,col)] = [int(s[index+2])]
      index += 3
  
  return Suguru.State(size, cells, known)
  
example5easy = '0505AA2AA1AA0AA0AB0AA0AC0AC0AB0AB1AC0AC5AD0AB0AB0AC0AD0AD4AD0AE0AF0AF0AD2AE0AE0'
example8tough = '0808AA3AA2AA0AB0AB2AC0AD0AD2AA0AA0AE0AB0AB0AC0AC0AD0AE2AE0AE0AB0AF3AC0AC0AD0AG0AE0AH0AF0AF0AF0AF0AD0AG0AH0AH0AH0AI0AJ0AJ0AJ0AG0AK0AH0AI0AI0AI0AJ0AJ0AL0AK0AK0AM0AI0AN0AN0AN0AL0AK0AM0AM0AM0AM0AN4AN3'
exampleExtraLarge = '1015'
