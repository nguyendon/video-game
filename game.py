import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Coin settings
coin_size = 20
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = 0
coin_speed = 3
score = 0

# Obstacle settings
obstacle_size = 50
obstacle_x = random.randint(0, WIDTH - obstacle_size)
obstacle_y = 0
obstacle_speed = 4

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Move coin
    coin_y += coin_speed
    if coin_y > HEIGHT:
        coin_y = 0
        coin_x = random.randint(0, WIDTH - coin_size)

    # Move obstacle
    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = 0
        obstacle_x = random.randint(0, WIDTH - obstacle_size)

    # Collision detection with coin
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
    
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_y = 0
        coin_x = random.randint(0, WIDTH - coin_size)

    # Collision detection with obstacle
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size)
    if player_rect.colliderect(obstacle_rect):
        running = False

    # Draw everything
    window.fill(BLACK)
    
    # Draw player
    pygame.draw.rect(window, WHITE, (player_x, player_y, player_size, player_size))
    
    # Draw coin
    pygame.draw.circle(window, YELLOW, (coin_x + coin_size//2, coin_y + coin_size//2), coin_size//2)
    
    # Draw obstacle
    pygame.draw.rect(window, RED, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    window.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(60)

# Quit game
pygame.quit()