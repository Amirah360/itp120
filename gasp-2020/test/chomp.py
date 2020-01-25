from gasp import *

GRID_SIZE = 30                     # This sets size of everything
MARGIN = GRID_SIZE                 # How much space to leave round edge

BACKGROUND_COLOR = color.BLACK     # Colors we use
WALL_COLOR = (0.6 * 255, 0.9 * 255, 0.9 * 255)

CHOMP_COLOR = color.YELLOW
CHOMP_SIZE = GRID_SIZE * 0.8        # How big to make Chomp
CHOMP_SPEED = 0.25                  # How fast Chomp moves

FOOD_COLOR = color.RED
FOOD_SIZE = GRID_SIZE * 0.15        # How big to make food

GHOST_COLORS = [color.RED,             # A list of all Ghost colors
                color.GREEN,           # Put this at the top with the
                color.BLUE,            # other constants
                color.PURPLE]

GHOST_SPEED = 0.25                      # How fast Ghosts move

GHOST_SHAPE = [
    (0, -0.5),
    (0.25, -0.75),       # Coordinates which define Ghost's shape
    (0.5, -0.5),         # measured grid units
    (0.75, -0.75),
    (0.75, 0.5),
    (0.5, 0.75),
    (-0.5, 0.75),
    (-0.75, 0.5),
    (-0.75, -0.75),
    (-0.5, -0.5),
    (-0.25, -0.75)
  ]

CAPSULE_COLOR = color.WHITE           # Put these at top of your program
CAPSULE_SIZE = GRID_SIZE * 0.3        # How big to make capsules

SCARED_COLOR = color.WHITE     # Color ghosts turn when Chomp eats a capsule
SCARED_TIME = 300              # How long Ghosts stay scared

WARNING_TIME = 50


class Immovable:
    def is_a_wall(self):
        return False               # Most objects aren't walls so say no

    def eat(self, chomp):          # Default eat method
        pass                       # Do nothing


class Nothing(Immovable):
    pass


class Movable:
    def __init__(self, maze, point, speed):
        self.maze = maze                      # For finding other objects
        self.place = point                    # Our current position
        self.speed = speed                    # Remember speed
        self.start = point                    # Our starting position

    def furthest_move(self, movement):
        (move_x, move_y) = movement           # How far to move
        (current_x, current_y) = self.place   # Where are we now?
        nearest = self.nearest_grid_point()   # Where's nearest grid point?
        (nearest_x, nearest_y) = nearest
        maze = self.maze

        if move_x > 0:              # Are we moving towards a wall on right?
            next_point = (nearest_x+1, nearest_y)
            if maze.object_at(next_point).is_a_wall():
                if current_x+move_x > nearest_x:         # Are we close enough?
                    move_x = nearest_x - current_x       # Stop just before it

        elif move_x < 0:            # Are we moving towards a wall on left?
            next_point = (nearest_x-1, nearest_y)
            if maze.object_at(next_point).is_a_wall():
                if current_x+move_x < nearest_x:         # Are we close enough?
                    move_x = nearest_x - current_x       # Stop just before it

        if move_y > 0:              # Are we moving towards a wall above us?
            next_point = (nearest_x, nearest_y+1)
            if maze.object_at(next_point).is_a_wall():
                if current_y+move_y > nearest_y:         # Are we close enough?
                    move_y = nearest_y - current_y       # Stop just before it

        elif move_y < 0:            # Are we moving towards a wall below us?
            next_point = (nearest_x, nearest_y-1)
            if maze.object_at(next_point).is_a_wall():
                if current_y+move_y < nearest_y:         # Are we close enough?
                    move_y = nearest_y - current_y       # Stop just before it

        if move_x > self.speed:     # Don't move further than our speed allows
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
        grid_x = int(current_x + 0.5)       # Find nearest vertical grid line
        grid_y = int(current_y + 0.5)       # Find nearest horizontal grid line
        return (grid_x, grid_y)             # Return where they cross

    def capsule_eaten(self):        # Called when a Capsule has been eaten
        pass                        # Normally, do nothing


