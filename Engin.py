import time
import csv
import pygame
global setup, chess_pieces

zerosev=[-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]

def setups():
    csv_file=open("Resources/Game_setups/setups.csv", "r")
    csv_r=csv.reader(csv_file, delimiter=",")
    setup={}
    for row in csv_r:
        try:
            setup[row[0]]=row[1]
        except IndexError:
            continue
    csv_file.close()
    return setup

def check_check(side, position, n=0): #Returns True for no check and False fo check
    x, y=0, 0
    if side==True:
        king=("k")
    else:
        king=("K")
    for row in position:
        try:
            x, y=position.index(row), row.index(king)
            break
        except ValueError:
            pass
    for i in range(x-1, x+2): #All the tiles around the king
        for j in range(y-1, y+2):
            if check_king(i, j, x, y, position, side)==False:
                return False
            else:
                pass
    moves2=[2, -2]
    moves1=[1, -1]
    for i in moves1:
        for j in moves2:
            if x-i<0 or y-j<0:
                break
            try:
                if position[x-i][y-j]==("-"):
                    pass
                elif position[x-i][y-j].lower()==("n") and position[x-i][y-j].islower()!=side:
                    return False
                else:
                    pass
            except IndexError:
                pass
    for i in moves2:
        for j in moves1:
            if x-i<0 or y-i<0:
                break
            try:
                if position[x-i][y-j]==("-"):
                    pass
                elif position[x-i][y-j].lower()==("n") and position[x-i][y-j].islower()!=side:
                    return False
                else:
                    pass
            except IndexError:
                pass
    return True #The king is not under check

def check_king(i, j, x, y, position, side):
    legal=None
    if i==-1 or j==-1 or i==8 or j==8:
        return True
    if position[i][j]==("-"):
        cx, cy=i-x, j-y
        nx=x
        ny=y
        while True:
            nx+=cx
            ny+=cy
            if nx==-1 or ny==-1:
                break
            else:
                pass
            try:
                if position[nx][ny]==("p"):
                    legal=[[[-1], [-1, 1]], [[-1], [-1, 1]]]
                elif position[nx][ny]==("P"):
                    legal=[[[1], [-1, 1]], [[1], [-1, 1]]]
                try:
                    empty=chess_pieces[position[nx][ny]].legal_moves_check([nx, ny], [x, y], legal)
                except KeyError:
                    empty=False
                if empty==True and position[nx][ny].islower()!=side:
                    return False
                elif position[nx][ny]==("-"):
                    pass
                else:
                    break
            except IndexError:
                break
    elif position[i][j].islower()==side:
        pass
    else:
        if position[i][j]==("p"):
            legal=[[[-1], [-1, 1]], [[-1], [-1, 1]]]
        elif position[i][j]==("P"):
            legal=[[[1], [-1, 1]], [[1], [-1, 1]]]
        if chess_pieces[position[i][j]].legal_moves_check([i, j], [x, y], legal)==True:
            return False
        else:
            pass
    return True

def no_move(side, position):
    for row in range(0, 8):
        for piece in range(0, 8):
            pice=position[row][piece]
            if pice==("-") or pice.islower()==side:
                pass
            else:
                for x in range(0, 8):
                    for y in range(0, 8):
                        if position[x][y].islower()==side:
                            if pice==("P"):
                                legal_moves=[[[1], [-1, 1]], [[1], [-1, 1]]]
                            elif pice==("p"):
                                legal_moves=[[[-1], [-1, 1]], [[-1], [-1, 1]]]
                            else:
                                legal_moves=None
                            pass
                        elif position[x][y]==("-"):
                            if pice==("P"):
                                if x==6:
                                    legal_moves=[[[1], [0]], [[1], [0]]]
                                else:
                                    legal_moves=[[[1], [0]], [[1], [0]]]
                            elif pice==("p"):
                                if x==1:
                                    legal_moves=[[[-1, -2], [0]], [[-1, -2], [0]]]
                                else:
                                    legal_moves=[[[-1], [0]], [[-1], [0]]]
                            else:
                                legal_moves=None
                        else:
                            continue
                        if pice.lower()==("k"):
                            legal_moves=[[[-1, 0, 1], [-1, 0, 1]]]
                        else:
                            pass
                        possible_move=chess_pieces[pice].legal_moves_check([row, piece], [x, y], pos=position, le=10, legal_moves=legal_moves)
                        if possible_move==True:
                            pass
                        else:
                            continue
                        position1=[]
                        for i in position:
                            rows=[]
                            for j in i:
                                rows.append(j)
                            position1.append(rows)
                        position1[x][y]=pice
                        position1[row][piece]=("-")
                        fix_check=check_check(not(side), position1)
                        if fix_check==False:
                            pass
                        else:
                            return False #There is a possible move
    return True #There are no possible moves

setup=setups()

