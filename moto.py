import pygame


class Moto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.size = 70
        self.fast_gear = False
        self.speed_normal = 3
        self.speed_fast = 7

        self.vx = 0
        self.vy = 0

        # Ajuste da hitbox
        self.hitbox_largura = 20
        self.hitbox_altura = 20

        try:
            self.img_esquerda = pygame.transform.scale(
                pygame.image.load("moto_esquerda.png").convert_alpha(),
                (self.size, self.size)
            )

            self.img_direita = pygame.transform.scale(
                pygame.image.load("moto_direita.png").convert_alpha(),
                (self.size, self.size)
            )

            self.img_cima = pygame.transform.scale(
                pygame.image.load("moto_cima.png").convert_alpha(),
                (self.size, self.size)
            )

            self.img_baixo = pygame.transform.scale(
                pygame.image.load("moto_baixo.png").convert_alpha(),
                (self.size, self.size)
            )

            self.image = self.img_esquerda

        except FileNotFoundError:
            print("AVISO: Imagens da moto não encontradas.")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((100, 150, 255))

        # Rect visual da imagem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Hitbox real, centralizada na moto
        self.hitbox = pygame.Rect(0, 0, self.hitbox_largura, self.hitbox_altura)
        self.hitbox.center = self.rect.center

        self.font_label = pygame.font.SysFont("Arial", 14, bold=True)

    def toggle_gear(self):
        self.fast_gear = not self.fast_gear

    def atualizar_hitbox(self):
        self.hitbox.center = self.rect.center

    def handle_input(self, keys):
        speed = self.speed_fast if self.fast_gear else self.speed_normal

        self.vx = 0
        self.vy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -speed
            self.image = self.img_esquerda

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = speed
            self.image = self.img_direita

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -speed
            self.image = self.img_cima

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = speed
            self.image = self.img_baixo

    def update(self, screen_width, screen_height, obstaculos):
        old_rect_x = self.rect.x
        old_rect_y = self.rect.y

        # Movimento horizontal
        self.rect.x += self.vx
        self.atualizar_hitbox()

        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                self.rect.x = old_rect_x
                self.atualizar_hitbox()
                self.vx = 0
                break

        # Movimento vertical
        self.rect.y += self.vy
        self.atualizar_hitbox()

        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                self.rect.y = old_rect_y
                self.atualizar_hitbox()
                self.vy = 0
                break

        # Limites da tela
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))
        self.atualizar_hitbox()

    def draw(self, surface):
        # Contorno amarelo quando está em alta velocidade
        if self.fast_gear:
            pygame.draw.rect(
                surface,
                (255, 204, 0),
                (
                    self.hitbox.x - 2,
                    self.hitbox.y - 2,
                    self.hitbox.width + 4,
                    self.hitbox.height + 4
                ),
                2
            )

        # Desenha a imagem da moto
        surface.blit(self.image, self.rect)

        # Hitbox real da moto em azul/ciano
        pygame.draw.rect(surface, (0, 255, 255), self.hitbox, 2)

        # Texto do jogador
        lbl_player = self.font_label.render("Você (Moto)", True, (255, 255, 255))
        surface.blit(lbl_player, (self.rect.x - 15, self.rect.y - 18))