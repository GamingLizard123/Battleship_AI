import numpy as np
import random

class EasyBot():
    def __init__(self):
        self.hits_map = np.zeros([10,10]) #local map of enemy board
        self.ship_map = np.zeros([10,10]) #local map of own ships for placement use
        self.ships = {"Carrier": [False,5,list()], "Battleship": [False,4,list()], "Submarine": [False,3,list()], "Cruiser": [False,3,list()],"Destroyer": [False,2,list()]} #local temp copy of ships list
        self.success_log = ["log start:"] #log of past impacts, filled with hit or miss
        self.p_ships = {"Carrier": [True,5], "Battleship": [True,4], "Submarine": [True,3], "Cruiser": [True,3],"Destroyer": [True,2]} #bot keeps track of active ships
        self.ships_sunk_coords = []

    def set_ships(self):
        """takes in no arguments
        returns a dictionary with an array of values in form [bool(ship in play), int(ship length), list(coords in array form)]"""
        for key in self.ships:
            while True:
                
                start_x_coord = np.random.randint(0,10)
                start_y_coord = np.random.randint(0,10)
                if self.ship_map[start_x_coord][start_y_coord] == 0:
                    break
            while True:
                
                #get the ship length
                ship_length = self.ships[key][1]
                #Get decision
                choice = random.choice(["up","down","left","right"])
                
                #placing is available bool
                place = True

                if choice == "left":
                    #check if the last point exists
                    if start_x_coord - ship_length < 0:
                        #last point doesn't exist do nothing
                        print("bot thinking")
                    else:
                        for i in range(ship_length):
                        #else check if everypoint exists and is free
                            #if it isn't place = False
                            if self.ship_map[start_x_coord-i][start_y_coord] == 1:
                                place = False
                        if place == True:
                        #if it passes loop succesfully and place is still true
                            for i in range(ship_length):
                                #loop through everypoint and add to the ship's list and local ship map
                                self.ships[key][2].append([start_x_coord-i, start_y_coord])
                                self.ship_map[start_x_coord-i][start_y_coord] = 1
                            #afterwards set ship in play to true
                            self.ships[key][0] = True
                            #continue and break while loop
                            break    

                elif choice == "right":
                    #everything above
                    if start_x_coord + ship_length > 9:
                        print("bot thinking")
                    else:
                        for i in range(ship_length):
                            if self.ship_map[start_x_coord+i][start_y_coord] == 1:
                                place = False
                        if place == True:
                            for i in range(ship_length):
                                self.ships[key][2].append([start_x_coord+i,start_y_coord])
                                self.ship_map[start_x_coord+i][start_y_coord] = 1
                            self.ships[key][0] = True
                            break
                elif choice == "down":
                    #everything above
                    if start_y_coord + ship_length > 9:
                        print("bot thinking")
                    else:
                        for i in range(ship_length):
                            if self.ship_map[start_x_coord][start_y_coord+i] == 1:
                                place = False
                        if place == True:
                            for i in range(ship_length):
                                self.ships[key][2].append([start_x_coord,start_y_coord+i])
                                self.ship_map[start_x_coord][start_y_coord+i] = 1
                            self.ships[key][0] = True
                            break
                elif choice == "up":
                    #everything above
                    if start_y_coord - ship_length < 10:
                        print("bot thinking")
                    else:
                        for i in range(ship_length):
                            if self.ship_map[start_x_coord][start_y_coord-i] == 1:
                                place = False
                        if place == True:
                            for i in range(ship_length):
                                self.ships[key][2].append([start_x_coord,start_y_coord-i])
                                self.ship_map[start_x_coord][start_y_coord-i] = 1
                            self.ships[key][0] = True
                            break
                else:
                    raise Warning("Choice missed: unknown error occuring, not from this script")
        return self.ships

    def strike(self):
        while True:
            x_coord = np.random.randint(0,10)
            y_coord = np.random.randint(0,10)
            if self.hits_map[x_coord][y_coord] == 0:
                self.hits_map[x_coord][y_coord] = 1
                break
        return [x_coord,y_coord]

class MediumBot(EasyBot):
    def __init__(self):
        super().__init__()
        self.target_stack = []
        self.last_shot = list()
    def strike(self):
        #check if last shot was hit or miss (if == [] counts as miss)
        #if hit add surrounding squares to target stack if not already in shot list
        if self.success_log[-1] == "sunk":
            self.target_stack = []
        if self.success_log[-1] == "hit":
            
            x = self.last_shot[0]
            y = self.last_shot[1]
            if 0<x:
                if self.hits_map[x-1][y] == 0:
                    self.target_stack.append([x-1,y])
            if 9>x:
                if self.hits_map[x+1][y] == 0:    
                    self.target_stack.append([x+1,y])
            if 0<y:
                if self.hits_map[x][y-y] == 0:
                    self.target_stack.append([x,y-1])
            if 9>y:
                if self.hits_map[x][y+1] == 0:
                    self.target_stack.append([x,y+1])
        #check if the target stack is empty if it is: hunt
        if self.target_stack == []:
            
            targ =  self.hunt()
            
            self.hits_map[targ[0]][targ[1]] = 1
        
        #if it is not empty pop off a coord from the target stack
        else:
            
            targ = self.target_stack.pop()
            self.hits_map[targ[0]][targ[1]] = 1
            print(targ)
        #reset the last shot var to the new coord that is going to be shot at
        self.last_shot = targ
        return targ
        #return the coords [x,y] 
        
    def hunt(self):
        #parity
        #hit even number squares
        hitsequence = list((self.p_ships.keys())) #list(reversed(self.p_ships.keys())) <--- smalles ship first

        for key in hitsequence:
           if self.p_ships[key][0] == True:
                while True:
                    row,column = random.choice(range(10)), random.choice(range(10))
                    if (row+column) % self.p_ships[key][1] != 0:
                        continue
                    if self.hits_map[row][column] == 0:
                        self.hits_map[row][column] = 1
                        self.last_shot = [row,column]
                        return [row,column]


        raise Warning("END OF FUNCTION, CODE FAIL")
    
