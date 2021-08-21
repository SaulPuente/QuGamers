# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:35:18 2021

@author: saulp
"""


import pygame as p
import GameEngine
import ArmyCode
import QuantumEngine

from numpy import pi as pi

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
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse = p.mouse.get_pos()
                if HEIGHT*7/8 - 50 <= mouse[1] <= HEIGHT*7/8 + 50 and WIDTH/2 - 20 <= mouse[0] <= WIDTH/2 + 20: 
                    showing = "game"
                    intro = False
                    #quit()
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
    

import sys


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
    r = False
    
    validMoves = gs.getValidMoves()
    validAttacks = gs.getAllPossibleAttacks()
    
    qc1 = QuantumEngine.circuit()
    for soldier in whiteArmy:
        qc1.addQubit(soldier.qubit.qr)#,soldier.qubit.cr)
    qc2 = QuantumEngine.circuit()
    for soldier in blackArmy:
        qc2.addQubit(soldier.qubit.qr)#,soldier.qubit.cr)
    #print(nSoldiers)
    gs.spa = (nSoldiers)//2
    
    gs.wSoldiers = (nSoldiers)//2
    gs.bSoldiers = (nSoldiers)//2
    
    attackMade = False
    movedPieceID = -1
    
    winner = "draw"
    fff = False
    
    # basic font for user typed
    base_font = p.font.Font(None, 32)
    user_text = ''
  
    # create rectangle
    input_rect = p.Rect(HEIGHT, 330, 140, 32)
  
    #color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = p.Color('lightskyblue3')
  
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = p.Color('chartreuse4')
    color = color_passive
    
    active = False
    
    
    angle = 0
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
                
                if input_rect.collidepoint(e.pos):
                    active = True
                else:
                    active = False
                    
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                #print(gs.whiteToMove,1) 
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                    
                    if 0 < row < DIMENSION and 0 < col < DIMENSION:
                        fff = isinstance(gs.board[row][col], ArmyCode.soldier)
                    
                    #print("wtf1")
                    #---------------------------------------------------------------
                        if moveMade and not attackMade and fff:
                            attackMade = True
                            movedPieceID = -1
                            gs.whiteToMove = not gs.whiteToMove
                            fff = False
                    #print(moveMade)
                        elif not moveMade and fff:
                        #print("wtf2")
                            moveMade = True
                            attackMade = True
                            movedPieceID = -1
                            gs.whiteToMove = not gs.whiteToMove
                            fff = False
                    #print(gs.whiteToMove,2)
                    #---------------------------------------------------------------
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                    
                #--------------------------------
                #print(gs.whiteToMove,3) 
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
                            if r:
                                qc1.R(gs.selectedPiece.qubit.qr,angle)
                                r = False
                            if m  and gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                                v = qc1.collapse(gs.selectedPiece,gs)
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
                            if r:
                                qc2.R(gs.selectedPiece.qubit.qr,angle)
                                r = False
                            if m  and gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                                v = qc2.collapse(gs.selectedPiece,gs)
                                m = False
                                
                            gs.selectedPiece.status["prob0"], gs.selectedPiece.status["prob1"] = QuantumEngine.get_probs(qc2.qc,gs.selectedPiece.status["ID"] - gs.spa,gs.spa)
                            
                else:
                    clickedd = False
                    
                #---------------------------------
                #Intento de superposición ---------------------------------------------
                #print(gs.whiteToMove,4) 
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
                        #print(move1.getChessNotation())
                        #print(move2.getChessNotation())
                        if move1 in validMoves and move2 in validMoves and not moveMade:
                            gs.makeMove(move1)
                            gs.makeMove(move2,superposition)
                            
                            moveMade = True
                            
                            movedPieceID = gs.selectedPiece.status["ID"]
                            
                            if gs.selectedPiece.status["image1"][0] == 'w':
                                qc1.H(gs.selectedPiece.qubit.qr)
                            elif gs.selectedPiece.status["image1"][0] == 'b':
                                qc2.H(gs.selectedPiece.qubit.qr)
                            
                        #print(move2.getChessNotation())
                        #if move2 in validMoves:
                            #gs.makeMove(move2,superposition)
                            #moveMade = True
                        
                        #print(gs.board[playerClicks[1][0]][playerClicks[1][1]])
                        #print(gs.board[playerClicks[2][0]][playerClicks[2][1]])
                        
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
                    #print(move.getChessNotation())
                    if move in validMoves and not moveMade:
                        movedPieceID = gs.selectedPiece.status["ID"]
                        gs.makeMove(move)
                        moveMade = True
                        
                    if move in validAttacks and moveMade and not attackMade and movedPieceID == gs.selectedPiece.status["ID"]:
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                            if playerClicks[0] == gs.board[playerClicks[0][0]][playerClicks[0][1]].status["state0"]:
                                state = 0
                            elif playerClicks[0] == gs.board[playerClicks[0][0]][playerClicks[0][1]].status["state1"]:
                                state = 1
                            if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "w":
                                v = qc1.collapse(gs.selectedPiece,gs)
                            elif gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "b":
                                v = qc2.collapse(gs.selectedPiece,gs)
                            if v == state:
                                if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "w":
                                    gs.makeAttack(move,qc2,gs)
                                elif gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "b":
                                    gs.makeAttack(move,qc1,gs)
                                attackMade = True
                                movedPieceID = -1
                        else:
                            gs.makeAttack(move)
                            attackMade = True
                            movedPieceID = -1
                        
                    if move in validAttacks and not moveMade and not attackMade:
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                            if playerClicks[0] == gs.board[playerClicks[0][0]][playerClicks[0][1]].status["state0"]:
                                state = 0
                            elif playerClicks[0] == gs.board[playerClicks[0][0]][playerClicks[0][1]].status["state1"]:
                                state = 1
                            if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "w":
                                v = qc1.collapse(gs.selectedPiece,gs)
                            elif gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "b":
                                v = qc2.collapse(gs.selectedPiece,gs)
                            if v == state:
                                if gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "w":
                                    gs.makeAttack(move,qc2,gs)
                                elif gs.board[playerClicks[0][0]][playerClicks[0][1]].status["image1"][0] == "b":
                                    gs.makeAttack(move,qc1,gs)
                                attackMade = True
                                moveMade = True
                                movedPieceID = -1
                        else:
                            gs.makeAttack(move)
                            attackMade = True
                            moveMade = True
                            movedPieceID = -1
                    #print(playerClicks[0],playerClicks[1])
                    
                        
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
                if e.key == p.K_u: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_h and len(playerClicks) > 0:
                    if not gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"]:
                        #print(gs.board[playerClicks[0][0]][playerClicks[0][1]].status["superposition"])
                        superposition = True
                if e.key == p.K_d:
                    print(qc1.qc)
                    qc1.qc.draw(output='mpl', filename='circuit1.png')
                    print(qc2.qc)
                    qc2.qc.draw(output='mpl', filename='circuit2.png')
                if e.key == p.K_x:
                    x = True
                if e.key == p.K_y:
                    y = True
                if e.key == p.K_z:
                    z = True
                if e.key == p.K_m:
                    m = True
                if e.key == p.K_r:
                    r = True
                if e.key == p.K_BACKSPACE:
  
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
  
                # Unicode standard is used for string
                # formation
                else:
                    newChar = e.unicode
                    #print(newChar.isdigit())
                    if newChar.isdigit() or newChar == "p" or newChar == "i" or newChar == ".": 
                        user_text += newChar
                if user_text.isdigit():
                    angle = float(user_text)
                elif len(user_text) >= 2:
                    if user_text == "pi":
                        angle = pi
                    elif user_text[-2:] == "pi":
                        angle = float(user_text[:-2])*pi
                    elif user_text == "0.":
                        angle = 0
                    else:
                        for i in range(len(user_text)):
                            if user_text[i] == ".":
                                if len(user_text) > i + 1:
                                    if user_text[-1] != "p":
                                        angle = float(user_text[:i]) + (1/(10**len(user_text[i+1:])))*float(user_text[i+1:])
                                    elif user_text[-1] == ".":
                                        angle = float(user_text[:-1])
                elif len(user_text) == 0 or user_text == ".":
                    angle = 0
                #print(angle)
                
                
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
        #print(gs.whiteToMove,5) 
        
            
        
        if moveMade:
            
########################3333
            #print(gs.whiteToMove,6) 
            validAttacks = gs.getAllPossibleAttacks()
            if not any(validAttacks) and not attackMade:
                #print("?")
                moveMade = False
                attackMade = False
                gs.whiteToMove = not gs.whiteToMove
                validMoves = gs.getValidMoves()
                validAttacks = gs.getAllPossibleAttacks()
            if attackMade:
                validAttacks = gs.getAllPossibleAttacks()
                validMoves = gs.getValidMoves()
                moveMade = False
                attackMade = False
        #print(gs.whiteToMove,7) 
        #print(nSoldiers)
        #print(gs.wSoldiers,gs.bSoldiers)        
        if gs.wSoldiers == 0:
            winner = "Player 2 wins!"
        elif gs.bSoldiers == 0:
            winner = "Player 1 wins!"
            
############################3333
            
        
        
            
        #print(angle)
        #print(qc1)
        #print(qc2)
        drawGameState(screen, gs, clickedd, validMoves, sqSelected, validAttacks, winner)
        
        screen.blit(p.font.SysFont(None, 24).render("Ry's angle:", 0, p.Color("black")), (520, 300))
        if active:
            color = color_active
        else:
            color = color_passive
        # draw rectangle and argument passed which should
        # be on screen
        p.draw.rect(screen, color, input_rect)
  
        text_surface = base_font.render(user_text, True, p.Color("black"))#(255, 255, 255))
        #text_surface = p.font.SysFont(None, 24).render(user_text, True, (255, 255, 255))
      
        # render at position stated in arguments
        
        
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
        #print(user_text)
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
 
    
def writeWinner(screen,winner):
    screen.blit(p.font.SysFont(None, 24).render(winner, 0, p.Color("black")), (520, 5))
################      
        
 
        
def drawGameState(screen,gs, clickedd, validMoves, sqSelected,validAttacks,winner):
    screen.blit(background, (0,0))
    drawBoard(screen)
    if clickedd and (sqSelected[0] >= 0 and sqSelected[0] < DIMENSION) and (sqSelected[1] >= 0 and sqSelected[1] < DIMENSION):
 #       drawPossibleMoves(screen,gs.row,gs.col)
        ##################
        highlightSquares(screen, gs, validMoves, sqSelected, validAttacks)
        
        if winner != "draw":
            writeWinner(screen,winner)
        elif gs.selectedPiece != "--":
            writeStatus(screen,gs.selectedPiece)
    if winner != "draw":
            writeWinner(screen,winner)
    #screen.blit(p.font.SysFont(None, 24).render("Ry's angle:", 0, p.Color("black")), (HEIGHT, 200))
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