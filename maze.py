# Batuhan Yenidunya
#
# 01.06.2020 | A* Search for Maze Solving

import sys
import argparse

# Parsing command line inputs before Kivy parser.
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--rows", help="number of rows in maze")
parser.add_argument("-c", "--cols", help="number of cols in maze")

args = parser.parse_args()
sys.argv = [sys.argv[0]]

# IMPORTS
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionPrevious
import numpy as np

# Global variables
MainSelectionTitle = ActionPrevious(title='Selected: Road', with_previous=False, app_icon="icon_transparent.ico")
SELECTION = "r"
GRID = []  # Main grid for maze

# Maze's node template. Crates border for nodes.
Builder.load_string("""
<Node>:
    canvas.before:
        Color:
            rgba: .5, .5, .5, 0.6
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
""")

# Node's in Maze
class Node(ButtonBehavior, Label):
    def __init__(self, X, Y):
        super(Node, self).__init__()
        self.status = "w"
        self.X = X
        self.Y = Y 
        self.g = 0
        self.f = 0
        self.neighbors = []
        self.previous = None

    def lint(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 255, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

    def normalize(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 0.6)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.status = "w"
        self.g = 0
        self.f = 0
        self.previous = None

    def addNeighbors(self):
        global GRID
        xs = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        ys = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        for (xa, ya) in zip(xs, ys):
            try:
                if xa == 0 and ya == 0:
                    continue
                if self.X + xa < 0:
                    continue
                if self.Y + ya < 0:
                    continue
                if GRID[self.X + xa][self.Y + ya] not in self.neighbors and GRID[self.X + xa][self.Y + ya].status != "w":
                    self.neighbors.append(GRID[self.X + xa][self.Y + ya])
            except Exception:
                pass

    def on_press(self):
        global SELECTION, GRID
        
        self.canvas.before.clear()

        if self.status != "w":
            with self.canvas.before:
                Color(0.5, 0.5, 0.5, 0.6)
                Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
            self.status = "w"
            return    

        if SELECTION == "r":
            with self.canvas.before:
                Color(255, 255, 255, 0.7)
                Rectangle(pos=self.pos, size=self.size)
            self.status = "r"

        elif SELECTION == "st":
            with self.canvas.before:
                Color(0, 1, 0, 0.7)
                Rectangle(pos=self.pos, size=self.size)
            self.status = "st"

        elif SELECTION == "e":
            with self.canvas.before:
                Color(1, 0, 0, 0.7)
                Rectangle(pos=self.pos, size=self.size)
            self.status = "e"

    def on_release(self):
        global SELECTION, MainSelectionTitle
        SELECTION = "r"
        MainSelectionTitle.title = "Selected: Road"

def a_star_search(GRID):

    # Cost function used for both heuristic and path. 
    # you can implement manhattan distance for path cost if you want. 
    def euclideanDist(a, b):
        p1 = np.array((a.X, a.Y))
        p2 = np.array((b.X, b.Y))
        distance = np.linalg.norm(p2 - p1)
        return distance

    rows = len(GRID)
    cols = len(GRID[0])
    startNode = None
    endNode = None

    for i in range(rows):
        for j in range(cols):
            if GRID[i][j].status == "st":
                startNode = GRID[i][j]
            if GRID[i][j].status == "e":
                endNode = GRID[i][j]

    for i in range(rows):
        for j in range(cols):
            GRID[i][j].g = euclideanDist(startNode, GRID[i][j])
            GRID[i][j].addNeighbors()

    openSet = []
    closeSet = []
    openSet.append(startNode)

    winner = 0
    while len(openSet) > 0:
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i

        current = openSet[winner]

        if current == endNode:
            path = []
            temp = current
            path.append(temp)
            print(startNode.previous)
            while temp.previous is not None:
                path.append(temp.previous)
                temp = temp.previous
            return path

        openSet.remove(current)
        closeSet.append(current)

        neighbors = current.neighbors

        for neighbor in neighbors:
            if neighbor not in closeSet:
                tempG = current.g + euclideanDist(current, neighbor)
                newPath = False
                if neighbor in openSet and tempG < neighbor.g:
                    neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    newPath = True
                    openSet.append(neighbor)
                if newPath:
                    neighbor.h = euclideanDist(neighbor, endNode)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current
    return 0

class Maze(App):

    def __init__(self, rows, cols):
        super(Maze, self).__init__()
        global GRID
        self.rows = rows
        self.cols = cols
        GRID = [[0 for x in range(cols)] for y in range(rows)]

    def Start(self, btn):
        global SELECTION, MainSelectionTitle
        SELECTION = "st"
        MainSelectionTitle.title = "Selected: Start"

    def End(self, btn):
        global SELECTION, MainSelectionTitle
        SELECTION = "e"
        MainSelectionTitle.title = "Selected: End"
        
    def Search(self, btn):
        global GRID, MainSelectionTitle
        MainSelectionTitle.title = "Searching..."
        path = a_star_search(GRID)
        if path != 0:
            for node in path:
                node.lint()
            MainSelectionTitle.title = "Done, requires restart"
        else:
            MainSelectionTitle.title = "No solution, requires restart"

    def Restart(self, btn):
        global GRID, SELECTION, MainSelectionTitle
        MainSelectionTitle.title = "Restarting..."
        for i in range(self.rows):
            for j in range(self.cols):
                GRID[i][j].normalize()
        SELECTION = "r"
        MainSelectionTitle.title = "Selected: Road"

    def build(self):
        global MainSelectionTitle, GRID, BACKUP_GRID
        
        maze = self
        root = GridLayout(cols=1, rows=2, spacing=[1, 1])  # Root layout for app. 
        actionbar = ActionBar(pos_hint={'top': 0})  # ActionBar for menu
        actionview = ActionView()
        
        ap2 = ActionPrevious(title='A*', with_previous=False, app_icon="icon_transparent.ico")
        actionview.add_widget(MainSelectionTitle)
        actionview.add_widget(ap2)

        start = ActionButton(text='Start', on_press=maze.Start)
        end = ActionButton(text='End', on_press=maze.End)
        search = ActionButton(text='Search', on_press=maze.Search)
        res = ActionButton(text='Restart', on_press=maze.Restart)

        actionview.add_widget(start)
        actionview.add_widget(end)
        actionview.add_widget(search)
        actionview.add_widget(res)

        actionbar.add_widget(actionview)
        root.add_widget(actionbar)

        layout = GridLayout(cols=self.cols, rows=self.rows, spacing=[5, 5])  # Maze layout
        
        # Initializing maze
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                node = Node(i, j)
                layout.add_widget(node)
                GRID[i][j] = node
        
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    if int(args.rows) and int(args.cols):
        print("STARTING Kivy Window")
        Maze(int(args.rows), int(args.cols)).run()  # Main app
    else:
        raise NotImplementedError("Please enter # of rows and cols with -r and -c")
