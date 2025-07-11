import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Get the current screen info
screen_info = pygame.display.Info()
DESKTOP_WIDTH = screen_info.current_w
DESKTOP_HEIGHT = screen_info.current_h

# Base resolution (for scaling calculations)
BASE_WIDTH = 800
BASE_HEIGHT = 600

# Initial window size
WIDTH = BASE_WIDTH
HEIGHT = BASE_HEIGHT

# Create resizable window
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Coin Collector")

# Scale factor for game objects
scale_x = 1.0
scale_y = 1.0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)

# Power-up Types
POWERUP_INVINCIBLE = 'invincible'
POWERUP_DOUBLE_POINTS = 'double_points'
POWERUP_HEALTH = 'health'
POWERUP_SLOW_OBSTACLES = 'slow_obstacles'

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.base_size = 30
        self.size = self.base_size
        self.active = False
        self.start_time = 0
        self.duration = 10

        self.color = {
            POWERUP_INVINCIBLE: GOLD,
            POWERUP_DOUBLE_POINTS: GREEN,
            POWERUP_HEALTH: RED,
            POWERUP_SLOW_OBSTACLES: CYAN
        }[type]

    def scale(self, scale_x, scale_y):
        self.size = int(self.base_size * min(scale_x, scale_y))

    def is_expired(self):
        if self.type == POWERUP_HEALTH:
            return True
        return time.time() - self.start_time > self.duration if self.active else False

    def activate(self):
        self.active = True
        self.start_time = time.time()

    def time_remaining(self):
        if not self.active:
            return 0
        return max(0, self.duration - (time.time() - self.start_time))

