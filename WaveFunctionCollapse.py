import pygame
import numpy
import random
 
pygame.init()
 
FPS = 5000
 
SCREENWIDTH, SCREENHEIGHT = 800,800
 
WIDTH = 200
HEIGHT = 200
BOXWIDTH = SCREENWIDTH / WIDTH
BOXHEIGHT = SCREENHEIGHT / HEIGHT
 
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RORANGE = (255,70,0)
ORANGE = (255,180,0)
DGREEN = (0,140,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
 
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Wave Function Collapse")
clock = pygame.time.Clock()
 
font8 = pygame.font.Font("freesansbold.ttf",8)
def DrawTextSmall(surface, txt, color, pos):
    text = font8.render(txt,1, pygame.Color(color))
    pygame.Surface.blit(surface,text, pos)
 
class Grid:
    def __init__(self):
        self.pos = [Cell() for i in range(WIDTH * HEIGHT)]
        
 
    def Render(self):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                thisCell = self.pos[j * HEIGHT + i]
                if thisCell.IsCollapsed and len(thisCell.options):
                    pygame.draw.rect(screen,thisCell.options[0].color , ((i* BOXWIDTH),(j * BOXHEIGHT), BOXWIDTH, BOXHEIGHT))
                    if thisCell.options[0].sockets[0] == "R1":
                        pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT + (BOXHEIGHT * 0.666)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
                    if thisCell.options[0].sockets[1] == "R1":
                        pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.666)),(j * BOXHEIGHT + (BOXHEIGHT * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
                    if thisCell.options[0].sockets[2] == "R1":
                        pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
                    if thisCell.options[0].sockets[3] == "R1":
                        pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH),(j * BOXHEIGHT + (BOXHEIGHT * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
                    if thisCell.options[0].sockets != ["0","0","0","0"]:
                        pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT + (BOXWIDTH * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
                    #DrawTextSmall(screen, thisCell.options[0].sockets[0], BLACK, ((i* BOXWIDTH + (BOXWIDTH / 2)),(j * BOXHEIGHT)))
                    #DrawTextSmall(screen, thisCell.options[0].sockets[1], BLACK, ((i* BOXWIDTH + BOXWIDTH - 5),(j * BOXHEIGHT + (BOXHEIGHT / 2))))
                    #DrawTextSmall(screen, thisCell.options[0].sockets[2], BLACK, ((i * BOXWIDTH + (BOXWIDTH / 2)),(j * BOXHEIGHT + BOXHEIGHT - 10)))
                    #DrawTextSmall(screen, thisCell.options[0].sockets[3], BLACK, ((i* BOXWIDTH),(j * BOXHEIGHT + (BOXHEIGHT / 2))))
                else:
                    pygame.draw.rect(screen, BLACK, ((i* BOXWIDTH),(j * BOXHEIGHT), BOXWIDTH, BOXHEIGHT))
                    #thisCell = Cell()
 
                #DrawTextSmall(screen,str(len(thisCell.options)),BLACK, ((i* BOXWIDTH), (j * BOXHEIGHT), BOXWIDTH, BOXHEIGHT))

    def SingleRender(self, position):
        thisCell = self.pos[position]
        i = position % WIDTH
        j = position // WIDTH
        if thisCell.IsCollapsed and len(thisCell.options):
            pygame.draw.rect(screen,thisCell.options[0].color , ((i* BOXWIDTH),(j * BOXHEIGHT), BOXWIDTH, BOXHEIGHT))
            if thisCell.options[0].sockets[0] == "R1":
                pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT + (BOXHEIGHT * 0.666)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
            if thisCell.options[0].sockets[1] == "R1":
                pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.666)),(j * BOXHEIGHT + (BOXHEIGHT * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
            if thisCell.options[0].sockets[2] == "R1":
                pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
            if thisCell.options[0].sockets[3] == "R1":
                pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH),(j * BOXHEIGHT + (BOXHEIGHT * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
            if thisCell.options[0].sockets != ["0","0","0","0"]:
                pygame.draw.rect(screen, WHITE, ((i* BOXWIDTH + (BOXWIDTH * 0.333)),(j * BOXHEIGHT + (BOXWIDTH * 0.333)), BOXWIDTH / 3 + 1, BOXHEIGHT / 3 + 1))
 
    def Generate(self):
        possibleTiles = self.LowestEntropy()
        if possibleTiles != None:
            selectedTile = random.choice(possibleTiles)
            if self.pos[selectedTile].IsCollapsed != True:
                self.collapse(selectedTile)
 
    def LowestEntropy(self):
        outputlist = [None]
        for i in range(len(self.pos)):
            thisCell = self.pos[i]
            if thisCell.IsCollapsed == False:
 
                if outputlist[0] == None:
                    outputlist.clear()
                    outputlist.append(i)
                    continue
 
                testingLen = len(thisCell.options)
                currentlen = len(self.pos[outputlist[0]].options)
 
                if  testingLen < currentlen:
                    outputlist.clear()
                    outputlist.append(i)
 
                elif testingLen == currentlen:
                    outputlist.append(i)
 
        if outputlist[0] == None:
            return None
        else:
            return outputlist


    def collapse(self, thisPosition):
        thisCell = self.pos[thisPosition]
 
        if len(thisCell.options) == 0:
            thisCell.options.append(Tile("ERROR",PURPLE, ["0","0","0","0"]))
 
        thisCell.options = [random.choice(thisCell.options)]
        thisCell.IsCollapsed = True
        #print(f"X:{posx}, Y:{posy}")
 
        #up
        upOptions = []
        if thisPosition // HEIGHT < HEIGHT - 1:
            othercell = self.pos[thisPosition + WIDTH]
            for option in othercell.options:
                if thisCell.options[0].sockets[0] == option.sockets[2] or thisCell.options[0].sockets[0] == "ANY":
                    upOptions.append(option)
            othercell.options = upOptions
 
        #right
        rightOptions = []
        if thisPosition % WIDTH != WIDTH - 1:
            othercell = self.pos[thisPosition + 1]
            for option in othercell.options:
                if thisCell.options[0].sockets[1] == option.sockets[3] or thisCell.options[0].sockets[1] == "ANY":
                    rightOptions.append(option)
            othercell.options = rightOptions
 
        #down
        downOptions = []
        if thisPosition // HEIGHT != 0:
            othercell = self.pos[thisPosition - WIDTH]
            for option in othercell.options:
                if thisCell.options[0].sockets[2] == option.sockets[0] or thisCell.options[0].sockets[2] == "ANY":
                    downOptions.append(option)
            othercell.options = downOptions
 
        #left
        leftOptions = []
        if thisPosition % WIDTH != 0:
            othercell = self.pos[thisPosition - 1]
            for option in othercell.options:
                if thisCell.options[0].sockets[3] == option.sockets[1] or thisCell.options[0].sockets[3] == "ANY":
                    leftOptions.append(option)
            othercell.options = leftOptions

        self.SingleRender(thisPosition)
 
 
class Tile:
    def __init__(self, tile, color, sockets):
        self.tile= tile
        self.color= color
        self.sockets= sockets #clockwise starting from up
        
 
class Cell:
    def __init__(self):
        self.IsCollapsed = False
        self.options = []
        for i in tileSet:
            self.options.append(i)
 
tileSet = [
    #Tile("empty",BLACK, ["0","0","0","0"]),
 
    Tile("rotation0",BLACK, ["R1","R1","0","0"]),
    Tile("rotation1",BLACK, ["0","R1","R1","0"]),
    Tile("rotation2",BLACK, ["0","0","R1","R1"]),
    Tile("rotation3",BLACK, ["R1","0","0","R1"]),
 
    #Tile("Straight0",BLACK, ["R1","0","R1","0"]),
    Tile("Straight1",BLACK, ["0","R1","0","R1"]),
 
    #Tile("End0",BLACK, ["R1","0","0","0"]),
    #Tile("End1",BLACK, ["0","R1","0","0"]),
    #Tile("End2",BLACK, ["0","0","R1","0"]),
    #Tile("End3",BLACK, ["0","0","0","R1"]),
 
    #Tile("Tblock0",BLACK, ["R1","R1","R1","0"]),
    #Tile("Tblock1",BLACK, ["R1","R1","0","R1"]),
    #Tile("Tblock2",BLACK, ["R1","0","R1","R1"]),
    #Tile("Tblock3",BLACK, ["0","R1","R1","R1"]),
 
    #Tile("Crossblock",BLACK, ["R1","R1","R1","R1"]),
 
    #Tile("ERROR", PURPLE, ["error","error","error","error"]),
]
 
def CheckIfClear(grid):
    for cell in grid.pos:
        if len(cell.options) == len(tileSet):
            return
    screen.fill(BLACK)
    grid.pos = [Cell() for i in range(WIDTH * HEIGHT)]
 
def main():
    grid = Grid()
 
    pygame.key.set_repeat(50,50)
    TotalTime = 0
 
    running = True
 
    while running: 
        if TotalTime >= WIDTH * HEIGHT:
            CheckIfClear(grid)
 
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                running = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill(BLACK)
                    grid.pos = [Cell() for i in range(WIDTH * HEIGHT)]
                elif event.key == pygame.K_SPACE:
                    screen.fill(BLACK)
                    grid.Render()
 
        grid.Generate()
        TotalTime += 1
        pygame.display.update()
        clock.tick(FPS)
 
    
 

main()