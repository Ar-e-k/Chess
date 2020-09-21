import pygame
import sys
import math
import os
import Engin
import csv
from pickle import load as pl
from pickle import dump as pd

def main():
    pygame.init()
    pygame.font.init()
    screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Chess")
    pygame.time.Clock()
    setup=Engin.setups()
    status=("menu")
    slider=False
    global screen_x, screen_y
    screen_x, screen_y=pygame.display.Info().current_w, pygame.display.Info().current_h
    menu=Menu_screen(screen, setup)
    while True: #Main game function capturing all the initial input and then sending it to the right place
        for event in pygame.event.get():
            #print(event)
            try:
                pos=pygame.mouse.get_pos()
                if slider==True and menu.slid_area.collidepoint(pos):
                    if status==("menu"):
                        but=["New game", "Load game", "Options", "Exit"]
                    else:
                        but=["Themes", "Fonts", "Sets", "Exit"]
                    if pos[0]<screen_x/8*3+screen_y/16:
                        pos[0]=screen_x/8*3+screen_y/16
                    elif pos[0]>screen_x/8*3+screen_y/16+screen_x/2-screen_y/8:
                        pos[0]=screen_x/8*3+screen_y/16+screen_x/2-screen_y/8
                    else:
                        pass
                    menu.time=int(((1500/(screen_x/2-screen_y/8)*(pos[0]-screen_x/2-screen_y/8))+screen_x/8*3+screen_y/16)/60)*60+300
                    menu.menu()
                    menu.buttons(but)
                    menu.slid([255, 0, 0])
                elif slider==False:
                    if color==[255, 0, 0]:
                        menu.menu()
                        menu.buttons(but)
                        menu.slid([0, 0, 0])
                        color=[0, 0, 0]
                    else:
                        pass
                else:
                    pass
            except:
                pass
            if event.type==pygame.KEYDOWN:
                if event.key==27: #Quit the game
                    pygame.quit()
                    sys.exit()
                elif event.key==115: #Saves the position and the layout of the pieces on the board
                    castelings=[
                        game.wKing,
                        game.bKing,
                        game.leftBrock,
                        game.rightBrock,
                        game.leftWrock,
                        game.rightWrock
                        ]
                    save_game(game.current_position, [game.captured_black, game.captured_white], game.on_move, castelings, game.time)
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                if status==("menu") or status==("menu-options"): #Sends to the menu screen input handeling
                    if menu.ball.collidepoint(pos)==True:
                        slider=not(slider)
                        if status==("menu"):
                            but=["New game", "Load game", "Options", "Exit"]
                        else:
                            but=["Themes", "Fonts", "Sets", "Exit"]
                        if slider==True:
                            color=[255, 0, 0]
                        else:
                            color=[0, 0, 0]
                        menu.menu()
                        menu.buttons(but)
                        menu.slid(color)
                    else:
                        slider=False
                    status=menu.button_control(status, pos)
                    if status==("in game") or status==("load game"):
                        if status==("in game"):
                            set, taken, move, cast, time=load_game("new_game")
                            time=[menu.time, menu.time]
                        elif status==("load game"):
                            set, taken, move, cast, time=load_game("chess")
                        status=("in game")
                        game=In_game(screen, setup, set, taken, pygame.time.get_ticks()/1000, move, cast, time)
                    else:
                        pass
                elif status==("in game"): #Sends to the in game class input handeling
                    game.input_handling(pos)
                elif status==("setups"):
                    status=menu.setup_control(pos)
                else:
                    pass

def load_game(game):
    file=open("Resources/"+game+".save", "rb")
    f=pl(file)
    game=f[0]
    taken=f[1]
    move=f[2]
    cast=f[3]
    try:
        time=f[4]
    except IndexError:
        time=None
    file.close()
    game1=[]
    for row in game:
        a=[]
        for let in row:
            a.append(let)
        game1.append(a)
    return game1, taken, move, cast, time

def save_game(bd, taken, move, cast, time):
    file=open("Resources/chess.save", "wb")
    bp=[]
    for row in bd:
        s=("")
        for v in row:
            s=s+v
        bp.append(s)
    time=list(time.values())
    nw=[bd, taken, move, cast, time]
    pd(nw, file)
    file.close()

