from typing import List, Tuple, Iterator

from math import sin, cos
from math import pi as PI

import pygame
import pygame.display as display
import pygame.event as events
import pygame.draw as draw
import pygame.gfxdraw as gfxdraw
import pygame.transform as transform
from pygame.time import Clock

from utils import *
from color import *

class FourierAnimation:
    def __init__(self, logo, size=(800, 800), frame=30, title="Fourier Drawing", teleport=True):
        self.size = size
        self.frame = frame
        self.logo = logo
        self.title = title
        self.zoom = False
        self.teleport = teleport

        self.MIDDLE = Vec2d(*map(lambda x:x/2, self.size))
        self.scale = min(size)/2 - 100
        
        self.trail_length = len(self.logo)
        self.origin_path = [(self.MIDDLE + Vec2d(*p) * self.scale).float_tuple for p in self.logo]
        self.waves =sorted([
                Wave(k, X_k) for k, X_k in\
                enumerate(dft([complex(*p) for p in self.logo]))
            ],
            key=lambda w: w.amp,
            reverse=True
        )
        self.t = 0
        self.dt = PI*2/len(self.waves)

        self.trail = []

    def draw(self, screen):
        screen.fill(BLACK)
        
        draw.aalines(screen, DARKER_GREY, True, self.origin_path)

        origin = self.MIDDLE
        for wave in self.waves:
            radius = mapf(wave.amp, b=(0, self.scale))
            gfxdraw.aacircle(screen, int(origin.x), int(origin.y), int(max(2, radius)), DARK_GREY)

            angle = self.t * wave.freq + wave.phase
            end_point = origin + (radius * cos(angle), radius * sin(angle))
            draw.aaline(screen, WHITE, origin.int_tuple, end_point.int_tuple)

            origin = end_point

        self.trail.append(origin)
        if len(self.trail) > 1:
            if self.teleport:
                prev = self.trail[0]
                for i in self.trail[1:]:
                    if prev.dist(i) < 10:
                        draw.aaline(screen, NICE_RED, prev.float_tuple, i.float_tuple)
                    prev = i
            else:
                draw.aalines(screen, NICE_RED, trail)
            self.t += self.dt

        if self.zoom:
            scaled = transform.scale2x(screen)
            screen.fill(BLACK)
            screen.blit(scaled, (WIDTH / 2 - origin.x * 2, HEIGHT / 2 - origin.y * 2))

    def start(self):
        pygame.init()
        
        screen = display.set_mode(self.size)
        display.set_caption(self.title)
        clock = Clock()

        running = True
        while running:
            
            clock.tick(self.frame)
            
            for event in events.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw(screen)
            display.flip()

        pygame.quit()
