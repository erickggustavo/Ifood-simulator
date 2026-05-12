import pygame

class Cidade:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # 1. Carregamento do Mapa (Plano de Fundo)
        try:
            self.background = pygame.image.load('cidade.png').convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except FileNotFoundError:
            print("AVISO: Imagem do mapa não encontrada. Usando fundo provisório.")
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((60, 60, 60))

        # --- HITBOXES TOTAIS (CIDADE MAPEADA E LIMPA) ---
        self.obstaculos = [
            # Bordas Externas
            pygame.Rect(0, -10, 1000, 10), pygame.Rect(0, 650, 1000, 10),
            pygame.Rect(-10, 0, 10, 650), pygame.Rect(1000, 0, 10, 650),

            # BLOCOS SUPERIORES
            pygame.Rect(259, 40, 315, 49),    
            pygame.Rect(946, 42, 50, 114),    
            pygame.Rect(659, 95, 88, 59),     

            # BLOCOS CENTRAIS E ARMAZÉM
            pygame.Rect(251, 41, 198, 223),   
            pygame.Rect(533, 168, 232, 97),   
            pygame.Rect(851, 165, 144, 101),  
            pygame.Rect(752, 348, 132, 207),  
            pygame.Rect(313, 351, 66, 64),    
            pygame.Rect(556, 350, 113, 110),  
            pygame.Rect(530, 377, 60, 38),    
            pygame.Rect(485, 427, 84, 35),    
            pygame.Rect(400, 350, 34, 9),     

            # BLOCOS INFERIORES E CANTO ESQUERDO
            pygame.Rect(143, 350, 93, 201),   
            pygame.Rect(4, 352, 58, 291),     
            pygame.Rect(241, 494, 117, 56),   
            pygame.Rect(433, 465, 317, 158),  

            # ZONAS DE SEGURANÇA E BORDAS EXTRAS
            pygame.Rect(146, 237, 100, 29),
            pygame.Rect(63, 623, 385, 20),
        ]    
        
        # --- ZONAS DE OBJETIVO (Sistema de Missões) ---
        # 1. Ponto de Coleta (Em cima do desenho da caixa na Zona A)
        self.ponto_coleta_rect = pygame.Rect(80, 50, 120, 120)
        
        # 2. Ponto de Entrega B (Topo Direita)
        self.ponto_b_rect = pygame.Rect(770, 20, 200, 100)
        
        # 3. Ponto de Entrega C (NOVO: Canto inferior direito, na rua vazia)
        self.ponto_c_rect = pygame.Rect(780, 566, 177, 70)

        # --- FONTE PARA DESENHAR A ZONA C ---
        pygame.font.init()
        self.fonte_zona = pygame.font.SysFont("arial", 22, bold=True)

    def get_spawn_point(self):
        """Retorna as coordenadas ideais para a moto nascer (na rua, fora dos prédios)."""
        return 100, 300

    def draw(self, surface):
        """Desenha a cidade na tela."""
        surface.blit(self.background, (0, 0))
        
        # --- DESENHANDO A MARCAÇÃO DA ZONA C ---
        # Desenha uma borda verde clara (LimeGreen) indicando a área
        pygame.draw.rect(surface, (50, 205, 50), self.ponto_c_rect, 4)
        
        # Cria o texto "ZONA C" (Branco)
        texto = self.fonte_zona.render("ZONA C", True, (255, 255, 255))
        
        # Centraliza o texto exatamente no meio do nosso retângulo
        texto_rect = texto.get_rect(center=self.ponto_c_rect.center)
        
        # Desenha um fundo preto fininho atrás do texto para dar leitura
        fundo_texto = pygame.Rect(texto_rect.x - 5, texto_rect.y - 2, texto_rect.width + 10, texto_rect.height + 4)
        pygame.draw.rect(surface, (0, 0, 0), fundo_texto)
        
        # Cola o texto na tela
        surface.blit(texto, texto_rect)
        
        # DICA DE DEBUG: Se quiser ver as áreas das missões invisíveis, descomente as linhas abaixo:
        # pygame.draw.rect(surface, (0, 0, 255), self.ponto_coleta_rect, 2) # Azul para Coleta
        # pygame.draw.rect(surface, (0, 255, 0), self.ponto_b_rect, 2)      # Verde para B
        # pygame.draw.rect(surface, (0, 255, 0), self.ponto_c_rect, 2)      # Verde para C