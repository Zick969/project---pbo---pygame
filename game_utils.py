import pygame
from labirin import labirin
from settings import TILE_SIZE


def get_tile_rect(symbol):
    for row_index, row in enumerate(labirin):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                return pygame.Rect(
                    col_index * TILE_SIZE,
                    row_index * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
    return None


def get_all_tile_rect(symbol):
    rects = []

    for row_index, row in enumerate(labirin):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                rects.append(
                    pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                )

    return rects


def spawn_player(player):
    for row_index, row in enumerate(labirin):
        for col_index, cell in enumerate(row):
            if cell == "P":
                player.x = col_index * TILE_SIZE
                player.y = row_index * TILE_SIZE

def draw_level_menu(screen, font, easy_btn, medium_btn, hard_btn):
    screen.fill((0, 0, 0))

    title = font.render("PILIH LEVEL", True, (255, 255, 255))
    screen.blit(title, (520, 120))

    pygame.draw.rect(screen, (0, 200, 0), easy_btn)
    pygame.draw.rect(screen, (200, 200, 0), medium_btn)
    pygame.draw.rect(screen, (200, 0, 0), hard_btn)

    screen.blit(font.render("EASY", True, (255, 255, 255)), (590, 245))
    screen.blit(font.render("MEDIUM", True, (255, 255, 255)), (550, 365))
    screen.blit(font.render("HARD", True, (255, 255, 255)), (590, 485))