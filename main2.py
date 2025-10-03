# Turbo Runners - Development Version with MAJOR Issues
# ============================================================
# WARNING: This version has severe bugs and incomplete features
# DO NOT SHIP THIS VERSION!!!
# ============================================================
#
# DEVELOPMENT LOG:
# Day 1: Started basic player movement - physics feel wrong
# Day 2: Added platforms - collision detection has gaps
# Day 3: Tried to fix collision - made it worse, players fall through
# Day 4: Added moving platforms - they don't carry the player properly
# Day 5: Camera implementation - causes motion sickness, needs complete rewrite
# Day 6: Added enemies - movement stutters, hit detection too sensitive
# Day 7: Attempted Level 2 - completely unbalanced, nearly impossible
# Day 8: Boss fight - projectiles don't hit properly, camera offset issues
# Day 9: Power-ups - effects are permanent instead of temporary (broken)
# Day 10: Performance optimization - failed, still getting lag spikes
# Day 11: Attempted Level 3 - gave up, not implemented
# Day 12: Trying to fix jump mechanics - unreliable, works half the time
# Day 13: Nothing works, considering starting over...
#
# CRITICAL BUGS TO FIX:
# TODO: Fix collision detection - completely broken
# TODO: Fix platform movement - players falling through constantly  
# TODO: Fix camera - causes motion sickness, jitters randomly
# TODO: Fix jump - only works half the time due to on_ground issues
# TODO: Fix boss fight - projectile hit detection doesn't work
# TODO: Fix power-ups - effects should be temporary not permanent
# TODO: Implement Level 3 - currently just prints error message
# TODO: Add invincibility frames after damage
# TODO: Fix enemy speed and hit detection
# TODO: Optimize performance - random FPS drops
# FIXME: Game crashes randomly
# FIXME: Performance is terrible
# FIXME: Too many debug print statements left in code
# FIXME: Level 2 is unplayable
# FIXME: Player speed gets permanently boosted
# FIXME: Screen shake way too intense
#
# Features that were attempted and failed:
# - Particle system (too slow)
# - Sound effects (incomplete)
# - Music (not implemented)
# - Save system (gave up on JSON implementation)
# - Procedural level generation (unplayable)
# - Proper player-platform physics (still broken)
#
# Code quality issues:
# - Lots of commented out debug prints
# - Failed code experiments left in comments
# - Magic numbers everywhere
# - No proper state management
# - Collision detection is a mess
# - No optimization or profiling done
#
# ============================================================

import pygame
import sys
import random
import time
import math
# FIXME: Missing import for collections module - causing issues with some features
# import json  # Was trying to use this for save system - gave up

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
# BUG: Missing GREEN color definition - used later in code

# Game settings
# BUG: Gravity feels wrong, tried multiple values
GRAVITY = 1.2  # Was 0.8, changed to 1.2, now too strong
# GRAVITY = 0.5  # Too floaty
# GRAVITY = 2.0  # Way too fast - players complained
JUMP_SPEED = -12  # BUG: Was -15, changed but now can't reach platforms
PLAYER_SPEED = 5
# TODO: Add level time limits - currently hardcoded
LEVEL_TIME_LIMITS = {1: 120, 2: 90}  # BUG: Missing level 3 time limit
# FIXME: Sometimes timer goes negative???


