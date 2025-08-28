# New updated code
import pygame
import sys
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
FOREST_GREEN = (34, 139, 34)
DEEP_BLUE = (44, 62, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)

# Game settings
GRAVITY = 0.8
JUMP_SPEED = -15
PLAYER_SPEED = 5
LEVEL_TIME_LIMITS = {1: 120, 2: 90, 3: 60}


class AnimatedBackground:
    def __init__(self):
        self.clouds = []
        self.stars = []

        # Create stationary clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 60)
            })

        # Create stationary stars
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, 300)
            })

    def update(self):
        # No movement updates needed
        pass

    def draw(self, screen):
        # Draw stationary stars
        for star in self.stars:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 2)

        # Draw stationary clouds
        for cloud in self.clouds:
            pygame.draw.ellipse(screen, (200, 200, 200),
                                (cloud['x'], cloud['y'], cloud['size'], cloud['size'] // 2))


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        self.running = False
        self.animation_frame = 0
        self.projectiles = []

    def update(self, platforms):
        # Handle movement
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Mouse controls
        if mouse_buttons[0]:
            self.running = True
            self.speed = PLAYER_SPEED * 1.8
        else:
            self.running = False
            self.speed = PLAYER_SPEED

        # Keyboard movement with acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = max(self.vel_x - 0.5, -self.speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = min(self.vel_x + 0.5, self.speed)
        else:
            self.vel_x *= 0.8  # Friction

        self.rect.x += self.vel_x

        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vel_x = 0

        # Death by falling
        if self.rect.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.rect.x = 50
            self.rect.y = 500
            self.vel_y = 0
            self.vel_x = 0

        # Update animation
        self.animation_frame += 1

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_SPEED

    def shoot(self):
        # Create a new projectile
        self.projectiles.append({
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'life': 30,
            'hit': False
        })

    def update_projectiles(self):
        # Update projectiles
        for proj in self.projectiles[:]:
            if not proj['hit']:
                proj['x'] += 15
            proj['life'] -= 1
            if proj['life'] <= 0:
                self.projectiles.remove(proj)

    def draw(self, screen, camera_offset=0):
        # Draw projectiles with camera offset
        for proj in self.projectiles:
            pygame.draw.circle(screen, (0, 191, 255), 
                             (int(proj['x'] + camera_offset), int(proj['y'])), 6)

        # Draw Blippo with correct camera offset
        x = self.rect.x + camera_offset
        bounce = math.sin(self.animation_frame * 0.3) * 2 if self.running else 0
        color = ORANGE if self.running else YELLOW

        body_rect = pygame.Rect(x, self.rect.y + bounce, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, color, body_rect, border_radius=10)

        # Simple eyes
        pygame.draw.circle(screen, BLACK, (x + 10, self.rect.y + 15 + bounce), 5)
        pygame.draw.circle(screen, BLACK, (x + 30, self.rect.y + 15 + bounce), 5)

        # Simple smile
        pygame.draw.arc(screen, BLACK, (x + 8, self.rect.y + 25 + bounce, 24, 15), 0, 3.14, 3)


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=2, direction=1, range_limit=150):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.original_x = x
        self.speed = speed
        self.direction = direction
        self.range_limit = range_limit
        self.color = FOREST_GREEN

    def update(self):
        # Check if we're about to exceed the range limit
        new_x = self.rect.x + (self.speed * self.direction)
        
        if abs(new_x - self.original_x) > self.range_limit:
            # Reverse direction before moving
            self.direction *= -1
            # Clamp position to stay within range
            if new_x > self.original_x + self.range_limit:
                self.rect.x = self.original_x + self.range_limit
            elif new_x < self.original_x - self.range_limit:
                self.rect.x = self.original_x - self.range_limit
        else:
            # Safe to move
            self.rect.x = new_x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)


class Platform:
    def __init__(self, x, y, width, height, color=FOREST_GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)


