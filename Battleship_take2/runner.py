import pygame as pg 
import numpy as np
import sys
import bot as b

class Runner():
#-----------------------init----------------------------#
    def __init__(self):
        #screen data
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 700
        self.SCREEN = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        #game data
        self.player_turn = True
        self.gamestart = False
        self.game_end = False
        self.winner = ""

        #map data
        self.bot_map = np.zeros([10,10]) #1 for ship position and 0 for empty
        self.p_map = np.zeros([10,10])

        self.bot_hits = np.zeros([10,10]) #1 for there has been a hit here and 0 for no hits here
        self.p_hits = np.zeros([10,10])
        
        #ship data [in play, length, list of positions]
        self.bot_ships = {"Carrier": [False,5,list()], "Battleship": [False,4,list()], "Submarine": [False,3,list()], "Cruiser": [False,3,list()],"Destroyer": [False,2,list()]}
        self.p_ships = {"Carrier": [False,5,list()], "Battleship": [False,4,list()], "Submarine": [False,3,list()], "Cruiser": [False,3,list()],"Destroyer": [False,2,list()]}
        self.p_ships_sunk = {"Carrier": list(), "Battleship": list(), "Submarine": list(), "Cruiser": list(),"Destroyer": list()}
        
        #function data
        self.player_place_switch = False

