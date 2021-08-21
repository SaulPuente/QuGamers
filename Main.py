# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:35:18 2021

@author: saulp
"""


import pygame as p
import GameEngine
import ArmyCode
import QuantumEngine

WIDTH = 700
HEIGHT = 512
DIMENSION = 10
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
#--------------------------------------------------------
p.display.set_caption("Quantum Emblem") 

ipos1 = [(0,0),(1,0),(2,0),(0,1),(1,1)]
ipos2 = [(DIMENSION-1,DIMENSION-1),(DIMENSION-1,DIMENSION-2),(DIMENSION-1,DIMENSION-3),
         (DIMENSION-2,DIMENSION-1),(DIMENSION-2,DIMENSION-2)]

images1 = ["wS0","wS1","wS2","wS3","wS4"]
images1H = ["wS0H","wS1H","wS2H","wS3H","wS4H"]
images2 = ["bS0","bS1","bS2","bS3","bS4"]
images2H = ["bS0H","bS1H","bS2H","bS3H","bS4H"]

nSoldiers = 0

background = p.transform.scale(p.image.load("images/TX Tileset Grass.png"), (SQ_SIZE*DIMENSION, SQ_SIZE*DIMENSION))

quantumGame = False  #probar las características cuánticas del juego
#_--------------------------------


def loadImages():
    pieces = ["bR","bN","bB","bQ","bK","bp","wR","wN","wB","wQ","wK","wp", "bpH", "wpH", 
              "wS0", "wS0H", "wS1", "wS1H", "wS2", "wS2H", "wS3", "wS3H", "wS4", "wS4H",
              "bS0","bS1","bS2","bS3","bS4","bS0H","bS1H","bS2H","bS3H","bS4H"]
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        

showing = "intro" 

p.init()   

song = '8_Bit_Adventure.mp3'
p.mixer.init()
p.mixer.music.load(song)
p.mixer.music.play(-1)
p.event.wait()
logo = p.transform.scale(p.image.load("images/logo.png"), (WIDTH, HEIGHT))
fondo = p.transform.scale(p.image.load("images/fondo.png"), (WIDTH, HEIGHT))

def main():
    global running 
    global showing
    running = True
    while running:
        for event in p.event.get():
                #print(event)
                if event.type == p.QUIT:
                    p.quit()
                    #quit()
        if showing == "intro":
            intro()
        elif showing == "game":
            playGame()
    
    
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100)
 
# defining a font
smallfont = p.font.SysFont('Corbel',35)

text = smallfont.render('Start' , True , color)  

def intro():
    #global running
    global showing
    
    intro = True
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(255,255,255,50))
    mouse = (0,0)
    while intro:
        for e in p.event.get():
            if e.type == p.QUIT:
                showing = "-"
                intro = False
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse = p.mouse.get_pos()
                if HEIGHT*7/8 - 50 <= mouse[1] <= HEIGHT*7/8 + 50 and WIDTH/2 - 20 <= mouse[0] <= WIDTH/2 + 20: 
                    showing = "game"
                    intro = False
                    quit()
        drawStartMenu(screen, mouse)           
        clock.tick(MAX_FPS)
        p.display.flip()
    #running = True
    
def drawStartMenu(screen, mouse):
    screen.fill((60,25,60)) 
    
    screen.blit(fondo, p.Rect(0,0,WIDTH,HEIGHT))
    screen.blit(logo, p.Rect(0,0,WIDTH,HEIGHT))
    # superimposing the text onto our button 
    if HEIGHT*7/8 - 50 <= mouse[1] <= HEIGHT*7/8 + 50 and WIDTH/2 - 20 <= mouse[0] <= WIDTH/2 + 20:
        p.draw.rect(screen,color_light,[WIDTH/2 - 20,HEIGHT*7/8 - 50,100,40]) 
          
    else: 
        p.draw.rect(screen,color_dark,[WIDTH/2 - 20,HEIGHT*7/8 - 50,100,40]) 
    screen.blit(text , (WIDTH/2-10,HEIGHT*7/8 - 45)) 
      
    # updates the frames of the game 
    p.display.update() 
    

def playGame():
    global nSoldiers
    global running
    global showing
    clickedd = False
    #status = ""
    
    #-------
    #p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(255,255,255,50))
    gs = GameEngine.GameState(DIMENSION)
    ###########
    whiteArmy = createArmy(images1, images1H, ipos1)
    blackArmy = createArmy(images2, images2H, ipos2)
    
    putSoldiers(gs, whiteArmy)
    putSoldiers(gs, blackArmy)
    
    superposition = False
    cont = False
    x = False
    y = False
    z = False
    cx = False
    m = False
    
    validMoves = gs.getValidMoves()
    validAttacks = gs.getAllPossibleAttacks()
    
    qc1 = QuantumEngine.circuit()
    for soldier in whiteArmy:
        qc1.addQubit(soldier.qubit.qr)#,soldier.qubit.cr)
    qc2 = QuantumEngine.circuit()
    for soldier in blackArmy:
        qc2.addQubit(soldier.qubit.qr)#,soldier.qubit.cr)
    
    gs.spa = (nSoldiers+1)//2
    ##############3
    moveMade = False #flag variable for when a move is made
    loadImages()
    #running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                showing = "-"
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                    
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                    
                #--------------------------------
                
                if len(playerClicks) == 1 and (playerClicks[0][0] >= 0 
                    and playerClicks[0][0] < DIMENSION) and (playerClicks[0][1] >= 0 
                    and playerClicks[0][1] < DIMENSION):
                    clickedd = True
                    gs.selectPiece(row,col)
                    
                    gs.selectedPiece = gs.board[row][col]
                    
                    #print(gs.selectedPiece.status["ID"],gs.spa)
                    #print(type(gs.selectedPiece.status["ID"]),type(gs.spa))
                    if gs.selectedPiece != "--":
                        if gs.selectedPiece.status["image1"][0] == 'w'  and gs.whiteToMove:
                            if x:
                                qc1.X(gs.selectedPiece.qubit.qr)
                                x = False
                            if y:
                                qc1.Y(gs.selectedPiece.qubit.qr)
                                y = False
                            if z:
                                qc1.Z(gs.selectedPiece.qubit.qr)
                                z = False
                            if m  and gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                                qc1.collapse(gs.selectedPiece,gs)
                                m = False
                                
                            
                            gs.selectedPiece.status["prob0"], gs.selectedPiece.status["prob1"] = QuantumEngine.get_probs(qc1.qc,gs.selectedPiece.status["ID"],gs.spa)
                            
                        elif gs.selectedPiece.status["image1"][0] == 'b' and not gs.whiteToMove:
                            if x:
                                qc2.X(gs.selectedPiece.qubit.qr)
                                x = False
                            if y:
                                qc2.Y(gs.selectedPiece.qubit.qr)
                                y = False
                            if z:
                                qc2.Z(gs.selectedPiece.qubit.qr)
                                z = False
                            if m  and gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                                qc2.collapse(gs.selectedPiece,gs)
                                m = False
                                
                            gs.selectedPiece.status["prob0"], gs.selectedPiece.status["prob1"] = QuantumEngine.get_probs(qc2.qc,gs.selectedPiece.status["ID"] - gs.spa,gs.spa)
                            
                else:
                    clickedd = False
                    
                #---------------------------------
                #Intento de superposición ---------------------------------------------
                if superposition and cont==False: #clickedd se hace falso cuando das clic una tercera vez
                    
                #    len(playerClicks) == 3
                    
                    if len(playerClicks) == 3 and (playerClicks[0][0] >= 0 
                    and playerClicks[0][0] < DIMENSION) and (playerClicks[0][1] >= 0 
                    and playerClicks[0][1] < DIMENSION) and (playerClicks[1][0] >= 0 
                    and playerClicks[1][0] < DIMENSION) and (playerClicks[1][1] >= 0 
                    and playerClicks[1][1] < DIMENSION) and (playerClicks[2][0] >= 0 
                    and playerClicks[2][0] < DIMENSION) and (playerClicks[2][1] >= 0 
                    and playerClicks[2][1] < DIMENSION):
                        move1 = GameEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                        move2 = GameEngine.Move(playerClicks[0],playerClicks[2], gs.board)
                        
                        
                    #print(gs.board)
                        print(move1.getChessNotation())
                        print(move2.getChessNotation())
                        if move1 in validMoves and move2 in validMoves:
                            gs.makeMove(move1)
                            gs.makeMove(move2,superposition)
                            
                            moveMade = True
                            
                            if gs.selectedPiece.status["image1"][0] == 'w':
                                qc1.H(gs.selectedPiece.qubit.qr)
                            elif gs.selectedPiece.status["image1"][0] == 'b':
                                qc2.H(gs.selectedPiece.qubit.qr)
                            
                        #print(move2.getChessNotation())
                        #if move2 in validMoves:
                            #gs.makeMove(move2,superposition)
                            #moveMade = True
                        
                        print(gs.board[playerClicks[1][0]][playerClicks[1][1]])
                        print(gs.board[playerClicks[2][0]][playerClicks[2][1]])
                        
                        sqSelected = ()
                        playerClicks = []
                        superposition = False
                        
                elif len(playerClicks) == 2 and (playerClicks[0][0] >= 0 
                    and playerClicks[0][0] < DIMENSION) and (playerClicks[0][1] >= 0 
                    and playerClicks[0][1] < DIMENSION) and (playerClicks[1][0] >= 0 
                    and playerClicks[1][0] < DIMENSION) and (playerClicks[1][1] >= 0 
                    and playerClicks[1][1] < DIMENSION):
                    cont=True
                    move = GameEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    #print(gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
                else:
                    cont=False
                #------------------------------------------------------------------------------
                
                    #status += move.getChessNotation() +"\n"
                    #font = p.font.SysFont(None, 24)
                    #img = font.render(status, True, p.Color("black"))
                    #screen.blit(img, p.Rect(520, 0,88,512))
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_h and len(playerClicks) > 0:
                    if not gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                        print(gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"])
                        superposition = True
                if e.key == p.K_d:
                    print(qc1.qc)
                    print(qc2.qc)
                if e.key == p.K_x:
                    x = True
                if e.key == p.K_y:
                    y = True
                if e.key == p.K_z:
                    z = True
                if e.key == p.K_m:
                    m = True
                    
                #------------------------------------------------------------------------------
                
                    #status += move.getChessNotation() +"\n"
                    #font = p.font.SysFont(None, 24)
                    #img = font.render(status, True, p.Color("black"))
                    #screen.blit(img, p.Rect(520, 0,88,512))
            #key handlers
            #elif e.type == p.KEYDOWN:
             #   if e.key == p.K_z: #undo when z is pressed
              #      gs.undoMove()
               #     moveMade = True
                #if e.key == p.K_h:
                 #   superposition = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
########################3333
            validAttacks = gs.getAllPossibleAttacks()
############################3333
            moveMade = False
            
        #print(qc1)
        #print(qc2)
        drawGameState(screen, gs, clickedd, validMoves, sqSelected, validAttacks)
        clock.tick(MAX_FPS)
        p.display.flip()
####################3
def highlightSquares(screen,gs, validMoves, sqSelected, validAttacks):
    if sqSelected != ()  and (sqSelected[0] >= 0 and sqSelected[0] < DIMENSION) and (sqSelected[1] >= 0 and sqSelected[1] < DIMENSION): #if theres a square selected
        r,c = sqSelected 
        if isinstance(gs.board[r][c],ArmyCode.soldier):
            if gs.board[r][c].status["image1"][0] == ("w" if gs.whiteToMove else "b"): # if sqSelected is the color of the person on turn
            #highlight selected square
                s = p.Surface((SQ_SIZE,SQ_SIZE))
                s.set_alpha(50) #transparency value [0-255]
                s.fill(p.Color('green'))
                screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
                s.fill(p.Color("blue"))
                for move in validMoves:
                    if move.startRow == r and move.startCol ==c:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
                s.fill(p.Color("red"))
                for move in validAttacks:
                    if move.startRow == r and move.startCol ==c:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
                        
                        
def writeStatus(screen,soldier):
    for i, item in enumerate(soldier.status.items()):
        if 5 + 24*(i+1) < HEIGHT and i < 9:
            screen.blit(p.font.SysFont(None, 24).render(item[0] + ": " + str(item[1]), 0, p.Color("black")), (520, 5 + 24*i))
    
################      
        
 
        
def drawGameState(screen,gs, clickedd, validMoves, sqSelected,validAttacks):
    screen.blit(background, (0,0))
    drawBoard(screen)
    if clickedd and (sqSelected[0] >= 0 and sqSelected[0] < DIMENSION) and (sqSelected[1] >= 0 and sqSelected[1] < DIMENSION):
 #       drawPossibleMoves(screen,gs.row,gs.col)
        ##################
        highlightSquares(screen, gs, validMoves, sqSelected, validAttacks)
        
        if gs.selectedPiece != "--":
            writeStatus(screen,gs.selectedPiece)
        ##################
    drawPieces(screen, gs.board)
    
    #----------
    #lines = gs.moves.splitlines()
    #for i, l in enumerate(lines):
    #    if 5 + 24*(i+1) < HEIGHT:
    #        screen.blit(p.font.SysFont(None, 24).render(l, 0, p.Color("black")), (520, 5 + 24*i))
    
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE),2)
    p.draw.rect(screen,p.Color("white"), p.Rect(DIMENSION*SQ_SIZE,0, WIDTH - DIMENSION*SQ_SIZE, HEIGHT))
    
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                if piece.status["superposition"] == False:
                    screen.blit(IMAGES[piece.status["image1"]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(IMAGES[piece.status["image2"]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Intentando generar unidades para el ejercito
def createArmy(im1, im2, pos):
    global nSoldiers
    
    army = []
    
    for i in range(len(im1)):
        army.append(ArmyCode.soldier())
        
        army[i].status["state0"] = (pos[i][0],pos[i][1])
        army[i].status["state1"] = (pos[i][0],pos[i][1])
        army[i].status["istate"] = (pos[i][0],pos[i][1])
        
        army[i].status["image1"] = im1[i]
        
        army[i].status["image2"] = im2[i]
        
        army[i].status["ID"] = nSoldiers
        
        army[i].createQubit()
        
        nSoldiers += 1
        
    return army
        

#Intento de colocar las unidades en el tablero
def putSoldiers(gs, army):
    for soldier in army:
        gs.board[soldier.status["state0"][0]][soldier.status["state0"][1]] = soldier
        

        
#------------------------------    
"""
def drawPossibleMoves(screen,row,col):
    for i in range(-3,4):
        for j in range(-3,4):
            if (i**2 + j**2 <= 2**2) and (i + row >= 0 and i + row < DIMENSION and j + col >= 0 and j + col < DIMENSION):
                p.draw.rect(screen,p.Color(0,0,255,50), p.Rect((col+j)*SQ_SIZE,(row+i)*SQ_SIZE, SQ_SIZE, SQ_SIZE),3)
            elif (i**2 + j**2 > 2**2) and (abs(i) + abs(j) <= 3) and (i + row >= 0 and i + row < DIMENSION and j + col >= 0 and j + col < DIMENSION):
              #  print(i,j)
                p.draw.rect(screen,p.Color(255,0,0,50), p.Rect((col+j)*SQ_SIZE,(row+i)*SQ_SIZE, SQ_SIZE, SQ_SIZE),3)
"""
#___________________________________________

if __name__ == "__main__":
    main()
    
p.quit()