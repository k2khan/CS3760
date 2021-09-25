from Map import *
from Pacman import *
from State import *
from TextDisplay import *
from MyPlayer import *

maxTime = float(input('Maximum time for player to make a move? '))

if input('Text player (0) or your player (1) ' ) == '0':
  player = TextPlayer(maxTime)
else:
  player = MyPlayer(maxTime)

mapId = int(input('What map do you want to use (0-3): '))
if mapId == 0:  # Wide ope\n, o\ne ghost
  gameMap = '###############\n#.............#\n#.P.........O.#\n#.............#\n#.............#\n#...........G.#\n#.............#\n###############'.split('\n')
elif mapId == 1: #   Trapped!
  gameMap = '########\n#   P G#\n#G######\n#......#\n########'.split('\n')
elif mapId == 2: # Classic
  gameMap = '############################\n#............##............#\n#.####.#####.##.#####.####.#\n#O####.#####.##.#####.####O#\n#.####.#####.##.#####.####.#\n#..........................#\n#.####.##.########.##.####.#\n#.####.##.########.##.####.#\n#......##....##....##......#\n######.##### ## #####.######\n######.##### ## #####.######\n######.#            #.######\n######.# ####  #### #.######\n#     .  #G  GG  G#  .     #\n######.# ########## #.######\n######.#            #.######\n######.# ########## #.######\n#............##............#\n#.####.#####.##.#####.####.#\n#.####.#####.##.#####.####.#\n#O..##.......  .......##..O#\n###.##.##.########.##.##.###\n###.##.##.########.##.##.###\n#......##....##....##......#\n#.##########.##.##########.#\n#.............P............#\n############################'.split('\n')
elif mapId == 3: # Small
  gameMap = '####################\n#......#G  G#......#\n#.##...##  ##...##.#\n#.#O.#........#.O#.#\n#.##.#.######.#.##.#\n#........P.........#\n####################'.split('\n')
gameMap = Map(gameMap)

size = int(input('Size of graphics screen (0 for text): '))  
if size > 0:
  from GraphicsDisplay import *
  display = GraphicsDisplay(gameMap, size)
else:
  display = TextDisplay(gameMap)
  
p = Pacman(gameMap, 500, maxTime, player, display)
p.play()
          
