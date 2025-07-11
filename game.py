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
BLACK = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

class Game:
    def __init__(self):
        # Player settings
        self.player_size = 50
        self.player_x = WIDTH // 2 - self.player_size // 2
        self.player_y = HEIGHT - self.player_size - 10
        self.player_speed = 5
        self.max_health = 5
        self.current_health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1500  # 1.5 seconds of invulnerability after hit
        self.player_color = WHITE

        # Level settings
        self.level = 1
        self.coins_for_next_level = 10  # Coins needed to advance to next level
        self.coins_collected_this_level = 0
        self.level_multiplier = 1.2  # Speed increase per level

        # Coin settings
        self.coin_size = 20
        self.base_coin_speed = 3
        self.coin_speed = self.base_coin_speed
        self.coins = [self.create_coin()]  # List to hold multiple coins

        # Obstacle settings
        self.obstacle_size = 50
        self.base_obstacle_speed = 4
        self.obstacle_speed = self.base_obstacle_speed
        self.obstacles = [self.create_obstacle()]  # List to hold multiple obstacles

        # Game state
        self.game_over = False
        self.score = 0

    def create_coin(self):
        return {
            'x': random.randint(0, WIDTH - self.coin_size),
            'y': random.randint(-100, 0)
        }

    def create_obstacle(self):
        return {
            'x': random.randint(0, WIDTH - self.obstacle_size),
            'y': random.randint(-200, -50)
        }

    def reset_game(self):
        # Reset player position and health
        self.player_x = WIDTH // 2 - self.player_size // 2
        self.player_y = HEIGHT - self.player_size - 10
        self.current_health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.player_color = WHITE

        # Reset level
        self.level = 1
        self.coins_collected_this_level = 0
        self.coin_speed = self.base_coin_speed
        self.obstacle_speed = self.base_obstacle_speed

        # Reset coins and obstacles
        self.coins = [self.create_coin()]
        self.obstacles = [self.create_obstacle()]

        # Reset score
        self.score = 0

        # Reset game state
        self.game_over = False

    def advance_level(self):
        self.level += 1
        self.coins_collected_this_level = 0

        # Increase speeds based on level
        self.coin_speed = self.base_coin_speed * (self.level_multiplier ** (self.level - 1))
        self.obstacle_speed = self.base_obstacle_speed * (self.level_multiplier ** (self.level - 1))

        # Add more coins and obstacles as levels progress
        max_coins = min(3, 1 + self.level // 3)  # Add more coins every 3 levels, max 3
        max_obstacles = min(3, 1 + self.level // 4)  # Add more obstacles every 4 levels, max 3

        while len(self.coins) < max_coins:
            self.coins.append(self.create_coin())
        while len(self.obstacles) < max_obstacles:
            self.obstacles.append(self.create_obstacle())

        # Give bonus health every 5 levels
        if self.level % 5 == 0:
            self.current_health = min(self.max_health, self.current_health + 1)

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
            current_time = pygame.time.get_ticks()

            # Update invulnerability
            if self.invulnerable:
                if current_time - self.invulnerable_timer > self.invulnerable_duration:
                    self.invulnerable = False
                    self.player_color = WHITE
                else:
                    # Flash player while invulnerable
                    if (current_time // 200) % 2:  # Flash every 200ms
                        self.player_color = WHITE
                    else:
                        self.player_color = BLUE

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < WIDTH - self.player_size:
                self.player_x += self.player_speed

            # Update coins
            player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
            for coin in self.coins[:]:
                coin['y'] += self.coin_speed
                if coin['y'] > HEIGHT:
                    self.coins.remove(coin)
                    self.coins.append(self.create_coin())
                else:
                    coin_rect = pygame.Rect(coin['x'], coin['y'], self.coin_size, self.coin_size)
                    if player_rect.colliderect(coin_rect):
                        self.score += self.level  # Score based on level
                        self.coins_collected_this_level += 1
                        self.coins.remove(coin)
                        self.coins.append(self.create_coin())

                        # Check for level advancement
                        if self.coins_collected_this_level >= self.coins_for_next_level:
                            self.advance_level()

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle['y'] += self.obstacle_speed
                if obstacle['y'] > HEIGHT:
                    self.obstacles.remove(obstacle)
                    self.obstacles.append(self.create_obstacle())
                else:
                    obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'],
                                             self.obstacle_size, self.obstacle_size)
                    if player_rect.colliderect(obstacle_rect) and not self.invulnerable:
                        self.current_health -= 1
                        if self.current_health <= 0:
                            self.game_over = True
                        else:
                            # Start invulnerability period
                            self.invulnerable = True
                            self.invulnerable_timer = current_time
                            # Reset obstacle position
                            self.obstacles.remove(obstacle)
                            self.obstacles.append(self.create_obstacle())

    def draw_health_bar(self):
        # Health bar background
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 40
        pygame.draw.rect(window, RED, (bar_x, bar_y, bar_width, bar_height))

        # Health bar fill
        health_percentage = self.current_health / self.max_health
        health_width = bar_width * health_percentage
        pygame.draw.rect(window, GREEN, (bar_x, bar_y, health_width, bar_height))

        # Health text
        font = pygame.font.Font(None, 24)
        health_text = font.render(f'Health: {int(health_percentage * 100)}%', True, WHITE)
        window.blit(health_text, (bar_x + bar_width + 10, bar_y + 2))

    def draw_level_progress(self):
        # Level progress bar
        bar_width = 200
        bar_height = 20
        bar_x = WIDTH - bar_width - 10
        bar_y = 40
        pygame.draw.rect(window, BLUE, (bar_x, bar_y, bar_width, bar_height))

        # Progress fill
        progress = self.coins_collected_this_level / self.coins_for_next_level
        progress_width = bar_width * progress
        pygame.draw.rect(window, PURPLE, (bar_x, bar_y, progress_width, bar_height))

        # Progress text
        font = pygame.font.Font(None, 24)
        progress_text = font.render(f'Level Progress: {int(progress * 100)}%', True, WHITE)
        text_rect = progress_text.get_rect(right=bar_x - 10, centery=bar_y + bar_height//2)
        window.blit(progress_text, text_rect)

    def draw(self):
        window.fill(BLACK)

        # Draw player
        pygame.draw.rect(window, self.player_color, (self.player_x, self.player_y, self.player_size, self.player_size))

        # Draw coins
        for coin in self.coins:
            pygame.draw.circle(window, YELLOW, (coin['x'] + self.coin_size//2,
                                              coin['y'] + self.coin_size//2), self.coin_size//2)

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(window, RED, (obstacle['x'], obstacle['y'],
                                         self.obstacle_size, self.obstacle_size))

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(level_text, (WIDTH - 150, 10))

        # Draw health bar and level progress
        self.draw_health_bar()
        self.draw_level_progress()

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

            # Final score and level
            final_score_font = pygame.font.Font(None, 48)
            final_score_text = final_score_font.render(f'Final Score: {self.score} - Level: {self.level}', True, WHITE)
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
