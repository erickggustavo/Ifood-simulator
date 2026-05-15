import pygame
import math


class Pedestre(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed=1.0):
        super().__init__()

        self.speed = speed

        # Mostrar hitbox do pedestre
        self.mostrar_hitbox = True

        # Cor da hitbox do pedestre: verde
        self.cor_hitbox = (0, 255, 0)

        # Tamanho da hitbox do pedestre
        self.hitbox_largura = 15
        self.hitbox_altura = 15

        self.start_pos = (start_x, start_y)
        self.end_pos = (end_x, end_y)
        self.target_x = end_x
        self.target_y = end_y

        self.x = float(start_x)
        self.y = float(start_y)

        self.frames = {"down": [], "right": [], "left": [], "up": []}
        self.current_frame = 0.0
        self.animation_speed = 0.15
        self.current_direction = "down"

        self._load_spritesheet()

        self.image = self.frames[self.current_direction][0]

        # Retângulo visual da imagem
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Hitbox real independente da imagem
        self.hitbox = pygame.Rect(0, 0, self.hitbox_largura, self.hitbox_altura)
        self.hitbox.center = self.rect.center

    def _load_spritesheet(self):
        try:
            sheet = pygame.image.load("pedestres.png").convert_alpha()

            frame_width = sheet.get_width() // 4
            frame_height = sheet.get_height() // 4

            directions = ["down", "right", "left", "up"]

            for row, direction in enumerate(directions):
                for col in range(4):
                    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

                    area = (
                        col * frame_width,
                        row * frame_height,
                        frame_width,
                        frame_height
                    )

                    frame.blit(sheet, (0, 0), area)
                    frame = pygame.transform.scale(frame, (32, 32))

                    self.frames[direction].append(frame)

        except FileNotFoundError:
            print("AVISO: Spritesheet do pedestre não encontrado. Usando quadrado amarelo.")

            fallback_img = pygame.Surface((32, 32))
            fallback_img.fill((255, 204, 0))

            for dir_key in self.frames.keys():
                self.frames[dir_key] = [fallback_img for _ in range(4)]

    def atualizar_hitbox(self):
        self.hitbox.center = self.rect.center

    def update(self, obstaculos):
        old_x = self.x
        old_y = self.y

        dist_x = self.target_x - self.x
        dist_y = self.target_y - self.y
        distancia_total = math.hypot(dist_x, dist_y)

        if distancia_total < 2.0:
            if self.target_x == self.end_pos[0] and self.target_y == self.end_pos[1]:
                self.target_x, self.target_y = self.start_pos
            else:
                self.target_x, self.target_y = self.end_pos
        else:
            dir_x = dist_x / distancia_total
            dir_y = dist_y / distancia_total

            self.x += dir_x * self.speed
            self.y += dir_y * self.speed

            if abs(dir_x) > abs(dir_y):
                self.current_direction = "right" if dir_x > 0 else "left"
            else:
                self.current_direction = "down" if dir_y > 0 else "up"

        # Atualiza posição visual
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # Atualiza hitbox
        self.atualizar_hitbox()

        # Colisão com obstáculos usando a hitbox real
        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                self.x = old_x
                self.y = old_y

                self.rect.centerx = int(self.x)
                self.rect.centery = int(self.y)

                self.atualizar_hitbox()

                if self.target_x == self.end_pos[0] and self.target_y == self.end_pos[1]:
                    self.target_x, self.target_y = self.start_pos
                else:
                    self.target_x, self.target_y = self.end_pos

                break

        # Animação
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames[self.current_direction]):
            self.current_frame = 0.0

        self.image = self.frames[self.current_direction][int(self.current_frame)]

    def draw(self, surface):
        # Desenha pedestre
        surface.blit(self.image, self.rect)

        # Desenha hitbox verde
        if self.mostrar_hitbox:
            pygame.draw.rect(surface, self.cor_hitbox, self.hitbox, 2)