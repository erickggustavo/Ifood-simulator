import pygame
import math

class Pedestre(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed=1.0):
        super().__init__()
        
        self.speed = speed
        
        # Variáveis de Movimento (Vai e volta entre os pontos A e B)
        self.start_pos = (start_x, start_y)
        self.end_pos = (end_x, end_y)
        self.target_x = end_x
        self.target_y = end_y
        
        # Posição atual (usamos float para movimento mais suave)
        self.x = float(start_x)
        self.y = float(start_y)
        
        # Variáveis de Animação
        self.frames = {'down': [], 'right': [], 'left': [], 'up': []}
        self.current_frame = 0.0
        self.animation_speed = 0.15 
        self.current_direction = 'down'
        
        self._load_spritesheet()
        
        # Define a imagem inicial e o retângulo de colisão
        self.image = self.frames[self.current_direction][0]
        self.rect = self.image.get_rect()
        
        # --- A CORREÇÃO ESTÁ AQUI: Diminuindo a hitbox em 10 pixels ---
        self.rect = self.rect.inflate(-10, -10)
        # --------------------------------------------------------------
        
        self.rect.center = (self.x, self.y)

    def _load_spritesheet(self):
        """Carrega e recorta o spritesheet em quadros individuais."""
        try:
            sheet = pygame.image.load('pedestres.png').convert_alpha()
            frame_width = sheet.get_width() // 4
            frame_height = sheet.get_height() // 4
            directions = ['down', 'right', 'left', 'up']
            
            for row, direction in enumerate(directions):
                for col in range(4):
                    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    area = (col * frame_width, row * frame_height, frame_width, frame_height)
                    frame.blit(sheet, (0, 0), area)
                    frame = pygame.transform.scale(frame, (32, 32))
                    self.frames[direction].append(frame)
                    
        except FileNotFoundError:
            print("AVISO: Spritesheet do pedestre não encontrado. Usando quadrado amarelo.")
            fallback_img = pygame.Surface((32, 32))
            fallback_img.fill((255, 204, 0)) # Amarelo
            for dir_key in self.frames.keys():
                self.frames[dir_key] = [fallback_img for _ in range(4)]

    def update(self, obstaculos):
        """Atualiza a posição e a animação do pedestre com colisão."""
        # Salva a posição antes de mover (para caso ele bata na parede)
        old_x = self.x
        old_y = self.y
        
        # 1. Lógica de Movimento
        dist_x = self.target_x - self.x
        dist_y = self.target_y - self.y
        distancia_total = math.hypot(dist_x, dist_y)
        
        if distancia_total < 2.0:
            # Chegou no destino, inverte o caminho
            if self.target_x == self.end_pos[0] and self.target_y == self.end_pos[1]:
                self.target_x, self.target_y = self.start_pos
            else:
                self.target_x, self.target_y = self.end_pos
        else:
            # Move em direção ao alvo
            dir_x = dist_x / distancia_total
            dir_y = dist_y / distancia_total
            self.x += dir_x * self.speed
            self.y += dir_y * self.speed
            
            # Define a direção da animação
            if abs(dir_x) > abs(dir_y):
                self.current_direction = 'right' if dir_x > 0 else 'left'
            else:
                self.current_direction = 'down' if dir_y > 0 else 'up'

        # Atualiza a Hitbox do pedestre
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # --- NOVA LÓGICA DE COLISÃO CONTRA OS PRÉDIOS ---
        for obs in obstaculos:
            if self.rect.colliderect(obs):
                # Bateu! Desfaz o movimento voltando para a posição segura
                self.x = old_x
                self.y = old_y
                self.rect.centerx = int(self.x)
                self.rect.centery = int(self.y)
                
                # Força o pedestre a dar meia-volta imediatamente
                if self.target_x == self.end_pos[0] and self.target_y == self.end_pos[1]:
                    self.target_x, self.target_y = self.start_pos
                else:
                    self.target_x, self.target_y = self.end_pos
                break # Já bateu, não precisa checar os outros blocos

        # 2. Lógica de Animação
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames[self.current_direction]):
            self.current_frame = 0.0
            
        self.image = self.frames[self.current_direction][int(self.current_frame)]