#------------------Functionality------------------#
    def main(self):
        botmoves = 0
        playermoves = 0
        #choose bot difficulty
        bot = b.HardBot()
        #initialize pygame
        pg.init()
        pg.display.set_caption("Battleship")
        
        while True:
            #handle quit event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    print(f"bot moves: {botmoves}\nplayer moves: {playermoves}")
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        
                        rel = pg.mouse.get_rel() 
                        
                        #check if the last ship has been placed already
                        if self.p_ships["Destroyer"][0] == True and self.gamestart == False:
                            
                            self.bot_ships = bot.set_ships()
                            for key in self.bot_ships:
                                for coord in self.bot_ships[key][2]:
                                    self.bot_map[coord[0]][coord[1]] = 1

                            for key in self.p_ships:
                                self.p_ships_sunk[key] = self.p_ships[key][2]
                            self.gamestart = True
                            
                            

                        if self.gamestart and self.player_turn and not self.game_end:
                            #take pos in bot board
                            pos = [(pos[1]-50)//52, (pos[0]-20)//52]
                            if -1<pos[0]<10 and -1<pos[1]<10:
                                
                                self.player_strike(pos)
                                playermoves += 1

                        elif not self.gamestart and self.player_turn:
                            #place ships
                            pos = [(pos[1]-50)//52,(pos[0]-950)//52]

                            if -1<pos[0]<10 and -1<pos[1]<10:
                                self.player_place(pos,rel)
                    
            if self.gamestart and not self.player_turn and not self.game_end:
                strike_coord = bot.strike()
                botmoves += 1



                self.p_hits[strike_coord[0],strike_coord[1]] = 1
                if self.p_map[strike_coord[0]][strike_coord[1]] == 1:

                    

                    for key in self.p_ships:
                        if strike_coord in self.p_ships[key][2]:
                            self.p_ships[key][2].remove(strike_coord)
                            if self.p_ships[key][2] == []:
                                self.p_ships[key][0] = False
                                bot.p_ships[key][0] = False
                                bot.success_log.append("sunk")
                                for coord in  self.p_ships_sunk[key]:
                                    bot.hit_ship_coord.append(coord)
                    
                    bot.success_log.append("hit")
                else:
                    bot.success_log.append("miss")
                
                
                
                if bot.success_log[-1] == "hit":
                    print("hit")
                
                self.player_turn = True
            
            if np.array_equiv(self.p_hits, bot.hits_map) and self.gamestart and not self.player_turn:
                raise Warning("Runner player hits map does not match bot's local enemy map")


            #check end game conditions
            if self.gamestart:
                bgame_done = True
                for key in self.bot_ships:
                    if self.bot_ships[key][0] == True:
                        bgame_done = False
                pgame_done = True
                for key in self.p_ships:
                    if self.p_ships[key][0] == True:
                        pgame_done = False
                
                if bgame_done == True or pgame_done == True:
                    self.game_end = True
                    if bgame_done:
                        self.winner = "player"
                    else:
                        self.winner = "bot"
                    
                    
            self.draw_board()
            
            pg.display.flip()


    def player_strike(self, pos):
        #check if the place has already been shot at
        if self.bot_hits[pos[1]][pos[0]] == 0:
            
            self.bot_hits[pos[1]][pos[0]] = 1
            for key in self.bot_ships:
                if pos in self.bot_ships[key][2]:
                    self.bot_ships[key][2].remove(pos)
                    
                    if self.bot_ships[key][2] == []:
                        self.bot_ships[key][0] = False
            self.player_turn = False
                    

        #if not, check if there

    def player_place(self,pos,rel):
        #get the top most ship that hasn't been placed yet
        
        shipname = None

        for key in self.p_ships:
            if self.p_ships[key][0] == False:
                shipname = key
                break
        
        #check if it the switch is on (a position has already been entered for start)
        if not self.player_place_switch and not shipname == None:
            #if not take position and save it as the first pos in ship data and update ship map
            if self.p_map[pos[1],pos[0]] == 0:
                self.p_ships[shipname][2].append([pos[1],pos[0]])
                self.player_place_switch = True
            
        elif not shipname == None and self.player_place_switch:
            #check which way the ship needs to placed (compare values from rel)
            shiplength = self.p_ships[key][1]
            #left or right
            if abs(rel[0]) >= abs(rel[1]):
                #left
                
                if rel[0] < 0:
                    
                    #check if last point exists
                    x_coord = self.p_ships[key][2][0][0] # in the ship you have chosen get the list of positions, get first position, get x coord of that position
                    if (x_coord - shiplength) > -1:
                        #iterate through every point to check if the point is not taken
                        for i in range(shiplength-1):
                            #if taken or doesn't exist, reset (set s_ships[key][2] = list(), set switch to false)
                            if self.p_map[x_coord-(i+1)][self.p_ships[key][2][0][1]] == 1:
                                self.p_ships[key][2]=list()
                                self.player_place_switch = False
                                return
                         #if it passes both tests add all points through iteration to list in p_ships
                         #iterate through p_ships and assign all points in the p_map 1
                        for i in range(shiplength-1):
                            self.p_ships[key][2].append([x_coord-(i+1), self.p_ships[key][2][0][1]])
                        for coord in self.p_ships[key][2]:
                            self.p_map[coord[0]][coord[1]] = 1
                        self.p_ships[key][0] = True
                        self.player_place_switch = False
                        #set the p_ships as True for placed
                    else:
                        #if taken or doesn't exist, reset (set s_ships[key][2] = list(), set switch to false)
                        self.p_ships[key][2] = list()
                        self.player_place_switch = False
                    

                #right
                else:
                    x_coord = self.p_ships[key][2][0][0]

                    if (x_coord + shiplength) < 10:
                        for i in range(shiplength-1):
                            if self.p_map[x_coord+(i+1)][self.p_ships[key][2][0][1]] == 1:
                                self.p_ships[key][2] = list()
                                self.player_place_switch = False
                                return
                        for i in range(shiplength-1):
                            self.p_ships[key][2].append([x_coord+(1+i), self.p_ships[key][2][0][1]])

                        for coord in self.p_ships[key][2]:
                            self.p_map[coord[0],coord[1]] = 1
                        
                        self.p_ships[key][0] = True
                        self.player_place_switch = False
                    else:
                        self.p_ships[key][2] = list()
                        self.player_place_switch = False

            else:
                #down
                y_coord = self.p_ships[key][2][0][1]
                if rel[1] > 0: 
                    if (y_coord + shiplength) < 10:
                        for i in range(shiplength-1):
                            if self.p_map[self.p_ships[key][2][0][0]][y_coord+(i+1)] == 1:
                                self.p_ships[key][2] = list()
                                self.player_place_switch = False
                                return
                        for i in range(shiplength-1):
                            self.p_ships[key][2].append([self.p_ships[key][2][0][0], y_coord +(i+1)])
                        
                        for coord in self.p_ships[key][2]:
                            self.p_map[coord[0]][coord[1]] = 1
                        self.p_ships[key][0] = True
                        self.player_place_switch = False
                    else:
                        self.player_place_switch = False
                        self.p_ships[key][2] = list()

                #up
                else:
                    if (y_coord - shiplength) > -1:
                        for i in range(shiplength-1):
                            if self.p_map[self.p_ships[key][2][0][0]][y_coord-(i+1)] == 1:
                                self.p_ships[key][2] = list()
                                self.player_place_switch = False
                                return
                        for i in range(shiplength-1):
                            self.p_ships[key][2].append([self.p_ships[key][2][0][0], y_coord -(i+1)])
                        
                        for coord in self.p_ships[key][2]:
                            self.p_map[coord[0]][coord[1]] = 1
                        self.p_ships[key][0] = True
                        self.player_place_switch = False
                    else:
                        self.player_place_switch = False
                        self.p_ships[key][2] = list()


        #if all the ships have been set start the game (possible set back: player has to click the screen one more time on the bot board to start game)
        #this is a precausionary measure and will not be triggered if everything is correct
        else: 
            self.gamestart = True
            print("Warning: gamestart triggered at player_place_ships() function")
        
#-----------------------Graphics----------------------------#
    def draw_board(self):
        WIDTH = 50
        HEIGHT = 50
        MARGIN = 2
        white = (255,255,255)
        red = (255,0,0)
        green = (117, 255, 122)
        grey = (183,201,188)
        blue = (102,206,209)
        Board_Title_Font = pg.font.Font('freesansbold.ttf', 32)
        Ships_Font = pg.font.Font('freesansbold.ttf', 16)

        #fill screen
        self.SCREEN.fill((0,0,0))

    #draw bot board
        bot_board_offset = [20,50]
        
        BotBoard_Text = Board_Title_Font.render('Bot Board', True, white)
        BotBoard_TextRect = BotBoard_Text.get_rect()
        BotBoard_TextRect.center = (270,35)
        self.SCREEN.blit(BotBoard_Text, BotBoard_TextRect)

        for row in range(10):
            for column in range(10):
                color = blue
                if self.bot_hits[column][row] == 1:
                    color = white
                if self.bot_map[row][column] == 1:
                    if self.gamestart == False:
                        color = grey
                    if self.bot_hits[column][row] == 1:
                        color = red
                
                pg.draw.rect(self.SCREEN, color, [(MARGIN+WIDTH)*column+(MARGIN+bot_board_offset[0]), (MARGIN+HEIGHT)*row+(MARGIN+bot_board_offset[1]), WIDTH,HEIGHT])
        
    #draw player board
        p_board_offset = [950,50]

        pBoard_Text = Board_Title_Font.render('Player Board', True, white)
        pBoard_TextRect = pBoard_Text.get_rect()
        pBoard_TextRect.center = (1220,35)
        self.SCREEN.blit(pBoard_Text, pBoard_TextRect)

        for row in range(10):
            for column in range(10):
                color = blue

                if self.p_hits[column][row] == 1:
                    color = white
                if self.p_map[column][row] == 1:
                    color = grey
                    if self.p_hits[column][row] == 1:
                        color = red
                pg.draw.rect(self.SCREEN, color, [(MARGIN+WIDTH)*column+MARGIN+p_board_offset[0], (MARGIN+HEIGHT)*row+MARGIN+p_board_offset[1], WIDTH,HEIGHT])
     
    #draw text for game state *(and if hit or miss) <-- do later
        if self.gamestart:
            text = 'Play'
        else:
            text = "Place Ships"
        board_state_text = Board_Title_Font.render(text, True, white)
        board_state_textrect = board_state_text.get_rect()
        board_state_textrect.center = (750,50)
        self.SCREEN.blit(board_state_text, board_state_textrect)
        
    #placing ships
        count = 0
        for key in self.p_ships:
            if self.p_ships[key][0]:
                ship_text = Ships_Font.render(f"{key}", True, white)
                ship_textrect = ship_text.get_rect()
                ship_textrect = (count*100+970, 600)
                self.SCREEN.blit(ship_text,ship_textrect)
            count+=1

        bcount = 0
        for key in self.bot_ships:
            if self.bot_ships[key][0]:
                bship_text = Ships_Font.render(f"{key}", True, white)
                bship_textrect = bship_text.get_rect()
                bship_textrect.center = (bcount*100 + 50, 600)
                self.SCREEN.blit(bship_text, bship_textrect)
            bcount += 1

    #draw end game text
        if self.game_end:
            endFont = pg.font.Font('freesansbold.ttf', 65)
            if self.winner == "player":
                color = green
            else:
                color = red
            endtext = endFont.render(f"{self.winner} Won!", True, color)
            endtextrect = endtext.get_rect()
            endtextrect.center = (750,350)
            self.SCREEN.blit(endtext, endtextrect)
if __name__ == "__main__":
    run = Runner()
    run.main()