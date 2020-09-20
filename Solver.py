import Maze
import random
import numpy as np
from PIL import Image
from collections import namedtuple

class Maze_Solver(object):
    def __init__(self, maze:Maze.Maze):
        self.maze = maze

        self.vertices = []
        self.edges = []

        self.width = self.maze.width
        self.length = self.maze.length
        self.board = self._blank_grid()

    def _blank_grid(self):
        zero = np.zeros((self.length, self.width))
        for y in range(self.length):
            for x in range(self.width):
                if self.board[y][x] in ['S', 'E', '.']:
                    zero[y, x] = 1

        return zero

    def _add_directions(self, current, dir):
        pass

    def _create_graph(self):
        queue = []
        queue.append([1, 0])

        visited = []
        previous = None

        while len(queue) > 0:
            current = queue.pop()

            visited.append(current)

            local_dots = list(self.neighbours(current[0], current[1]))
            local_dots = list(filter(lambda x: self.board[current[1], current[1]] == 1, local_dots))

            if len(local_dots) == 1:
                dir = [current[0] - local_dots[0][0], current[1] - local_dots[0][1]]



            else:
                pass

            if previous is None:
                previous = current

    def neighbours(self, x:int, y:int):
        for yp in range(-1, 2):
            for xp in range(-1, 2):
                if xp + x < 0 or xp + x > self.width:
                    continue

                if yp + y < 0 or yp + y > self.length:
                    continue

                yield xp + x, yp + y


def main():
    pass

if __name__ == '__main__':
    main()