"""
Файл с меню содержит.

 - класс кнопки
"""
import pygame as pg


class Button:
    """Класс реализующий кнопку."""

    def __init__(self, font_path, text: str, color, size, func) -> None:
        """Метод для инициализации кнопки."""
        font = pg.font.Font(font_path, size=size)
        act_font = pg.font.Font(font_path, size=size + 10)

        self.curr = font.render(text, False, color)
        self.act = act_font.render(text, False, (255, 0, 0))
        self.non_act = font.render(text, False, color)

        self.x, self.y = self.curr.get_size()
        self.coords: list = [0, 0]

        self.func = func

    def set_coords(self, coords):
        """Метод, чтобы устанавливать координаты для кнопки."""
        self.coords = coords

    def render(self, screen: pg.Surface):
        """Метод для отрисовки кнопки на экране."""
        screen.blit(self.curr, self.coords)

    def animation(self):
        """Метод анимирующий кнопку при наведении мыши."""
        mouse_pos = pg.mouse.get_pos()
        if (
            self.coords[0] < mouse_pos[0] < (self.x + self.coords[0])
            and
            self.coords[1] < mouse_pos[1] < (self.y + self.coords[1])
        ):
            self.curr = self.act
        else:
            self.curr = self.non_act
        self.x, self.y = self.curr.get_size()

    def action(self, *args, **kwargs):
        """Метод привязывающий выполнение функции к нажатию на кнопку."""
        if self.curr == self.act and pg.mouse.get_pressed(num_buttons=3)[0]:
            self.func(*args, **kwargs)
