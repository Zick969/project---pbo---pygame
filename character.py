import pygame
import random
from settings import PLAYER_SPEED_NORMAL

class Character:
    def __init__(self, x, y, image_path):
        self.direction = random.choice(["up", "down", "left", "right"])
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = PLAYER_SPEED_NORMAL

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height)
        )

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def limit_move(self):
        if self.x < 30:
            self.x = 30
        if self.x + self.width > 1250:
            self.x = 1250 - self.width
        if self.y < 30:
            self.y = 30
        if self.y + self.height > 710:
            self.y = 710 - self.height


class Player(Character):
    def move(self, keys, cek_tembok):
        old_x = self.x
        old_y = self.y

        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        if cek_tembok(self.get_rect()):
            self.x = old_x
            self.y = old_y


class Monster(Character):
    def move(self, cek_tembok):
        old_x = self.x
        old_y = self.y

        if random.randint(1, 50) == 5:
            self.direction = random.choice(
                ["up", "down", "left", "right"]
            )

        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        if cek_tembok(self.get_rect()):
            self.x = old_x
            self.y = old_y


class Robot(Monster):
    def move(self, cek_tembok):
        old_x = self.x
        old_y = self.y

        if random.randint(1, 50) == 5:
            self.direction = random.choice(
                ["up", "down", "left", "right"]
            )

        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        if cek_tembok(self.get_rect()):
            self.x = old_x
            self.y = old_y