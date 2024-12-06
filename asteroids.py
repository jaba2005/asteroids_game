"""

Файл содержит.

 - класс для астероидов

"""
import pygame as pg
import numpy as np
from static import ASTEROIDS
from settings import DISPLAY_HEIGHT, DISPLAY_WIDTH


# PROBS = [1 / (2 * (i + 1)) for i in range(len(ASTEROIDS))]
PROBS = [1/3, 1/3, 1/6, 1/6]


class Asteroid(pg.sprite.Sprite):
    """Класс астероида."""

    def __init__(self):
        """
        Инициализация должна обеспечивать.

         - появление астероида со случайными параметрами (готово)

        """
        super().__init__()
        side = np.random.randint(0, 4)
        if side == 0:  # сверху вниз
            x = np.random.randint(0, DISPLAY_WIDTH)
            y = -80
            dx = (DISPLAY_WIDTH // 2 - x)
            if dx == 0:
                dx = 1
            dx //= abs(dx)
            self.direction = np.array(
                [dx * np.random.randint(1, 5), np.random.randint(1, 5)]
            )
        elif side == 1:  # справа налево
            x = DISPLAY_WIDTH + 10
            y = np.random.randint(0, DISPLAY_HEIGHT)
            dy = (DISPLAY_HEIGHT // 2 - x)
            if dy == 0:
                dy = 1
            dy //= abs(dy)
            self.direction = np.array(
                [-np.random.randint(1, 5), dy * np.random.randint(1, 5)]
            )
        elif side == 2:  # снизу вверх
            x = np.random.randint(0, DISPLAY_WIDTH)
            y = DISPLAY_HEIGHT + 10
            dx = (DISPLAY_WIDTH // 2 - x)
            if dx == 0:
                dx = 1
            dx //= abs(dx)
            self.direction = np.array(
                [dx * np.random.randint(1, 5), -np.random.randint(1, 5)]
            )
        else:  # слева направо
            x = -80
            y = np.random.randint(0, DISPLAY_HEIGHT)
            dy = (DISPLAY_HEIGHT // 2 - x)
            if dy == 0:
                dy = 1
            dy //= abs(dy)
            self.direction = np.array(
                [np.random.randint(1, 5), dy * np.random.randint(1, 5)]
            )
        self.rotation_per_tick = np.random.randint(-2, 2)
        self.rotation_angle = 0
        img = np.random.choice(ASTEROIDS, p=PROBS)
        self.img_src = pg.image.load(img)
        self.image = self.img_src
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, **kwargs):
        """
        Метод должен обеспечивать.

         - движение астероида по заданной траектории (готово)
         - удаление астероида при столкновении с ракетой (готово)
         - удаление астероида при выходе за край экрана (готово)

        """
        if (
            self.rect.x < -200 or self.rect.x > DISPLAY_WIDTH + 200
            or
            self.rect.y < -200 or self.rect.y > DISPLAY_HEIGHT + 200
        ):
            self.kill()
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        self.rotation_angle += self.rotation_per_tick
        self.image = pg.transform.rotate(self.img_src, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
