import pygame as pg


class Camera:
    def __init__(self, position=pg.Vector2(0, 0)):
        self.position = position
