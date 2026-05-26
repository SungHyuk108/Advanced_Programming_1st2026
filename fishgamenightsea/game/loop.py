"""메인 게임 루프 및 입력 처리."""
import sys

import pygame

from game import title_ui
from game.config import (
    FPS,
    STATE_ACHIEVEMENT,
    STATE_COLLECTION,
    STATE_IDLE,
    STATE_INVENTORY,
    STATE_SHOP_CATEGORY,
    STATE_SHOP_MAIN,
    STATE_TITLE,
    STATE_HELP,
)
from game.display import clock, screen
from game.fishing_game import FishingGame
from game.title_ui import button_rects, menu_buttons


def run():
    game = FishingGame()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        action_pressed = mouse_pressed or keys[pygame.K_SPACE]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE
                    elif game.state == STATE_SHOP_CATEGORY:
                        game.state = STATE_SHOP_MAIN
                    elif game.state in [
                        STATE_SHOP_MAIN,
                        STATE_COLLECTION,
                        STATE_ACHIEVEMENT,
                        STATE_HELP,
                    ]:
                        game.state = STATE_TITLE
                    elif game.state != STATE_TITLE:
                        game.state = STATE_TITLE

                elif event.key == pygame.K_SPACE:
                    if game.state not in [
                        STATE_TITLE,
                        STATE_SHOP_MAIN,
                        STATE_SHOP_CATEGORY,
                        STATE_COLLECTION,
                        STATE_ACHIEVEMENT,
                        STATE_HELP,
                    ]:
                        game.handle_action()

                elif event.key == pygame.K_i:
                    if game.state == STATE_IDLE:
                        game.state = STATE_INVENTORY
                    elif game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE

                elif event.key == pygame.K_p:
                    if game.state == STATE_IDLE:
                        game.state = STATE_SHOP_MAIN
                    elif game.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                        game.state = STATE_IDLE

                elif event.key == pygame.K_s:
                    if game.state == STATE_INVENTORY:
                        game.sell_all_fish()
                elif event.key == pygame.K_UP:
                    if game.state == STATE_COLLECTION:
                        game.codex_scroll = max(0, game.codex_scroll - 40)

                elif event.key == pygame.K_DOWN:
                    if game.state == STATE_COLLECTION:
                        game.codex_scroll += 40
                elif event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                ]:
                    if game.state == STATE_SHOP_CATEGORY:
                        game.buy_item(game.shop_category, event.key - pygame.K_1)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.state == STATE_TITLE and title_ui.show_menu:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            game.state = menu_buttons[i]["scene"]
                            break
                    if title_ui.help_button_rect.collidepoint(event.pos):
                        game.state = STATE_HELP

                elif game.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                    game.handle_shop_click(event.pos)
                elif game.state not in [
                    STATE_COLLECTION,
                    STATE_ACHIEVEMENT,
                    STATE_INVENTORY,
                    STATE_HELP,
                ]:
                    game.handle_action()

        game.update(dt, action_pressed)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
