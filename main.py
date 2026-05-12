import pygame
import sys
import random

from Cidade import Cidade
from Moto import Moto
from Pedestre import Pedestre
from interface import Interface

WIDTH, HEIGHT = 1000, 650 
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Entrega Consciente: O Dilema do Trânsito")
        self.clock = pygame.time.Clock()
        
        self.cidade = Cidade(WIDTH, HEIGHT)
        self.interface = Interface(WIDTH, HEIGHT)
        
        # Chama o reset_game para iniciar as variáveis do jogo
        self.reset_game()

    def gerar_ponto_seguro(self, cidade):
        """Gera coordenadas (x, y) que NÃO colidem com os prédios da cidade."""
        while True:
            # Pega um ponto aleatório na tela
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
        
            # Cria um retângulo falso para testar colisão (tamanho do pedestre)
            rect_teste = pygame.Rect(x, y, 32, 32)
        
            colidiu = False
            for obs in cidade.obstaculos:
                if rect_teste.colliderect(obs):
                    colidiu = True
                    break
                
            # Se não bateu em nada, o ponto é válido e sai do While!
            if not colidiu:
                return x, y

    def reset_game(self):
        self.state = "PLAYING"
        self.time_left = 60.0 # Tempo ajustado para as 3 missões
        self.infractions = 0
        self.message_timer = 180 # Mantém a mensagem inicial mais tempo na tela
        self.current_message = "Vá até a caixa na Zona A para coletar!"
        self.end_message = ""
        
        # --- VARIÁVEIS DE MISSÃO ---
        self.encomenda_coletada = False
        self.entrega_b_feita = False
        self.entrega_c_feita = False
        
        # Ponto de nascimento da moto
        self.moto = Moto(100, 300)        
        self.pedestres = pygame.sprite.Group()
        
        # --- GERANDO MÚLTIPLOS PEDESTRES ALEATÓRIOS ---
        quantidade_pedestres = 12  # Aumente ou diminua a dificuldade aqui
        
        for _ in range(quantidade_pedestres):
            # Gera um ponto inicial e um de destino sem bater em prédios
            start_x, start_y = self.gerar_ponto_seguro(self.cidade)
            end_x, end_y = self.gerar_ponto_seguro(self.cidade)
            
            # Sorteia uma velocidade para o pedestre
            velocidade = random.uniform(0.5, 1.5)
            
            # Cria o pedestre e adiciona ao grupo
            p = Pedestre(start_x, start_y, end_x, end_y, velocidade)
            self.pedestres.add(p)

    def trigger_infraction(self, msg, time_penalty, is_fatal=False):
        if self.state != "PLAYING": return
        if is_fatal:
            self.state = "GAME_OVER"
            self.end_message = f"ACIDENTE: {msg}"
            return
        
        self.infractions += 1
        self.time_left -= time_penalty
        self.current_message = f"{msg} (-{time_penalty}s)"
        self.message_timer = 90

    def process_input(self):
        """Lida com os eventos do teclado e cliques do mouse."""
        for event in pygame.event.get():
            # 1. Fecha o jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 2. Comandos de Teclado (Espaço e Reset)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == "PLAYING":
                    self.moto.toggle_gear()
                if event.key == pygame.K_r and self.state != "PLAYING":
                    self.reset_game()

        # 3. Movimentação Contínua (WASD / Setas) - Fica fora do 'for'!
        keys = pygame.key.get_pressed()
        if self.state == "PLAYING":
            self.moto.handle_input(keys)
            

    def update(self):
        if self.state != "PLAYING":
            return

        # 1. Atualiza o tempo
        dt = self.clock.tick(FPS) / 1000.0
        self.time_left -= dt
        
        if self.time_left <= 0:
            self.state = "GAME_OVER"
            self.end_message = "O TEMPO ESGOTOU!"
            return

        # 2. Atualiza posições
        self.moto.update(WIDTH, HEIGHT, self.cidade.obstaculos)
        self.pedestres.update(self.cidade.obstaculos)  

        # 3. Timer de mensagens
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.current_message = ""

        # 4. PROGRESSÃO DAS MISSÕES E VITÓRIA
        rect_moto = self.moto.rect
        
        # FASE 1: Coletar a encomenda
        if not self.encomenda_coletada:
            if rect_moto.colliderect(self.cidade.ponto_coleta_rect):
                self.encomenda_coletada = True
                self.current_message = "Coletado! Entregue nas Zonas B e C!"
                self.message_timer = 180 # Mensagem fica 3 segundos na tela
                
        # FASE 2: Fazer as entregas
        else:
            # Checa se encostou no Ponto B
            if not self.entrega_b_feita and rect_moto.colliderect(self.cidade.ponto_b_rect):
                self.entrega_b_feita = True
                self.current_message = "Entrega B Concluída!"
                self.message_timer = 120
                
            # Checa se encostou no Ponto C
            if not self.entrega_c_feita and rect_moto.colliderect(self.cidade.ponto_c_rect):
                self.entrega_c_feita = True
                self.current_message = "Entrega C Concluída!"
                self.message_timer = 120

            # Checa a Vitória (Tem que ter feito as duas!)
            if self.entrega_b_feita and self.entrega_c_feita:
                self.state = "VICTORY"
                self.end_message = "Sucesso! Você fez todas as entregas!"

        # 5. COLISÃO COM PEDESTRES
        if pygame.sprite.spritecollideany(self.moto, self.pedestres):
            if self.moto.fast_gear:
                self.trigger_infraction("Atropelamento!", 0, is_fatal=True)
            elif self.message_timer == 0:
                self.trigger_infraction("Esbarrão no pedestre!", 5)

    def draw(self):
        self.cidade.draw(self.screen)
        self.pedestres.draw(self.screen)
        self.moto.draw(self.screen)
        
        self.interface.draw_hud(
            self.screen, self.time_left, self.moto.fast_gear, 
            self.infractions, self.current_message
        )
        
        if self.state != "PLAYING":
            self.interface.draw_end_screen(
                self.screen, self.state, self.end_message, self.infractions
            )
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    while True:
        game.process_input()
        game.update()
        game.draw()