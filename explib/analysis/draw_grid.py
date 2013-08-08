import math, os, time

import pygame
from goals.gfx import render
import exp

def gridify(data, n, m):
    grid = [[None for _ in range(m)] for _ in range(n)]
    for i, d in enumerate(data):
        grid[i/n][i%n] = d

    return grid


class TestGridRenderer(render.Renderer):

    def __init__(self, window, testset, results, size = (800, 800), margin = 0):
        render.Renderer.__init__(self, window, size = size, margin = margin)
        self.window = window
        self.res = int(round(math.sqrt(len(testset))))
        self.testgrid = gridify(testset, self.res, self.res)
        self.testcolor = (180, 180, 180)
        self.resgrids = [gridify([r_i[1] for r_i in res], self.res, self.res) for res in results]
        self.colors = [(0, 21, 80), (189, 21, 80)]

    def draw_grid(self, point_grid, color = (255, 0, 0)):
        for i in range(self.res):
            for j in range(self.res):
                x, y, _ = point_grid[i][j]

                pygame.draw.circle(self.canvas, color, self.coo2screen(x, y), 3)
                if i > 0:
                    x_W, y_W, _ = point_grid[i-1][j]
                    pygame.draw.line(self.canvas, color, self.coo2screen(x, y), self.coo2screen(x_W, y_W))
                if j > 0:
                    x_N, y_N, _ = point_grid[i][j-1]
                    pygame.draw.line(self.canvas, color, self.coo2screen(x, y), self.coo2screen(x_N, y_N))

    def draw(self):
        self.draw_grid(self.testgrid, color = self.testcolor)
        for i, rg in enumerate(self.resgrids):
            self.draw_grid(rg, color = self.colors[i%len(self.colors)])

    def coo2screen(self, x, y):
        return int(50+700*x), int(50+700*y)

if __name__ == "__main__":

    datadir = "~/Research/local/data/interact"
    datadir = os.path.expanduser(datadir)

    filename = "primary[0_0001].test"
    data = exp.load_test(datadir, filename)
    ticks   = data["ticks"]
    testset = data["testset"]
    presults = data["results"]

    filename = "secondary[0_0001][0_0001].test"
    data = exp.load_test(datadir, filename)
    ticks   = data["ticks"]
    testset = data["testset"]
    sresults = data["results"]

    window = render.PygameWindow(size = (800, 800))
    tgrid = TestGridRenderer(window, testset, [sresults[-1]])

    window.update()
    while True:
        time.sleep(1.0)
