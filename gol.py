#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

class GameOfLife:
  def __init__(self, w , h, seed):
    self.w = w
    self.h = h
    self.seed = seed
    self.board = [[0 for i in range(self.w)] for j in range(self.h)]
    self.board = self.loadPattern(self.board, self.seed)

  def loadPattern(self, board, seed):
    if (self.seed == "glider"):
      self.board[3][1] = 1
      self.board[3][2] = 1
      self.board[3][3] = 1
      self.board[2][3] = 1
      self.board[1][2] = 1
    elif (self.seed == "glider-gun"):
      self.board[3][1] = 1
      self.board[3][2] = 1
      self.board[3][3] = 1
      self.board[2][3] = 1
      self.board[1][2] = 1
    else:
      print ("again")
    return self.board

  def isAlive(self, cell):
    return (cell == 1)

  def countNeighbors(self, board, x, y, w, h):
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if self.isAlive(self.board[(x-i) % w][(y-j) % h]):
          count +=1
    return count

  def genNextState(self, board, w, h):
    self.newBoard = [[0 for i in range(w)] for j in range(h)]
    for i in range(w):
      for j in range(h):
        cellState = self.countNeighbors(self.board,i,j,w,h)
        if self.isAlive(self.board[i][j]):
          cellState -= 1 # remove yourself from alive count
          if(cellState < 2 or cellState > 3):
            self.newBoard[i][j] = 0
          else:
            self.newBoard[i][j] = 1
        else:
          if cellState == 3:
            self.newBoard[i][j] = 1
          else:
            self.newBoard[i][j] = 0
    return self.newBoard

  def printBoard (self, board, w, h):
    for i in range(w):
      for j in range(h):
        print (self.board[i][j], end="")
      print (" ")
    return

def main():
  parser = argparse.ArgumentParser(
      description="GameofLife. Default 30 generations of the 'infinite' seed"
  )
  parser.add_argument("--universe-size", type=str, default="30,30",
      help="comma-separated dimensions of universe (x by y)",
  )
  parser.add_argument(
      "-seed", type=str, default="glider", help="seed for Life"
  )
  parser.add_argument(
      "-n", type=int, default=30, help="number of universe iterations"
  )
  parser.add_argument("-quality", type=int, default=200, help="image quality in DPI")
  parser.add_argument("-cmap", type=str, default="binary", help="colour scheme")
  parser.add_argument(
      "-interval",
      type=int,
      default=300,
      help="interval (in milliseconds) between iterations",
  )
#	parser.add_argument(
#			"--seed-position",
#			type=str,
#			default="40,40",
#			help="comma-separated coordinates of seed",
#	)
  args = parser.parse_args()
  w = int(args.universe_size.split(",")[0])
  h = int(args.universe_size.split(",")[1])
  generations = int(args.n)
  seed = str(args.seed)
  board = [ [] ]
  game = GameOfLife(w, h, seed)
  print ("Simulating the universe ...")
  # Print the initial board
  game.printBoard(game.board, w , h)
  fig = plt.figure(dpi=int(args.quality))
  plt.axis("off")
  plt.grid(True)
  ims = []
  for gen in range(generations):
    ims.append((plt.imshow(game.board, cmap="binary"),))
    game.board = game.genNextState(game.board, w, h)
    #print ("Generation #", gen)
    #game.printBoard(game.board, w , h)

  im_ani = animation.ArtistAnimation(
      fig, ims, interval=int(args.interval), repeat_delay=3000, blit=True)
  im_ani.save((str(args.seed) + ".gif"), writer="imagemagick")

if __name__ == "__main__":
  main()