class piece:

    def __init__(self, side, name, legal, img):
        self.le=0
        self.legal_moves=legal
        self.side=side
        self.name=name
        self.double_row=30
        self.image=pygame.image.load("Resources/Game_setups/Sets/"+setup["Sets"]+"/"+img+".png")

    def legal_moves_check(self, orgin, move, legal_moves=None, pos=None, le=None):
        if le!=None:
            self.le=le
        else:
            pass
        in_way=True
        if legal_moves==None:
            legal_moves=self.legal_moves
        else:
            pass
        if orgin==move:
            return False
        else:
            pass
        if self.name.lower()!=("b"):
            for set in legal_moves[0:self.le]:
                if orgin[0]-move[0] in set[0] and orgin[1]-move[1] in set[1]:
                    if self.name.lower() in ["k", "n"]:
                        pass
                    else:
                        if pos!=None:
                            if orgin[0]-move[0]==0:
                                direct=1
                            else:
                                direct=0
                            in_way=self.something_in_the_way_s(pos, orgin, move, direct)
                        else:
                            pass
                    return (True and in_way)
                else:
                    pass
        if self.name.lower() in ["b", "q"]:
            if orgin[0]-move[0]==orgin[1]-move[1] or orgin[0]-move[0]==-(orgin[1]-move[1]):
                if pos!=None:
                    in_way=self.something_in_the_way_d(pos, orgin, move, int(((orgin[0]-move[0])/(orgin[1]-move[1]))))
                else:
                    pass
                return (True and in_way)
            else:
                pass
        return False

    def double_move(self, orgin, move): #Notes was there a double move so legal el psant can be inplemented
        self.le=10
        if self.name.islower()==True:
            chess_pieces["p"].double_row=30
        else:
            chess_pieces["P"].double_row=30
        if self.name==("P"):
            if orgin[0]==6:
                self.double_row=orgin[1]
            elif orgin[0]==3 and chess_pieces["p"].double_row+1==orgin[1]:
                legal_moves=[[[1], [1, 0]], [[1], [1, 0]]]
                self.le=-1
                return True
            elif orgin[0]==3 and chess_pieces["p"].double_row-1==orgin[1]:
                legal_moves=[[[1], [0, -1]], [[1], [0, -1]]]
                self.le=-1
                return True
            else:
                self.le=-1
        elif self.name==("p"):
            if orgin[0]==1:
                self.double_row=orgin[1]
            elif orgin[0]==4 and chess_pieces["P"].double_row+1==orgin[1]:
                legal_moves=[[[-1], [-1, 0]], [[-1], [-1, 0]]]
                self.le=-1
                return True
            elif orgin[0]==4 and chess_pieces["P"].double_row-1==orgin[1]:
                legal_moves=[[[-1], [0, 1]], [[-1], [0, 1]]]
                self.le=-1
                return True
            else:
                self.le=-1
        else:
            pass
        return False

    def something_in_the_way_s(self, pos, orgin, move, direct): #Checkes for something in way of a sideways move
        while orgin[direct]!=move[direct]+1 and orgin[direct]!=move[direct]-1:
            if orgin[direct]>move[direct]:
                move[direct]+=1
            else:
                move[direct]-=1
            if pos[move[0]][move[1]]!=("-"):
                return False
            else:
                pass
        return True

    def something_in_the_way_d(self, pos, orgin, move, direct): #Checkes for something in way of a diagonal move
        while orgin[0]!=move[0]+1 and orgin[0]!=move[0]-1:
            if orgin[0]>move[0]:
                move[0]+=1
                move[1]+=direct
            else:
                move[0]-=1
                move[1]-=direct
            if pos[move[0]][move[1]]!=("-"):
                return False
            else:
                pass
        return True

#Defines dics that deffine the legal moves of every piece and pone
pieces_white={
    'R':[[[0], zerosev], [zerosev, [0]]],
    'N':[[[-2, 2], [-1, 1]], [[-1, 1], [-2, 2]]],
    'B':[],
    'K':[[[-1, 0, 1], [-1, 0, 1]], [[0], [-2, 2]]],
    'Q':[[[0], zerosev], [zerosev, [0]]],
    'P':[[[1], [-1, 0, 1]], [[2], [0]]]
    }
pieces_black={
    'r':[[[0], zerosev], [zerosev, [0]]],
    'n':[[[-2, 2], [-1, 1]], [[-1, 1], [-2, 2]]],
    'b':[],
    'k':[[[-1, 0, 1], [-1, 0, 1]], [[0], [-2, 2]]],
    'q':[[[0], zerosev], [zerosev, [0]]],
    'p':[[[-1], [-1, 0, 1]], [[-2], [0]]]
    }
image={
    'R':"Wrock",
    'N':"Wnight",
    'B':"Wbishop",
    'K':"Wking",
    'Q':"Wquin",
    'P':"Wpone",
    'r':"Brock",
    'n':"Bnight",
    'b':"Bbishop",
    'k':"Bking",
    'q':"Bquin",
    'p':"Bpone",
    }
chess_pieces={}

for part in pieces_white:
    chess_pieces[part]=piece(False, part, pieces_white[part], image[part])
for part in pieces_black:
    chess_pieces[part]=piece(True, part, pieces_black[part], image[part])