class Chomp(Movable):
    def __init__(self, maze, point):
        self.direction = 0                   # Start off facing right
        Movable.__init__(self, maze, point,  # Call Movable initializer
                         CHOMP_SPEED)

    def move(self):
        keys = keys_pressed()
        if 'left' in keys:
            self.move_left()     # Is left arrow pressed?
        elif 'right' in keys:
            self.move_right()    # Is right arrow pressed?
        elif 'up' in keys:
            self.move_up()       # Is up arrow pressed?
        elif 'down' in keys:
            self.move_down()     # Is down arrow pressed?
        self.maze.chomp_is(self, self.place)  # Tell Maze where we are

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

        # If we can't move, do nothing.
        if self.furthest_move(move) == (0, 0):
            return
        # If we're moving horizontally
        if move_x != 0 and current_y != nearest_y:
            move_x = 0                      # but aren't on grid line
            move_y = nearest_y - current_y  # move towards grid line
        # If we're moving vertically
        elif move_y != 0 and current_x != nearest_x:
            move_y = 0                      # but aren't on grid line
            move_x = nearest_x - current_x  # Move towards grid line

        move = self.furthest_move((move_x, move_y))  # Don't go too far
        self.move_by(move)

    def draw(self):
        maze = self.maze
        screen_point = maze.to_screen(self.place)
        # Work out half of mouth angle
        angle = self.get_angle()
        # Rotate according to direction
        endpoints = (self.direction + angle, self.direction + 360 - angle)
        self.body = Arc(
            screen_point,
            CHOMP_SIZE,  # Draw sector
            endpoints[0],
            endpoints[1],
            filled=True,
            color=CHOMP_COLOR
        )

    def get_angle(self):
        # Work out distance
        (x, y) = self.place
        # to nearest grid point
        (nearest_x, nearest_y) = (self.nearest_grid_point())
        # Between -1/2 and 1/2
        distance = (abs(x-nearest_x) + abs(y-nearest_y))
        # Between 1 and 46
        return 1 + 90 * distance

    def move_by(self, move):
        self.update_position(move)
        old_body = self.body          # Get old body for removal
        self.draw()                   # Make new body
        remove_from_screen(old_body)  # Remove old body

        (x, y) = self.place                        # Get distance to
        nearest_point = self.nearest_grid_point()  # nearest grid point
        (nearest_x, nearest_y) = nearest_point
        distance = (abs(x-nearest_x) +             # As before
                    abs(y-nearest_y))

        if distance < self.speed * 3 / 4:        # Are we close enough to eat?
            object = self.maze.object_at(nearest_point)
            object.eat(self)                     # If so, eat it

    def update_position(self, move):
        (old_x, old_y) = self.place              # Get old coordinates
        (move_x, move_y) = move                  # Unpack vector
        (new_x, new_y) = (old_x+move_x, old_y+move_y)  # Get new coordinates
        self.place = (new_x, new_y)                    # Update coordinates

        if move_x > 0:                   # If we're moving right ...
            self.direction = 0           # ... turn to face right.
        elif move_y > 0:                 # If we're moving up ...
            self.direction = 90          # ... turn to face up.
        elif move_x < 0:                 # If we're moving left ...
            self.direction = 180         # ... turn to face left.
        elif move_y < 0:                 # If we're moving down ...
            self.direction = 270         # ... turn to face down.

    def chomp_is(self, chomp, point):
        pass                             # Chomp knows where Chomp is


class Maze:
    def __init__(self, levels):
        self.levels = levels
        self.level = -1
        self.have_window = False        # We haven't made window yet
        self.game_over = False          # Game isn't over yet
        self.loss = False
        self.height = len(levels[0])
        self.width = len(levels[0][0])
        self.make_window(self.width, self.height)
        set_speed(40)                   # Set loop rate to 40 loops per second

    def next_level(self):
        self.level += 1
        if self.level >= len(self.levels) or self.loss:
            return False
        self.game_over = False
        clear_screen()
        self.set_layout(self.levels[self.level])     # Make all objects
        return True

    def set_layout(self, layout):
        self.make_map(self.width, self.height)   # Start new map
        self.movables = []
        self.food_count = 0                      # Start with no Food

        max_y = self.height - 1
        for x in range(self.width):              # Go through whole layout
            for y in range(self.height):
                char = layout[max_y - y][x]      # See discussion 1 page ago
                self.make_object((x, y), char)   # Create object

        for movable in self.movables:            # Draw all movables
            movable.draw()

    def make_window(self, width, height):
        grid_width = (width - 1) * GRID_SIZE     # Work out size of window
        grid_height = (height - 1) * GRID_SIZE
        screen_width = 2 * MARGIN + grid_width
        screen_height = 2 * MARGIN + grid_height
        # Create window
        begin_graphics(screen_width, screen_height, "Chomp", BACKGROUND_COLOR)

    def to_screen(self, point):
        (x, y) = point
        x = x * GRID_SIZE + MARGIN     # Work out coordinates of point
        y = y * GRID_SIZE + MARGIN     # on screen
        return (x, y)

    def make_map(self, width, height):
        self.width = width                 # Store size of layout
        self.height = height
        self.map = []                      # Start with empty list
        new_row = []                       # Make new row list
        for x in range(width):
            new_row.append(Nothing())      # Add entry to list
        for y in range(height):
            self.map.append(new_row[:])    # Put row in map

    def make_object(self, point, character):
        (x, y) = point
        if character == '%':                         # Is it a wall?
            self.map[y][x] = Wall(self, point)
        elif character == 'P':                       # Is it Chomp?
            self.movables.append(Chomp(self, point))
        elif character == '.':
            self.food_count = self.food_count + 1    # Add 1 to count
            self.map[y][x] = Food(self, point)       # Put new object in map
        elif character == 'G':                       # Is it a Ghost?
            # Create a Ghost and Add it to list of Movables
            self.movables.append(Ghost(self, point))
        elif character == 'o':                       # Is it a Capsule?
            self.map[y][x] = Capsule(self, point)    # Put new Capsule in map

    def finished(self):
        return self.game_over        # Stop if game is over

    def done(self):
        end_graphics()               # We've finished
        self.map = []
        self.movables = []

    def object_at(self, point):
        (x, y) = point

        if y < 0 or y >= self.height:    # If point is outside maze,
            return Nothing()             # return nothing.

        if x < 0 or x >= self.width:
            return Nothing()

        return self.map[y][x]

    def play(self):
        for movable in self.movables:     # Move each object
            movable.move()
        update_when('next_tick')          # Pause before next loop

    def remove_food(self, place):
        (x, y) = place
        self.map[y][x] = Nothing()             # Make map entry empty
        self.food_count = self.food_count - 1  # There is 1 less bit of Food
        if self.food_count == 0:               # If there is no food left...
            self.win()                         # ... Chomp wins

    def win(self):
        print("You win!")
        self.game_over = True

    def chomp_is(self, chomp, point):
        for movable in self.movables:           # Go through Movables
            movable.chomp_is(chomp, point)      # Pass message on to each

    def lose(self):
        print("You lose!")
        self.game_over = True
        self.loss = True

    def remove_capsule(self, place):
        (x, y) = place
        self.map[y][x] = Nothing()      # Make map entry empty
        for movable in self.movables:   # Tell all Movables that a capsule
            movable.capsule_eaten()     # has been eaten


