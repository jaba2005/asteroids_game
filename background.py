"""
Файл для фоновых объектов содержит.

 - Класс для реализации анимации фоновых объектов
 - Класс для отображения хп бара
 - Класс для отображения статичной надписи
"""
import pygame as pg
from settings import DISPLAY_HEIGHT, DISPLAY_WIDTH


class BgObjectAnimated(pg.sprite.Sprite):
    """
    Класс, реализующий фоновый объект.

    Используется для анимированных объектов.
    """

    def __init__(
            self,
            x, y,
            animation_files: list[str],
            frame_duration: int = 500,
            scale_by: int = 1,
            killed=False
                ):
        """Инициализация фонового объекта."""
        super().__init__()
        self.frames = [pg.image.load(img) for img in animation_files]
        if scale_by != 1:
            self.frames = [
                pg.transform.scale_by(img, scale_by) for img in self.frames
            ]
        self.indx = 0
        self.image = self.frames[self.indx]
        self.duration = frame_duration
        self.last_time = pg.time.get_ticks()
        self.rect = self.image.get_rect(center=(x, y,))
        self.killed = killed

    def update(self, **kwargs):
        """Метод реализующий смену кадров."""
        curr_time = pg.time.get_ticks()
        if curr_time - self.last_time > self.duration:
            self.indx += 1
            if self.indx == len(self.frames):
                if self.killed:
                    self.kill()
                self.indx = 0
            self.last_time = curr_time
            self.image = self.frames[self.indx]


class HpBar(pg.sprite.Sprite):
    """Класс, реализующий отображение количества ОЗ."""

    def __init__(self, player, imgs):
        """Инициализация объекта с необходимыми параметрами."""
        super().__init__()
        self.player = player
        self.player_hp = self.player.hp
        self.imgs = {5 - i: pg.image.load(imgs[i]) for i in range(len(imgs))}
        self.image = self.imgs[self.player_hp]
        self.rect = self.image.get_rect()

    def update(self, **kwargs):
        """Метод, обеспечивающий смену изображения при изменении ОЗ."""
        new_hp = self.player.hp
        if new_hp != self.player_hp:
            self.image = self.imgs[new_hp]
            self.player_hp = new_hp


class Title(pg.sprite.Sprite):
    def __init__(self, text, font, size):
        super().__init__()
        self.text = text
        self.font = pg.font.Font(font, size=size)
        self.image = self.font.render(self.text, False, (255, 255, 255))
        self.rect = self.image.get_rect(
            center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2,)
        )
