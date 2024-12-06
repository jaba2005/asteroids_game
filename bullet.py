"""

Файл содержит.

 - класс, реализующий функционал пули

"""
import pygame as pg
import numpy as np
from static import BULLET, EXPLOSION
from settings import DISPLAY_HEIGHT, DISPLAY_WIDTH
from asteroids import Asteroid
from background import BgObjectAnimated


class Bullet(pg.sprite.Sprite):
    """Непосредственно сам класс."""

    def __init__(self, x, y, direction: np.ndarray, player):
        """Инициализация пули происходит в момент выстрела."""
        super().__init__()
        self.player = player
        self.direction = direction * 3
        self.img_src = pg.image.load(BULLET)
        default_direction = np.array([1, 0])
        self.rect = self.img_src.get_rect(center=(x, y))
        normalized_dir = direction / np.linalg.norm(direction)
        angle = np.arccos(
            np.clip(
                np.dot(default_direction, normalized_dir),
                -1.0,
                1.0
            )
        )
        if direction[0] < 0 and direction[1] > 0:
            angle = -angle
        elif direction[0] > 0 and direction[1] > 0:
            angle = -angle
        self.image = pg.transform.rotate(
            self.img_src,
            angle / np.pi * 180
        )

    def update(self, **kwargs):
        """Полет пули."""
        group = self.groups()[0]  # обращение к группе со всеми спрайтами
        for sprite in group.sprites():
            if self.rect.colliderect(sprite.rect) and type(sprite) is Asteroid:
                group.add(
                    BgObjectAnimated(
                        *self.rect.center,
                        EXPLOSION,
                        frame_duration=100,
                        scale_by=4,
                        killed=True
                    )
                )
                self.player.score += 1
                self.kill()
                sprite.kill()

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        if (
            self.rect.x < -5 or self.rect.x > DISPLAY_WIDTH + 5
            or
            self.rect.y < -5 or self.rect.y > DISPLAY_HEIGHT + 5
        ):
            self.kill()