class Wall(Immovable):
    def __init__(self, maze, point):
        self.place = point                          # Store our position
        self.screen_point = maze.to_screen(point)
        self.maze = maze                            # Keep hold of Maze
        self.draw()

    def draw(self):
        (x, y) = self.place
        neighbors = [(x+1, y), (x-1, y),        # Make list of our neighbors.
                     (x, y+1), (x, y-1)]
        for neighbor in neighbors:              # Check each neighbor in turn.
            self.check_neighbor(neighbor)

    def is_a_wall(self):
        return True                    # This object is a wall, so say yes

    def check_neighbor(self, neighbor):
        maze = self.maze
        object = maze.object_at(neighbor)            # Get object

        if object.is_a_wall():                       # Is it a wall?
            here = self.screen_point                 # Draw line from here...
            there = maze.to_screen(neighbor)         # ... to there if it is
            Line(here, there, color=WALL_COLOR, thickness=2)


class Food(Immovable):
    def __init__(self, maze, point):
        self.place = point
        self.screen_point = maze.to_screen(point)
        self.maze = maze
        self.draw()

    def draw(self):
        self.dot = Circle(self.screen_point,
                          FOOD_SIZE,
                          color=FOOD_COLOR,
                          filled=True)

    def eat(self, chomp):
        remove_from_screen(self.dot)           # Remove dot from screen
        self.maze.remove_food(self.place)      # Tell Maze


