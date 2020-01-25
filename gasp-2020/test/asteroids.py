from gasp import *
import math
import time
import random

x = 600
y = 600


class Game:
    def __init__(self):
        begin_graphics(x, y, background=(0, 0, 0))
        global game
        game = self
        self.round = 1
        self.playing = True
        self.lives = 3
        self.respawn = False
        self.wait = False
        self.respawn_text = None
        set_speed(200)
        while self.playing:
            clear_screen()
            self.start_round()
            self.time = time.time()
            self.text = Text("0", (100, 100), size=18, color=color.WHITE)
            self.playing = self.play_game()
            self.round += 1
        clear_screen()
        Text(
            "You died on round "+str(self.round-1),
            (x/2-100, y/2),
            ize=18,
            color=color.WHITE
        )
        sleep(1)
        end_graphics()

    def start_round(self):
        Text(
            "Round "+str(self.round),
            (x/2-50, y/2),
            size=18,
            color=color.WHITE
        )
        pos_x = list(range(0, int(x/4)))
        for i in range(3 * int(x/4), x):
            pos_x.append(i)
        pos_y = list(range(0, int(y/4)))
        for i in range(3*int(y/4), y):
            pos_y.append(i)
        sleep(1)
        clear_screen()
        i = 0
        self.astroids = []
        self.explosions = []
        while i < 5+self.round:
            self.astroids.append(Astroid(
                random.randint(1, 3),
                pos_x[random.randint(0, len(pos_x)-1)],
                pos_y[random.randint(0, len(pos_y)-1)])
            )
            i += 1
        self.ship = Ship()
        self.shots = []

    def play_game(self):
        while True:
            if self.respawn:
                self.respawn_text = Text(
                    "press 'r' to respawn",
                    (x/2-100, y/2),
                    color=color.WHITE,
                    size=18
                )
                self.wait = True
                self.respawn = False
            elif self.wait:
                if "r" in keys_pressed():
                    self.ship = Ship()
                    self.wait = False
                    remove_from_screen(self.respawn_text)
            else:
                self.ship.update()
            for shot in self.shots:
                shot.update()
            for e in self.explosions:
                e.update()
            for astroid in self.astroids:
                astroid.update()
            # sleep(.01)
            update_when("next_tick")
            t = str(1 / (time.time() - self.time))
            remove_from_screen(self.text)
            self.time = time.time()
            self.text = Text(t, (100, 100), color=color.WHITE)
            if len(self.astroids) == 0:
                return True
            if self.lives == 0:
                return False


class Ship:
    def __init__(self):
        self.ship = Polygon(
            [(x/2, y/2+10), (x/2-5, y/2-5), (x/2, y/2), (x/2+5, y/2-5)],
            color=color.WHITE,
            filled=True
        )
        self.rot = 0
        self.x = x / 2
        self.y = y / 2
        self.move_x = 0
        self.move_y = 0
        self.speed = 0
        self.shot_time = time.time()
        self.text = Text(
            "Lives: "+str(game.lives),
            (0, y-30),
            size=18,
            color=color.WHITE
        )

    def update(self):
        if "d" in keys_pressed():
            rotate_by(self.ship, +4)
            self.rot += 4
        if "a" in keys_pressed():
            rotate_by(self.ship, -4)
            self.rot -= 4
        if "w" in keys_pressed(): 
            self.move_x += .05 * math.cos(math.radians(90 - self.rot))
            self.move_y += .05 * math.sin(math.radians(90 - self.rot))
            self.speed = math.sqrt(self.move_x**2+self.move_y**2)
            if self.speed > 1.5:
                a = math.atan2(self.move_y, self.move_x)
                self.move_x = 1.5 * math.cos(a)
                self.move_y = 1.5*math.sin(a)
        elif "s" in keys_pressed():
            self.speed -= .015
            a = math.atan2(self.move_y, self.move_x)
            self.move_x = self.speed * math.cos(a)
            self.move_y = self.speed*math.sin(a)
            if self.speed < 0:
                self.move_x = 0
                self.move_y = 0
        else:
            self.speed -= .005
            a = math.atan2(self.move_y, self.move_x)
            self.move_x = self.speed * math.cos(a)
            self.move_y = self.speed * math.sin(a)
            if self.speed < 0:
                self.move_x = 0
                self.move_y = 0
        if " " in keys_pressed() and time.time() > self.shot_time:
            self.shot_time = time.time() + .4
            game.shots.append(Shot(self.x, self.y, -1*(self.rot-90)))
        self.x += self.move_x
        self.y += self.move_y
        if self.x > x:
            self.x = 0
        if self.x < 0:
            self.x = x
        if self.y > y:
            self.y = 0
        if self.y < 0:
            self.y = y
        move_to(self.ship, (self.x, self.y))

    def kill(self):
        remove_from_screen(self.ship)
        remove_from_screen(self.text)
        game.lives -= 1
        game.respawn = True
        game.explosions.append(Explosion(self.x, self.y))