class HardBot (MediumBot):
    def __init__(self):
        super().__init__()
        self.PROB_MAP = np.zeros([10,10])
        self.hit_ship_coord = []

        
    
    def strike(self):
        #get the result of the last shot
        #update the probability map accordingly
        #get the highest value from the probability map
        #update the last shot and the hits map
        #return the location for hit
        if self.success_log[-1] == "hit":
            self.hit_ship_coord.append(self.last_shot)
            
        
        self.gen_prob_map()
        max = np.argmax(self.PROB_MAP)
    
        max_row = int(max/10)
        max_col = int(max%10)
        target = [max_row,max_col]
        self.last_shot = target
        self.hits_map[target[0]][target[1]] = 1
        
        return target
        raise Warning("WARNING: Bot unable to predict. Reverting to lower class for target")

        return EasyBot().strike()


    def gen_prob_map(self):
       
       prob_map = np.zeros([10,10])

       for key in self.ships:
            length = self.ships[key][1]-1

            for col in range(10):
                for row in range(10):
                    if self.hits_map[row][col] != 1:
                        # get potential ship endpoints
                        endpoints = []
                        # add 1 to all endpoints to compensate for python indexing
                        if row - length >= 0:
                            endpoints.append(((col - length, row), (col + 1, row + 1)))
                        if row + length <= 9:
                            endpoints.append(((col, row), (col + length + 1, row + 1)))
                        if col - length >= 0:
                            endpoints.append(((col, row - length), (col + 1, row + 1)))
                        if col + length <= 9:
                            endpoints.append(((col, row), (col + 1, row + length + 1)))

                        for (start_col, start_row), (end_col, end_row) in endpoints:
                            if np.all(self.hits_map[start_col:end_col, start_row:end_row] == 0):
                                prob_map[start_col:end_col, start_row:end_row] += 1

                    
                    if self.hits_map[col][row] == 1 and [col, row] not in self.ships_sunk_coords:
                        
                        #looking to the right of coord that we are at right now
                        if col+1 <10 and self.hits_map[col+1][row] == 0:

                            #if the coord to its left exists and if has already been hit and the ship it's attached to hasn't been sunk,
                            # then the coord to the right of current is likely to have a ship

                            if (col-1 > -1) and ([col-1, row] in self.hit_ship_coord) and ([col-1, row] not in self.ships_sunk_coords):
                                
                                prob_map[col+1][row] += 25
                            #otherwise it is not as likely to contain ship coord
                            else:
                                prob_map[col+1][row] += 10
                        
                        if col-1 > -1 and self.hits_map[col-1][row] == 0:
                            if col + 1 < 10 and [col+1, row] in self.hit_ship_coord and [col+1, row] not in self.ships_sunk_coords:
                                prob_map[col-1][row] += 25
                            else:
                                prob_map[col-1][row] += 10
                        
                        if row+1<10 and self.hits_map[col][row+1] == 0:
                            if row-1 >-1 and [col,row-1] in self.hit_ship_coord and [col,row-1] not in self.ships_sunk_coords:
                                prob_map[col][row+1] += 25
                            else:
                                prob_map[col][row+1] += 10

                        if row-1 >-1 and self.hits_map[col][row-1] == 0:
                            if row+1 < 10 and [col,row+1] in self.hit_ship_coord and [col,row+1] not in self.ships_sunk_coords:
                                prob_map[col][row-1] += 25
                            else:
                                prob_map[col][row-1] += 10

                    elif self.hits_map[col][row] == 1 and [col,row] not in self.hit_ship_coord:
                        
                        prob_map[col][row] = 0

                        if col+1 <10 and self.hits_map[col+1][row] == 0:
                            if not((col-1 > -1) and ([col-1, row] in self.hit_ship_coord) and ([col-1, row] not in self.ships_sunk_coords)):
                                
                                prob_map[col+1][row] -= 25
                            else:
                                prob_map[col+1][row] -= 10
                        
                        if col-1 > -1 and self.hits_map[col-1][row] == 0:
                            if not(col + 1 < 10 and [col+1, row] in self.hit_ship_coord and [col+1, row] not in self.ships_sunk_coords):
                                prob_map[col-1][row] -= 25
                            else:
                                prob_map[col-1][row] -= 10
                        
                        if row+1<10 and self.hits_map[col][row+1] == 0:
                            if not(row-1 >-1 and [col,row-1] in self.hit_ship_coord and [col,row-1] not in self.ships_sunk_coords):
                                prob_map[col][row+1] -= 25
                            else:
                                prob_map[col][row+1] -= 10

                        if row-1 >-1 and self.hits_map[col][row-1] == 0:
                            if not(row+1 < 10 and [col,row+1] in self.hit_ship_coord and [col,row+1] not in self.ships_sunk_coords):
                                prob_map[col][row-1] -= 25
                            else:
                                prob_map[col][row-1] -= 10
                    
       self.PROB_MAP = prob_map
