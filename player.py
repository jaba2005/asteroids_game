"""

Файл содержит.

 - класс, реализующий функционал корабля

"""
import pygame as pg
import numpy as np
from bullet import Bullet
from settings import DISPLAY_HEIGHT, DISPLAY_WIDTH
from background import BgObjectAnimated
from asteroids import Asteroid
from static import EXPLOSION


EXPLOSION_IMGS = [pg.image.load(i) for i in EXPLOSION]

class Player(pg.sprite.Sprite):
    """Непосредственно сам класс."""

    def __init__(self, x, y, img_path):
        """Инициализация всех нужных параметров."""
        super().__init__()
        self.start = (x, y)
        self.score = 0
        self.image_src = pg.image.load(img_path) # желательно вынести это из класса
        self.image_src = pg.transform.rotozoom(self.image_src, 0, 0.5)
        self.image = self.image_src
        self.angle = 0
        self.rotation_angle_rad = 0.09
        self.rect = self.image.get_rect(center=(x, y,))
        self.direction = np.array([0, -4])
        self.attack_speed = 300  # Интервал выстрелов в миллисекундах
        self.hp = 5
        self.save_time = 3000
        self.respawn_time = pg.time.get_ticks()
        self.last_shot_time = self.respawn_time

    def rotate(self, angle):
        """
        Метод для изменения направления.

        Нужен потому, что направление хранится в отельной переменной

        """
        rotatin_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        self.direction = self.direction @ rotatin_matrix

    @property
    def rotaion_angle_grad(self):
        """Преобразует радианы в градусы."""
        return self.rotation_angle_rad / np.pi * 180

    def update(self, keys, **kwargs):
        """Обработчик действий."""
        curr_tick = pg.time.get_ticks()
        if keys[pg.K_UP]:
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]
        if keys[pg.K_LEFT]:
            self.angle += self.rotaion_angle_grad
            self.rotate(self.rotation_angle_rad)
        if keys[pg.K_RIGHT]:
            self.angle -= self.rotaion_angle_grad
            self.rotate(-self.rotation_angle_rad)
        if keys[pg.K_SPACE]:
            if curr_tick - self.last_shot_time > self.attack_speed:
                self.last_shot_time = curr_tick
                self.groups()[0].add(
                    Bullet(*self.rect.center, self.direction, self)
                )
        group = self.groups()[0]  # обращение к группе со всеми спрайтами

        if curr_tick - self.respawn_time >= self.save_time:
            for sprite in group.sprites():
                if self.rect.colliderect(sprite.rect) and type(sprite) is Asteroid:
                    group.add(
                        BgObjectAnimated(
                            *self.rect.center,
                            EXPLOSION_IMGS,
                            frame_duration=100,
                            scale_by=4,
                            killed=True
                        )
                    )
                    if self.hp == 1:
                        self.hp -= 1
                        self.kill()
                        break
                    self.rect = self.image.get_rect(center=self.start)
                    self.hp -= 1
                    self.respawn_time = curr_tick
                    break

        x = self.rect.center[0]
        dx = abs(self.rect.x - x)
        y = self.rect.center[1]
        dy = abs(self.rect.y - y)
        if x < -dx:
            self.rect.x = DISPLAY_WIDTH - dx
        if x > DISPLAY_WIDTH:
            self.rect.x = -dx
        if y < -dy:
            self.rect.y = DISPLAY_HEIGHT - dy
        if y > DISPLAY_HEIGHT:
            self.rect.y = -dy

        self.image = pg.transform.rotate(self.image_src, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
