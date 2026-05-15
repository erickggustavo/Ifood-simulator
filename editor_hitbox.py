import pygame

WIDTH, HEIGHT = 1000, 650

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor de Hitbox")

background = pygame.image.load("cidade.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

hitboxes = []
drawing = False
start_pos = None
current_rect = None

running = True

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                x1, y1 = start_pos
                x2, y2 = event.pos

                x = min(x1, x2)
                y = min(y1, y2)
                w = abs(x2 - x1)
                h = abs(y2 - y1)

                current_rect = pygame.Rect(x, y, w, h)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False

                if current_rect and current_rect.width > 5 and current_rect.height > 5:
                    hitboxes.append(current_rect)
                    print(f"pygame.Rect({current_rect.x}, {current_rect.y}, {current_rect.width}, {current_rect.height}),")

                current_rect = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if hitboxes:
                    removida = hitboxes.pop()
                    print(f"Removida: pygame.Rect({removida.x}, {removida.y}, {removida.width}, {removida.height}),")

            if event.key == pygame.K_c:
                print("\n# HITBOXES GERADAS:")
                for rect in hitboxes:
                    print(f"pygame.Rect({rect.x}, {rect.y}, {rect.width}, {rect.height}),")
                print("# FIM\n")

            if event.key == pygame.K_ESCAPE:
                running = False

    for rect in hitboxes:
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    if current_rect:
        pygame.draw.rect(screen, (0, 255, 0), current_rect, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()