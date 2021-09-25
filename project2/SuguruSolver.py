from Suguru import *
from time import *
import hashlib

class SuguruSolver:
  def __init__(self, problem, maxTime, visualizer):
    self._problem = problem
    self._maxTime = maxTime
    self._time = time()
    self._visualizer = visualizer
    self._numExpansions = 0
    self._backTracks = 0
    
  def timeRemaining(self):
    return time() < self._time + self._maxTime
    
  def solution(self):
    self._time = time()
    solution = self.solve()
    solutionTime = time() - self._time

    if self._visualizer:
      self._visualizer.draw(solution)    

    print('Solution key =', hashlib.md5(str(solution).encode()).hexdigest())
    print('Number of nodes expanded =', self._numExpansions)
    print('Number of backtracks =', self._backTracks)
    print('Search time per node =', solutionTime / max(1,self._numExpansions))
    print('Search time =', solutionTime)
    
    return solution

  def solve(self, state=None):
    if not self.timeRemaining():
      return None
    
    if state is None:
      state = self._problem.getInitial()
      filledIn = [ k for (k,v) in state._known.items() if len(v) == 1 ]
      state = self.infer(state, filledIn, True)
      
    if state.isGoal():
      return state
      
    if state.isInconsistent():
      return None
      
    if self._visualizer:
      self._visualizer.draw(state)
      
    self._numExpansions += 1
    location = self.selectUnassignedLocation(state)
    for value in state.getPossibleValues(location):
      if self.isConsistent(state, location, value):
        newState = self._problem.result(state, (location, value))
        newState = self.infer(newState, [location])
        
        if self._visualizer:
          self._visualizer._guesses.add(location)
        
        solution = self.solve(newState)
        if solution is not None:
          return solution
        self._backTracks += 1
          
    return None              
    
  def getPuzzle(self):
    return self._problem
