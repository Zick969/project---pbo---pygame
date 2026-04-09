import pygame
import sys

from settings import * #* berarti memanggil 1 file
from character import Player, Monster, Robot
from labirin import cek_tembok, labirin
from game_utils import *

pygame.init() #game
pygame.mixer.init() #suara

pygame.mixer.music.load("asset/game_backsound.mp3")
pygame.mixer.music.set_volume(0.30)
pygame.mixer.music.play(-1) #-1 akan diulang terus

screen = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Game Escape from Maze Hunter")

font_menu = pygame.font.SysFont(None, 60)

#tombol mode
easy_btn = pygame.Rect(500, 220, 300, 80)
medium_btn = pygame.Rect(500, 340, 300, 80)
hard_btn = pygame.Rect(500, 460, 300, 80)

game_state = GAME_STATE_MENU_AWAL
selected_level = None

laser_timer = 0
bomb_timer = 0

clock = pygame.time.Clock() #mengatur FPS

player = Player(100, 200, "asset/player.png")
monster = Monster(600, 200, "asset/monster.png")
robot = Robot(850, 440, "asset/robot.png")

spawn_player(player)

kunci_img = pygame.transform.scale(
    pygame.image.load("asset/kunci.png").convert_alpha(),
    (TILE_SIZE, TILE_SIZE)
)

petir_img = pygame.transform.scale(
    pygame.image.load("asset/petir.png").convert_alpha(),
    (TILE_SIZE, TILE_SIZE)
)

love_img = pygame.transform.scale(
    pygame.image.load("asset/love.png").convert_alpha(),
    (35, 35)
)

duri_img = pygame.transform.scale(
    pygame.image.load("asset/duri.png").convert_alpha(),
    (70, 70)
)

bomb_img = pygame.transform.scale(
    pygame.image.load("asset/bomb.png").convert_alpha(),
    (30, 30)
)

laser_img = pygame.transform.scale(
    pygame.image.load("asset/laser.png").convert_alpha(),
    (30, 30)
)
pintu_img = pygame.transform.scale(
    pygame.image.load("asset/pintuExit.png").convert_alpha(),
    (90, 90)
)

wall_img = pygame.transform.scale(
    pygame.image.load("asset/dinding.png").convert_alpha(),
    (TILE_SIZE, TILE_SIZE)
)

menu_img = pygame.transform.scale(
    pygame.image.load("asset/menu_awal.jpeg").convert(),
    (LEBAR, TINGGI)
)

ledakan_img = pygame.transform.scale(
    pygame.image.load("asset/ledakan.png").convert_alpha(),
    (200, 200)
)

game_over_img = pygame.transform.scale(
    pygame.image.load("asset/game_over.png").convert(),
    (1000, 500)
)

win_img = pygame.transform.scale(
    pygame.image.load("asset/you_win.png").convert(),
    (1000, 500)
)

#mencari posisi objek di maze
kunci_rect = get_tile_rect("K")
petir_rect = get_tile_rect("T")
pintu_rect = get_tile_rect("E")
duri_rects = get_all_tile_rect("D")

kunci_ada = True
petir_ada = True

timer_pesanKunci = 0
timer_pesanPetir = 0
timer_pesanPintu = 0
timer_boostspeed = 0
damage_timer = 0

lives = LIVES
start_time = 0
elapsed_time = 0

