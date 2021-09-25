from Pente import *
import subprocess
import sys
import os
import time
import psutil
import logging

player1name = "submission4"
player2name = "submission1"
timeLimit = 1

exec(f'from {player1name} import *')
if player1name != 'HumanPlayer':
  exec(f'player1 = {player1name}({timeLimit})')
else:
  exec(f'player1 = {player1name}({1e6})')

exec(f'from {player2name} import *')
if player2name != 'HumanPlayer':
  exec(f'player2 = {player2name}({timeLimit})')
else:
  exec(f'player2 = {player2name}({1e6})')



size = 0
if size > 0:
  from Graphics import *
  g = Graphics(size)
else:
  g = None

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

state = Pente()

moveSequence = []

while not state.gameOver():
  print(state)
  
  if state.getTurn() % 2 == 0:
    player1._startTime = time.time()
    player1.findMove(state)
    move = player1.getMove()
    print(f'White moves {state.moveToStr(move)}\n')
  else:
    player2._startTime = time.time()
    player2.findMove(state)
    move = player2.getMove()
    print(f'Black moves {state.moveToStr(move)}\n')
  state = state.result(move)
  moveSequence.append(move)


  if g is not None:
    g.draw(state)

print(state)
if state.winner() == 0:
  print("White wins!")
  with open("4vs1.txt", "a") as myFile:
    myFile.write("White Wins!" + "\n")
  restart_program()
elif state.winner() == 1:
  print("Black wins!")
  with open("4vs1.txt", "a") as myFile:
    myFile.write("Black Wins!" + "\n")
  restart_program()
else:
  print("It's a draw")

  
print('Move sequence:', ' '.join([state.moveToStr(m) for m in moveSequence]))
