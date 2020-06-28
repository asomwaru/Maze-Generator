import time
import random
import numpy as np
from PIL import Image


class Node(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False

        # N S E W
        self.walls = [1, 1, 1, 1]

    def clear(self):
        self.walls = [1, 1, 1, 1]
        self.visited = False

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __add__(self, other):
        if type(other) == Node:
            return [self.x + other.x, self.y + other.y]
        elif type(other) == list and len(other) == 2:
            return [self.x + other[0], self.y + other[1]]

    def __sub__(self, other):
        if type(other) == Node:
            return [self.x - other.x, self.y - other.y]
        elif type(other) == list and len(other) == 2:
            return [self.x - other[0], self.y - other[1]]


class Maze(object):
    def __init__(self, length: int = 5, width: int = 5,
                 start_node=(0, 0)):

        self.length = length
        self.width = width

        self.grid = [[Node(x, y) for x in range(self.width)] for y in range(self.length)]

        if type(start_node) in [list, tuple]:
            self.start_node = self.grid[start_node[1]][start_node[0]]
        elif type(start_node) == Node:
            self.start_node = start_node

    def display_maze(self):
        row = [' ']
        for x in range(self.width):
            if self.grid[0][x].walls[0]:
                row.append('_')
            else:
                row.append(' ')

            row.append(' ')

        print("".join(row))

        for y in range(self.length):
            row = []
            for x in range(self.width):
                current = self.grid[y][x]
                if x == 0:
                    if current.walls[3] == 1:
                        row.append('|')
                    else:
                        row.append(' ')

                if current.walls[1] == 1:
                    row.append('_')
                else:
                    row.append(' ')

                if current.walls[2] == 1 and x + 1 < self.width and self.grid[y][x + 1].walls[3] == 1:
                    row.append('|')
                elif current.x == self.width - 1:
                    if current.walls[2] == 1:
                        row.append('|')
                else:
                    row.append(' ')

            print("".join(row))

    def change_wall(self, x: int, y: int, wall: int):
        if wall == 0:
            if y == 0:
                self.grid[y][x].walls[0] = int(not self.grid[y][x].walls[0])
            else:
                self.grid[y][x].walls[0] = int(not self.grid[y][x].walls[0])
                self.grid[y - 1][x].walls[1] = int(not self.grid[y - 1][x].walls[1])

        elif wall == 1:
            if y == self.length - 1:
                self.grid[y][x].walls[1] = int(not self.grid[y][x].walls[1])
            else:
                self.grid[y][x].walls[1] = int(not self.grid[y][x].walls[1])
                self.grid[y + 1][x].walls[0] = int(not self.grid[y + 1][x].walls[0])

        elif wall == 2:
            if x == self.width - 1:
                self.grid[y][x].walls[2] = int(not self.grid[y][x].walls[2])
            else:
                self.grid[y][x].walls[2] = int(not self.grid[y][x].walls[2])
                self.grid[y][x + 1].walls[3] = int(not self.grid[y][x + 1].walls[3])

        elif wall == 3:
            if x == 0:
                self.grid[y][x].walls[3] = int(not self.grid[y][x].walls[3])
            else:
                self.grid[y][x].walls[3] = int(not self.grid[y][x].walls[3])
                self.grid[y][x - 1].walls[2] = int(not self.grid[y][x - 1].walls[2])

    def neighbors(self, x: int, y: int, diagonal: bool = False):
        for yp in range(-1, 2):
            for xp in range(-1, 2):
                if xp == 0 and yp == 0:
                    continue

                if not diagonal and [abs(xp), abs(yp)] == [1, 1]:
                    continue

                if xp + x < 0 or xp + x >= self.width:
                    continue

                if yp + y < 0 or yp + y >= self.length:
                    continue

                yield self.grid[yp + y][xp + x]

    def all_visited(self) -> bool:
        return all([all([self.grid[y][x].visited for x in range(self.width)]) for y in range(self.length)])

    def clear(self):
        for y in range(self.length):
            for x in range(self.width):
                self.grid[y][x].clear()

    @staticmethod
    def wall_exists(first: Node, second: Node, wall: int) -> bool:
        if wall in [0, 2]:
            return first.walls[wall] == second.walls[wall + 1]
        elif wall in [1, 3]:
            return first.walls[wall] == second.walls[wall - 1]

    @staticmethod
    def convert_pos(position):
        directions = {
            "N": [0, -1],
            "S": [0, 1],
            "E": [1, 0],
            "W": [-1, 0]
        }

        coord = {
            'N': 0,
            'S': 1,
            'E': 2,
            'W': 3
        }

        wall = ''

        for x, y in directions.items():
            if position == y:
                wall = x
                break

        wall = coord[wall]
        return wall

    def display_visited(self):
        for y in range(self.length):
            print(*[self.grid[y][x].visited for x in range(self.width)])

    def convert_to_image(self):
        l, w = (self.length * 2) + 1, (self.width * 2) + 1
        offset = 1
        img = Image.new('RGB', (w, l), color=(255, 255, 255))
        arr = np.array(img)

        arr[0, :] = (0, 0, 0)
        arr[:, 0] = (0, 0, 0)
        arr[l - 1, :] = (0, 0, 0)
        arr[:, w - 1] = (0, 0, 0)

        for y in range(self.length):
            for x in range(self.width):
                translate_y = [i + 1 for i in list(range(0, l - 1, 2))]
                translate_x = [i + 1 for i in list(range(0, w - 1, 2))]
                current = self.grid[y][x]

                if current.walls[2]:
                    arr[translate_y[y], translate_x[x] + offset] = (0, 0, 0)
                    arr[translate_y[y] + offset, translate_x[x] + offset] = (0, 0, 0)
                    arr[translate_y[y] - offset, translate_x[x] + offset] = (0, 0, 0)

                if current.walls[1]:
                    arr[translate_y[y] + offset, translate_x[x] + offset] = (0, 0, 0)
                    arr[translate_y[y] + offset, translate_x[x] - offset] = (0, 0, 0)
                    arr[translate_y[y] + offset, translate_x[x]] = (0, 0, 0)

        arr[0,1] = (0, 255, 0)
        arr[l - 1, w - 2] = (255, 0, 0)

        new_img = Image.fromarray(arr.astype('uint8'), 'RGB')
        new_img.save('maze.png')

    def iterative_backtrack(self):
        queue = [self.start_node]

        while len(queue) > 0:
            # self.display_maze()
            current = queue.pop()
            current.visited = True

            available_nodes = [x for x in self.neighbors(current.x, current.y) if not x.visited]
            random.shuffle(available_nodes)

            if len(available_nodes) > 0:
                queue.append(current)
                next_cell = available_nodes.pop()
                position = next_cell - current

                wall = self.convert_pos(position)
                self.change_wall(current.x, current.y, wall)

                queue.append(next_cell)

    def Aldous_Broder(self):
        current = self.start_node

        while not self.all_visited():
            available_nodes = [x for x in self.neighbors(current.x, current.y)]
            next_node = random.choice(available_nodes)

            if not next_node.visited:
                position = next_node - current
                wall = self.convert_pos(position)

                self.change_wall(current.x, current.y, wall)

            current.visited = True
            current = next_node

    # Unfinished
    def hunt_kill(self):
        pass


def main():
    m = Maze(length=30, width=30)

    m.iterative_backtrack()
    m.display_maze()
    m.convert_to_image()


if __name__ == '__main__':
    main()
