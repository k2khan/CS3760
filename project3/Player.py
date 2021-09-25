import time

class Player:
  def __init__(self, timeLimit):
    self._timeLimit = timeLimit
    self._startTime = time.time()
    self._move = 'Stay'
    
  def resetTime(self):
    self._startTime = time.time()  
  
  def timeRemaining(self):
    return time.time() - self._startTime < self._timeLimit
    
  def setMove(self, move):
    if self.timeRemaining():
      self._move = move
    
  def getMove(self):
    return self._move
    
  def findMove(self, state):
    pass

class TextPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
    
  def findMove(self, state):
    move = input('Move (UDLRS): ')
    try:
      move = { 'U': 'Up', 'D': 'Down', 'L': 'Left', 'R': 'Right', 'S': 'Stay' }[move]
    except:
      move = 'Stay'
      
    if move not in state.actions():
      move = 'Stay'
      
    self.setMove(move)
