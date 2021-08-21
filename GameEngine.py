# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 00:25:39 2021

@author: saulp
"""
import ArmyCode
from Main import DIMENSION
#global DIMENSION

class GameState():
    def __init__(self, n):
        '''
        self.board = [
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],]
        '''
        self.board = [["--" for i in range(n)] for j in range(n)]
        self.whiteToMove = True
        self.moveLog = []
        
        self.moves = " " #-----------
        self.selectedPiece = "--"
        self.spa = 0
    
    def makeMove(self,move,superposition = False):
        #-----------------------------------
        if not superposition:
            move.pieceMoved.status['state0'] = (move.endRow,move.endCol)
            self.whiteToMove = not self.whiteToMove
        else:
            move.pieceMoved.status['state1'] = (move.endRow,move.endCol)
            move.pieceMoved.status['superposition'] = True
        #-----------------------------------
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        
        #-------------
        self.moves = move.getChessNotation() +" \n" + self.moves 
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] =move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    def selectPiece(self, row, col):
        self.row = row
        self.col = col
    def getValidMoves(self):   
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if isinstance(self.board[r][c],ArmyCode.soldier):
                    turn = self.board[r][c].status["image1"][0]
                    if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                        piece = self.board[r][c].status["image1"][1]
                        if piece != '--':
                            self.getBarbieMoves(r,c,moves)
        return moves
    
############################    
    
    def getAllPossibleAttacks(self):
        attacks = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
 #               if self.board[r][c] =="--":
                if isinstance(self.board[r][c],ArmyCode.soldier):
                    turn = self.board[r][c].status["image1"][0]
                    if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                        piece = self.board[r][c].status["image1"][1]
                        if piece != '--':
                            self.getBarbieAttack(r,c,attacks)
        return attacks
    
    
    def getBarbieMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1),(1,1),(-1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            if abs(d[0]) == 1 and abs(d[1]) == 1:
                lim=2
            else:
                lim=3 
            for i in range(1,lim):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece.status["image1"][0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
                
    def getBarbieAttack(self,r,c,attacks):
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,2),(2,-1),(1,-2),(-2,1),(1,2),(2,1),(-1,-2),(-2,-1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0] 
            endCol = c + d[1] 
            if ((d[0]**2+d[1]**2) == 1):
               endRow = r + d[0]*3 
               endCol = c + d[1]*3
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if isinstance(endPiece,ArmyCode.soldier):
                    if endPiece.status["image1"][0] != allyColor:
                        attacks.append(Move((r,c),(endRow,endCol),self.board))
           #checar cuando le bloqueen el camino
                                 
##################

        #----------
        
class Move():
    
    abcd = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    
    #rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
    #              "5": 3, "6": 2, "7": 1, "8": 0}
    rankToRows = {str(j):i for i,j in enumerate(range(DIMENSION-1,-1,-1))}
    
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    #filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
    #               "e": 4, "f": 5, "g": 6, "h": 7}
    filesToCols = {j: i for i,j in enumerate(abcd[:DIMENSION])}
    
    colsToFiles = {v: k for k,v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
      
      self.startRow = startSq[0]
      self.startCol = startSq[1]
      self.endRow = endSq[0]
      self.endCol = endSq[1]
      self.pieceMoved = board[self.startRow][self.startCol]
      self.pieceCaptured = board[self.endRow][self.endCol]
      self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
 #     print(self.moveID)
      
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
      
            
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + " -> " + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]