def reset_game():
    global kunci_ada, petir_ada
    global timer_pesanKunci, timer_pesanPetir
    global timer_pesanPintu, timer_boostspeed
    global damage_timer
    global lives, start_time, elapsed_time
    global game_state
    global laser_timer, bomb_timer

    spawn_player(player)

    monster.x = 600
    monster.y = 200

    robot.x = 850
    robot.y = 440

    if selected_level == LEVEL_EASY:
        monster.speed = PLAYER_SPEED_NORMAL
        robot.speed = PLAYER_SPEED_NORMAL

    elif selected_level == LEVEL_MEDIUM:
        monster.speed = PLAYER_SPEED_MEDIUM
        robot.speed = PLAYER_SPEED_MEDIUM

    elif selected_level == LEVEL_HARD:
        monster.speed = PLAYER_SPEED_HARD
        robot.speed = PLAYER_SPEED_HARD

    kunci_ada = True
    petir_ada = True

    timer_pesanKunci = 0
    timer_pesanPetir = 0
    timer_pesanPintu = 0
    timer_boostspeed = 0
    damage_timer = 0
    laser_timer = 0
    bomb_timer = 0

    lives = LIVES
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    game_state = GAME_STATE_PLAY


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == GAME_STATE_MENU_AWAL:
                    game_state = GAME_STATE_MENU

            elif game_state == GAME_STATE_MENU:
                if easy_btn.collidepoint(mouse_pos):
                    selected_level = LEVEL_EASY
                    reset_game()

                elif medium_btn.collidepoint(mouse_pos):
                    selected_level = LEVEL_MEDIUM
                    reset_game()

                elif hard_btn.collidepoint(mouse_pos):
                    selected_level = LEVEL_HARD
                    reset_game()

        if event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_MENU_AWAL:
                if event.key == pygame.K_SPACE:
                    game_state = GAME_STATE_MENU

            elif game_state in ["GAME_OVER", "WIN"]:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    keys = pygame.key.get_pressed()

    if game_state == GAME_STATE_PLAY:
        player.move(keys, cek_tembok)
        monster.move(cek_tembok)
        robot.move(cek_tembok)

        elapsed_time = (
            pygame.time.get_ticks() - start_time
        ) // 1000

        if timer_boostspeed > 0:
            timer_boostspeed -= 1
        else:
            player.speed = PLAYER_SPEED_NORMAL

        if damage_timer > 0:
            damage_timer -= 1

         #cek collison
        if player.get_rect().colliderect(kunci_rect) and kunci_ada:
            kunci_ada = False
            timer_pesanKunci = 180

        if player.get_rect().colliderect(petir_rect) and petir_ada:
            petir_ada = False
            player.speed = PLAYER_SPEED_BOOST
            timer_boostspeed = 600
            timer_pesanPetir = 180

        for musuh in [monster, robot]:
            if (
                player.get_rect().colliderect(musuh.get_rect())
                and damage_timer == 0
            ):
                lives -= 1
                damage_timer = 120
                spawn_player(player)

        for duri in duri_rects:
            if (
                player.get_rect().colliderect(duri)
                and damage_timer == 0
            ):
                lives -= 1
                damage_timer = 120
                spawn_player(player)

        if selected_level in [LEVEL_MEDIUM, LEVEL_HARD]:
            laser_timer += 1

            laser_rect1 = pygame.Rect(83, 414, 400, 10) #kiri
            laser_rect2 = pygame.Rect(984, 215, 260, 10)

            laser_rects = [laser_rect1, laser_rect2]

            if laser_timer % 180 < 90:
                if (
                        any(
                            player.get_rect().colliderect(laser)
                            for laser in laser_rects
                        )
                        and damage_timer == 0
                ):

                    lives -= 1
                    damage_timer = 120
                    spawn_player(player)

        if selected_level == LEVEL_HARD:
            bomb_timer += 1

            if bomb_timer >= 300:
                ledakan_rect1 = pygame.Rect(120, 0, 200, 200) #kiri
                ledakan_rect2 = pygame.Rect(913, 415, 200, 200)

                ledakan_rects = [ledakan_rect1, ledakan_rect2]

                if (
                        any(
                            player.get_rect().colliderect(ledakan)
                            for ledakan in ledakan_rects
                        )
                        and damage_timer == 0
                ):

                    lives -= 1
                    damage_timer = 120
                    spawn_player(player)

            if bomb_timer >= 360:
                bomb_timer = 0

        if player.get_rect().colliderect(pintu_rect):
            if not kunci_ada:
                game_state = "WIN"
            else:
                timer_pesanPintu = 180

        if lives <= 0:
            game_state = "GAME_OVER"

    screen.fill(HITAM)

    if game_state == GAME_STATE_MENU_AWAL:
        screen.blit(menu_img, (0, 0))

    elif game_state == GAME_STATE_MENU:
        draw_level_menu(screen, font_menu, easy_btn, medium_btn, hard_btn)

    else:
        for row_index, row in enumerate(labirin):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == "#":
                    screen.blit(wall_img, (x, y))
                elif cell == "K" and kunci_ada:
                    screen.blit(kunci_img, (x, y))
                elif cell == "T" and petir_ada:
                    screen.blit(petir_img, (x, y))
                elif cell == "D":
                    screen.blit(duri_img, (x, y))
                elif cell == "L" and selected_level in [LEVEL_MEDIUM, LEVEL_HARD]:
                    screen.blit(laser_img, (x, y))
                elif cell == "B" and selected_level in [LEVEL_HARD]:
                    screen.blit(bomb_img, (x, y))
                elif cell == "E":
                    screen.blit(pintu_img, (x, y))

        if game_state == GAME_STATE_PLAY:
            if damage_timer == 0 or damage_timer % 20 < 5:
                player.draw(screen)

            monster.draw(screen)
            robot.draw(screen)

            if selected_level in [LEVEL_MEDIUM, LEVEL_HARD]:
                if laser_timer % 180 < 90:
                    pygame.draw.rect(screen, (255, 0, 0), (83, 414, 400, 10))
                    pygame.draw.rect(screen, (255, 0, 0), (984, 215, 260, 10))

            if selected_level == LEVEL_HARD:
                if bomb_timer >= 300:
                    screen.blit(ledakan_img, (913, 415)) #bawah
                    screen.blit(ledakan_img, (120, 0)) #atas

            font = pygame.font.SysFont(None, 40)

            timer_text = font.render(
                f"Time: {elapsed_time}s", True, PUTIH
            )
            screen.blit(timer_text, (1100, 10))

            for i in range(lives):
                screen.blit(love_img, (20 + i * 40, 7))

            if timer_pesanKunci > 0:
                text = font.render(
                    "Mendapatkan Kunci", True, PUTIH
                )
                screen.blit(text, (530, 50))
                timer_pesanKunci -= 1

            if timer_pesanPetir > 0:
                text = font.render(
                    "Player bergerak lebih cepat",
                    True,
                    PUTIH
                )
                screen.blit(text, (460, 50))
                timer_pesanPetir -= 1

            if timer_pesanPintu > 0:
                text = font.render(
                    "Ambil kunci terlebih dahulu",
                    True,
                    PUTIH
                )
                screen.blit(text, (400, 50))
                timer_pesanPintu -= 1

        elif game_state in ["GAME_OVER", "WIN"]:
            player.draw(screen)
            monster.draw(screen)
            robot.draw(screen)

            overlay = pygame.Surface((LEBAR, TINGGI))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            x = LEBAR // 2 - 500
            y = TINGGI // 2 - 250

            if game_state == "GAME_OVER":
                screen.blit(game_over_img, (x, y))
            else:
                screen.blit(win_img, (x, y))

    player.limit_move()
    monster.limit_move()
    robot.limit_move()

    pygame.display.update()

pygame.quit()
sys.exit()