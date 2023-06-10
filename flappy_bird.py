import pygame
import os
import sys
import time
import random

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Charger les images
BG_IMG = pygame.transform.scale(pygame.image.load("background3.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
BIRD_IMG = pygame.transform.scale(pygame.image.load("bird.png"), (40, 40))
PIPE_IMG = pygame.transform.scale(pygame.image.load("pipe.png"), (50, SCREEN_HEIGHT / 3))


# Définir les constantes du jeu
BIRD_Y = 300
GRAVITY = 0.5
FLAP_SPEED = -10
PIPE_GAP = 200
PIPE_SPEED = 5
FONT = pygame.font.Font(None, 36)


def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False


def main():
    # Initialiser les variables
    bird_rect = pygame.Rect(100, BIRD_Y, 40, 40)
    bird_speed = 0
    rotation = 0
    score = 0
    pipes = []
    bg_x = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_speed = FLAP_SPEED
                rotation = 20

        # Mettre à jour la position de l'oiseau
        bird_speed += GRAVITY
        bird_rect.y += int(bird_speed)
        rotation = max(-90, rotation - 3)

        # Déplacer l'arrière-plan
        bg_x -= 1
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

        # Créer de nouveaux tuyaux
        if len(pipes) == 0 or pipes[-1].bottomright[0] < SCREEN_WIDTH - 300:
            top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipes.append(pygame.Rect(SCREEN_WIDTH, 0, 80, top_height))
            pipes.append(pygame.Rect(SCREEN_WIDTH, top_height + PIPE_GAP, 80, SCREEN_HEIGHT))

        # Déplacer les tuyaux et mettre à jour le score
        pipes_to_remove = []
        for pipe in pipes:
            pipe.x -= PIPE_SPEED
            if pipe.right < 0:
                pipes_to_remove.append(pipe)
            if pipe.x + pipe.width == 100:
                score += 1

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # Vérifier les collisions
        if check_collision(bird_rect, pipes) or bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
            text = FONT.render("Game Over", True, (255, 0, 0))
            WIN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            time.sleep(2)
            return

        # Dessiner tout
        WIN.blit(BG_IMG, (bg_x, 0))
        WIN.blit(BG_IMG, (bg_x + SCREEN_WIDTH, 0))
        for pipe in pipes:
            WIN.blit(PIPE_IMG, (pipe.x, pipe.y))
        rotated_bird = pygame.transform.rotate(BIRD_IMG, rotation)
        WIN.blit(rotated_bird, (100, bird_rect.y))

        # Afficher le score
        score_text = FONT.render(str(int(score)), True, (255, 255, 255))
        WIN.blit(score_text, (SCREEN_WIDTH // 3, 50))

        # Mettre à jour l'affichage
        pygame.display.update()


if __name__ == "__main__":
    main()
