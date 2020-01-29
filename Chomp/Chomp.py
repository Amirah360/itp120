from gasp import *

the_maze = Maze()

while not the_maze.finished():
    the_maze.play()

the_maze.done()

#The things below are global constants, that's why they're written in all caps

GRIDE_SIZE = 30
MARGIN = GRID_SIZE

BACKGROUND_COLOR = color.BLACK 
WALL_COLOR = (0.6 * 225, 0.9 * 255, 0.9 * 225)

#   % - Wall
#   . - Food
#   o - Capsule
#   G - Ghost
#   P - Chomp

the_layout = [
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",     # There are 31 '%'s in this line
  "%.....%.................%.....%",
  "%o%%%.%.%%%.%%%%%%%.%%%.%.%%%o%",
  "%.%.....%......%......%.....%.%",
  "%...%%%.%.%%%%.%.%%%%.%.%%%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%.%%%.%.%%% %%%.%.%%%.%...%",
  "%.%%%.......%GG GG%.......%%%.%",
  "%...%.%%%.%.%%%%%%%.%.%%%.%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%%%.%.%%%%.%.%%%%.%.%%%...%",
  "%.%.....%......%......%.....%.%",
  "%o%%%.%.%%%.%%%%%%%.%%%.%.%%%o%",
  "%.....%........P........%.....%",
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]

la_layout = [
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",    
  "%.....%.................%.....%",
  "%o%%%.%.................%.%%%o%",
  "%.%.....%......%......%.....%.%",
  "%.....................%.%%%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%.%%%.%.%%% %%%.%.%%%.%...%",
  "%.%%%.......%GG GG%.......%%%.%",
  "%...%.%%%.%.%%%%%%%.%.%.%.%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%.................%.%%%...%",
  "%.%.....%......%......%.....%.%",
  "%o%%%.%.%%%.......%.....%.%%%o%",
  "%.....%........P........%.....%",
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]

Hourglass = [
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",    
  "%.....%.................%.....%",
  "%o%%%.%.%.............%.%.%%%o%",
  "%.%.....%.............%.....%.%",
  "%...%%%.%.............%.%%%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%.%%%.%.%%% %%%.%.%%%.%...%",
  "%.%%%.......%GG GG%.......%%%.%",
  "%...%.%%%.%.%%%%%%%.%.%%%.%...%",
  "%%%.%...%.%.........%.%...%.%%%",
  "%...%%%.%.............%.%%%...%",
  "%.%.....%.............%.....%.%",
  "%o%%%.%.%%%.........%%%.%.%%%o%",
  "%.....%........P........%.....%",
  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]

class Maze:

    def __init__(self):
        self.have_window = False     
        self.game_over = False      
        self.set_layout(the_layout)     
        set_speed(20)       
#speed is the loop rate 20 loops per sec

    def set_layout(self, layout):
        height = len(layout)                   
        width = len(layout[0])                 
        self.make_window(width, height)
        self.make_map(width, height)        

#layout height is the y value width is x value 
        max_y = height - 1
        for x in range(width):      
            for y in range(height):
                char = layout[max_y - y][x]    
                self.make_object((x, y), char) 

    def make_window(self, width, height):
        grid_width = (width-1) * GRID_SIZE     
        grid_height = (height-1) * GRID_SIZE
        screen_width = 2*MARGIN + grid_width
        screen_height = 2*MARGIN + grid_height
        begin_graphics(screen_width, screen_height, "Chomp", BACKGROUND_COLOR)

    def to_screen(self, point):
        (x, y) = point
        x = x*GRID_SIZE + MARGIN    
        y = y*GRID_SIZE + MARGIN     
        return (x, y)    

#Next class, This is the info about the Immovable class
#This class is a superclass for objects which are stationary. When one of these objects is created it is expected to draw itself on the screen. The Maze object will keep a note of which object is at each location.

class Immovable:
    pass

class Nothing(Immovable):
    pass

    def make_map(self, width, height):
        self.width = width              
        self.height = height
        self.map = []                      
        for y in range(height):
            new_row = []                   
            for x in range(width):
                new_row.append(Nothing())  
            self.map.append(new_row)
        
    def make_object(self, point, character):
        (x, y) = point
        if character == '%':            
            self.map[y][x] = Wall(self, point)

    def finished(self):
        return self.game_over       

    def play(self):
        update_when('next_tick')     

    def done(self):
        end_graphics()               
        self.map = []               

#######

class Wall(Immovable):
    def __init__(self, maze, point):
        self.place = point                      
        self.screen_point = maze.to_screen(point)
        self.maze = maze                    
        self.draw()

    def draw(self):
        (screen_x, screen_y) = self.screen_point
        dot_size = GRID_SIZE * 0.2
    
        Circle(self.screen_point, dot_size, color=WALL_COLOR, filled=True)

    def object_at(self, point):
        (x, y) = point

        if y < 0 or y >= self.height:       
            return Nothing()                

        if x < 0 or x >= self.width:
            return Nothing()

        return self.map[y][x]

    def is_a_wall(self):
        return False 

    def is_a_wall(self):
        return True   

    def draw(self):
        dot_size = GRID_SIZE * 0.2              
        Circle(self.screen_point, dot_size,
               color = WALL_COLOR, filled = 1)   
        (x, y) = self.place

        #list of neighbors
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        # Checks each neighbor.
        for neighbor in neighbors:
            self.check_neighbor(neighbor)
 
    def check_neighbor(self, neighbor):
        maze = self.maze
        object = maze.object_at(neighbor)           

        if object.is_a_wall():                  
            here = self.screen_point                 
            there = maze.to_screen(neighbor)         
            Line(here, there, color=WALL_COLOR, thickness=2) 

