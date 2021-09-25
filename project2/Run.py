maxTime = 999999 
puzzle = input('Entry the string encoding for the puzzle: ')
graphics = 0

from MySolver import *
from Suguru import *

p = Suguru(suguruFromString(puzzle))
if graphics > 0:
  from SuguruVisualizer import *
  visualizer = SuguruVisualizer(p.getInitial(), graphics)
else:
  visualizer = None
print('Solving puzzle:')

solution=MySolver(p, maxTime, visualizer).solution()

import hashlib

solutionHash = hashlib.md5(str(solution).encode()).hexdigest()
if solutionHash == puzzle.split('-')[1]:
  print('Correct solution')
else:
  print('Solution is incorrect')

if visualizer and solution and solution.isGoal():
  visualizer.draw(solution)

  
