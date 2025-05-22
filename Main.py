import pygame
import random
from Constants import *
from Cell import *

def printArr(arr: list) -> None:
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(f'[{j}, {i}]')
            print(arr[i][j].collapsed)
            print(arr[i][j].idx)
            print(arr[i][j].options)
            print("\n")

def validPosition(x:int, y:int) -> bool:
    return x >= 0 and x < SIZE and y >= 0 and y < SIZE

def makeArr(size: int) -> list:
    arr = [] 
    for i in range(size):
        arr.append([]) 
        for j in range(size):
            arr[i].append(Cell())
    
    return arr

def loadImg() -> list:
    pygame.image.load("Images/bridge.png") 
    pygame.image.load("Images/component.png")
    pygame.image.load("Images/connection.png")
    pygame.image.load("Images/corner.png")
    pygame.image.load("Images/dskew.png")
    pygame.image.load("Images/skew.png")
    pygame.image.load("Images/substrate.png")
    pygame.image.load("Images/t.png")
    pygame.image.load("Images/track.png")
    pygame.image.load("Images/transition.png")
    pygame.image.load("Images/turn.png")
    pygame.image.load("Images/viad.png")
    pygame.image.load("Images/vias.png")
    pygame.image.load("Images/wire.png")

    path = ["Images/component.png", "Images/substrate.png", "Images/bridge.png", "Images/connection.png", "Images/corner.png", "Images/dskew.png", "Images/skew.png", "Images/t.png", "Images/track.png", "Images/transition.png", "Images/turn.png", "Images/viad.png", "Images/vias.png", "Images/wire.png"]

    return path

def createRules() -> list:
    rules = [
    ["aaa", "aaa", "aaa", "aaa"], #0
    ["bbb", "bbb", "bbb", "bbb"], #1
    ["bcb", "bdb", "bcb", "bdb"], #2
    ["bcb", "bba", "aaa", "abb"], #3
    ["bbb", "bbb", "bba", "abb"], #4
    ["bcb", "bcb", "bcb", "bcb"], #5
    ["bcb", "bcb", "bbb", "bbb"], #6
    ["bbb", "bcb", "bcb", "bcb"], #7
    ["bcb", "bbb", "bcb", "bbb"], #8
    ["bdb", "bbb", "bcb", "bbb"], #9
    ["bcb", "bcb", "bbb", "bbb"], #10
    ["bbb", "bcb", "bbb", "bcb"], #11
    ["bcb", "bbb", "bbb", "bbb"], #12
    ["bbb", "bdb", "bbb", "bdb"]  #13
    ]

    return rules 

def draw(arr: list, path: list, surface):
    imgWidth = WIDTH // SIZE
    imgHeight = HEIGHT // SIZE
    for i in range(SIZE):
        for j in range(SIZE):
            cell = arr[i][j]
            x = i * imgWidth
            y = j * imgHeight
            if cell.collapsed == False:
                pygame.draw.rect(surface, WHITE, (x, y, imgWidth, imgHeight), 1, border_radius=1)
            else:
                img = pygame.image.load(path[cell.idx]).convert()
                img = pygame.transform.scale(img, (imgWidth, imgHeight))
                surface.blit(img, (x, y))

def findLowestEntropy(arr: list) -> tuple:
    min = 100
    lowest = [] 
    #find minimum first
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if len(arr[i][j].options) <= min and len(arr[i][j].options) != 0:
                min = len(arr[i][j].options)

    #append all the minimums to lowest
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if len(arr[i][j].options) == min and arr[i][j].collapsed == False:
                lowest.append((arr[i][j], (i, j)))
    
    if len(lowest) == 0:
        return None
    else:
        return lowest[random.randint(0, len(lowest) - 1)]

def changeValue(arr: list, rules: list):
    lowest = findLowestEntropy(arr) 
    
    if lowest == None:
        return -1
    cell, (x, y) = lowest 
    cell.collapsed = True
    cell.idx = cell.options[random.randint(0,len(cell.options) - 1)]
    cell.options = []

    for i in range(0, 4):
        #change above cell
        newOptions = [] 
        if i == 0:
            newY = y - 1
            if validPosition(x, newY) and not arr[x][newY].collapsed: 
                newCell = arr[x][newY]
                for j in newCell.options:
                    if rules[cell.idx][0] == rules[j][2][::-1]:
                        newOptions.append(j)
        
                newCell.options = newOptions
        #change right of cell 
        elif i == 1:
            newX = x + 1
            if validPosition(newX, y) and not arr[newX][y].collapsed: 
                newCell = arr[newX][y]
                for j in newCell.options:
                    if rules[cell.idx][1] == rules[j][3][::-1]:
                        newOptions.append(j)
            
                newCell.options = newOptions
        #change below cell 
        elif i == 2:
            newY = y + 1
            if validPosition(x, newY) and not arr[x][newY].collapsed: 
                newCell = arr[x][newY]
                for j in newCell.options:
                    if rules[cell.idx][2] == rules[j][0][::-1]:
                        newOptions.append(j)

                newCell.options = newOptions 
        #change left of cell 
        elif i == 3:
            newX = x - 1
            if validPosition(newX, y) and not arr[newX][y].collapsed: 
                newCell = arr[newX][y]
                for j in newCell.options:
                    if rules[cell.idx][3] == rules[j][1][::-1]:
                        newOptions.append(j)
            
                newCell.options = newOptions
    return 1 

pygame.init()
random.seed(1)
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")
running = True
arr = makeArr(SIZE)
rules = createRules()
path = loadImg()

while running:
    surface.fill(BLACK)
    (x, y) = pygame.mouse.get_pos()
    x = x // (WIDTH // SIZE)
    y = y // (HEIGHT // SIZE)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            changeValue(arr, rules)
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                printArr(arr)
    
    changeValue(arr, rules)
    draw(arr, path, surface)
    pygame.display.update()

pygame.quit()