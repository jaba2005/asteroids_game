"""

Нужно дописать.

 - статистику (готово)
 - меню (готово)
 - динамический фон (готово)

"""
import pygame as pg
from player import Player
from asteroids import Asteroid
from background import BgObjectAnimated, HpBar, Title
from menu import Button
from static import *
from settings import *


def set_coords_for_menu_btns(buttons):
    i = 0
    for btn in buttons:
        x = (DISPLAY_WIDTH - btn.x) // 2
        y = (DISPLAY_HEIGHT - btn.y * 3) // 4 * (i + 1) + btn.y * i
        btn.set_coords((x, y))
        i += 1


BACKGROUND = pg.image.load(BACKGROUND_SPACE)
ICON = pg.image.load(FAVICON)


pg.init()
pg.display.set_caption('Asteroids')
pg.display.set_icon(ICON)
pg.event.set_allowed([pg.QUIT])

running = True
pause = True
fullscreen = False
restart = True
endgame = False
endgame_title_added = False
statistics_frame = False

clock = pg.time.Clock()
display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

def init_all_classes():
    global player, all_sprites, hp_bar
    player = Player(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2, SPACE_SHIP_IMG)
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)

    hp_bar = HpBar(
        player=player,
        imgs=HP_BAR
    )
    all_sprites.add(hp_bar)

init_all_classes()

with open('statistics.txt', 'r') as file:
    asteroids_destroyed = int(file.readline())

all_sprites: pg.sprite.Group = pg.sprite.Group()

bg_objects: pg.sprite.Group = pg.sprite.Group()
bg_objects.add(
    BgObjectAnimated(200, 200, BG_TRASH_ANIMATION, 1000)
)
bg_objects.add(
    BgObjectAnimated(700, 300, BG_TRASH_ANIMATION2, 2000, scale_by=4)
)
bg_objects.add(
    BgObjectAnimated(100, 500, BG_TRASH_ANIMATION3, 1000, scale_by=2)
)

def play_btn_func():
    global pause, restart
    if restart:
        init_all_classes()
    pause = False

def exit_btn_func():
    global running
    running = False
    with open('statistics.txt', 'w') as file:
        file.write(str(asteroids_destroyed + player.score))

def statistics_btn_func():
    global asteroids_destroyed, statistics_frame, statistics_title, all_sprites, pause
    if not statistics_frame:
        ans = asteroids_destroyed + player.score
        statistics_title = Title(
            f'всего астероидов уничтожено: {ans}', FONT, size=30
        )
        bg_objects.add(statistics_title)
        statistics_frame = True
        pause = False


play_button = Button(
    FONT, 'играть', (255, 255, 255), 100, play_btn_func
)
statistics_button = Button(
    FONT, 'статистика', (255, 255, 255), 100, statistics_btn_func
)
exit_button = Button(
    FONT, 'выход', (255, 255, 255), 100, exit_btn_func
)
menu_buttons = (play_button, statistics_button, exit_button)

set_coords_for_menu_btns(menu_buttons)

time = pg.time.get_ticks()

if __name__ == '__main__':
    while running:
        keys = pg.key.get_pressed()
        events = pg.event.get()

        if pause:
            display.blit(BACKGROUND, (0, 0))

            bg_objects.update()
            bg_objects.draw(display)

            set_coords_for_menu_btns(menu_buttons)
            for btn in menu_buttons:
                btn.render(display)
                btn.animation()
                btn.action()

        elif endgame:
            if not endgame_title_added:
                title = Title('игра окончена', FONT, size=110)
                all_sprites.add(
                    title
                )
                endgame_title_added = True
            display.blit(BACKGROUND, (0, 0))
            bg_objects.update()
            bg_objects.draw(display)
            all_sprites.update()
            all_sprites.draw(display)
            if keys[pg.K_SPACE]:
                pause = True
                restart = True
                endgame = False
                endgame_title_added = False
                title.kill()

        elif statistics_frame:
            display.blit(BACKGROUND, (0, 0))
            bg_objects.update()
            bg_objects.draw(display)
            if keys[pg.K_SPACE]:
                statistics_frame = False
                pause = True
                statistics_title.kill()

        else:
            if keys[pg.K_ESCAPE]:
                pause = True
                restart = False

            display.blit(BACKGROUND, (0, 0))

            bg_objects.update()
            bg_objects.draw(display)

            curr_time = pg.time.get_ticks()
            if curr_time - time > 1000:
                time = curr_time
                all_sprites.add(Asteroid())

            all_sprites.update(keys=keys)
            all_sprites.draw(display)

            if player.hp == 0:
                endgame = True
                asteroids_destroyed += player.score

        for event in events:
            if event.type == pg.QUIT:
                running = False

        pg.display.flip()
        clock.tick(FPS)