class Shot:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.moved = 0
        self.move_x = 3 * math.cos(math.radians(direction))
        self.move_y = 3 * math.sin(math.radians(direction))
        self.shot = Circle(
            (self.x, self.y),
            2,
            filled=True,
            color=color.WHITE
        )

    def update(self):
        self.x += self.move_x
        self.y += self.move_y
        if self.x > x:
            self.x = 0
        if self.x < 0:
            self.x = x
        if self.y > y:
            self.y = 0
        if self.y < 0:
            self.y = y
        self.moved += math.sqrt(self.move_x**2 + self.move_y**2)
        if self.moved > 400:
            self.kill()
        move_to(self.shot, (self.x, self.y))

    def kill(self):
        game.shots.remove(self)
        remove_from_screen(self.shot)


class Astroid:
    def __init__(self, size, x, y):
        self.x = x
        self.y = y
        self.points = []
        self.size = size
        r = 0
        self.rad = 10 * (1 + size)
        while r < math.pi * 2:
            self.points.append(
                (int(10*(random.random()+size)*math.cos(r)+self.x),
                 int(10*(random.random()+size)*math.sin(r)+self.y))
            )
            r += math.pi / 5
        self.rock = Polygon(self.points, color=color.WHITE, filled=True)
        self.direction = math.pi*2*random.random()

    def update(self):
        for shot in game.shots:
            if math.sqrt((self.x-shot.x)**2+(self.y-shot.y)**2) < self.rad:
                shot.kill()
                self.kill()
                if self.size != 1:
                    self.split()
        shot2ship = math.sqrt((self.x-game.ship.x)**2+(self.y-game.ship.y)**2)
        if shot2ship < self.rad+3:
            if not game.wait and not game.respawn:
                game.ship.kill()
        self.x += math.cos(self.direction)
        self.y += math.sin(self.direction)
        if self.x > x:
            self.x = 0
        if self.x < 0:
            self.x = x
        if self.y > y:
            self.y = 0
        if self.y < 0:
            self.y = y
        move_to(self.rock, (self.x, self.y))

    def split(self):
        game.astroids.append(Astroid(self.size-1, self.x, self.y))
        game.astroids.append(Astroid(self.size-1, self.x, self.y))

    def kill(self):
        game.astroids.remove(self)
        remove_from_screen(self.rock)
        game.explosions.append(Explosion(self.x, self.y))


class Explosion:
    def __init__(self, x, y):
        self.points = []
        i = 0
        while i < 10:
            self.points.append(ExplotionPoint(x, y))
            i += 1

    def update(self):
        running = False
        for p in self.points:
            if p.update():
                running = True
            else:
                self.points.remove(p)
        if not running:
            for p in self.points:
                remove_from_screen(p.circle)
            game.explosions.remove(self)


class ExplotionPoint:
    def __init__(self, x, y):
        self.circle = Circle((x, y), 2, filled=True, color=color.WHITE)
        self.moved = 0
        self.direction = random.random() * 2 * math.pi
        self.max_moved = random.randint(30, 50)
        self.speed = random.randint(50, 100) / 50

    def update(self):
        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed
        self.moved += math.sqrt(dx**2+dy**2)
        move_by(self.circle, dx, dy)
        if self.moved > self.max_moved:
            remove_from_screen(self.circle)
            return False
        return True


Game()