class Game:
    def __init__(self):
        # Screen settings
        self.fullscreen = False
        self.width = WIDTH
        self.height = HEIGHT

        # Base sizes (for scaling)
        self.base_player_size = 50
        self.base_coin_size = 20
        self.base_obstacle_size = 50
        self.base_powerup_size = 30

        # Player settings
        self.player_size = self.base_player_size
        self.player_x = self.width // 2 - self.player_size // 2
        self.player_y = self.height - self.player_size - 10
        self.base_player_speed = 5
        self.player_speed = self.base_player_speed
        self.max_health = 5
        self.current_health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1500
        self.player_color = WHITE

        # Level settings
        self.level = 1
        self.coins_for_next_level = 10
        self.coins_collected_this_level = 0
        self.level_multiplier = 1.2

        # Coin settings
        self.coin_size = self.base_coin_size
        self.base_coin_speed = 3
        self.coin_speed = self.base_coin_speed
        self.coins = [self.create_coin()]

        # Obstacle settings
        self.obstacle_size = self.base_obstacle_size
        self.base_obstacle_speed = 4
        self.obstacle_speed = self.base_obstacle_speed
        self.original_obstacle_speed = self.obstacle_speed
        self.obstacles = [self.create_obstacle()]

        # Power-up settings
        self.power_ups = []
        self.base_power_up_speed = 2
        self.power_up_speed = self.base_power_up_speed
        self.power_up_spawn_chance = 0.02
        self.active_power_ups = {
            POWERUP_INVINCIBLE: None,
            POWERUP_DOUBLE_POINTS: None,
            POWERUP_SLOW_OBSTACLES: None
        }

        # Initialize sizes
        self.update_scale_factors()

        # Game state
        self.game_over = False
        self.score = 0

    def update_scale_factors(self):
        global scale_x, scale_y
        scale_x = self.width / BASE_WIDTH
        scale_y = self.height / BASE_HEIGHT

        # Update sizes based on new scale
        self.player_size = int(self.base_player_size * min(scale_x, scale_y))
        self.coin_size = int(self.base_coin_size * min(scale_x, scale_y))
        self.obstacle_size = int(self.base_obstacle_size * min(scale_x, scale_y))
        self.player_speed = self.base_player_speed * min(scale_x, scale_y)
        self.coin_speed = self.base_coin_speed * min(scale_x, scale_y)
        self.obstacle_speed = self.base_obstacle_speed * min(scale_x, scale_y)
        self.power_up_speed = self.base_power_up_speed * min(scale_x, scale_y)

        # Update power-up sizes
        for power_up in self.power_ups:
            power_up.scale(scale_x, scale_y)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.width = DESKTOP_WIDTH
            self.height = DESKTOP_HEIGHT
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.width = BASE_WIDTH
            self.height = BASE_HEIGHT
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # Update positions and sizes
        self.update_scale_factors()
        self.player_x = min(max(self.player_x * (self.width / WIDTH), 0),
                           self.width - self.player_size)
        self.player_y = self.height - self.player_size - 10

    def handle_resize(self, size):
        self.width, self.height = size
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.update_scale_factors()
        self.player_y = self.height - self.player_size - 10

    def create_coin(self):
        return {
            'x': random.randint(0, self.width - self.coin_size),
            'y': random.randint(-100, 0)
        }

    def create_obstacle(self):
        return {
            'x': random.randint(0, self.width - self.obstacle_size),
            'y': random.randint(-200, -50)
        }

    def create_power_up(self):
        power_up_type = random.choice([
            POWERUP_INVINCIBLE,
            POWERUP_DOUBLE_POINTS,
            POWERUP_HEALTH,
            POWERUP_SLOW_OBSTACLES
        ])
        return PowerUp(
            random.randint(0, self.width - self.base_powerup_size),
            random.randint(-100, -30),
            power_up_type
        )

    def reset_game(self):
        # Reset player position and health
        self.player_x = self.width // 2 - self.player_size // 2
        self.player_y = self.height - self.player_size - 10
        self.current_health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.player_color = WHITE

        # Reset level
        self.level = 1
        self.coins_collected_this_level = 0
        self.coin_speed = self.base_coin_speed * min(scale_x, scale_y)
        self.obstacle_speed = self.base_obstacle_speed * min(scale_x, scale_y)

        # Reset coins and obstacles
        self.coins = [self.create_coin()]
        self.obstacles = [self.create_obstacle()]

        # Reset power-ups
        self.power_ups = []
        self.active_power_ups = {
            POWERUP_INVINCIBLE: None,
            POWERUP_DOUBLE_POINTS: None,
            POWERUP_SLOW_OBSTACLES: None
        }

        # Reset score
        self.score = 0

        # Reset game state
        self.game_over = False

    def advance_level(self):
        self.level += 1
        self.coins_collected_this_level = 0

        # Increase speeds based on level
        self.coin_speed = (self.base_coin_speed *
                          (self.level_multiplier ** (self.level - 1)) *
                          min(scale_x, scale_y))
        self.obstacle_speed = (self.base_obstacle_speed *
                             (self.level_multiplier ** (self.level - 1)) *
                             min(scale_x, scale_y))
        self.original_obstacle_speed = self.obstacle_speed

        # Add more coins and obstacles as levels progress
        max_coins = min(3, 1 + self.level // 3)
        max_obstacles = min(3, 1 + self.level // 4)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    if self.fullscreen:
                        self.toggle_fullscreen()
                    else:
                        return False
            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.handle_resize(event.size)
        return True

    def update_power_ups(self):
        # Update existing power-ups
        for power_up_type, power_up in list(self.active_power_ups.items()):
            if power_up and power_up.is_expired():
                if power_up_type == POWERUP_SLOW_OBSTACLES:
                    self.obstacle_speed = self.original_obstacle_speed
                self.active_power_ups[power_up_type] = None

        # Spawn new power-ups
        if random.random() < self.power_up_spawn_chance:
            self.power_ups.append(self.create_power_up())

        # Update falling power-ups
        for power_up in self.power_ups[:]:
            power_up.y += self.power_up_speed
            if power_up.y > self.height:
                self.power_ups.remove(power_up)

    def apply_power_up(self, power_up):
        if power_up.type == POWERUP_HEALTH:
            self.current_health = min(self.max_health, self.current_health + 1)
        else:
            power_up.activate()
            self.active_power_ups[power_up.type] = power_up

            if power_up.type == POWERUP_SLOW_OBSTACLES:
                self.obstacle_speed = self.original_obstacle_speed * 0.5

    def update(self):
        if not self.game_over:
            current_time = pygame.time.get_ticks()

            # Update power-ups
            self.update_power_ups()

            # Check if invincible power-up is active
            invincible_power_up = self.active_power_ups[POWERUP_INVINCIBLE]
            is_power_up_invincible = invincible_power_up and invincible_power_up.active

            # Update regular invulnerability
            if self.invulnerable and not is_power_up_invincible:
                if current_time - self.invulnerable_timer > self.invulnerable_duration:
                    self.invulnerable = False
                    self.player_color = WHITE
                else:
                    # Flash player while invulnerable
                    if (current_time // 200) % 2:
                        self.player_color = WHITE
                    else:
                        self.player_color = BLUE

            # Update power-up invincibility color
            if is_power_up_invincible:
                if (current_time // 200) % 2:
                    self.player_color = GOLD
                else:
                    self.player_color = WHITE

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < self.width - self.player_size:
                self.player_x += self.player_speed

            # Update coins
            player_rect = pygame.Rect(self.player_x, self.player_y,
                                    self.player_size, self.player_size)
            for coin in self.coins[:]:
                coin['y'] += self.coin_speed
                if coin['y'] > self.height:
                    self.coins.remove(coin)
                    self.coins.append(self.create_coin())
                else:
                    coin_rect = pygame.Rect(coin['x'], coin['y'],
                                          self.coin_size, self.coin_size)
                    if player_rect.colliderect(coin_rect):
                        # Check for double points power-up
                        points = self.level
                        if self.active_power_ups[POWERUP_DOUBLE_POINTS]:
                            points *= 2
                        self.score += points
                        self.coins_collected_this_level += 1
                        self.coins.remove(coin)
                        self.coins.append(self.create_coin())

                        # Check for level advancement
                        if self.coins_collected_this_level >= self.coins_for_next_level:
                            self.advance_level()

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle['y'] += self.obstacle_speed
                if obstacle['y'] > self.height:
                    self.obstacles.remove(obstacle)
                    self.obstacles.append(self.create_obstacle())
                else:
                    obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'],
                                             self.obstacle_size, self.obstacle_size)
                    if (player_rect.colliderect(obstacle_rect) and
                        not self.invulnerable and
                        not is_power_up_invincible):
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

            # Check power-up collisions
            for power_up in self.power_ups[:]:
                power_up_rect = pygame.Rect(power_up.x, power_up.y,
                                          power_up.size, power_up.size)
                if player_rect.colliderect(power_up_rect):
                    self.apply_power_up(power_up)
                    self.power_ups.remove(power_up)

    def draw_power_up_status(self):
        font = pygame.font.Font(None, int(24 * min(scale_x, scale_y)))
        y_offset = int(80 * scale_y)

        for power_up_type, power_up in self.active_power_ups.items():
            if power_up and power_up.active:
                time_left = power_up.time_remaining()
                if time_left > 0:
                    text = f"{power_up_type.title()}: {time_left:.1f}s"
                    text_surface = font.render(text, True, power_up.color)
                    window.blit(text_surface, (10, y_offset))
                    y_offset += int(25 * scale_y)

    def draw_diamond(self, surface, color, x, y, size):
        points = [
            (x + size//2, y),  # top
            (x + size, y + size//2),  # right
            (x + size//2, y + size),  # bottom
            (x, y + size//2)  # left
        ]
        pygame.draw.polygon(surface, color, points)

    def draw_health_bar(self):
        # Health bar background
        bar_width = int(200 * scale_x)
        bar_height = int(20 * scale_y)
        bar_x = int(10 * scale_x)
        bar_y = int(40 * scale_y)
        pygame.draw.rect(window, RED, (bar_x, bar_y, bar_width, bar_height))

        # Health bar fill
        health_percentage = self.current_health / self.max_health
        health_width = bar_width * health_percentage
        pygame.draw.rect(window, GREEN, (bar_x, bar_y, health_width, bar_height))

        # Health text
        font = pygame.font.Font(None, int(24 * min(scale_x, scale_y)))
        health_text = font.render(f'Health: {int(health_percentage * 100)}%', True, WHITE)
        window.blit(health_text, (bar_x + bar_width + 10, bar_y + 2))

    def draw_level_progress(self):
        # Level progress bar
        bar_width = int(200 * scale_x)
        bar_height = int(20 * scale_y)
        bar_x = self.width - bar_width - int(10 * scale_x)
        bar_y = int(40 * scale_y)
        pygame.draw.rect(window, BLUE, (bar_x, bar_y, bar_width, bar_height))

        # Progress fill
        progress = self.coins_collected_this_level / self.coins_for_next_level
        progress_width = bar_width * progress
        pygame.draw.rect(window, PURPLE, (bar_x, bar_y, progress_width, bar_height))

        # Progress text
        font = pygame.font.Font(None, int(24 * min(scale_x, scale_y)))
        progress_text = font.render(f'Level Progress: {int(progress * 100)}%', True, WHITE)
        text_rect = progress_text.get_rect(right=bar_x - 10, centery=bar_y + bar_height//2)
        window.blit(progress_text, text_rect)

    def draw(self):
        window.fill(BLACK)

        # Draw player
        pygame.draw.rect(window, self.player_color,
                        (self.player_x, self.player_y, self.player_size, self.player_size))

        # Draw coins
        for coin in self.coins:
            pygame.draw.circle(window, YELLOW,
                             (int(coin['x'] + self.coin_size//2),
                              int(coin['y'] + self.coin_size//2)),
                             self.coin_size//2)

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(window, RED,
                           (obstacle['x'], obstacle['y'],
                            self.obstacle_size, self.obstacle_size))

        # Draw power-ups
        for power_up in self.power_ups:
            self.draw_diamond(window, power_up.color,
                            int(power_up.x), int(power_up.y), power_up.size)

        # Draw score and level
        font = pygame.font.Font(None, int(36 * min(scale_x, scale_y)))
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        window.blit(score_text, (int(10 * scale_x), int(10 * scale_y)))
        window.blit(level_text, (self.width - int(150 * scale_x), int(10 * scale_y)))

        # Draw health bar and level progress
        self.draw_health_bar()
        self.draw_level_progress()

        # Draw active power-up status
        self.draw_power_up_status()

        # Draw game over screen
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            window.blit(overlay, (0, 0))

            # Game Over text
            game_over_font = pygame.font.Font(None, int(74 * min(scale_x, scale_y)))
            game_over_text = game_over_font.render('Game Over!', True, RED)
            game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - int(50 * scale_y)))
            window.blit(game_over_text, game_over_rect)

            # Final score and level
            final_score_font = pygame.font.Font(None, int(48 * min(scale_x, scale_y)))
            final_score_text = final_score_font.render(f'Final Score: {self.score} - Level: {self.level}', True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(self.width//2, self.height//2 + int(20 * scale_y)))
            window.blit(final_score_text, final_score_rect)

            # Restart instruction
            restart_font = pygame.font.Font(None, int(36 * min(scale_x, scale_y)))
            restart_text = restart_font.render('Press R to Restart or ESC to Quit', True, GREEN)
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + int(80 * scale_y)))
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
