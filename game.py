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
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        # Player settings
        self.player_size = 50
        self.player_x = WIDTH // 2 - self.player_size // 2
        self.player_y = HEIGHT - self.player_size - 10
        self.player_speed = 5

        # Coin settings
        self.coin_size = 20
        self.coin_x = random.randint(0, WIDTH - self.coin_size)
        self.coin_y = 0
        self.coin_speed = 3
        self.score = 0

        # Obstacle settings
        self.obstacle_size = 50
        self.obstacle_x = random.randint(0, WIDTH - self.obstacle_size)
        self.obstacle_y = 0
        self.obstacle_speed = 4

        # Game state
        self.game_over = False

    def reset_game(self):
        # Reset player position
        self.player_x = WIDTH // 2 - self.player_size // 2
        self.player_y = HEIGHT - self.player_size - 10

        # Reset coin
        self.coin_x = random.randint(0, WIDTH - self.coin_size)
        self.coin_y = 0

        # Reset obstacle
        self.obstacle_x = random.randint(0, WIDTH - self.obstacle_size)
        self.obstacle_y = 0

        # Reset score
        self.score = 0

        # Reset game state
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def update(self):
        if not self.game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < WIDTH - self.player_size:
                self.player_x += self.player_speed

            # Move coin
            self.coin_y += self.coin_speed
            if self.coin_y > HEIGHT:
                self.coin_y = 0
                self.coin_x = random.randint(0, WIDTH - self.coin_size)

            # Move obstacle
            self.obstacle_y += self.obstacle_speed
            if self.obstacle_y > HEIGHT:
                self.obstacle_y = 0
                self.obstacle_x = random.randint(0, WIDTH - self.obstacle_size)

            # Collision detection with coin
            player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
            coin_rect = pygame.Rect(self.coin_x, self.coin_y, self.coin_size, self.coin_size)

            if player_rect.colliderect(coin_rect):
                self.score += 1
                self.coin_y = 0
                self.coin_x = random.randint(0, WIDTH - self.coin_size)

            # Collision detection with obstacle
            obstacle_rect = pygame.Rect(self.obstacle_x, self.obstacle_y, self.obstacle_size, self.obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                self.game_over = True

    def draw(self):
        window.fill(BLACK)

        # Draw player
        pygame.draw.rect(window, WHITE, (self.player_x, self.player_y, self.player_size, self.player_size))

        # Draw coin
        pygame.draw.circle(window, YELLOW, (self.coin_x + self.coin_size//2, self.coin_y + self.coin_size//2), self.coin_size//2)

        # Draw obstacle
        pygame.draw.rect(window, RED, (self.obstacle_x, self.obstacle_y, self.obstacle_size, self.obstacle_size))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        window.blit(score_text, (10, 10))

        # Draw game over screen
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            window.blit(overlay, (0, 0))

            # Game Over text
            game_over_font = pygame.font.Font(None, 74)
            game_over_text = game_over_font.render('Game Over!', True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            window.blit(game_over_text, game_over_rect)

            # Final score
            final_score_font = pygame.font.Font(None, 48)
            final_score_text = final_score_font.render(f'Final Score: {self.score}', True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            window.blit(final_score_text, final_score_rect)

            # Restart instruction
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render('Press R to Restart or ESC to Quit', True, GREEN)
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
            window.blit(restart_text, restart_rect)

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
