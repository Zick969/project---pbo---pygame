import pygame
from settings import TILE_SIZE

labirin = [
    "##########################",
    "#K   #        #       #E #",
    "#   B#        #       #  #",
    "###     ####  #   #  ##  #",
    "#        ##       #L     #",
    "#  #      #              #",
    "#  ####       DD      ####",
    "#        T   ####  #     #",
    "#L                 #     #",
    "#  ###   ##             ##",
    "#  #     #      #   B    #",
    "####            ##  ##   #",
    "#      #    #            #",
    "#P    D#    #      DD    #",
    "##########################"
]


def cek_tembok(rect):
    for row_index, row in enumerate(labirin):
        for col_index, cell in enumerate(row):
            if cell == "#":
                wall_rect = pygame.Rect(
                    col_index * TILE_SIZE,
                    row_index * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                if rect.colliderect(wall_rect):
                    return True
    return False