class Menu_screen: #Controls the buttons on the screen

    def __init__(self, screen, setup):
        self.screen=screen
        self.game_setups=setup
        self.type=None
        self.time=900
        self.read_setups()
        self.menu()
        self.buttons(["New game", "Load game", "Options", "Exit"])
        self.slid()

    def read_setups(self):
        file=open("Resources/Game_setups/Font/"+self.game_setups["Font"]+".txt", "r")
        for row in file:
            self.font=row.split(",")
            break
        file.close()
        self.font=pygame.font.SysFont(self.font[0], int(self.font[1]))
        file=open("Resources/Game_setups/Theme/"+self.game_setups["Theme"]+".thame", "rb")
        theme=pl(file)
        file.close()
        self.font_color, self.box=theme[0], theme[1]

    def menu(self): #Puts on a background
        bc=pygame.image.load("Resources/Background.png").convert()
        bc=pygame.transform.scale(bc, [screen_x, screen_y])
        self.screen.blit(bc, [0, 0])
        #pygame.display.flip()

    def buttons(self, options_texts):
        self.buttons_on_scree=[]
        for i in range(0, 4):
            rec=pygame.Rect((screen_x/3, (screen_y/8*1.5)+(i*3*screen_y/16), screen_x/3, screen_y/8))
            self.buttons_on_scree.append(rec)
            pygame.draw.rect(self.screen, self.box, self.buttons_on_scree[i])
            self.screen.blit(self.font.render(options_texts[i], False, self.font_color), (screen_x/32+screen_x/3, (screen_y/8*1.75)+(i*3*screen_y/16)))
        pygame.display.flip()

    def slid(self, color=[0, 0, 0]):
        self.slid_area=pygame.Rect((screen_x/8*3, screen_y/32, screen_x/2, screen_y/8))
        #pygame.draw.rect(self.screen, self.box, self.slid_area, 1)
        self.slider=pygame.Rect((screen_x/8*3+screen_y/16, screen_y/32+screen_y/16-screen_y/64, screen_x/2-screen_y/8, screen_y/32))
        pygame.draw.rect(self.screen, self.box, self.slider)
        self.ball=pygame.draw.circle(self.screen, color, (int(((screen_x/2-screen_y/8)/1500*(self.time-300))+(screen_x/8*3+screen_y/16)), int(screen_y/32+screen_y/16)), int(screen_y/16))
        self.screen.blit(self.font.render(str(self.time/60), False, [0, 0, 0]), (screen_x/8*7, screen_y/32+screen_y/16))
        pygame.display.flip()

    def button_control(self, status, pos):
        if self.buttons_on_scree[0].collidepoint(pos)==True:
            if status==("menu"):
                #print("Start game")
                return ("in game")
            elif status==("menu-options"):
                self.setup_menu("Theme")
                return ("setups")
        elif self.buttons_on_scree[1].collidepoint(pos)==True:
            if status==("menu"):
                #print("Load game")
                return ("load game")
            elif status==("menu-options"):
                self.setup_menu("Font")
                return ("setups")
        elif self.buttons_on_scree[2].collidepoint(pos)==True:
            if status==("menu"):
                self.buttons(["Themes", "Fonts", "Sets", "Exit"])
                return ("menu-options")
            elif status==("menu-options"):
                self.setup_menu("Sets")
                return ("setups")
        elif self.buttons_on_scree[3].collidepoint(pos)==True:
            pygame.quit()
            sys.exit()
        else:
            #print("Misclick")
            if status==("menu"):
                return ("menu")
            elif status==("menu-optios"):
                return ("menu-options")

    def setup_menu(self, type):
        self.menu()
        path, dirs, files=next(os.walk("Resources/Game_setups/"+type))
        self.type=type
        themes=len(files)
        if themes==0:
            themes=len(dirs)
            opt=dirs
            del files
        else:
            opt=files
            for i in range(0, len(opt)):
                opt[i], a=opt[i].split(".")
            del dirs
        del path
        self.options_on_scree={}
        for i in range(1, themes+1):
            rec=pygame.Rect((screen_x/3, (screen_y/8*1.5)+(i*3*screen_y/16), screen_x/3, screen_y/8/i))
            self.options_on_scree[opt[i-1]]=rec
            pygame.draw.rect(self.screen, self.box, self.options_on_scree[opt[i-1]])
            self.screen.blit(self.font.render(opt[i-1], False, self.font_color), (screen_x/32+screen_x/3, (screen_y/8*1.75)+(i*3*screen_y/16)))
        pygame.display.flip()

    def setup_control(self, pos):
        for key in self.options_on_scree:
            if self.options_on_scree[key].collidepoint(pos)==True:
                new_theme=key
                break
            else:
                pass
        else:
            return ("setups")
        setups=self.game_setups.copy()
        setups[self.type]=new_theme
        csv_file=open("Resources/Game_setups/setups.csv", "w")
        csv_write=csv.writer(csv_file)
        csv_write.writerows(setups.items())
        csv_file.close()
        self.menu()
        self.buttons(["New game", "Load game", "Options", "Exit"])
        return ("menu")

