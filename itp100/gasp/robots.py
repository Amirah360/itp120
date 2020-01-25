from gasp import *

#challenge 3
begin_graphics()
ball_x = 5
ball_y = 5
c = Circle((ball_x, ball_y), 5)
while ball_x < 635:
    sleep(0.02)
    ball_x += 4
    ball_y += 3
    move_to(c, (ball_x, ball_y))
end_graphics()

begin_graphics()         
finished = False

def place_player():
    global player_x, player_y, player_shape
    player_x = random_between(0, 63)
    player_y = random_between(0, 47)

def collided():
    if player_y == robot_y and player_x == robot_x:
        return True
    else:
        return False

def safely_place_player():
    place_player()
    global player_x, player_y, player_shape

    while collided():
        place_player()
        player_shape = Circle((10* player_x + 5, 10 * player_y + 5), 5, filled=True)

def safely_place_player():
    place_player()
    global player_x, player_y, player_shape

    while collided():
        place_player()

def place_robot():
    global robot_x, robot_y, robot_shape
    robot_x = random_between(0, 63)
    robot_y = random_between(0, 47)
    robot_shape = Box((10*robot_x, 10*robot_y), 8, 8)

def move_player():
    global player_x, player_y, player_shape
    
