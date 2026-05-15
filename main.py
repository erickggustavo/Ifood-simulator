import pygame
import sys
import random

from cidade import Cidade
from moto import Moto
from pedestre import Pedestre
from interface import Interface

WIDTH, HEIGHT = 1000, 650
FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Entrega Consciente: O Dilema do Trânsito")
        self.clock = pygame.time.Clock()

        # =========================
        # ÁUDIOS
        # =========================
        self.som_moto = pygame.mixer.Sound("assets/audios/moto.mp3")
        self.som_atropelamento = pygame.mixer.Sound("assets/audios/atropelamento.mp3")
        self.som_coleta = pygame.mixer.Sound("assets/audios/coleta.mp3")
        self.som_entrega = pygame.mixer.Sound("assets/audios/entrega.mp3")

        self.som_moto.set_volume(0.3)
        self.som_atropelamento.set_volume(0.8)
        self.som_coleta.set_volume(0.8)
        self.som_entrega.set_volume(0.8)

        pygame.mixer.music.load("assets/audios/musica.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.canal_moto = pygame.mixer.Channel(0)

        self.cidade = Cidade(WIDTH, HEIGHT)

        # Esconde hitboxes do mapa
        if hasattr(self.cidade, "mostrar_hitboxes"):
            self.cidade.mostrar_hitboxes = False

        self.interface = Interface(WIDTH, HEIGHT)

        self.reset_game()

    def gerar_ponto_seguro(self, cidade):
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)

            rect_teste = pygame.Rect(x, y, 32, 32)

            colidiu = False

            for obs in cidade.obstaculos:
                if rect_teste.colliderect(obs):
                    colidiu = True
                    break

            if not colidiu:
                return x, y

    def reset_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)

        self.state = "PLAYING"
        self.time_left = 60.0
        self.infractions = 0
        self.message_timer = 180
        self.current_message = "Vá até a caixa na Zona A para coletar!"
        self.end_message = ""

        self.encomenda_coletada = False
        self.entrega_b_feita = False
        self.entrega_c_feita = False
        self.colidindo_pedestre = False

        spawn_x, spawn_y = self.cidade.get_spawn_point()
        self.moto = Moto(spawn_x, spawn_y)

        self.pedestres = pygame.sprite.Group()

        quantidade_pedestres = 12

        for _ in range(quantidade_pedestres):
            start_x, start_y = self.gerar_ponto_seguro(self.cidade)
            end_x, end_y = self.gerar_ponto_seguro(self.cidade)

            velocidade = random.uniform(0.5, 1.5)

            p = Pedestre(start_x, start_y, end_x, end_y, velocidade)

            # Esconde hitbox do pedestre
            if hasattr(p, "mostrar_hitbox"):
                p.mostrar_hitbox = False

            self.pedestres.add(p)

    def trigger_infraction(self, msg, time_penalty, is_fatal=False):
        if self.state != "PLAYING":
            return

        if is_fatal:
            self.state = "GAME_OVER"
            self.end_message = f"ACIDENTE: {msg}"
            return

        self.infractions += 1
        self.time_left -= time_penalty
        self.current_message = f"{msg} (-{time_penalty}s)"
        self.message_timer = 90

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and self.state == "PLAYING":
                    self.moto.toggle_gear()

                if event.key == pygame.K_r and self.state != "PLAYING":
                    self.reset_game()

        keys = pygame.key.get_pressed()

        if self.state == "PLAYING":
            self.moto.handle_input(keys)

            moto_movendo = (
                keys[pygame.K_w] or
                keys[pygame.K_s] or
                keys[pygame.K_a] or
                keys[pygame.K_d] or
                keys[pygame.K_UP] or
                keys[pygame.K_DOWN] or
                keys[pygame.K_LEFT] or
                keys[pygame.K_RIGHT]
            )

            if moto_movendo:
                if not self.canal_moto.get_busy():
                    self.canal_moto.play(self.som_moto, loops=-1)
            else:
                self.canal_moto.stop()

        else:
            self.canal_moto.stop()

    def update(self):
        if self.state != "PLAYING":
            return

        dt = self.clock.tick(FPS) / 1000.0
        self.time_left -= dt

        if self.time_left <= 0:
            self.state = "GAME_OVER"
            self.end_message = "O TEMPO ESGOTOU!"
            return

        self.moto.update(WIDTH, HEIGHT, self.cidade.obstaculos)
        self.pedestres.update(self.cidade.obstaculos)

        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.current_message = ""

        rect_moto = self.moto.hitbox

        if not self.encomenda_coletada:
            if rect_moto.colliderect(self.cidade.ponto_coleta_rect):
                self.som_coleta.play()
                self.encomenda_coletada = True
                self.current_message = "Coletado! Entregue nas Zonas B e C!"
                self.message_timer = 180

        else:
            if not self.entrega_b_feita and rect_moto.colliderect(self.cidade.ponto_b_rect):
                self.som_entrega.play()
                self.entrega_b_feita = True
                self.current_message = "Entrega B Concluída!"
                self.message_timer = 120

            if not self.entrega_c_feita and rect_moto.colliderect(self.cidade.ponto_c_rect):
                self.som_entrega.play()
                self.entrega_c_feita = True
                self.current_message = "Entrega C Concluída!"
                self.message_timer = 120

            if self.entrega_b_feita and self.entrega_c_feita:
                self.state = "VICTORY"
                self.end_message = "Sucesso! Você fez todas as entregas!"

        for pedestre in self.pedestres:
            if self.moto.hitbox.colliderect(pedestre.hitbox):

                if not self.colidindo_pedestre:
                    self.som_atropelamento.play()
                    self.colidindo_pedestre = True

                if self.moto.fast_gear:
                    self.trigger_infraction("Atropelamento!", 0, is_fatal=True)

                elif self.message_timer == 0:
                    self.trigger_infraction("Esbarrão no pedestre!", 20)

                break

        else:
            self.colidindo_pedestre = False

    def draw(self):
        self.cidade.draw(self.screen)

        # Desenha pedestres sem mostrar hitbox
        self.pedestres.draw(self.screen)

        # Desenha moto sem mostrar hitbox
        self.screen.blit(self.moto.image, self.moto.rect)

        lbl_player = self.moto.font_label.render("Você (Moto)", True, (255, 255, 255))
        self.screen.blit(lbl_player, (self.moto.rect.x - 15, self.moto.rect.y - 18))

        self.interface.draw_hud(
            self.screen,
            self.time_left,
            self.moto.fast_gear,
            self.infractions,
            self.current_message
        )

        if self.state != "PLAYING":
            self.interface.draw_end_screen(
                self.screen,
                self.state,
                self.end_message,
                self.infractions
            )

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()

    while True:
        game.process_input()
        game.update()
        game.draw()