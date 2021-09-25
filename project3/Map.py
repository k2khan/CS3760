class Map:
  def __init__(self, gameMap):
    self._map = gameMap
    self._height = len(self._map)
    self._width = len(self._map[0])
    
    # Calculate the distances in the map
    locations = []
    for row in range(self._height):
      for col in range(self._width):
        if self.onMap((row,col)):
          locations.append((row,col))
    dist = {}
    inf = self._width * self._height
    for loc in locations:
      dist[(loc,loc)] = 0
      (row,col) = loc
      for loc2 in [ (row+1,col), (row-1,col), (row,col+1), (row,col-1) ]:
        if loc2 in locations:
          dist[(loc,loc2)] = 1
    for loc1 in locations:
      for loc2 in locations:
        for loc3 in locations:
          dist[(loc2,loc3)] = min(dist.get((loc2,loc3),inf), dist.get((loc2,loc1),inf) + dist.get((loc3,loc1),inf))
    self._distances = dist    
    
  def getHeight(self):
    return self._height
    
  def getWidth(self):
    return self._width
    
  def onMap(self, position):
    return self._map[position[0]][position[1]] != '#'
    
  def mapDistance(self, loc1, loc2):
    return self._distances[(loc1,loc2)]
    
  def getPlayerLocation(self):
    for row, line in enumerate(self._map):
      if 'P' in line:
        return (row, line.index('P'))
        
  def getGhostLocations(self):
    positions = []
    for row, line in enumerate(self._map):
      for col in [i for i in range(len(line)) if line.startswith('G', i)]:
        positions.append( (row,col) )
    return positions
    
  def getPellets(self):
    positions = []
    for row, line in enumerate(self._map):
      for col in [i for i in range(len(line)) if line.startswith('.', i)]:
        positions.append( (row,col) )
    return set(positions)
    
  def getPowerups(self):
    positions = []
    for row, line in enumerate(self._map):
      for col in [i for i in range(len(line)) if line.startswith('O', i)]:
        positions.append( (row,col) )
    return set(positions)
    
    
