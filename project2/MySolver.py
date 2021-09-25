from SuguruSolver import *

class MySolver(SuguruSolver):  
  def __init__(self, problem, maxTime, visualizer):
    SuguruSolver.__init__(self, problem, maxTime, visualizer)
    self._allNeighbors = self.allNeighbors()
    
  # You should improve these functions to improve performance
  def selectUnassignedLocation(self, state):
    # Find the first location on the board has more than one possibility
    # then return it.  In class we talked about heuristics that might 
    # perform better than this.

    #Returns first location with MRV
    smallestLength = 999
    smallestLocation = ()
    for location in self._allNeighbors:
      if not state.isValueKnown(location):
        if len(state.getPossibleValues(location)) < smallestLength:
          smallestLength = len(state.getPossibleValues(location))
          smallestLocation = (location)
    return smallestLocation

  #Get set of all locations, and the possible neighbors for each location
  def allNeighbors(self):
    row = self._problem.getSize()[0]
    column = self._problem.getSize()[1]
    mapping = {}
    for r in range(row):
      for c in range(column):
        location = (r, c) 

        neighbors = []
        for dx in [-1, 0, 1]:
          for dy in [-1, 0, 1]:
            x = location[0] + dx
            y = location[1] + dy
            neighbors.append((x, y))

        #Remove neighbors that are out of bounds
        trueNeighbors = []
        for i in neighbors:
          if i[0] >= 0 and i[0] < row and i[1] >= 0 and i[1] < column:
            trueNeighbors.append(i)

        trueNeighbors.remove(location)
        mapping[location] = trueNeighbors
    return mapping


  def isConsistent(self, state, location, value):
    # Check if putting value at location on the board is consistent
    # with the problem constraints.  This needs to be implemented.
    # Right now it says that it is always consistent.

    #Find all true neighbors
    trueNeighbors = self._allNeighbors.get(location) 

    #Check consistency within a cell
    for i in state.getCell(state.getCellId(location)):
      if i == location:
        continue
      if state.isValueKnown(i):
        if state.getPossibleValues(i)[0] == value:
          return False

    #Check consistency with adjacent tiles
    for i in trueNeighbors:
      if state.isValueKnown(i):
        if state.getPossibleValues(i)[0] == value:
          return False

    return True
    
  def infer(self, state, changedLocations, initial=False):
    # Perform inference to reduce the possibilities values that can
    # be filled in.  There are a variety of heuristic you could do
    # here to improve performance.  Currently it makes no improvements.

    visitedCells = []
    if initial == False:
      for location in self._allNeighbors:
        possibleValues = state.getPossibleValues(location)
        neighboringCellIds = []
        trueNeighbors = self._allNeighbors.get(location) 
        for i in trueNeighbors:
          if state.getCellId(i) not in neighboringCellIds:
            if location not in state.getCell(state.getCellId(i)):
              neighboringCellIds.append(state.getCellId(i))
        #First technique based on https://dkmgames.com/Suguru/SuguruTutAdvanced.htm
        for i in range(len(neighboringCellIds)):
          cell = state.getCell(neighboringCellIds[i])
          mapping = {}
          for k in cell:
            mapping[k] = state.getPossibleValues(k) #Maps each location to the possible values of a cell
          for l in possibleValues:
            sameValueLocations = []
            for key, value in mapping.items():
              if l in value:
                sameValueLocations.append(key)
            if (set(sameValueLocations) <= set(trueNeighbors)) and (len(sameValueLocations) > 0):
              if l in state.getPossibleValues(location):
                state.removePossibleValue(location, l)
                if len(state.getPossibleValues(location)) == 1:
                  changedLocations.append(location)

    while (len(changedLocations) > 0):
      location = changedLocations.pop()
      if state.isValueKnown(location):
        value = state.getPossibleValues(location)[0] #Get value of location that was popped

      #Find all true neighbors
      trueNeighbors = self._allNeighbors.get(location)

      #Check for inference within a cell 
      for i in state.getCell(state.getCellId(location)):
        if i == location:
          continue
        if value in state.getPossibleValues(i):
          state.removePossibleValue(i, value)
          if len(state.getPossibleValues(i)) == 1:
            changedLocations.append(i)

      #Check inference with adjacent tiles
      for i in trueNeighbors:
        if value in state.getPossibleValues(i):
          state.removePossibleValue(i, value)
          if len(state.getPossibleValues(i)) == 1:
            changedLocations.append(i)

      #This checks for the inference described here: https://dkmgames.com/Suguru/SuguruTutBasic.htmA
      neighboringCellIds = []
      if state.isValueKnown(location):
        trueNeighbors = self._allNeighbors.get(location) 
        for i in trueNeighbors:
          if state.getCellId(i) not in neighboringCellIds:
            if location not in state.getCell(state.getCellId(i)):
              neighboringCellIds.append(state.getCellId(i))
        
        for i in range(len(neighboringCellIds)):
          cell = state.getCell(neighboringCellIds[i])
          count = 0
          for j in cell:
            if j in trueNeighbors:
              count += 1
          size = state.cellSize(neighboringCellIds[i])
          if len(cell) >= value:
            if (size - 1) == count:
              resultLocation = [x for x in cell if x not in trueNeighbors][0]
              if not state.isValueKnown(resultLocation):
                state.setPossibleValues(resultLocation, value)
                if len(state.getPossibleValues(resultLocation)) == 1:
                  changedLocations.append(resultLocation)
      
        allValues = []
        if state.getCellId(location) not in visitedCells:
          visitedCells.append(state.getCellId(location))
          result = 0
          for j in state.getCell(state.getCellId(location)):
            if len(state.getPossibleValues(j)) > 0:
              allValues.append(state.getPossibleValues(j))
          if len(allValues) > 1:
            allValues = [item for items in allValues for item in items]
            for k in range(state.cellSize(state.getCellId(location))):
              if allValues.count(k) == 1:
                result = k 
                for j in state.getCell(state.getCellId(location)):
                  if result in state.getPossibleValues(j):
                    state.setPossibleValues(j, result)
                    if len(state.getPossibleValues(j)) == 1:
                      changedLocations.append(j)

    return state
