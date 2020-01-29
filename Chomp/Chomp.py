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

class Maze 
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