class AnimatedBackground:
    """Background with animated clouds and stars"""
    def __init__(self):
        self.clouds = []
        self.stars = []
        
        # Create clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 60),
                'speed': random.uniform(0.2, 0.5)  # BUG: Speed not used properly
            })
        
        # Create stars
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, 300)
                # BUG: Missing 'twinkle' property
            })
    
    def update(self):
        # TODO: Implement cloud movement
        # Currently clouds are stationary - need to add scrolling
        pass
    
    def draw(self, screen):
        # Draw stars
        for star in self.stars:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 2)
        
        # Draw clouds
        for cloud in self.clouds:
            # BUG: Cloud color should vary
            pygame.draw.ellipse(screen, (200, 200, 200),
                                (cloud['x'], cloud['y'], cloud['size'], cloud['size'] // 2))


class Player:
    """Main player character - Blippo"""
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
        # BUG: Missing invincibility timer for damage
        
    def update(self, platforms):
        """Update player position and state"""
        # CRITICAL BUG: Sometimes platforms is None - causes crash
        # print(f"DEBUG: platforms count: {len(platforms)}")  # Debug spam
        
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Mouse controls for running
        if mouse_buttons[0]:
            self.running = True
            # BUG: Speed multiplier way too high now
            self.speed = PLAYER_SPEED * 3.5  # Tried 2.5, 3.0, now 3.5 - too fast!
        else:
            self.running = False
            self.speed = PLAYER_SPEED
        
        # Keyboard movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # BUG: Acceleration too aggressive
            self.vel_x = max(self.vel_x - 1.2, -self.speed)  # Should be 0.5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = min(self.vel_x + 1.2, self.speed)
        else:
            # FIXME: Friction barely works - slides forever
            self.vel_x *= 0.98  # Tried 0.95, 0.97, 0.98 - still wrong
        
        self.rect.x += self.vel_x
        
        # Apply gravity
        # BUG: Gravity applied twice somehow???
        self.vel_y += GRAVITY
        # self.vel_y += GRAVITY * 0.5  # Tried to fix, made it worse
        self.rect.y += self.vel_y
        
        # Platform collision - COMPLETELY BROKEN
        self.on_ground = False
        collision_count = 0  # Debug variable
        for platform in platforms:
            # BUG: Collision detection has gaps
            # Tried multiple approaches, none work perfectly
            if self.rect.colliderect(platform.rect):
                collision_count += 1
                # BUG: Only checking falling, player phases through from sides
                if self.vel_y > 0:
                    # FIXME: Position correction causes jitter
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # TODO: Add side collision
                # TODO: Add top collision (bonk head)
        
        # print(f"Collisions: {collision_count}")  # More debug spam
        
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
            # BUG: Respawn position might be inside obstacle
            self.rect.x = 50
            self.rect.y = 500
            self.vel_y = 0
            self.vel_x = 0
        
        # Update animation
        self.animation_frame += 1
    
    def jump(self):
        """Make player jump"""
        # BUG: Jump doesn't work half the time
        # on_ground flag not reliable due to collision issues
        # if self.on_ground:  # Original code
        # Tried removing check - now can infinite jump
        if self.on_ground or self.vel_y < 5:  # Hacky fix attempt - made it worse
            self.vel_y = JUMP_SPEED
            # self.vel_y = JUMP_SPEED * 1.2  # Tried to compensate for weak jump
            # TODO: Add jump sound effect
            # TODO: Add coyote time
            # TODO: Add jump buffering
        # print(f"Jump attempt: on_ground={self.on_ground}, vel_y={self.vel_y}")  # Debug
    
    def shoot(self):
        """Create projectile"""
        # BUG: No cooldown on shooting - can spam
        self.projectiles.append({
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'life': 30,
            'hit': False
        })
    
    def update_projectiles(self):
        """Update all projectiles"""
        for proj in self.projectiles[:]:
            if not proj['hit']:
                proj['x'] += 15
            proj['life'] -= 1
            if proj['life'] <= 0:
                self.projectiles.remove(proj)
    
    def draw(self, screen, camera_offset=0):
        """Draw player and projectiles"""
        # Draw projectiles
        for proj in self.projectiles:
            pygame.draw.circle(screen, (0, 191, 255), 
                             (int(proj['x'] + camera_offset), int(proj['y'])), 6)
        
        # Draw Blippo
        x = self.rect.x + camera_offset
        # BUG: Animation bounce calculation incorrect
        bounce = math.sin(self.animation_frame * 0.5) * 3 if self.running else 0  # Should be 0.3 and 2
        color = ORANGE if self.running else YELLOW
        
        body_rect = pygame.Rect(x, self.rect.y + bounce, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, color, body_rect, border_radius=10)
        
        # Eyes
        pygame.draw.circle(screen, BLACK, (x + 10, self.rect.y + 15 + bounce), 5)
        pygame.draw.circle(screen, BLACK, (x + 30, self.rect.y + 15 + bounce), 5)
        
        # Smile
        pygame.draw.arc(screen, BLACK, (x + 8, self.rect.y + 25 + bounce, 24, 15), 0, 3.14, 3)


class MovingPlatform(pygame.sprite.Sprite):
    """Platform that moves back and forth"""
    def __init__(self, x, y, width, height, speed=2, direction=1, range_limit=150):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.original_x = x
        self.original_y = y  # Added but not used properly
        self.speed = speed
        self.direction = direction
        self.range_limit = range_limit
        self.color = FOREST_GREEN
        # BUG: Movement feels jerky and unpredictable
        self.move_timer = 0  # Tried to add timing - made it worse
    
    def update(self):
        """Update platform position"""
        # CRITICAL: Players fall through moving platforms constantly
        # Tried fixing for hours, still broken
        
        self.move_timer += 1
        
        # BUG: Speed calculation is wrong
        # actual_speed = self.speed * 1.5  # Tried to make it faster
        actual_speed = self.speed * random.uniform(0.8, 1.2)  # WHY DID I ADD RANDOM?!
        
        new_x = self.rect.x + (actual_speed * self.direction)
        
        # BUG: Range check completely broken
        if abs(new_x - self.original_x) >= self.range_limit:
            self.direction *= -1
            # FIXME: Clamping causes platform to "teleport" sometimes
            if new_x > self.original_x + self.range_limit:
                self.rect.x = self.original_x + self.range_limit
            elif new_x < self.original_x - self.range_limit:
                self.rect.x = self.original_x - self.range_limit
            # BUG: Forgot to update new_x after clamping
        else:
            self.rect.x = new_x
        
        # Failed attempt to carry player with platform
        # TODO: Make player move with platform
        # Tried: player.rect.x += self.speed * self.direction  - didn't work
        # Tried: storing last_x and calculating delta - also failed
    
    def draw(self, screen):
        """Draw the platform"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)


class Platform:
    """Static platform"""
    def __init__(self, x, y, width, height, color=FOREST_GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)


class MovingObstacle:
    """Moving enemy obstacle"""
    def __init__(self, x, y, width, height, obstacle_type="patrol", speed=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = obstacle_type
        # BUG: Speed way too fast now
        self.speed = speed * 2  # Doubled it to make game "harder" - now unfair
        self.direction = 1
        self.original_x = x
        self.original_y = y
        # TODO: Add patrol boundaries
        self.frame_count = 0
        # BUG: Hit detection too large
        self.hit_padding = 10  # Makes enemies hit from further away
    
    def update(self):
        """Update obstacle movement"""
        self.frame_count += 1
        
        if self.type == "patrol":
            # BUG: Movement stutters every few frames
            if self.frame_count % 3 == 0:  # Why did I add this?
                self.rect.x += self.speed * self.direction
            
            # BUG: Patrol range hardcoded, too large now
            if abs(self.rect.x - self.original_x) > 300:  # Was 200
                self.direction *= -1
                # Sometimes enemies just disappear off screen
        
        elif self.type == "floating":
            # TODO: Implement floating movement
            # Attempted implementation - doesn't work
            # self.rect.y = self.original_y + math.sin(self.frame_count * 0.1) * 50
            pass  # Gave up
    
    def draw(self, screen):
        """Draw the obstacle"""
        if self.type == "patrol":
            pygame.draw.rect(screen, RED, self.rect, border_radius=5)
            # Eyes
            pygame.draw.circle(screen, BLACK, (self.rect.x + 10, self.rect.y + 10), 4)
            pygame.draw.circle(screen, BLACK, (self.rect.x + 25, self.rect.y + 10), 4)
        elif self.type == "floating":
            # BUG: Spike drawing incomplete
            points = [
                (self.rect.x, self.rect.bottom),
                (self.rect.x + self.rect.width // 2, self.rect.y),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(screen, DARK_RED, points)


class LordZing:
    """Final boss enemy"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 100)
        self.original_x = x
        self.original_y = y
        self.animation_frame = 0
        self.movement_range = 100
        self.defeated = False
        # BUG: Health should vary by level
        self.health = 3
    
    def update(self):
        """Update boss movement and animation"""
        if not self.defeated:
            self.animation_frame += 1
            # Movement pattern
            self.rect.x = self.original_x + math.sin(self.animation_frame * 0.05) * self.movement_range
            self.rect.y = self.original_y + math.sin(self.animation_frame * 0.03) * 30
    
    def take_damage(self):
        """Reduce boss health"""
        self.health -= 1
        if self.health <= 0:
            self.defeated = True
        # TODO: Add damage animation/feedback
    
    def draw(self, screen):
        """Draw the boss"""
        if not self.defeated:
            pygame.draw.rect(screen, PURPLE, self.rect, border_radius=10)
            # Eyes
            pygame.draw.circle(screen, RED, (self.rect.x + 20, self.rect.y + 25), 8)
            pygame.draw.circle(screen, RED, (self.rect.x + 60, self.rect.y + 25), 8)
            # Health indicator
            for i in range(self.health):
                pygame.draw.circle(screen, RED, (self.rect.x + 10 + i * 20, self.rect.y - 20), 8)


class Friend:
    """Friend character to rescue"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 55)
        self.animation_frame = 0
        self.rescued = False
        self.cage_bars = []
        
        # Create cage
        for i in range(6):
            self.cage_bars.append(pygame.Rect(x - 20 + i * 15, y - 20, 5, 95))
    
    def update(self):
        """Update friend animation"""
        self.animation_frame += 1
        # BUG: Struggle animation offset not reset
        if not self.rescued:
            struggle = math.sin(self.animation_frame * 0.2) * 3
            self.rect.x += struggle  # Should store original position
    
    def rescue(self):
        """Rescue the friend"""
        self.rescued = True
        self.cage_bars.clear()
        # TODO: Add rescue animation/celebration
    
    def draw(self, screen):
        """Draw the friend and cage"""
        # Draw cage if not rescued
        if not self.rescued:
            for bar in self.cage_bars:
                pygame.draw.rect(screen, GRAY, bar)
        
        # Draw friend
        color = LIGHT_BLUE if not self.rescued else (0, 255, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        # Eyes
        if not self.rescued:
            pygame.draw.ellipse(screen, BLACK, (self.rect.x + 8, self.rect.y + 12, 8, 12))
            pygame.draw.ellipse(screen, BLACK, (self.rect.x + 22, self.rect.y + 12, 8, 12))
        else:
            pygame.draw.circle(screen, BLACK, (self.rect.x + 10, self.rect.y + 15), 4)
            pygame.draw.circle(screen, BLACK, (self.rect.x + 25, self.rect.y + 15), 4)
            pygame.draw.arc(screen, BLACK, (self.rect.x + 5, self.rect.y + 25, 25, 20), 0, 3.14, 3)


class PowerUp:
    """Power-up collectible"""
    def __init__(self, x, y, power_type="speed"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = power_type
        self.collected = False
        # BUG: No duration tracking
    
    def update(self):
        # TODO: Add floating animation
        pass
    
    def draw(self, screen):
        """Draw power-up"""
        if not self.collected:
            # BUG: Missing color mapping for some types
            if self.type == "speed":
                color = (0, 255, 255)
            elif self.type == "jump":
                color = (255, 255, 0)
            else:  # attack - missing check
                color = (255, 0, 0)
            
            pygame.draw.rect(screen, color, self.rect, border_radius=15)


class Collectible:
    """Coin collectible"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.collected = False
    
    def update(self):
        # TODO: Add spinning animation
        pass
    
    def draw(self, screen):
        """Draw coin"""
        if not self.collected:
            pygame.draw.ellipse(screen, YELLOW, self.rect)
            pygame.draw.ellipse(screen, BLACK, self.rect, 2)


class Game:
    """Main game class"""
    # CRITICAL ISSUES:
    # - Collision detection broken
    # - Moving platforms don't carry player
    # - Camera causes motion sickness
    # - Level 2 is nearly impossible
    # - Level 3 not implemented
    # - Performance issues and lag spikes
    # - No proper error handling
    # - Boss fight is broken
    # - Power-ups have permanent effects
    # - Enemy hit detection too sensitive
    # - Jump mechanics unreliable
    # - Physics feel wrong
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Turbo Runners - DEV BUILD")  # Mark as dev
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.state = "menu"
        self.current_level = 1
        self.start_time = 0
        # BUG: Missing some game stats
        self.game_stats = {"deaths": 0, "coins_collected": 0}
        # self.game_stats["time_taken"] = 0  # Should add this
        
        self.background = AnimatedBackground()
        self.camera_offset = 0
        self.screen_shake = 0
        
        # Failed feature attempts
        # self.particles = []  # Tried to add particle system - too slow
        # self.sound_effects = {}  # Tried to add sounds - didn't finish
        # self.music_player = None  # Music not implemented
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game state for new game"""
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
        """Create level layout"""
        # FIXME: Level generation is messy and hardcoded
        # TODO: Load levels from JSON files
        # TODO: Add level editor
        
        print(f"Creating level {level}...")  # Debug print left in
        
        self.platforms.clear()
        self.moving_platforms.clear()
        self.obstacles.clear()
        self.collectibles.clear()
        self.power_ups.clear()
        
        # Ground platform
        # BUG: Ground platform too narrow for wide screens
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Failed attempts at procedural generation
        # def generate_platforms_procedural():
        #     # Tried to generate platforms automatically - gave up
        #     pass
        # 
        # def random_level():
        #     # Tried random level generation - was unplayable
        #     for i in range(10):
        #         x = random.randint(100, SCREEN_WIDTH - 100)
        #         y = random.randint(200, SCREEN_HEIGHT - 100)
        #         self.platforms.append(Platform(x, y, 100, 20))
        # random_level()  # Don't use this!
        
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
            
            # Obstacles
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
            
            # Boss and friend
            self.lord_zing = LordZing(950, 200)
            self.friend = Friend(1000, 250)
        
        elif level == 2:  # Medium - EXTREMELY BROKEN
            # BUG: Level 2 is nearly impossible to complete
            # Platforms are too far apart after "balancing"
            self.platforms.extend([
                Platform(150, 580, 100, 20),
                Platform(350, 480, 80, 20),
                Platform(550, 380, 80, 20),
                # BUG: Missing critical platforms - huge gaps
                # Platform(750, 280, 80, 20),  # Commented out by accident
            ])
            
            # Moving platforms move too fast and unpredictably
            self.moving_platforms.extend([
                MovingPlatform(250, 530, 80, 20, speed=3, range_limit=200),  # Too fast!
                MovingPlatform(450, 430, 80, 20, speed=2.5, range_limit=150),  # Also too fast!
            ])
            
            # BUG: Way too many enemies
            self.obstacles.extend([
                MovingObstacle(200, 610, 35, 35, "patrol", speed=2),
                MovingObstacle(400, 610, 35, 35, "patrol", speed=1.5),
                MovingObstacle(300, 610, 35, 35, "patrol", speed=2.5),  # Extra enemy
                MovingObstacle(500, 610, 35, 35, "patrol", speed=3),  # Another extra
            ])
            
            # Collectibles in impossible locations
            for i in range(8):
                # BUG: Coins too spread out, can't reach half of them
                collectible = Collectible(200 + i * 150, 450 - i * 40)  # Gaps too big
                self.collectibles.append(collectible)
            
            # Power-ups in bad positions
            self.power_ups.extend([
                PowerUp(300, 450, "jump"),
                PowerUp(600, 320, "speed"),
                # PowerUp(800, 220, "attack"),  # Forgot to add
            ])
            
            # Boss too far, hard to reach
            self.lord_zing = LordZing(1100, 50)  # Moved higher, harder
            self.friend = Friend(1150, 100)
        
        # TODO: Implement level 3 (Hard)
        else:
            # Level 3 not implemented yet
            print("Level 3 not implemented!")
    
    def update_camera(self):
        """Update camera to follow player"""
        # CRITICAL: Camera causes motion sickness
        # Smoothing is completely wrong
        
        target_offset = -self.player.rect.x + SCREEN_WIDTH // 3
        
        # BUG: Camera lerp value way too low
        self.camera_offset += (target_offset - self.camera_offset) * 0.02  # Was 0.05, made even slower
        
        # BUG: Camera jitters randomly
        # Added "stabilization" - made it worse
        if random.random() < 0.1:  # 10% chance each frame - WHY?!
            self.camera_offset += random.randint(-5, 5)
        
        # Screen shake - too intense
        if self.screen_shake > 0:
            # BUG: Shake amount too high
            shake_amount = self.screen_shake * 2  # Doubled for "effect"
            self.camera_offset += random.randint(-shake_amount, shake_amount)
            self.screen_shake -= 1
        
        # TODO: Add camera bounds
        # TODO: Add camera zones
        # TODO: Fix the jitter before release
        
        # print(f"Camera: {self.camera_offset}, Target: {target_offset}")  # Debug spam
    
    def handle_events(self):
        """Handle user input"""
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
                # BUG: Enter key not working for shooting
                # if event.key == pygame.K_RETURN:
                #     if self.state == "game":
                #         self.player.shoot()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "game":
                    if event.button == 1:
                        self.player.jump()
                    
                    # Attack Lord Zing
                    # FIXME: Attack range check incorrect
                    if (event.button == 1 and self.lord_zing and
                            abs(self.player.rect.centerx - self.lord_zing.rect.centerx) < 80):  # Should be 100
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
        """Restart current level"""
        self.game_stats["deaths"] += 1
        self.reset_game()
        self.state = "game"
    
    def update(self):
        """Update game logic"""
        if self.state == "game":
            self.background.update()
            self.update_camera()
            
            # Update game objects
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
            
            # Check obstacle collisions - BROKEN
            for obstacle in self.obstacles:
                # BUG: Hit detection too sensitive with padding
                hit_rect = self.player.rect.inflate(obstacle.hit_padding, obstacle.hit_padding)
                if hit_rect.colliderect(obstacle.rect):
                    # BUG: No invincibility frames - lose all lives instantly
                    self.player.lives -= 1
                    # BUG: Screen shake way too intense
                    self.screen_shake = 30  # Was 20, made even worse
                    
                    # print(f"HIT! Lives: {self.player.lives}")  # Debug spam
                    
                    if self.player.lives <= 0:
                        self.state = "game_over"
                        # BUG: Not recording time_taken
                        print("GAME OVER!")  # Forgot to remove debug print
                    else:
                        # Reset player - but position is bad
                        self.player.rect.x = 50
                        self.player.rect.y = 500  # BUG: Might spawn in obstacle
                        self.player.vel_y = 0
                        self.player.vel_x = 0
                    
                    # BUG: Should break after hit but doesn't
                    # Can hit multiple enemies in one frame
            
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
                    # BUG: Score increment completely wrong
                    self.player.score += 50  # Should be 200, giving way less
                    
                    # Apply power-up - effects are broken
                    if power_up.type == "speed":
                        # BUG: Speed boost too strong + permanent
                        self.player.speed = PLAYER_SPEED * 4  # Never resets!
                        print("SPEED BOOST!")  # Debug print left in
                    elif power_up.type == "jump":
                        # BUG: Jump power-up doesn't work as intended
                        self.player.jump()  # Just makes you jump, not boost
                        # TODO: Should increase jump height for duration
                    elif power_up.type == "attack":
                        # TODO: Attack power-up does nothing
                        pass
                    
                    # FIXME: No visual/audio feedback
                    # FIXME: No duration tracking - permanent effects
            
            # Check if friend rescued
            if self.friend and self.friend.rescued:
                if self.current_level < 3:
                    self.current_level += 1
                    self.reset_game()
                else:
                    self.state = "victory"
                    # TODO: Record final time
            
            # Check time limit
            # BUG: Will crash on level 3 because time limit not defined
            elapsed_time = time.time() - self.start_time
            if self.current_level in LEVEL_TIME_LIMITS:
                if elapsed_time > LEVEL_TIME_LIMITS[self.current_level]:
                    self.player.lives = 0
                    self.state = "game_over"
            
            # Check projectile hits - DOESN'T WORK
            if self.lord_zing and not self.lord_zing.defeated:
                for proj in self.player.projectiles[:]:
                    # BUG: Hit detection completely wrong
                    # Forgot to account for camera offset AND boss is moving
                    distance = abs(proj['x'] - self.lord_zing.rect.x)
                    # print(f"Proj at {proj['x']}, Boss at {self.lord_zing.rect.x}, dist: {distance}")  # Debug
                    
                    # BUG: Hit box too small, almost impossible to hit
                    if distance < 20:  # Should be 50 and use camera offset
                        self.lord_zing.take_damage()
                        proj['hit'] = True
                        self.screen_shake = 10
                        print(f"HIT BOSS! Health: {self.lord_zing.health}")  # Debug print
                        if self.lord_zing.defeated:
                            self.friend.rescue()
                            print("BOSS DEFEATED!")  # More debug spam
                    
                    # BUG: Projectiles sometimes pass through boss
                    # TODO: Use proper collision detection
                    # TODO: Fix the camera offset issue
            
            # PERFORMANCE ISSUE: Running too many checks
            # This loop runs 60 times per second even when paused
            # TODO: Optimize collision detection
            # TODO: Add spatial partitioning
            # TODO: Profile the code to find bottlenecks
    
    def draw_debug_overlay(self):
        """Draw scattered UI text all over screen"""
        debug_font = pygame.font.Font(None, 36)
        small_debug_font = pygame.font.Font(None, 28)
        tiny_debug_font = pygame.font.Font(None, 24)
        
        # Get current time for timer
        if hasattr(self, 'start_time') and self.current_level in LEVEL_TIME_LIMITS:
            elapsed = time.time() - self.start_time
            remaining = max(0, LEVEL_TIME_LIMITS[self.current_level] - elapsed)
            timer_text = f"Time: {remaining:.1f}s"
        else:
            timer_text = "Time: 0.0s"
        
        # Scatter game UI text all over the screen
        scattered_messages = [
            ("Hold MOUSE: Run", (50, 50), WHITE, small_debug_font),
            ("CLICK/SPACE: Jump", (850, 50), WHITE, small_debug_font),
            ("Level 1", (10, 150), YELLOW, debug_font),
            ("Level 2", (950, 150), YELLOW, debug_font),
            ("Level 3", (500, 30), YELLOW, debug_font),
            (timer_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40), RED, small_debug_font),
            (timer_text, (50, SCREEN_HEIGHT - 40), RED, small_debug_font),
            ("Score: 0", (400, 650), YELLOW, small_debug_font),
            ("Lives:", (10, 350), WHITE, tiny_debug_font),
            ("Hold MOUSE: Run", (SCREEN_WIDTH - 220, 450), WHITE, tiny_debug_font),
            ("CLICK/SPACE: Jump", (350, 150), WHITE, tiny_debug_font),
            ("Level 1", (SCREEN_WIDTH - 150, 250), YELLOW, small_debug_font),
            ("Level 2", (200, 500), YELLOW, small_debug_font),
            ("Level 3", (700, 600), YELLOW, small_debug_font),
            (f"Score: {self.player.score if hasattr(self, 'player') else 0}", (900, 550), YELLOW, tiny_debug_font),
            ("Lives:", (SCREEN_WIDTH - 100, 350), WHITE, tiny_debug_font),
            (timer_text, (400, 100), RED, tiny_debug_font),
            ("Hold MOUSE: Run", (100, 600), WHITE, small_debug_font),
            ("CLICK/SPACE: Jump", (SCREEN_WIDTH - 250, 600), WHITE, small_debug_font),
            ("Level 1", (500, 500), YELLOW, tiny_debug_font),
            ("Level 2", (10, 250), YELLOW, tiny_debug_font),
            ("Level 3", (SCREEN_WIDTH - 150, 550), YELLOW, tiny_debug_font),
        ]
        
        for message, pos, color, font in scattered_messages:
            text = font.render(message, True, color)
            # Add semi-transparent background
            text_rect = text.get_rect(topleft=pos)
            bg_surface = pygame.Surface((text_rect.width + 8, text_rect.height + 4))
            bg_surface.set_alpha(80)
            bg_surface.fill(BLACK)
            self.screen.blit(bg_surface, (pos[0] - 4, pos[1] - 2))
            self.screen.blit(text, pos)
    
    def draw_menu(self):
        """Draw main menu"""
        # Gradient background
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
            # BUG: Missing shooting instruction
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280 + i * 40))
            self.screen.blit(text, text_rect)
        
        # Draw debug overlay on menu
        self.draw_debug_overlay()
    
    def draw_level_select(self):
        """Draw level selection screen"""
        # Background
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
        level_times = ["120s", "90s", "???"]  # BUG: Level 3 time unknown
        
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
        
        # Draw debug overlay on level select
        self.draw_debug_overlay()
    
    def draw_game(self):
        """Draw game screen"""
        # Sky background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DEEP_BLUE[0] * (1 - color_ratio) + FOREST_GREEN[0] * color_ratio * 0.3)
            g = int(DEEP_BLUE[1] * (1 - color_ratio) + FOREST_GREEN[1] * color_ratio * 0.3)
            b = int(DEEP_BLUE[2] * (1 - color_ratio) + FOREST_GREEN[2] * color_ratio * 0.3)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.background.draw(self.screen)
        
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
                # BUG: Culling range too narrow
                if -30 < draw_x < SCREEN_WIDTH + 30:  # Should be -50 and +50
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
                    pygame.draw.rect(self.screen, PURPLE, draw_rect, border_radius=10)
                    pygame.draw.circle(self.screen, RED,
                                       (draw_rect.x + 20, draw_rect.y + 25), 8)
                    pygame.draw.circle(self.screen, RED,
                                       (draw_rect.x + 60, draw_rect.y + 25), 8)
                    # Health
                    for i in range(self.lord_zing.health):
                        pygame.draw.circle(self.screen, RED,
                                           (draw_rect.x + 10 + i * 20, draw_rect.y - 20), 8)
        
        # Draw Friend
        if self.friend:
            draw_x = self.friend.rect.x + camera_x
            if -100 < draw_x < SCREEN_WIDTH + 100:
                draw_rect = pygame.Rect(draw_x, self.friend.rect.y,
                                        self.friend.rect.width, self.friend.rect.height)
                
                # Cage
                if not self.friend.rescued:
                    for bar in self.friend.cage_bars:
                        bar_rect = pygame.Rect(bar.x + camera_x, bar.y, bar.width, bar.height)
                        pygame.draw.rect(self.screen, GRAY, bar_rect)
                
                # Friend
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
        
        # Draw player
        self.player.draw(self.screen, camera_x)
        
        # Draw UI
        self.draw_ui()
        
        # Draw debug overlay on game screen
        self.draw_debug_overlay()
    
    def draw_ui(self):
        """Draw UI elements"""
        # UI background
        ui_surface = pygame.Surface((300, 140))
        ui_surface.set_alpha(180)
        ui_surface.fill(DEEP_BLUE)
        self.screen.blit(ui_surface, (10, 10))
        
        # Lives
        lives_text = self.small_font.render("Lives:", True, WHITE)
        self.screen.blit(lives_text, (20, 20))
        for i in range(self.player.lives):
            heart_x = 80 + i * 25
            # BUG: Heart drawing slightly off
            pygame.draw.polygon(self.screen, RED, [
                (heart_x, 30), (heart_x + 5, 25), (heart_x + 10, 25),
                (heart_x + 15, 30), (heart_x + 15, 35), (heart_x + 7, 42), (heart_x, 35)  # Should be 7.5
            ])
        
        # Score
        score_text = self.small_font.render(f"Score: {self.player.score}", True, YELLOW)
        self.screen.blit(score_text, (20, 55))
        
        # Level
        level_text = self.small_font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (20, 90))
        
        # Timer
        elapsed_time = time.time() - self.start_time
        # BUG: Will crash on level 3
        if self.current_level in LEVEL_TIME_LIMITS:
            remaining_time = max(0, LEVEL_TIME_LIMITS[self.current_level] - elapsed_time)
            timer_color = RED if remaining_time < 20 else WHITE
            timer_text = self.small_font.render(f"Time: {remaining_time:.1f}s", True, timer_color)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
        
        # Controls - incomplete
        controls = [
            "Hold MOUSE: Run",
            "CLICK/SPACE: Jump",
            # TODO: Add shooting controls
        ]
        
        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, WHITE)
            self.screen.blit(control_surface, (SCREEN_WIDTH - 250, 60 + i * 25))
    
    def draw_game_over(self):
        """Draw game over screen"""
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
            # BUG: time_taken not recorded
        ]
        
        for i, stat in enumerate(analytics):
            stat_text = self.small_font.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            self.screen.blit(stat_text, stat_rect)
        
        # Buttons
        self.draw_interactive_buttons()
        
        # Draw debug overlay on game over
        self.draw_debug_overlay()
    
    def draw_victory(self):
        """Draw victory screen"""
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
        
        # Stats - incomplete
        analytics = [
            f"Final Score: {self.player.score}",
            f"Total Coins: {self.game_stats['coins_collected']}",
            f"Total Deaths: {self.game_stats['deaths']}",
            # TODO: Add performance rating
        ]
        
        for i, stat in enumerate(analytics):
            stat_text = self.small_font.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            self.screen.blit(stat_text, stat_rect)
        
        # Buttons
        self.draw_interactive_buttons()
        
        # Draw debug overlay on victory screen
        self.draw_debug_overlay()
    
    def draw_interactive_buttons(self):
        """Draw restart and menu buttons"""
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
        """Main game loop"""
        running = True
        frame_count = 0  # Debug counter
        
        # BUG: No error handling - game crashes randomly
        # TODO: Add try-except blocks
        
        while running:
            frame_count += 1
            
            # BUG: FPS drops randomly
            # if frame_count % 100 == 0:
            #     print(f"Frame: {frame_count}, FPS: {self.clock.get_fps():.1f}")  # Perf debug
            
            running = self.handle_events()
            self.update()
            
            # Draw based on state
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "level_select":
                self.draw_level_select()
            elif self.state == "game":
                self.draw_game()
                # BUG: Drawing twice sometimes? Performance issue
                # self.draw_game()  # Accidentally called twice during debug
            elif self.state == "game_over":
                self.draw_game_over()
            elif self.state == "victory":
                self.draw_victory()
            # TODO: Add pause state
            # TODO: Add settings state
            
            pygame.display.flip()
            
            # BUG: FPS lock doesn't work properly
            # Tried different approaches
            self.clock.tick(FPS)
            # self.clock.tick(FPS * 2)  # Tried doubling - made it worse
            # time.sleep(1/FPS)  # Tried manual delay - terrible
            
            # PERFORMANCE: Game sometimes runs at 30fps instead of 60
            # PERFORMANCE: Random lag spikes every few seconds
            # TODO: Fix memory leak
            # TODO: Fix performance issues before release
        
        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    # TODO: Add error handling
    # TODO: Add logging
    # TODO: Add crash reporting
    
    print("Starting Turbo Runners...")
    print("WARNING: This is a development build with known issues!")
    print("="*50)
    
    # BUG: No error handling, crashes will close immediately
    try:
        game = Game()
        game.run()
    except Exception as e:
        # FIXME: Error handling incomplete
        print(f"FATAL ERROR: {e}")
        print("Game crashed! Sorry!")
        # TODO: Save error log
        # TODO: Show user-friendly error message
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open

