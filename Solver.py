import Maze
import random
import numpy as np
from PIL import Image
import time
from pprint import pprint

class Maze_Solver(object):
    def __init__(self, maze:Maze.Maze):
        self.maze = maze

        self.vertices = []
        self.edges = []

        self.width = self.maze.width
        self.length = self.maze.length
        self.start_pos = None
        self.exit_pos = None
        self.board = self._get_2d()

        self._create_graph()

    def _get_2d(self):
        ascii = self.maze.simple_ascii()
        zero = np.zeros((len(ascii[0]), len(ascii)))

        for y in range(len(ascii)):
            for x in range(len(ascii[y])):
                if ascii[y][x] == '.':
                    zero[y, x] = 1
                elif ascii[y][x] == 'S':
                    self.start_pos = [x, y]
                    zero[y, x] = 1
                elif ascii[y][x] == 'E':
                    self.exit_pos = [x, y]
                    zero[y, x] = 1

        return zero

    def _add_directions(self, current, dir):
        dim = self.board.shape

        if current[0] + dir[0] < 0 or current[0] + dir[0] >= dim[1]:
            return -1

        if current[1] + dir[1] < 0 or current[1] + dir[1] >= dim[0]:
            return -1

        return [current[0] + dir[0], current[1] + dir[1]]

    def _look_around(self, position):
        if [position[0] - 1, position[1]] in self.vertices:
            return [position[0] - 1, position[1]]

        if [position[0] + 1, position[1]] in self.vertices:
            return [position[0] + 1, position[1]]

        if [position[0], position[1] - 1] in self.vertices:
            return [position[0] , position[1] - 1]

        if [position[0], position[1] + 1] in self.vertices:
            return [position[0], position[1] + 1]

    def _create_graph(self):
        queue = []
        queue.append(self.start_pos)
        # self.vertices.append(self.start_pos)
        # self.vertices.append(self.exit_pos)

        visited = []
        previous = None

        while len(queue) > 0:
            current = queue.pop(0)
            visited.append(current)

            if previous is not None:
                previous = self._look_around(current)

            local_dots = list(map(list, self.neighbours(current[0], current[1])))
            local_dots = list(filter(lambda i: self.board[i[1], i[0]] == 1 and i not in visited, local_dots))

            if len(local_dots) > 1:
                for x in local_dots[1:]:
                    if x not in visited and self.board[x[1], x[0]] == 1:
                        queue.append(list(x))

            elif len(local_dots) == 0:
                self.vertices.append(current)
                continue

            dir = [local_dots[0][0]-current[0], local_dots[0][1]-current[1]]

            next_pos = self._add_directions(current, dir)
            local_dots = list(map(list, self.neighbours(next_pos[0], next_pos[1])))
            local_dots = list(filter(lambda x: self.board[x[1], x[0]] == 1 and x not in visited, local_dots))

            while len(local_dots) in [0, 1] and next_pos not in self.vertices and next_pos not in  visited:
                temp_next = self._add_directions(next_pos, dir)

                if temp_next == -1 or self.board[temp_next[1], temp_next[0]] == 0:
                    break

                visited.append(next_pos)
                next_pos = self._add_directions(next_pos, dir)
                local_dots = list(map(list, self.neighbours(next_pos[0], next_pos[1])))
                local_dots = list(filter(lambda x: self.board[x[1], x[0]] == 1 and x not in visited, local_dots))

            self.vertices.append(list(next_pos))

            if previous == None:
                previous = current
                self.vertices.append(previous)

            self.edges.append([previous, next_pos])

            queue.append(next_pos)

    def neighbours(self, x:int, y:int):
        l, w = self.board.shape

        for yp in range(-1, 2):
            for xp in range(-1, 2):
                if abs(xp) == abs(yp):
                    continue

                if xp + x < 0 or xp + x >= w:
                    continue

                if yp + y < 0 or yp + y >= l:
                    continue

                yield xp + x, yp + y

    def show_nodes(self):
        l, w = self.board.shape

        img = Image.new('RGB', (w, l), color=(0, 0, 0))
        arr = np.array(img)

        for y in range(l):
            for x in range(w):
                if self.board[y, x] == 1:
                    arr[y, x] = (255, 255, 255)

        for x in self.vertices:
            arr[x[1], x[0]] = (0, 0, 255)

        new_img = Image.fromarray(arr.astype('uint8'), 'RGB')
        new_img.save("updated.png")


def main():
    m = Maze.Maze(length=6, width=6)
    m.iterative_backtrack()
    m.convert_to_image()

    sol = Maze_Solver(m)
    sol.show_nodes()


if __name__ == '__main__':
    main()
