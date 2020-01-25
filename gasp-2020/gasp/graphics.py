#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This program is part of GASP, an immediate mode graphics library and
# accompanying educational resources for beginning Programmers using Python.
# Copyright (C) 2020, the GASP Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import random
import contextlib
from time import sleep
from math import radians

# Suppress output message on pygame import
with contextlib.redirect_stdout(None):
    import pygame


# === Module Level Vars ===

display = None
sprites = []
GASP_BG_COLOR = (255,255,255)
framerate = 10
screen_height = None
screen_width = None
clock = pygame.time.Clock()

# === Classes ===

class GaspException(Exception):
    def __init__(self, value):
        self.value = value

        def __str__(self):
            return repr(self.value)


class Shape:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def move_to(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def move_by(self, x, y):
        self.x += x
        self.y += y


class Box(Shape):
    def __init__(self, position, width, height, color=(0, 0, 0), filled=False):
        super().__init__(position)
        self.width = width
        self.height = height
        self.color = color
        self.filled = filled
        sprites.append(self)
        self.draw()
        update_window()

    def draw(self):
        n = to_gasp_coord((self.x,self.y))
        x = n[0]
        y = n[1]
        if self.filled:
            pygame.draw.rect(
                display,
                self.color,
                (x,y, self.width, self.height)
            )
            return

        pygame.draw.rect(
            display,
            self.color,
            (x, y, self.width, self.height),
            2  # thickness
        )


class Polygon(Shape):
    def __init__(self, coords, color=(0, 0, 0), filled=False):
        #super().__init__(coords[0])
        self.points = coords
        self.color = color
        self.filled = filled
        sprites.append(self)
        self.draw()
        update_window()

    def move_by(self, x, y):
        self.points = [(point[0]+x,point[1]+y) for point in self.points]
        update_window()

    def move_to(self, coord):
        move_x = coord[0] - self.points[0][0]
        move_y = coord[1] - self.points[0][1]
        self.points = [ (point[0]+move_x, point[1] + move_y) for point in self.points]
        update_window()

    def draw(self):
        cp = [to_gasp_coord((point[0],point[1])) for point in self.points]
        if self.filled:
            pygame.draw.polygon(
                display,
                self.color,
                cp
            )
            return

        pygame.draw.rect(
            display,
            self.color,
            self.points,
            2  # thickness
        )


class Arc(Shape):
    def __init__(self,point,size,start_angle,end_angle,filled=True,color=(0,0,0)):
        self.point = point
        self.size = size
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.filled = filled
        self.color = color
        
        
        self.point = to_gasp_coord(self.point)

        sprites.append(self)
        self.draw()
        update_window()

    def draw(self):
        if self.filled:
            pygame.draw.arc(
                display,
                self.color,
                [self.point[0]-self.size, self.point[1]-self.size, 2*self.size, 2*self.size],
                radians(self.start_angle),
                radians(self.end_angle),
                100
            )

            return
        pygame.draw.arc(
            display,
            self.color,
            [self.point[0]-self.size, self.point[1]-self.size, 2*self.size, 2*self.size],
            radians(self.start_angle),
            radians(self.end_angle),
            1
        )
        

class Line(Shape):
    def __init__(self, start, end, color = (0, 0, 0), thickness = 1):
        super().__init__((start,end))
        self.start = start
        self.end = end
        self.color = color
        self.thickness = thickness
        sprites.append(self)
        self.draw()
        update_window()

    def draw(self):
        s = to_gasp_coord((self.start))
        e = to_gasp_coord((self.end))
        pygame.draw.line(
            display,
            self.color,
            s,
            e,
            self.thickness
        )
        return


class Text(Shape):
    def __init__(self, text, position, size=36, color = (255,255,0)):
        super().__init__(position)
        self.text = text
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.render = self.font.render(self.text, True, color)
        sprites.append(self)
        update_window()
        #print(f'Tried to render text at ({self.x}, {self.y})')

    def draw(self):
        display.blit(self.render, (self.x, self.y))


class Circle(Shape):
    def __init__(self, position, radius, color=(0, 0, 0), filled=False):
        super().__init__(position)

        self.radius = radius
        self.filled = filled
        self.color = color

        sprites.append(self)
        self.draw()
        update_window()

    def draw(self):
        #480
        if self.filled:
            pygame.draw.circle(
                display,
                self.color,
                to_gasp_coord((self.x, self.y)),
                self.radius
            )
            return

        pygame.draw.circle(
            display,
            self.color,
            to_gasp_coord((self.x, self.y)),
            self.radius,
            2
        )


# === Decorators ===

def no_window(func):
    def wrapper(*args, **kwargs):
        if display:
            raise GaspException("A window is already created!")
        return func(*args, **kwargs)
    return wrapper


def requires_window(func):
    def wrapper(*args, **kwargs):
        if not display:
            raise GaspException("A window has not been created!")
        return func(*args, **kwargs)
    return wrapper


# === Graphics ===

@no_window
def begin_graphics(s_w=640,s_h=480,screen_title=":O GASP!",background=(255,255,255)):
    global display   # I expected this to work without the global
    global GASP_BG_COLOR
    global screen_width
    global screen_height
    screen_width = s_w
    screen_height = s_h
    GASP_BG_COLOR = background
    pygame.init()
    display = pygame.display.set_mode((s_w, s_h))
    pygame.display.set_caption(screen_title)
    update_window()


@requires_window
def end_graphics():
    print("Goodbye!")
    pygame.quit()
    quit()


@requires_window
def remove_from_screen(obj: Shape):
    for i, sprite in enumerate(sprites):
        if sprite is obj:
            del sprites[i]
            return
    print("Tried to delete an object but it was not found!")


@requires_window
def move_to(obj: Shape, coord):
    obj.move_to(coord)
    update_window()

@requires_window
def move_by(obj: Shape, x, y):
    obj.move_by(x,y)
    update_window()

@requires_window
def update_window():
    display.fill(GASP_BG_COLOR)

    for spr in sprites:
        spr.draw()
    pygame.display.update()

@requires_window
def clear_screen():
    global sprites
    sprites = []
    update_window()

# === Misc Functions ===

def to_gasp_coord(coord):
    return (coord[0],screen_height-coord[1])

# Taken from: gitlab.com/gctaa/gasp/blob/master/gasp/api.py#L716
def random_between(num1, num2):
    if num1 == num2:
        return num1
    elif num1 > num2:
        return random.randint(num2, num1)
    else:
        return random.randint(num1, num2)

def set_speed(speed: int):
    global framerate
    framerate = speed

def update_when(event_type):
    """
    'key_pressed'
    'mouse_clicked'
    'next_tick'
    """
    if event_type == 'key_pressed':
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keystr = str(pygame.key.name(event.key))
                    key = keystr[1] if len(keystr) == 3 else keystr
                    return key

keys_down = {
        'left':0,
        'right':0
        }

def keys_pressed():
    keys = pygame.key.get_pressed()  #checking pressed keys
    out = []
    if keys[pygame.K_RIGHT]:
        out.append('right')
    if keys[pygame.K_LEFT]:
        out.append('left')
    if keys[pygame.K_UP]:
        out.append('up')
    if keys[pygame.K_DOWN]:
        out.append('down')
    if keys[pygame.K_w]:
        out.append('w')
    if keys[pygame.K_a]:
        out.append('a')
    if keys[pygame.K_d]:
        out.append('d')
    if keys[pygame.K_s]:
        out.append('s')

    pygame.event.pump()
    clock.tick(framerate)
    return out

def rotate_by(*args, **kwargs):
    pass
