import pygame as pg
import sys
from classes.input import Input
import config.constant as c
from classes.scene_manager import SceneManager

# init pygame
pg.init()
DISPLAY_SURFACE = pg.display.set_mode(c.DISPLAY_SIZE)
CLOCK = pg.time.Clock()
NATIVE_SURFACE = pg.Surface(c.NATIVE_RESOLUTION)

# set main scene
SceneManager.change_scene_to_file("./scenes/test_scene.py", "TestScene")

# main game loop
while True:
    # fps limit
    delta = CLOCK.tick(c.FPS) / 1000.0

    # handle window x btn click
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # feed input singleton
    Input.update(pg.key.get_pressed())

    # clear NATIVE_SURFACE
    NATIVE_SURFACE.fill("blue4")

    # update current_scene
    SceneManager.current_scene.update(delta)

    # render current_scene
    SceneManager.current_scene.draw(NATIVE_SURFACE)

    # NATIVE_SURFACE -> DISPLAY_SURFACE
    SCALED_NATIVE_SURFACE = pg.transform.scale(
        NATIVE_SURFACE, c.DISPLAY_SIZE)
    DISPLAY_SURFACE.blit(SCALED_NATIVE_SURFACE, (0, 0))

    # update DISPLAY_SURFACE
    pg.display.update()
