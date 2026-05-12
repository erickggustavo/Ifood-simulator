import pygame

class Interface:
    def __init__(self, screen_width, screen_height):
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        
        self.width = screen_width
        self.height = screen_height
        
        # Definição de Cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 50, 50)
        self.GREEN = (50, 255, 50)
        self.YELLOW = (255, 204, 0)
        
        # Definição de Fontes
        self.font_hud = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_msg = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_title = pygame.font.SysFont('Arial', 40, bold=True)
        self.font_text = pygame.font.SysFont('Arial', 18)

    def draw_hud(self, surface, time_left, is_fast_gear, infractions, popup_msg=""):
        """Desenha a barra superior com os status durante o jogo."""
        
        # Barra superior (Fundo preto para dar contraste com o mapa)
        pygame.draw.rect(surface, self.BLACK, (0, 0, self.width, 40))
        
        # 1. Cronômetro (Fica vermelho se o tempo estiver acabando)
        time_color = self.WHITE if time_left > 10 else self.RED
        time_text = self.font_hud.render(f"Tempo: {max(0, int(time_left))}s", True, time_color)
        surface.blit(time_text, (10, 10))

        # 2. Indicador de Marcha
        gear_color = self.RED if is_fast_gear else self.GREEN
        gear_str = "RÁPIDA (Risco)" if is_fast_gear else "NORMAL (Segura)"
        gear_text = self.font_hud.render(f"Marcha: {gear_str}", True, gear_color)
        # Centraliza o texto da marcha na tela
        surface.blit(gear_text, (self.width // 2 - gear_text.get_width() // 2, 10))

        # 3. Contador de Infrações
        inf_text = self.font_hud.render(f"Infrações: {infractions}", True, self.YELLOW)
        surface.blit(inf_text, (self.width - inf_text.get_width() - 10, 10))

        # 4. Mensagem Pop-up Flutuante (Ex: "Contramão! -2s")
        if popup_msg:
            msg_surf = self.font_msg.render(popup_msg, True, self.RED)
            # Cria um fundo preto arredondado atrás do texto para não misturar com o mapa
            bg_rect = msg_surf.get_rect(center=(self.width // 2, 70))
            bg_rect.inflate_ip(20, 10) # Dá um "respiro" nas bordas
            pygame.draw.rect(surface, self.BLACK, bg_rect, border_radius=5)
            surface.blit(msg_surf, msg_surf.get_rect(center=(self.width // 2, 70)))

    def draw_end_screen(self, surface, state, end_message, infractions):
        """Desenha a tela final de Vitória ou Derrota com a mensagem educativa."""
        
        # Cria uma película semi-transparente escura sobre o jogo parado
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(220) # Nível de transparência (0 a 255)
        overlay.fill(self.BLACK)
        surface.blit(overlay, (0, 0))

        # Título Principal (Vitória = Verde, Game Over = Vermelho)
        title_color = self.GREEN if state == "VICTORY" else self.RED
        title_text = "ENTREGA CONCLUÍDA" if state == "VICTORY" else "FIM DE JOGO"
        title_surf = self.font_title.render(title_text, True, title_color)
        surface.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 100))

        # O motivo de ter ganhado ou perdido (Ex: "Atropelamento por excesso de velocidade!")
        motivo_surf = self.font_msg.render(end_message, True, self.YELLOW)
        surface.blit(motivo_surf, (self.width // 2 - motivo_surf.get_width() // 2, 160))

        # Bloco de Texto com a Mensagem de Impacto Social
        resumo = [
            f"Total de Infrações Cometidas: {infractions}",
            "",
            "A PRESSA MATA.",
            "Aplicativos de entrega frequentemente impõem metas",
            "irreais que forçam o motoboy a arriscar a própria vida.",
            "A verdadeira segurança no trânsito começa por condições",
            "de trabalho justas e respeito aos limites da vida.",
            "",
            "Pressione 'R' para tentar novamente."
        ]

        # Imprime o bloco de texto linha por linha
        y_offset = 220
        for line in resumo:
            color = self.WHITE if "PRESSA" not in line else self.RED
            txt_surf = self.font_text.render(line, True, color)
            surface.blit(txt_surf, (self.width // 2 - txt_surf.get_width() // 2, y_offset))
            y_offset += 30