#####INTRODUCING CHOMP

class Movable:
    def __init__(self, maze, point, speed):
        self.maze = maze                      
        self.place = point                  
        self.speed = speed
#Aka Pacman
class Chomp(Movable):
    def __init__(self, maze, point):
        Movable.__init__(self, maze, point, 
                         CHOMP_SPEED)

    def move(self):
        keys = keys_pressed()
        if   'left' in keys: self.move_left()   
        elif 'right' in keys: self.move_right() 
        elif 'up' in keys: self.move_up()
        elif 'down' in keys: self.move_down()  

    def move_left(self):
        self.try_move((-1, 0))

    def move_right(self):
        self.try_move((1, 0))

    def move_up(self):
        self.try_move((0, 1))

    def move_down(self):
        self.try_move((0, -1))

    def try_move(self, move):
        (move_x, move_y) = move
        (current_x, current_y) = self.place
        (nearest_x, nearest_y) = (self.nearest_grid_point())

        if self.furthest_move(move) == (0, 0):  
            return
        if move_x != 0 and current_y != nearest_y:  
            move_x = 0                                 
            move_y = nearest_y - current_y          

        elif move_y != 0 and current_x != nearest_x:   
            move_y = 0                                  
            move_x = nearest_x - current_x          

        move = self.furthest_move((move_x, move_y)) 
        self.move_by(move)                             

    def furthest_move(self, movement):
        (move_x, move_y) = movement                     
        (current_x, current_y) = self.place         
        nearest = self.nearest_grid_point()             
        (nearest_x, nearest_y) = nearest
        maze = self.maze

        if move_x > 0:                              
            next_point = (nearest_x+1, nearest_y)
            if maze.object_at(next_point).is_a_wall():
                if current_x+move_x > nearest_x:         
                    move_x = nearest_x - current_x      

        elif move_x < 0:                                 
            next_point = (nearest_x-1, nearest_y)
            if maze.object_at(next_point).is_a_wall():
                if current_x+move_x < nearest_x:        
                    move_x = nearest_x - current_x       

        if move_y > 0:                                    
            next_point = (nearest_x, nearest_y+1)
            if maze.object_at(next_point).is_a_wall():
                if current_y+move_y > nearest_y:         
                    move_y = nearest_y - current_y      

        elif move_y < 0:                                
            next_point = (nearest_x, nearest_y-1)
            if maze.object_at(next_point).is_a_wall():
                if current_y+move_y < nearest_y:        
                    move_y = nearest_y - current_y 

        if move_x > self.speed:                 
            move_x = self.speed
        elif move_x < -self.speed:
            move_x = -self.speed

        if move_y > self.speed:
            move_y = self.speed
        elif move_y < -self.speed:
            move_y = -self.speed

        return (move_x, move_y)  

    def nearest_grid_point(self):
        (current_x, current_y) = self.place
        grid_x = int(current_x + 0.5)        
        grid_y = int(current_y + 0.5)       
        return (grid_x, grid_y)   

CHOMP_COLOR = color.YELLOW                   
CHOMP_SIZE = GRID_SIZE * 0.8                 
CHOMP_SPEED = 0.25                      

    def __init__(self, maze, point):
        self.direction = 0                   
        Movable.__init__(self, maze, point,  
                         CHOMP_SPEED)

    def draw(self):
        maze = self.maze
        screen_point = maze.to_screen(self.place)
        angle = self.get_angle()                
        endpoints = (self.direction + angle,        
                     self.direction + 360 - angle)
        self.body = Arc(screen_point, CHOMP_SIZE,   
                        endpoints[0], endpoints[1],
                        filled=True, color=CHOMP_COLOR)

    def get_angle(self):
        (x, y) = self.place                                 
        (nearest_x, nearest_y) = (self.nearest_grid_point())
        distance = (abs(x-nearest_x) + abs(y-nearest_y))      
        return 1 + 90*distance                              

    def make_object(self, point, character):
        (x, y) = point
        if character == '%':                    
            self.map[y][x] = Wall(self, point)
        elif character == 'P':                  
            chomp = Chomp(self, point)
            self.movables.append(chomp)
    def set_layout(self, layout):
        height = len(layout)             
        width = len(layout[0])
        self.make_window(width, height)
        self.make_map(width, height)
        self.movables = []              

        max_y = height - 1
        for x in range(width):           
            for y in range(height):
                char = layout[max_y - y][x]
                self.make_object((x, y), char)

        for movable in self.movables:
            movable.draw()

    def done(self):
        end_graphics()                  
        self.map = []                    
        self.movables = []      

    def play(self):
        for movable in self.movables:   
            movable.move()
        update_when('next_tick')

#####FOOD, GLORIOUS FOOD!

