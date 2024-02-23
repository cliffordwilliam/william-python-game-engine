import pygame
import sys
from pygame.math import Vector2
from classes.input import Input

FPS = 60
DISPLAY_SIZE = (1280, 720)
NATIVE_RESOLUTION = (320, 180)

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode(DISPLAY_SIZE)
CLOCK = pygame.time.Clock()
# sprite -> NATIVE_SURFACE -> DISPLAY_SURFACE
NATIVE_SURFACE = pygame.Surface(NATIVE_RESOLUTION)


while True:
    # fps limiter -> returns delta
    delta = CLOCK.tick(FPS) / 1000.0
    # event source
    for event in pygame.event.get():
        # window x btn click? terminate self
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # feed input singleton
    Input.update(pygame.key.get_pressed())

    # input handling
    if Input.is_action_pressed(pygame.K_SPACE):
        print("Space key is pressed")

    # get axis
    direction = Input.get_axis(pygame.K_LEFT, pygame.K_RIGHT)
    # print(direction)

    if Input.is_action_just_pressed(pygame.K_LEFT):
        print("Move Left action is just pressed")

    if Input.is_action_just_released(pygame.K_LEFT):
        print("Move Left action is just released")

    # clear NATIVE_SURFACE
    NATIVE_SURFACE.fill("blue4")
    # update source
    # sprite -> NATIVE_SURFACE source
    # NATIVE_SURFACE -> DISPLAY_SURFACE
    SCALED_NATIVE_SURFACE = pygame.transform.scale(
        NATIVE_SURFACE, DISPLAY_SIZE)
    DISPLAY_SURFACE.blit(SCALED_NATIVE_SURFACE, (0, 0))
    # update DISPLAY_SURFACE
    pygame.display.update()