class In_game: #Checks for end of the game

    def __init__(self, screen, setup, set, taken, time, move, cast, timer): #Specifies all the game variables
        self.screen=screen #Pygame surface that all happends on
        self.game_setups=setup
        self.current_position=set #This var is the all time positon that updates every move
        self.on_move=True #True specifies whose on the move, true being white until a move i made
        self.captured_black, self.captured_white=taken[0], taken[1] #This lists specifies all the pices that are captured on the sude
        self.start_time=time
        self.end_time=time
        self.time={"White":timer[0], "Black":timer[1]} #Specifies the time both sides have, in seconds
        self.wKing, self.bKing=cast[0], cast[1]
        self.leftBrock, self.rightBrock=cast[2], cast[3]
        self.leftWrock, self.rightWrock=cast[4], cast[5]
        self.moves=0
        self.move50rule=50
        self.save_positions=[]
        self.bc=pygame.image.load("Resources/game_Background.png").convert()
        self.read_setups() #Initializees some game setups
        self.board()

    def read_setups(self):
        file=open("Resources/Game_setups/Font/"+self.game_setups["Font"]+".txt", "r")
        for row in file:
            self.font=row.split(",")
            break
        file.close()
        self.font_size=int(self.font[1])
        self.font=pygame.font.SysFont(self.font[0], int(self.font[1]))
        file=open("Resources/Game_setups/Theme/"+self.game_setups["Theme"]+".thame", "rb")
        theme=pl(file)
        file.close()
        self.font_color, self.box=theme[0], theme[1]