class MovingObstacle:
    def __init__(self, x, y, width, height, obstacle_type="patrol", speed=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = obstacle_type
        self.speed = speed
        self.direction = 1
        self.original_x = x

    def update(self):
        if self.type == "patrol":
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.original_x) > 200:
                self.direction *= -1

    def draw(self, screen):
        if self.type == "patrol":
            # Simple red enemy
            pygame.draw.rect(screen, RED, self.rect, border_radius=5)
            # Simple eyes
            pygame.draw.circle(screen, BLACK, (self.rect.x + 10, self.rect.y + 10), 4)
            pygame.draw.circle(screen, BLACK, (self.rect.x + 25, self.rect.y + 10), 4)
        elif self.type == "floating":
            # Floating spikes
            points = [
                (self.rect.x, self.rect.bottom),
                (self.rect.x + self.rect.width // 2, self.rect.y),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(screen, DARK_RED, points)


class LordZing:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 100)
        self.original_x = x
        self.original_y = y
        self.animation_frame = 0
        self.movement_range = 100
        self.defeated = False
        self.health = 3

    def update(self):
        if not self.defeated:
            self.animation_frame += 1
            # Simple movement pattern
            self.rect.x = self.original_x + math.sin(self.animation_frame * 0.05) * self.movement_range
            self.rect.y = self.original_y + math.sin(self.animation_frame * 0.03) * 30

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.defeated = True

    def draw(self, screen):
        if not self.defeated:
            # Draw Lord Zing body
            pygame.draw.rect(screen, PURPLE, self.rect, border_radius=10)
            # Simple eyes
            pygame.draw.circle(screen, RED, (self.rect.x + 20, self.rect.y + 25), 8)
            pygame.draw.circle(screen, RED, (self.rect.x + 60, self.rect.y + 25), 8)
            # Health indicator
            for i in range(self.health):
                pygame.draw.circle(screen, RED, (self.rect.x + 10 + i * 20, self.rect.y - 20), 8)


class Friend:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 55)
        self.animation_frame = 0
        self.rescued = False
        self.cage_bars = []

        # Create cage bars
        for i in range(6):
            self.cage_bars.append(pygame.Rect(x - 20 + i * 15, y - 20, 5, 95))

    def update(self):
        self.animation_frame += 1
        # Simple struggling animation when not rescued
        if not self.rescued:
            struggle = math.sin(self.animation_frame * 0.2) * 3
            self.rect.x += struggle

    def rescue(self):
        self.rescued = True
        self.cage_bars.clear()

    def draw(self, screen):
        # Draw cage if not rescued
        if not self.rescued:
            for bar in self.cage_bars:
                pygame.draw.rect(screen, GRAY, bar)

        # Draw friend
        color = LIGHT_BLUE if not self.rescued else (0, 255, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Eyes
        if not self.rescued:
            # Worried eyes
            pygame.draw.ellipse(screen, BLACK, (self.rect.x + 8, self.rect.y + 12, 8, 12))
            pygame.draw.ellipse(screen, BLACK, (self.rect.x + 22, self.rect.y + 12, 8, 12))
        else:
            # Happy eyes
            pygame.draw.circle(screen, BLACK, (self.rect.x + 10, self.rect.y + 15), 4)
            pygame.draw.circle(screen, BLACK, (self.rect.x + 25, self.rect.y + 15), 4)
            # Happy smile
            pygame.draw.arc(screen, BLACK, (self.rect.x + 5, self.rect.y + 25, 25, 20), 0, 3.14, 3)


class PowerUp:
    def __init__(self, x, y, power_type="speed"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = power_type
        self.collected = False

    def update(self):
        pass

    def draw(self, screen):
        if not self.collected:
            if self.type == "speed":
                color = (0, 255, 255)
            elif self.type == "jump":
                color = (255, 255, 0)
            elif self.type == "attack":
                color = (255, 0, 0)

            pygame.draw.rect(screen, color, self.rect, border_radius=15)


class Collectible:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.collected = False

    def update(self):
        pass

    def draw(self, screen):
        if not self.collected:
            # Simple coin
            pygame.draw.ellipse(screen, YELLOW, self.rect)
            pygame.draw.ellipse(screen, BLACK, self.rect, 2)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Turbo Runners")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.state = "menu"
        self.current_level = 1
        self.start_time = 0
        self.game_stats = {"deaths": 0, "coins_collected": 0, "time_taken": 0}

        self.background = AnimatedBackground()
        self.camera_offset = 0
        self.screen_shake = 0

        self.reset_game()

    def reset_game(self):
        self.player = Player(50, 500)
        self.platforms = []
        self.moving_platforms = []
        self.obstacles = []
        self.collectibles = []
        self.power_ups = []
        self.lord_zing = None
        self.friend = None
        self.level_complete = False
        self.start_time = time.time()
        self.camera_offset = 0
        self.create_level(self.current_level)

    def create_level(self, level):
        self.platforms.clear()
        self.moving_platforms.clear()
        self.obstacles.clear()
        self.collectibles.clear()
        self.power_ups.clear()

        # Ground platform
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        if level == 1:  # Easy
            # Static platforms
            self.platforms.extend([
                Platform(200, 550, 150, 20),
                Platform(450, 450, 150, 20),
                Platform(700, 350, 150, 20)
            ])

            # Moving platforms
            self.moving_platforms.extend([
                MovingPlatform(350, 500, 100, 20, speed=1, range_limit=100),
                MovingPlatform(600, 300, 100, 20, speed=1.5, range_limit=80)
            ])

            # Moving obstacles
            self.obstacles.extend([
                MovingObstacle(300, 610, 35, 35, "patrol", speed=1),
                MovingObstacle(500, 400, 30, 30, "floating")
            ])

            # Collectibles
            for i in range(6):
                collectible = Collectible(250 + i * 150, 400 - i * 30)
                self.collectibles.append(collectible)

            # Power-ups
            self.power_ups.append(PowerUp(400, 400, "speed"))

            # Lord Zing and Friend at the end
            self.lord_zing = LordZing(950, 200)
            self.friend = Friend(1000, 250)

        elif level == 2:  # Medium
            self.platforms.extend([
                Platform(150, 580, 100, 20),
                Platform(350, 480, 80, 20),
                Platform(550, 380, 80, 20),
                Platform(750, 280, 80, 20),
                Platform(950, 180, 100, 20)
            ])

            self.moving_platforms.extend([
                MovingPlatform(250, 530, 80, 20, speed=2, range_limit=120),
                MovingPlatform(450, 430, 80, 20, speed=1.5, range_limit=100),
                MovingPlatform(650, 330, 80, 20, speed=2.5, range_limit=90),
                MovingPlatform(850, 230, 80, 20, speed=1.8, range_limit=110)
            ])

            self.obstacles.extend([
                MovingObstacle(200, 610, 35, 35, "patrol", speed=2),
                MovingObstacle(400, 610, 35, 35, "patrol", speed=1.5),
                MovingObstacle(500, 340, 30, 30, "floating"),
                MovingObstacle(700, 240, 30, 30, "floating"),
                MovingObstacle(800, 610, 35, 35, "patrol", speed=2.5)
            ])

            for i in range(8):
                collectible = Collectible(200 + i * 120, 450 - i * 25)
                self.collectibles.append(collectible)

            self.power_ups.extend([
                PowerUp(300, 450, "jump"),
                PowerUp(600, 320, "speed"),
                PowerUp(800, 220, "attack")
            ])

            self.lord_zing = LordZing(1000, 100)
            self.friend = Friend(1050, 150)

        elif level == 3:  # Hard
            self.platforms.extend([
                Platform(100, 600, 60, 15),
                Platform(250, 520, 50, 15),
                Platform(400, 440, 50, 15),
                Platform(550, 360, 50, 15),
                Platform(700, 280, 50, 15),
                Platform(850, 200, 50, 15),
                Platform(1000, 120, 80, 15)
            ])

            self.moving_platforms.extend([
                MovingPlatform(180, 570, 60, 15, speed=3, range_limit=80),
                MovingPlatform(320, 490, 60, 15, speed=2.5, range_limit=100),
                MovingPlatform(470, 410, 60, 15, speed=3.5, range_limit=70),
                MovingPlatform(620, 330, 60, 15, speed=3, range_limit=90),
                MovingPlatform(770, 250, 60, 15, speed=2.8, range_limit=85),
                MovingPlatform(920, 170, 60, 15, speed=3.2, range_limit=75)
            ])

            self.obstacles.extend([
                MovingObstacle(150, 610, 35, 35, "patrol", speed=3),
                MovingObstacle(300, 610, 35, 35, "patrol", speed=2.5),
                MovingObstacle(450, 610, 35, 35, "patrol", speed=3.5),
                MovingObstacle(350, 450, 30, 30, "floating"),
                MovingObstacle(500, 370, 30, 30, "floating"),
                MovingObstacle(650, 290, 30, 30, "floating"),
                MovingObstacle(800, 210, 30, 30, "floating"),
                MovingObstacle(600, 610, 35, 35, "patrol", speed=4),
                MovingObstacle(750, 610, 35, 35, "patrol", speed=3.2)
            ])

            for i in range(12):
                collectible = Collectible(150 + i * 80, 500 - i * 20)
                self.collectibles.append(collectible)

            self.power_ups.extend([
                PowerUp(200, 480, "jump"),
                PowerUp(400, 380, "speed"),
                PowerUp(600, 280, "attack"),
                PowerUp(800, 180, "jump")
            ])

            self.lord_zing = LordZing(1050, 80)
            self.friend = Friend(1100, 90)

    def update_camera(self):
        # Follow player with smooth camera
        target_offset = -self.player.rect.x + SCREEN_WIDTH // 3
        self.camera_offset += (target_offset - self.camera_offset) * 0.1

        # Add screen shake
        if self.screen_shake > 0:
            self.camera_offset += random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "game":
                        self.player.jump()
                    elif self.state == "menu":
                        self.state = "level_select"
                elif event.key == pygame.K_r and self.state == "game_over":
                    self.restart_level()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                if event.key == pygame.K_RETURN:
                    if self.state == "game":
                        self.player.shoot()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "game":
                    if event.button == 1:
                        self.player.jump()

                    # Attack Lord Zing if close enough
                    if (event.button == 1 and self.lord_zing and
                            abs(self.player.rect.centerx - self.lord_zing.rect.centerx) < 100):
                        self.lord_zing.take_damage()
                        self.screen_shake = 10
                        if self.lord_zing.defeated:
                            self.friend.rescue()

                # Menu interactions
                if self.state == "menu":
                    title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 100, 400, 80)
                    if title_rect.collidepoint(event.pos):
                        self.state = "level_select"

                elif self.state == "level_select":
                    for i in range(3):
                        level_button = pygame.Rect(400 + i * 120, 300, 100, 60)
                        if level_button.collidepoint(event.pos):
                            self.current_level = i + 1
                            self.reset_game()
                            self.state = "game"

                elif self.state in ["game_over", "victory"]:
                    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)
                    menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 480, 200, 60)

                    if restart_button.collidepoint(event.pos):
                        self.restart_level()
                    elif menu_button.collidepoint(event.pos):
                        self.state = "menu"

        return True

    def restart_level(self):
        self.game_stats["deaths"] += 1
        self.reset_game()
        self.state = "game"

    def update(self):
        if self.state == "game":
            self.background.update()
            self.update_camera()

            # Update all game objects
            self.player.update(self.platforms + self.moving_platforms)

            for platform in self.moving_platforms:
                platform.update()

            for obstacle in self.obstacles:
                obstacle.update()

            for collectible in self.collectibles:
                collectible.update()

            for power_up in self.power_ups:
                power_up.update()

            if self.lord_zing:
                self.lord_zing.update()

            if self.friend:
                self.friend.update()

            # Update projectiles
            self.player.update_projectiles()

            # Check obstacle collisions
            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    self.player.lives -= 1
                    self.screen_shake = 15
                    if self.player.lives <= 0:
                        self.state = "game_over"
                        self.game_stats["time_taken"] = time.time() - self.start_time
                    else:
                        # Reset player position
                        self.player.rect.x = 50
                        self.player.rect.y = 500
                        self.player.vel_y = 0
                        self.player.vel_x = 0

            # Check collectible collisions
            for collectible in self.collectibles:
                if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                    collectible.collected = True
                    self.player.score += 100
                    self.game_stats["coins_collected"] += 1

            # Check power-up collisions
            for power_up in self.power_ups:
                if not power_up.collected and self.player.rect.colliderect(power_up.rect):
                    power_up.collected = True
                    self.player.score += 200
                    # Apply power-up effect temporarily
                    if power_up.type == "speed":
                        self.player.speed = PLAYER_SPEED * 2
                    elif power_up.type == "jump":
                        self.player.jump()

            # Check if friend is rescued (level completion)
            if self.friend and self.friend.rescued:
                if self.current_level < 3:
                    self.current_level += 1
                    self.reset_game()
                else:
                    self.state = "victory"
                    self.game_stats["time_taken"] = time.time() - self.start_time

            # Check time limit
            elapsed_time = time.time() - self.start_time
            if elapsed_time > LEVEL_TIME_LIMITS[self.current_level]:
                self.player.lives = 0
                self.state = "game_over"
                self.game_stats["time_taken"] = elapsed_time

            # Check projectile hits on Lord Zing
            if self.lord_zing and not self.lord_zing.defeated:
                for proj in self.player.projectiles[:]:
                    if abs(proj['x'] - (self.lord_zing.rect.x + self.camera_offset)) < 50:
                        self.lord_zing.take_damage()
                        proj['hit'] = True
                        self.screen_shake = 10
                        if self.lord_zing.defeated:
                            self.friend.rescue()

    def draw_menu(self):
        # Simple gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DEEP_BLUE[0] * (1 - color_ratio) + FOREST_GREEN[0] * color_ratio)
            g = int(DEEP_BLUE[1] * (1 - color_ratio) + FOREST_GREEN[1] * color_ratio)
            b = int(DEEP_BLUE[2] * (1 - color_ratio) + FOREST_GREEN[2] * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        self.background.draw(self.screen)

        # Title
        title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 100, 400, 80)
        pygame.draw.rect(self.screen, FOREST_GREEN, title_rect, border_radius=10)

        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("TURBO RUNNERS", True, WHITE)
        title_text_rect = title_text.get_rect(center=title_rect.center)
        self.screen.blit(title_text, title_text_rect)

        # Subtitle
        subtitle = "Blippo's Epic Adventure"
        subtitle_text = self.small_font.render(subtitle, True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Instructions
        instructions = [
            "Help Blippo save his friend from the evil Lord Zing!",
            "Click the title or press SPACE to start",
            "Hold LEFT MOUSE to run faster",
            "Click or SPACE to jump",
            "Defeat Lord Zing to rescue your friend!"
        ]

        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280 + i * 40))
            self.screen.blit(text, text_rect)

    def draw_level_select(self):
        # Simple background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DEEP_BLUE[0] * (1 - color_ratio) + FOREST_GREEN[0] * color_ratio)
            g = int(DEEP_BLUE[1] * (1 - color_ratio) + FOREST_GREEN[1] * color_ratio)
            b = int(DEEP_BLUE[2] * (1 - color_ratio) + FOREST_GREEN[2] * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Title
        title_text = self.font.render("SELECT LEVEL", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Level buttons
        level_names = ["EASY", "MEDIUM", "HARD"]
        level_times = ["120s", "90s", "60s"]

        for i in range(3):
            x = 400 + i * 120
            y = 300

            button_rect = pygame.Rect(x, y, 100, 60)
            pygame.draw.rect(self.screen, GRAY, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3, border_radius=10)

            # Level number
            level_text = self.font.render(str(i + 1), True, WHITE)
            level_rect = level_text.get_rect(center=(x + 50, y + 20))
            self.screen.blit(level_text, level_rect)

            # Difficulty
            diff_text = self.small_font.render(level_names[i], True, WHITE)
            diff_rect = diff_text.get_rect(center=(x + 50, y + 45))
            self.screen.blit(diff_text, diff_rect)

            # Time limit
            time_text = self.small_font.render(level_times[i], True, YELLOW)
            time_rect = time_text.get_rect(center=(x + 50, y + 80))
            self.screen.blit(time_text, time_rect)

    def draw_game(self):
        # Simple sky background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DEEP_BLUE[0] * (1 - color_ratio) + FOREST_GREEN[0] * color_ratio * 0.3)
            g = int(DEEP_BLUE[1] * (1 - color_ratio) + FOREST_GREEN[1] * color_ratio * 0.3)
            b = int(DEEP_BLUE[2] * (1 - color_ratio) + FOREST_GREEN[2] * color_ratio * 0.3)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        self.background.draw(self.screen)

        # Apply camera offset to all drawn objects
        camera_x = int(self.camera_offset)

        # Draw platforms
        for platform in self.platforms:
            draw_rect = pygame.Rect(platform.rect.x + camera_x, platform.rect.y,
                                    platform.rect.width, platform.rect.height)
            pygame.draw.rect(self.screen, platform.color, draw_rect)
            pygame.draw.rect(self.screen, BLACK, draw_rect, 2)

        # Draw moving platforms
        for platform in self.moving_platforms:
            draw_rect = pygame.Rect(platform.rect.x + camera_x, platform.rect.y,
                                    platform.rect.width, platform.rect.height)
            pygame.draw.rect(self.screen, platform.color, draw_rect)
            pygame.draw.rect(self.screen, BLACK, draw_rect, 2)

        # Draw obstacles
        for obstacle in self.obstacles:
            if obstacle.type == "patrol":
                draw_rect = pygame.Rect(obstacle.rect.x + camera_x, obstacle.rect.y,
                                        obstacle.rect.width, obstacle.rect.height)
                pygame.draw.rect(self.screen, RED, draw_rect, border_radius=5)
                # Simple eyes
                pygame.draw.circle(self.screen, BLACK,
                                   (draw_rect.x + 10, draw_rect.y + 10), 4)
                pygame.draw.circle(self.screen, BLACK,
                                   (draw_rect.x + 25, draw_rect.y + 10), 4)

            elif obstacle.type == "floating":
                points = [
                    (obstacle.rect.x + camera_x, obstacle.rect.bottom),
                    (obstacle.rect.x + camera_x + obstacle.rect.width // 2, obstacle.rect.y),
                    (obstacle.rect.x + camera_x + obstacle.rect.width, obstacle.rect.bottom)
                ]
                pygame.draw.polygon(self.screen, DARK_RED, points)

        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                draw_x = collectible.rect.x + camera_x
                if -50 < draw_x < SCREEN_WIDTH + 50:
                    draw_rect = pygame.Rect(draw_x, collectible.rect.y,
                                          collectible.rect.width, collectible.rect.height)
                    pygame.draw.ellipse(self.screen, YELLOW, draw_rect)
                    pygame.draw.ellipse(self.screen, BLACK, draw_rect, 2)

        # Draw power-ups
        for power_up in self.power_ups:
            if not power_up.collected:
                draw_x = power_up.rect.x + camera_x
                if -50 < draw_x < SCREEN_WIDTH + 50:
                    draw_rect = pygame.Rect(draw_x, power_up.rect.y,
                                            power_up.rect.width, power_up.rect.height)
                    if power_up.type == "speed":
                        color = (0, 255, 255)
                    elif power_up.type == "jump":
                        color = (255, 255, 0)
                    elif power_up.type == "attack":
                        color = (255, 0, 0)
                    pygame.draw.rect(self.screen, color, draw_rect, border_radius=15)

        # Draw Lord Zing
        if self.lord_zing:
            draw_x = self.lord_zing.rect.x + camera_x
            if -100 < draw_x < SCREEN_WIDTH + 100:
                draw_rect = pygame.Rect(draw_x, self.lord_zing.rect.y,
                                        self.lord_zing.rect.width, self.lord_zing.rect.height)

                if not self.lord_zing.defeated:
                    # Lord Zing body
                    pygame.draw.rect(self.screen, PURPLE, draw_rect, border_radius=10)
                    # Simple eyes
                    pygame.draw.circle(self.screen, RED,
                                       (draw_rect.x + 20, draw_rect.y + 25), 8)
                    pygame.draw.circle(self.screen, RED,
                                       (draw_rect.x + 60, draw_rect.y + 25), 8)
                    # Health bars
                    for i in range(self.lord_zing.health):
                        pygame.draw.circle(self.screen, RED,
                                           (draw_rect.x + 10 + i * 20, draw_rect.y - 20), 8)

        # Draw Friend
        if self.friend:
            draw_x = self.friend.rect.x + camera_x
            if -100 < draw_x < SCREEN_WIDTH + 100:
                draw_rect = pygame.Rect(draw_x, self.friend.rect.y,
                                        self.friend.rect.width, self.friend.rect.height)

                # Draw cage if not rescued
                if not self.friend.rescued:
                    for bar in self.friend.cage_bars:
                        bar_rect = pygame.Rect(bar.x + camera_x, bar.y, bar.width, bar.height)
                        pygame.draw.rect(self.screen, GRAY, bar_rect)

                # Draw friend
                color = LIGHT_BLUE if not self.friend.rescued else (0, 255, 0)
                pygame.draw.rect(self.screen, color, draw_rect, border_radius=8)

                # Eyes
                if not self.friend.rescued:
                    pygame.draw.ellipse(self.screen, BLACK,
                                        (draw_rect.x + 8, draw_rect.y + 12, 8, 12))
                    pygame.draw.ellipse(self.screen, BLACK,
                                        (draw_rect.x + 22, draw_rect.y + 12, 8, 12))
                else:
                    pygame.draw.circle(self.screen, BLACK,
                                       (draw_rect.x + 12, draw_rect.y + 15), 4)
                    pygame.draw.circle(self.screen, BLACK,
                                       (draw_rect.x + 23, draw_rect.y + 15), 4)
                    pygame.draw.arc(self.screen, BLACK,
                                    (draw_rect.x + 5, draw_rect.y + 25, 25, 20), 0, 3.14, 3)

        # Draw player with camera offset
        self.player.draw(self.screen, camera_x)

        # Draw UI
        self.draw_ui()

    def draw_ui(self):
        # UI background
        ui_surface = pygame.Surface((300, 140))
        ui_surface.set_alpha(180)
        ui_surface.fill(DEEP_BLUE)
        self.screen.blit(ui_surface, (10, 10))

        # Lives with hearts
        lives_text = self.small_font.render("Lives:", True, WHITE)
        self.screen.blit(lives_text, (20, 20))
        for i in range(self.player.lives):
            heart_x = 80 + i * 25
            pygame.draw.polygon(self.screen, RED, [
                (heart_x, 30), (heart_x + 5, 25), (heart_x + 10, 25),
                (heart_x + 15, 30), (heart_x + 15, 35), (heart_x + 7.5, 42), (heart_x, 35)
            ])

        # Score
        score_text = self.small_font.render(f"Score: {self.player.score}", True, YELLOW)
        self.screen.blit(score_text, (20, 55))

        # Level
        level_text = self.small_font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (20, 90))

        # Timer
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, LEVEL_TIME_LIMITS[self.current_level] - elapsed_time)
        timer_color = RED if remaining_time < 20 else WHITE

        timer_text = self.small_font.render(f"Time: {remaining_time:.1f}s", True, timer_color)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))

        # Controls
        controls = [
            "Hold MOUSE: Run",
            "CLICK/SPACE: Jump", 
            "Press ENTER to Shoot"
        ]

        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, WHITE)
            self.screen.blit(control_surface, (SCREEN_WIDTH - 250, 60 + i * 25))

    def draw_game_over(self):
        # Background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DEEP_BLUE[0] + 20)
            g = int(DEEP_BLUE[1])
            b = int(DEEP_BLUE[2])
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Game Over text
        game_over_text = self.font.render("GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)

        # Stats
        analytics = [
            f"Level Reached: {self.current_level}",
            f"Score: {self.player.score}",
            f"Coins Collected: {self.game_stats['coins_collected']}",
            f"Deaths: {self.game_stats['deaths']}",
            f"Time Played: {self.game_stats['time_taken']:.1f}s"
        ]

        for i, stat in enumerate(analytics):
            stat_text = self.small_font.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            self.screen.blit(stat_text, stat_rect)

        # Buttons
        self.draw_interactive_buttons()

    def draw_victory(self):
        # Background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(FOREST_GREEN[0] + 20)
            g = int(FOREST_GREEN[1] + 20)
            b = int(FOREST_GREEN[2])
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Victory text
        victory_text = self.font.render("VICTORY!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(victory_text, victory_rect)

        # Success message
        success_text = self.small_font.render("Blippo saved his friend from Lord Zing!", True, WHITE)
        success_rect = success_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(success_text, success_rect)

        # Final stats
        analytics = [
            f"Final Score: {self.player.score}",
            f"Total Coins: {self.game_stats['coins_collected']}",
            f"Total Deaths: {self.game_stats['deaths']}",
            f"Total Time: {self.game_stats['time_taken']:.1f}s",
            f"Performance: {'LEGENDARY!' if self.game_stats['deaths'] < 2 else 'EXCELLENT!' if self.game_stats['deaths'] < 5 else 'GOOD EFFORT!'}"
        ]

        for i, stat in enumerate(analytics):
            stat_text = self.small_font.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            self.screen.blit(stat_text, stat_rect)

        # Buttons
        self.draw_interactive_buttons()

    def draw_interactive_buttons(self):
        # Restart button
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)
        menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 480, 200, 60)

        pygame.draw.rect(self.screen, FOREST_GREEN, restart_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, restart_button, 3, border_radius=10)

        pygame.draw.rect(self.screen, GRAY, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, menu_button, 3, border_radius=10)

        # Button text
        restart_text = self.small_font.render("RESTART LEVEL", True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_rect)

        menu_text = self.small_font.render("MAIN MENU", True, WHITE)
        menu_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_rect)

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            self.update()

            # Draw based on game state
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "level_select":
                self.draw_level_select()
            elif self.state == "game":
                self.draw_game()
            elif self.state == "game_over":
                self.draw_game_over()
            elif self.state == "victory":
                self.draw_victory()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()