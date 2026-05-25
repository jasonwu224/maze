# Wilson's algorithm for maze generation

import random as rand
import array as arr
import time

BITMAP = {'N': 1, 'E': 2, 'S': 4, 'W': 8}

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.len = width * height
        self.grid = arr.array('i', [0] * (width * height))

    def __len__(self):
        return self.len

    def __getitem__(self, key):
        "index 2D grid like grid[row, col] or grid[i] where i = row * width + col"
        match key:
            case int():
                row, col = divmod(key, self.width)
            case (row, col):
                pass
            case _:
                raise KeyError("Index correctly idiot")

        return self.grid[row * self.width + col]

    def __setitem__(self, key, value):
        match key:
            case int():
                row, col = divmod(key, self.width)
            case (row, col):
                pass
            case _:
                raise KeyError("Index correctly idiot")

        self.grid[row * self.width + col] = value

    def __str__(self):
        # Top border honors N bits on the first row so entrances can punch through.
        maze_str = "+"
        for x in range(self.width):
            maze_str += ("   " if (self[0, x] & BITMAP['N']) else "---") + "+"
        maze_str += "\n"

        for y in range(self.height):
            # Line 1: left/right wall + interior east walls.
            row_str = " " if (self[y, 0] & BITMAP['W']) else "|"
            for x in range(self.width):
                cell = self[y, x]
                east_wall = " " if (cell & BITMAP['E']) else "|"
                row_str += "   " + east_wall
            maze_str += row_str + "\n"

            row_str = "+"
            for x in range(self.width):
                cell = self[y, x]
                south_wall = "   " if (cell & BITMAP['S']) else "---"
                row_str += south_wall + "+"
            maze_str += row_str + "\n"

        return maze_str

DELTA = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
OPPOSITE = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

def main():
    # Wilson's algorithm to uniformly sample a maze from distribution of all mazes
    # with a loop-erased random walk
    width, height = 10, 10

    grid = Grid(width, height)
    visited = {(rand.randrange(height), rand.randrange(width))}

    while len(visited) < width * height:
        start = (rand.randrange(height), rand.randrange(width))
        if start in visited:
            continue

        # Storing the direction taken from each cell in a dict implicitly
        # erases loops: revisiting a cell overwrites its earlier choice, so
        # following the dict from `start` traces the loop-erased path.
        dirs = {}
        cell = start
        while cell not in visited:
            direction = rand.choice('NESW')
            dy, dx = DELTA[direction]
            ny, nx = cell[0] + dy, cell[1] + dx
            if not (0 <= ny < height and 0 <= nx < width):
                continue
            dirs[cell] = direction
            cell = (ny, nx)
        # carve out the path
        cell = start
        while cell not in visited:
            direction = dirs[cell]
            dy, dx = DELTA[direction]
            next_cell = (cell[0] + dy, cell[1] + dx)

            grid[cell] |= BITMAP[direction]
            grid[next_cell] |= BITMAP[OPPOSITE[direction]]

            (print("\033[H" + str(grid), end="", flush=True))
            time.sleep(0.05)

            visited.add(cell)
            cell = next_cell

    # Punch entrance (top of NW corner) and exit (bottom of SE corner).
    grid[0, 0] |= BITMAP['N']
    grid[height - 1, width - 1] |= BITMAP['S']
    print("\033[H" + str(grid), end="", flush=True)


if __name__ == "__main__":
    main()