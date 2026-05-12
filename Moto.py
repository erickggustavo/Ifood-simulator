import pygame

class Moto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.size = 20
        self.fast_gear = False
        self.speed_normal = 3
        self.speed_fast = 7
        
        # Velocidade atual
        self.vx = 0
        self.vy = 0

        # Carregamento do Sprite com Fallback (Segurança)
        try:
            self.image = pygame.image.load('moto.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except FileNotFoundError:
            # Se a imagem 'moto.png' ainda não existir na pasta, 
            # ele cria um quadrado azul para o jogo não "crashar".
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((50, 100, 255)) # Cor Azul

        # O Pygame usa o 'rect' para gerenciar posição e colisões dos Sprites
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Fonte para a label flutuante
        self.font_label = pygame.font.SysFont('Arial', 14, bold=True)

    def toggle_gear(self):
        """Alterna entre a marcha normal (segura) e a rápida (perigosa)."""
        self.fast_gear = not self.fast_gear

    def handle_input(self, keys):
        """Lê as teclas e define a velocidade da moto baseada na marcha."""
        speed = self.speed_fast if self.fast_gear else self.speed_normal
        self.vx, self.vy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.vx = -speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx = speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.vy = -speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.vy = speed

    def update(self, screen_width, screen_height, obstaculos):
        old_x = self.rect.x
        old_y = self.rect.y

        # Move X
        self.rect.x += self.vx
        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.rect.x = old_x
                self.vx = 0 # Para a moto
                break

        # Move Y
        self.rect.y += self.vy
        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.rect.y = old_y
                self.vy = 0 # Para a moto
                break
        
        # Limites da tela
        self.rect.x = max(0, min(self.rect.x, screen_width - self.size))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.size))

    def draw(self, surface):
        """Desenha a moto e seus efeitos visuais na tela."""
        # Se estiver na marcha rápida, desenha o contorno amarelo de perigo
        if self.fast_gear:
            pygame.draw.rect(
                surface, 
                (255, 204, 0), # Amarelo
                (self.rect.x - 2, self.rect.y - 2, self.size + 4, self.size + 4), 
                2
            )
            
        # Desenha a imagem (ou o quadrado azul de fallback)
        surface.blit(self.image, self.rect)
        
        # Desenha o identificador visual "Você (Moto)"
        lbl_player = self.font_label.render("Você (Moto)", True, (255, 255, 255))
        surface.blit(lbl_player, (self.rect.x - 15, self.rect.y - 18))