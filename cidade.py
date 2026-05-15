import pygame


class Cidade:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        # Ative ou desative a visualização das hitboxes aqui
        self.mostrar_hitboxes = True

        try:
            self.background = pygame.image.load("cidade.png").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except FileNotFoundError:
            print("AVISO: Imagem do mapa não encontrada. Usando fundo provisório.")
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((60, 60, 60))

        # --- HITBOXES TOTAIS ---
        self.obstaculos = [
            pygame.Rect(3, 348, 63, 311),
            pygame.Rect(64, 627, 384, 33),
            pygame.Rect(437, 550, 31, 108),
            pygame.Rect(496, 548, 52, 110),
            pygame.Rect(466, 604, 314, 46),
            pygame.Rect(643, 549, 137, 58),
            pygame.Rect(574, 550, 42, 106),
            pygame.Rect(437, 467, 238, 20),
            pygame.Rect(600, 486, 42, 15),
            pygame.Rect(539, 486, 41, 16),
            pygame.Rect(479, 484, 39, 19),
            pygame.Rect(555, 352, 120, 117),
            pygame.Rect(489, 416, 66, 51),
            pygame.Rect(521, 387, 34, 27),
            pygame.Rect(536, 370, 18, 17),
            pygame.Rect(505, 400, 16, 14),
            pygame.Rect(462, 445, 28, 22),
            pygame.Rect(475, 434, 13, 9),
            pygame.Rect(450, 456, 12, 13),
            pygame.Rect(497, 410, 9, 6),
            pygame.Rect(525, 380, 8, 6),
            pygame.Rect(544, 362, 11, 7),
            pygame.Rect(750, 349, 142, 200),
            pygame.Rect(779, 548, 95, 17),
            pygame.Rect(873, 548, 11, 10),
            pygame.Rect(967, 347, 31, 304),
            pygame.Rect(944, 5, 53, 267),
            pygame.Rect(850, 166, 94, 106),
            pygame.Rect(530, 170, 241, 101),
            pygame.Rect(652, 91, 68, 80),
            pygame.Rect(719, 123, 29, 47),
            pygame.Rect(748, 144, 23, 25),
            pygame.Rect(747, 131, 12, 11),
            pygame.Rect(721, 106, 11, 14),
            pygame.Rect(732, 114, 8, 9),
            pygame.Rect(824, 4, 40, 83),
            pygame.Rect(993, 269, 6, 82),
            pygame.Rect(4, 266, 6, 88),
            pygame.Rect(1, 4, 41, 268),
            pygame.Rect(40, 143, 26, 129),
            pygame.Rect(67, 144, 116, 19),
            pygame.Rect(154, 118, 28, 28),
            pygame.Rect(41, 4, 533, 22),
            pygame.Rect(156, 23, 418, 26),
            pygame.Rect(256, 48, 319, 44),
            pygame.Rect(574, 1, 249, 16),
            pygame.Rect(789, 14, 34, 38),
            pygame.Rect(805, 50, 17, 21),
            pygame.Rect(815, 69, 6, 10),
            pygame.Rect(795, 50, 7, 11),
            pygame.Rect(771, 18, 17, 18),
            pygame.Rect(760, 18, 8, 8),
            pygame.Rect(257, 170, 198, 102),
            pygame.Rect(142, 239, 118, 33),
            pygame.Rect(143, 352, 94, 202),
            pygame.Rect(236, 496, 123, 59),
            pygame.Rect(313, 349, 68, 70),
            pygame.Rect(378, 351, 62, 11),
            pygame.Rect(379, 360, 32, 30),
            pygame.Rect(409, 362, 16, 13),
            pygame.Rect(379, 386, 16, 18),
            pygame.Rect(392, 387, 11, 10),
            pygame.Rect(378, 402, 10, 9),
            pygame.Rect(48, 306, 275, 13), 
            pygame.Rect(926, 436, 9, 98),
            pygame.Rect(816, 598, 70, 11),
            pygame.Rect(270, 355, 7, 83),
            pygame.Rect(294, 454, 85, 10),
            pygame.Rect(393, 504, 7, 66),
            pygame.Rect(208, 587, 156, 6),
            pygame.Rect(137, 586, 34, 7),
            pygame.Rect(103, 400, 6, 79),
            pygame.Rect(103, 212, 7, 48),
            pygame.Rect(368, 309, 264, 10),
            pygame.Rect(691, 309, 149, 9),
            pygame.Rect(887, 307, 60, 15),
        ]

        # --- ZONAS DE OBJETIVO ---
        self.ponto_coleta_rect = pygame.Rect(41, 42, 88, 87)
        self.ponto_b_rect = pygame.Rect(641, 23, 87, 68)
        self.ponto_c_rect = pygame.Rect(782, 563, 190, 80)

        pygame.font.init()
        self.fonte_zona = pygame.font.SysFont("arial", 22, bold=True)

    def get_spawn_point(self):
        return 70, 325

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        # Zona C
        pygame.draw.rect(surface, (50, 205, 50), self.ponto_c_rect, 4)

        texto = self.fonte_zona.render("ZONA C", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=self.ponto_c_rect.center)

        fundo_texto = pygame.Rect(
            texto_rect.x - 5,
            texto_rect.y - 2,
            texto_rect.width + 10,
            texto_rect.height + 4
        )

        pygame.draw.rect(surface, (0, 0, 0), fundo_texto)
        surface.blit(texto, texto_rect)

        # --- HITBOXES VISÍVEIS ---
        if self.mostrar_hitboxes:
            for obs in self.obstaculos:
                pygame.draw.rect(surface, (255, 0, 0), obs, 2)

            # Áreas de missão
            pygame.draw.rect(surface, (0, 0, 255), self.ponto_coleta_rect, 2)
            pygame.draw.rect(surface, (0, 255, 0), self.ponto_b_rect, 2)
            pygame.draw.rect(surface, (0, 255, 0), self.ponto_c_rect, 2)