#Drawing staff on the screen
    def board(self): #Puts the background image on and continues
        self.bc=pygame.transform.scale(self.bc, [screen_x, screen_y])
        self.screen.blit(self.bc, [0, 0])
        self.casteling_update()
        self.draw_board()
        pygame.display.flip()

    def draw_board(self): #Draws the chess board
        self.visual_position={}
        self.chess_board=[]
        for i in range(0, 8):
            row=[]
            for j in range(0, 8):
                rec=pygame.Rect(screen_x/2+screen_y/12*(j-4), screen_y/12*(2+i), screen_y/12, screen_y/12)
                if i%2==0:
                    if j%2==0:
                        c=[255,255,255]
                    else:
                        c=[55, 55, 55]
                else:
                    if j%2==1:
                        c=[255,255,255]
                    else:
                        c=[55, 55, 55]
                pygame.draw.rect(self.screen, c, rec)
                self.draw_pieces(self.current_position[i][j], screen_x/2+screen_y/12*(j-4), screen_y/12*(2+i))
                row.append(rec)
            self.chess_board.append(row)
        self.draw_draw_button()
        self.draw_info()
        self.check()
        self.draw_captured(self.captured_black, -4, 0, False)
        self.draw_captured(self.captured_white, -4, 10, False)

    def draw_pieces(self, piece, x, y): #Draws the pices on the board
        if piece!=("-"):
            #img=pygame.image.load("Resources/Game_setups/Sets/"+self.setup["Sets"]+"/"+piece+".png").convert_alpha()
            self.visual_position[piece]=pygame.transform.scale(Engin.chess_pieces[piece].image, [int(screen_y/12), int(screen_y/12)])
            self.visual_position[piece]=pygame.transform.flip(self.visual_position[piece], False, False)
            self.screen.blit(self.visual_position[piece], [x, y])
        else:
            self.visual_position[piece]=("Empty")

    def draw_captured(self, side, x1, y1, sides): #Draw the captured pices on the side
        for i in range(0, len(side)):
            pice=side[i]
            x=screen_x/2+screen_y/12*(x1+i%8)
            y=screen_y/12*(y1+i//8)
            pice=pygame.transform.scale(Engin.chess_pieces[pice].image, [int(screen_y/12), int(screen_y/12)])
            pice=pygame.transform.flip(pice, sides, sides)
            self.screen.blit(pice, [x, y])

    def draw_info(self): #Display player info, including time and the number of moves
        white=pygame.Rect(0, 0, screen_x/6, 3*self.font_size+screen_y/40)
        black=pygame.Rect((screen_x/6)*5, 0, screen_x/6, 3*self.font_size+screen_y/40)
        self.time_taken=int(self.end_time-self.start_time)
        self.time_taken
        if self.moves%2==0:
            movesw=("Moves-"+str(self.moves//2))
            movesb=("Moves-"+str(self.moves//2))
        else:
            movesw=("Moves-"+str((self.moves//2)+1))
            movesb=("Moves-"+str(self.moves//2))
        if self.on_move!=True:
            pygame.draw.rect(self.screen, self.box, white)
            pygame.draw.rect(self.screen, [0,0,255], black)
            self.time["White"]-=self.time_taken
        else:
            pygame.draw.rect(self.screen, self.box, black)
            pygame.draw.rect(self.screen, [0,0,255], white)
            self.time["Black"]-=self.time_taken
        self.start_time=self.end_time
        w_time=str(self.time["White"]//60)+"."+str(self.time["White"]%60)
        b_time=str(self.time["Black"]//60)+"."+str(self.time["Black"]%60)
        self.screen.blit(self.font.render("White", False, self.font_color), [0, 0])
        self.screen.blit(self.font.render("Black", False, self.font_color), [(screen_x/6)*5, 0])
        self.screen.blit(self.font.render(w_time, False, self.font_color), [0, self.font_size])
        self.screen.blit(self.font.render(b_time, False, self.font_color), [(screen_x/6)*5, self.font_size])
        self.screen.blit(self.font.render((movesw), False, self.font_color), [0, 2*self.font_size])
        self.screen.blit(self.font.render((movesb), False, self.font_color), [(screen_x/6)*5, 2*self.font_size])

    def draw_draw_button(self):
        self.draw_but=pygame.Rect((0, screen_y/2+screen_y/32, screen_x/12, screen_y/16))
        pygame.draw.rect(self.screen, self.box, self.draw_but)
        self.screen.blit(self.font.render("Draw", False, self.font_color), (0, screen_y/2+screen_y/32))
#End on drawing staff on the screen
#Maing game functions
    def input_handling(self, pos): #The in game input handeling, while a piece is selected
        if self.draw_but.collidepoint(pos)==True:
            self.draw()
            return None
        else:
            pass
        x1, y1=self.find_square(pos)
        if x1==None:
            return None
        else:
            pass
        if self.current_position[x1][y1]==("-"):
            return None
        else:
            if Engin.chess_pieces[self.current_position[x1][y1]].side==self.on_move:
                return None
            else:
                self.red_box=pygame.Rect(screen_x/2+screen_y/12*(y1-4), screen_y/12*(2+x1), screen_y/12, screen_y/12)
                pygame.draw.rect(self.screen, [255,0,0], self.red_box, 5)
                #red_box=pygame.image.load("Resources/red_square.png").convert_alpha()
                #red_box=pygame.transform.scale(red_box, [64, 64])
                #self.screen.blit(red_box, [screen_x/2+screen_y/12*(y1-4), screen_y/12*(2+x1)])
                pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        pos=pygame.mouse.get_pos()
                        x2, y2=self.find_square(pos)
                        if x2==None:
                            break
                        else:
                            pass
                        self.el_pass=Engin.chess_pieces[self.current_position[x1][y1]].double_move([x1, y1], [x2, y2])
                        #print(Engin.chess_pieces[self.current_position[x1][y1]], [x1, y1], [x2, y2])
                        legal=Engin.chess_pieces[self.current_position[x1][y1]].legal_moves_check([x1, y1], [x2, y2], pos=self.current_position)
                        if legal==True:
                            self.on_move=not(self.on_move)
                            self.move(x1, y1, x2, y2)
                            return None
                            #pygame.display.flip()
                        else:
                            self.board()
                            return None

    def move(self, x1, y1, x2, y2): #Veryfy is the move valid and edits the current postion to be rerendered in new position
        pice=self.current_position[x1][y1]
        pos=[]
        for row in self.current_position:
            rowe=[]
            for i in row:
                rowe.append(i)
            pos.append(rowe)
        pos[x2][y2]=pos[x1][y1]
        pos[x1][y1]=("-")
        check=Engin.check_check(self.on_move, pos) #To check does the following move resolt in exploiting the player to check or not protecting against existing one
        if check==True:
            pass
        else:
            self.on_move=not(self.on_move)
            self.board()
            return None
        if pice.lower()==("k"):
            if -1==y1-y2 or y1-y2==1 or y1-y2==0:
                pass
            else:
                prop_casteling=self.make_castling(pice, x1, y1, x2, y2)
                if prop_casteling==True:
                    self.move_accepted(y1, x2, y2)
                    self.board() #Move accepted
                    return None
                else:
                    self.on_move=not(self.on_move)
                    self.board() #Move declined
                    return None
        else:
            pass
        if (x2==7 and pice==("p")): #Promotes the pones if they reach the end
            choice=self.promotion_screen(["q", "r", "b", "n"])
            pice=choice
        elif (x2==0 and pice==("P")):
            choice=self.promotion_screen(["Q", "R", "B", "N"])
            pice=choice
        else:
            pass
        if self.current_position[x2][y2]!=("-"):
            if Engin.chess_pieces[pice].side==self.current_position[x2][y2].islower() or self.current_position[x2][y2].lower()==("k"):
                self.on_move=not(self.on_move)
                self.board() #Move declined
                return None
            else:
                if pice.lower()==("p"): #Contols pones not to capture going forwards
                    if pice==("P"):
                        legal=Engin.chess_pieces[pice].legal_moves_check([x1, y1], [x2, y2], [[[1], [-1, 1]], [[1], [-1, 1]]])
                    else:
                        legal=Engin.chess_pieces[pice].legal_moves_check([x1, y1], [x2, y2], [[[-1], [-1, 1]], [[-1], [-1, 1]]])
                    if legal==True:
                        if Engin.chess_pieces[pice].side==True:
                            self.captured_black.append(Engin.chess_pieces[self.current_position[x2][y2]].name)
                        else:
                            self.captured_white.append(Engin.chess_pieces[self.current_position[x2][y2]].name)
                        self.current_position[x2][y2]=pice
                        self.current_position[x1][y1]=("-")
                        self.move50rule=50
                        self.move_accepted(y1, x2, y2, rest=True)
                        self.board() #Move accepted
                        return None
                    else:
                        self.on_move=not(self.on_move)
                        self.board() #Move declined
                        return None
                else:
                    if Engin.chess_pieces[pice].side==True:
                        self.captured_black.append(Engin.chess_pieces[self.current_position[x2][y2]].name)
                    else:
                        self.captured_white.append(Engin.chess_pieces[self.current_position[x2][y2]].name)
                    self.current_position[x2][y2]=pice
                    self.current_position[x1][y1]=("-")
                    self.move_accepted(y1, x2, y2, rest=True)
                    self.board() #Move accepted
                    return None
        else:
            if self.el_pass==True:
                if Engin.chess_pieces[pice].side==True:
                    self.captured_black.append(Engin.chess_pieces[self.current_position[x2-1][y2]].name)
                    self.current_position[x2-1][y2]=("-")
                else:
                    self.captured_white.append(Engin.chess_pieces[self.current_position[x2+1][y2]].name)
                    self.current_position[x2+1][y2]=("-")
                self.current_position[x2][y2]=pice
                self.current_position[x1][y1]=("-")
                self.move50rule=50
                self.move_accepted(y1, x2, y2, el=True, rest=True)
                self.board() #Move accepted
                return None
            else:
                pass
            if pice.lower()==("p"):
                if self.current_position[x1][y1]==("P"):
                    legal=Engin.chess_pieces[self.current_position[x1][y1]].legal_moves_check([x1, y1], [x2, y2], [[[1], [0]], [[1, 2], [0]]])
                else:
                    legal=Engin.chess_pieces[self.current_position[x1][y1]].legal_moves_check([x1, y1], [x2, y2], [[[-1], [0]], [[-1, -2], [0]]])
                if legal==True:
                    self.current_position[x2][y2]=self.current_position[x1][y1]
                    self.current_position[x1][y1]=("-")
                    self.move50rule=50
                    self.move_accepted(y1, x2, y2, rest=True)
                    self.board() #Move accepted
                    return None
                else:
                    self.on_move=not(self.on_move)
                    self.board() #Move declined
                    return None
            else:
                self.current_position[x2][y2]=self.current_position[x1][y1]
                self.current_position[x1][y1]=("-")
                self.move_accepted(y1, x2, y2)
                self.board() #Move accepted
                return None

    def find_square(self, pos): #Finds the position of the square on the board
        for row in self.chess_board:
            for square in row:
                if square.collidepoint(pos)==True:
                    x, y=int((square[1]*12)/screen_y-2), int((square[0]-screen_x/2)/screen_y*12+4)
                    return x, y
                    break
                else:
                    pass
        return None, None

    def move_accepted(self, y1, x2, y2, el=False, rest=False): #Runned if the move is accepted
        self.end_time=pygame.time.get_ticks()/1000
        self.moves+=1
        self.move50rule-=0.5
        if rest==True:
            self.cancel_castling(y1, x2, y2)
            self.save_positions=[]
        else:
            rest=self.cancel_castling(y1, x2, y2)
            if rest==True:
                self.save_positions=[]
            else:
                pass
        if el==False:
            pos1=[]
            for row in self.current_position:
                rowe=[]
                for i in row:
                    rowe.append(i)
                pos1.append(rowe)
            list=[pos1, self.on_move]
            self.save_positions.append(list)
        else:
            pass

    def check(self): #Checks for end of the game through checkmate or stalemate after every turn
        check=Engin.check_check(not(self.on_move), self.current_position)
        no_move=Engin.no_move(self.on_move, self.current_position)
        if self.on_move==True:
            won=("Black")
            lost=("White")
        else:
            won=("White")
            lost=("Black")
        result=won
        for row in self.current_position:
            can_mate=[
            ("q") in row,
            ("Q") in row,
            ("r") in row,
            ("R") in row,
            ("p") in row,
            ("P") in row,
            ("b") in row and row.count("b")>1,
            ("B") in row and row.count("B")>1,
            ("b") in row and ("n") in row,
            ("B") in row and ("N") in row
            ]
            if True in can_mate:
                break
            else:
                pass
        else:
            stance=("There is no possible way to win")
            self.end_game(result, stance)
        if no_move==True:
            if check==False:
                stance=(won+" have checkmated "+lost)
            else:
                stance=("Stalemate by the incompetence of "+won)
        elif self.time[won]<0:
            stance=(won+" has ended the game running out of time")
            result=lost
        elif self.move50rule==0:
            stance=(won+" have made 50th move without capture or pawn move, cousing a draw")
        elif [self.current_position, self.on_move] in self.save_positions:
            if self.save_positions.count([self.current_position, self.on_move])>2:
                stance=(won+" has coused the same position for the fird time")
            else:
                return None
        else:
            return None
        self.end_game(result, stance)

    def draw(self):
        yes=pygame.Rect((0, 0, screen_x/2, screen_y))
        pygame.draw.rect(self.screen, [0,255,0], yes)
        self.screen.blit(self.font.render("Accept", False, self.font_color), (screen_x/4-screen_x/12, screen_y/2))
        no=pygame.Rect((screen_x/2, 0, screen_x/2, screen_y))
        pygame.draw.rect(self.screen, [255,0,0], no)
        self.screen.blit(self.font.render("Reject", False, self.font_color), (screen_x/4*3-screen_x/12, screen_y/2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    if yes.collidepoint(pos)==True:
                        #print("accepted")
                        stance=("Both players have accepted a draw")
                        self.end_game("White", stance)
                    else:
                        self.board()
                        return None

    def end_game(self, win, stance):
        stance=str(stance)
        if win==("White"):
            color=[0,0,0]
        else:
            color=[255,255,255]
        self.screen.fill(color, [0, 0, screen_x, screen_y])
        self.screen.blit(self.font.render(stance, False, [255,0,0]), [0, 0, screen_x, screen_y])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    pass
#End of main game functions
#Functions for veryfing castelign
    def make_castling(self, pice, x1, y1, x2, y2): #Mooves the king and the rock to the set locations
        if self.current_position[x2][y2]!=("-"):
            return False
        else:
            pass
        if pice.islower()==True:
            if y1-y2==2:
                legal=self.checking_castling(pice, x1, y1, x2, y2, "black_left", True)
            else:
                legal=self.checking_castling(pice, x1, y1, x2, y2, "black_right", False)
        else:
            if y1-y2==2:
                legal=self.checking_castling(pice, x1, y1, x2, y2, "white_left", True)
            else:
                legal=self.checking_castling(pice, x1, y1, x2, y2, "white_right", False)
        if legal==True:
            return True
        else:
            return False

    def checking_castling(self, pice, x1, y1, x2, y2, way, long): #Checks if the check is legal
        check=Engin.check_check(self.on_move, self.current_position)
        if check==False:
            return False
        else:
            pass
        if self.casteling[way]==True:
            pass
        else:
            return False
        if long==True:
            if self.current_position[x1][y2+1]!=("-"):
                return False
            else:
                pass
            for j in range(y2+1, y1):
                pos=[]
                for row in self.current_position:
                    rowe=[]
                    for i in row:
                        rowe.append(i)
                    pos.append(rowe)
                pos[x1][j]=pice
                check=Engin.check_check(self.on_move, pos)
                if check==False:
                    return False
                else:
                    pass
        else:
            if self.current_position[x1][y2-1]!=("-"):
                return False
            else:
                pass
            for j in range(y1, y2-1):
                pos=[]
                for row in self.current_position:
                    rowe=[]
                    for i in row:
                        rowe.append(i)
                    pos.append(rowe)
                pos[x1][j]=pice
                check=Engin.check_check(self.on_move, pos)
                if check==False:
                    return False
                else:
                    pass
        self.current_position[x2][y2]=pice
        self.current_position[x1][y1]=("-")
        if long==True:
            self.current_position[x1][y2+1]=self.current_position[x1][0]
            self.current_position[x1][0]=("-")
        else:
            self.current_position[x1][y2-1]=self.current_position[x1][7]
            self.current_position[x1][7]=("-")
        return True

    def casteling_update(self): #Updates are the castelings valid
        self.casteling={
            "white_left":self.wKing and self.leftWrock,
            "white_right":self.wKing and self.rightWrock,
            "black_left":self.bKing and self.leftBrock,
            "black_right":self.bKing and self.rightBrock
            }

    def cancel_castling(self, y1, x2, y2): #Checks if the king or the rock moved and closes casteling ability if they are
        if self.current_position[x2][y2]==("R") and y1==0 and self.leftWrock==True:
            self.leftWrock=False
            return True
        elif self.current_position[x2][y2]==("R") and y1==7 and self.rightWrock==True:
            self.rightWrock=False
            return True
        elif self.current_position[x2][y2]==("r") and y1==7 and self.rightBrock==True:
            self.rightBrock=False
            return True
        elif self.current_position[x2][y2]==("r") and y1==0 and self.leftBrock==True:
            self.leftBrock=False
            return True
        elif self.current_position[x2][y2]==("K") and self.wKing==True:
            self.wKing=False
            return True
        elif self.current_position[x2][y2]==("k") and self.bKing==True:
            self.bKing=False
            return True
        else:
            return False
#End of casteling functions
#Contorls pone promotion
    def promotion_screen(self, options): #Shows the possible pices to promote to
        buttons={}
        for i in options:
            rec=pygame.Rect((screen_x/3, (screen_y/8*1.5)+(options.index(i)*3*screen_y/16), screen_x/3, screen_y/12))
            buttons[i]=(rec)
            pygame.draw.rect(self.screen, self.box, buttons[i])
            self.screen.blit(self.font.render(i, False, self.font_color), (screen_x/32+screen_x/3, (screen_y/8*1.6)+(options.index(i)*3*screen_y/16)))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    if self.promotion_control(pos, buttons)!=None:
                        return self.promotion_control(pos, buttons)
                    else:
                        pass

    def promotion_control(self, pos, buttons): #Handles the user promotion
        for i in buttons:
            if buttons[i].collidepoint(pos)==True:
                return i
            else:
                pass
        return None
#End of pone promotion

if __name__==("__main__"):
    main()