class Ghost(Movable):
    num = 0

    def __init__(self, maze, start):
        Ghost.num += 1
        self.next_point = start         # Don't move anywhere to start with
        self.movement = (0, 0)          # We were going nowhere

        self.color = GHOST_COLORS[Ghost.num % 4]   # Pick a color from list

        self.original_color = self.color     # Store original color
        self.time_left = 0                   # We're not scared yet

        Movable.__init__(self, maze,    # Just call Movable's initializer
                         start, GHOST_SPEED)

    def draw(self):
        maze = self.maze
        (screen_x, screen_y) = (
            maze.to_screen(self.place))    # Get our screen coordinates
        coords = []                        # Build up a list of coordinates
        for (x, y) in GHOST_SHAPE:
            coords.append((x*GRID_SIZE + screen_x,
                           y*GRID_SIZE + screen_y))

        self.body = Polygon(coords, color=self.color,  # Draw body
                            filled=True)

    def move(self):
        (current_x, current_y) = self.place  # Get vector to next point
        (next_x, next_y) = self.next_point
        move = (next_x - current_x,
                next_y - current_y)
        move = self.furthest_move(move)      # See how far we can go
        if move == (0, 0):                   # If we're getting nowhere...
            move = self.choose_move()        # ... try another direction
        self.move_by(move)                   # Make our move
        if self.time_left > 0:               # Are we scared?
            self.update_scared()             # Update time and color

    def update_scared(self):
        self.time_left = self.time_left - 1  # Decrease time left
        time_left = self.time_left
        if time_left < WARNING_TIME:         # Are we flashing?
            if time_left % 2 == 0:           # Is ``time_left`` even?
                color = self.original_color  # Return to our old color
            else:
                color = SCARED_COLOR         # Go the scared color
            self.change_color(color)         # Actually change color

    def choose_move(self):
        (move_x, move_y) = self.movement     # Direction we were going
        (nearest_x, nearest_y) = (self.nearest_grid_point())
        possible_moves = []

        if move_x >= 0 and self.can_move_by((1, 0)):  # Can we move right?
            possible_moves.append((1, 0))

        if move_x <= 0 and self.can_move_by((-1, 0)):  # Can we move left?
            possible_moves.append((-1, 0))

        if move_y >= 0 and self.can_move_by((0, 1)):   # Can we move up?
            possible_moves.append((0, 1))

        if move_y <= 0 and self.can_move_by((0, -1)):  # Can we move down?
            possible_moves.append((0, -1))

        # Is there anywhere to go?
        if len(possible_moves) != 0:
            # Pick random direction
            choice = random_between(0, len(possible_moves) - 1)
            move = possible_moves[choice]
            (move_x, move_y) = move
        else:
            move_x = -move_x            # Turn round as last resort
            move_y = -move_y
            move = (move_x, move_y)

        (x, y) = self.place
        self.next_point = (x+move_x, y+move_y)  # Set next point

        self.movement = move                    # Store this move for next time
        return self.furthest_move(move)         # Return move

    def can_move_by(self, move):
        # How far can we move in this direction?
        move = self.furthest_move(move)
        return move != (0, 0)               # Can we actually go anywhere?

    def move_by(self, move):
        (old_x, old_y) = self.place         # Get old coordinates
        (move_x, move_y) = move             # Unpack vector

        (new_x, new_y) = (old_x+move_x, old_y+move_y)  # Get new coordinates
        self.place = (new_x, new_y)                    # Update coordinates

        screen_move = (move_x * GRID_SIZE,
                       move_y * GRID_SIZE)
        # Move body on the screen
        move_by(self.body, screen_move[0], screen_move[1])

    def chomp_is(self, chomp, point):
        (my_x, my_y) = self.place
        (his_x, his_y) = point
        X = my_x - his_x
        Y = my_y - his_y
        DxD = X*X + Y*Y
        limit = 1.6*1.6
        if DxD < limit:
            self.bump_into(chomp)

    def capsule_eaten(self):
        self.change_color(SCARED_COLOR)      # Change to scared color
        self.time_left = SCARED_TIME

    def change_color(self, new_color):
        self.color = new_color               # Change color
        self.redraw()                        # Recreate the body

    def redraw(self):
        old_body = self.body
        self.draw()
        remove_from_screen(old_body)

    def bump_into(self, chomp):       # This should also be in your program
        if self.time_left != 0:       # Are we scared?
            self.captured(chomp)      # We've been captured
        else:
            self.maze.lose()          # Otherwise we lose as before

    def captured(self, chomp):
        self.place = self.start             # Return to our original place...
        self.color = self.original_color    # ... and color
        self.time_left = 0                  # We're not scared
        self.redraw()                       # Update screen


class Capsule(Immovable):
    def __init__(self, maze, point):
        self.place = point
        self.screen_point = maze.to_screen(point)
        self.maze = maze
        self.draw()

    def draw(self):
        (screen_x, screen_y) = self.screen_point
        self.dot = Circle((screen_x, screen_y),
                          CAPSULE_SIZE,
                          color=CAPSULE_COLOR,
                          filled=True)

    def eat(self, chomp):
        remove_from_screen(self.dot)          # Remove dot from screen
        self.maze.remove_capsule(self.place)  # Tell Maze to scare ghosts


# The shape of the maze.  Each character
# represents a different type of object
#   % - Wall
#   . - Food
#   o - Capsule
#   G - Ghost
#   P - Chomp
# Other characters are ignored

def create_levels(file_name):
    levels = []
    level = []
    making_level = False

    file = open(file_name, "r")

    for line in file.readlines():
        line = line[:-1]

        if "[start maze]" in line:
            level = []
            making_level = True
            first = True
            len_first = 0

        elif "[end maze]" in line:
            levels.append(level)
            making_level = False

        elif first:
            first = False
            len_first = len(line)

        elif making_level and len(line) != len_first:
            print(line)
            raise ValueError("Line Lengths don't match!")

        if making_level and "[start maze]" not in line:
            level_line = ""
            for character in line:
                if character in "%.oGP ":
                    level_line += character
            level.append(level_line)

    return levels


# Make Maze object
the_maze = Maze(create_levels("chomp_levels.dat"))

while the_maze.next_level():
    while not the_maze.finished():    # Keep playing until we're done
        the_maze.play()

the_maze.done()                   # We're finished
