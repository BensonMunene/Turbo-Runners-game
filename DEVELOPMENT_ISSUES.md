# Turbo Runners - Development Issues Documentation
## Version 0.3.2 (main2.py) - Known Bugs and Problems

## Table of Contents
1. [Critical Game-Breaking Issues](#critical-game-breaking-issues)
2. [Physics and Movement Problems](#physics-and-movement-problems)
3. [Collision Detection Failures](#collision-detection-failures)
4. [Camera System Issues](#camera-system-issues)
5. [Enemy and Obstacle Problems](#enemy-and-obstacle-problems)
6. [Boss Fight Bugs](#boss-fight-bugs)
7. [Power-Up System Failures](#power-up-system-failures)
8. [Level Design Issues](#level-design-issues)
9. [Performance Problems](#performance-problems)
10. [Missing Features](#missing-features)
11. [Code Quality Issues](#code-quality-issues)

## Critical Game-Breaking Issues

### 1. **Level 3 Not Implemented**
- **Location:** Lines 621-624
- **Severity:** CRITICAL
- **Description:** Level 3 (Hard difficulty) was attempted but never completed. Currently just prints "Level 3 not implemented!" to console.
- **Impact:** Players cannot complete the full game
- **Status:** Abandoned after multiple failed attempts

### 2. **Missing Time Limit for Level 3**
- **Location:** Line 48-49
- **Severity:** HIGH
- **Description:** `LEVEL_TIME_LIMITS` dictionary only contains entries for levels 1 and 2
- **Error:** Will cause KeyError crash if Level 3 is somehow accessed
- **Attempted Fix:** Added conditional checks, but still causes timer display issues

### 3. **No Invincibility Frames**
- **Location:** Lines 719-743
- **Severity:** CRITICAL
- **Description:** Player has no invincibility period after taking damage
- **Impact:** Can lose all 3 lives instantly by touching multiple enemies in one frame
- **Status:** Attempted implementation, gave up

---

## Physics and Movement Problems

### 4. **Gravity Too Strong**
- **Location:** Line 42
- **Severity:** HIGH
- **Description:** Gravity changed from 0.8 to 1.2 during "balancing" attempts
- **Impact:** Player falls too fast, feels heavy and unresponsive
- **Attempted Values:** 0.5 (too floaty), 2.0 (way too fast), settled on 1.2 (still wrong)
- **Code:**
  ```python
  GRAVITY = 1.2  # Was 0.8, changed to 1.2, now too strong
  ```

### 5. **Jump Height Too Weak**
- **Location:** Line 45
- **Severity:** HIGH
- **Description:** Jump speed reduced from -15 to -12
- **Impact:** Player cannot reach platforms that were designed for original jump height
- **Code:**
  ```python
  JUMP_SPEED = -12  # BUG: Was -15, changed but now can't reach platforms
  ```

### 6. **Jump Mechanics Unreliable**
- **Location:** Lines 181-193
- **Severity:** CRITICAL
- **Description:** Jump only works about 50% of the time due to unreliable `on_ground` flag
- **Root Cause:** Collision detection issues prevent reliable ground detection
- **Attempted Fix:** Added hacky condition `if self.on_ground or self.vel_y < 5:` which made it worse (allows infinite jumping)
- **Code:**
  ```python
  if self.on_ground or self.vel_y < 5:  # Hacky fix attempt - made it worse
      self.vel_y = JUMP_SPEED
  ```

### 7. **Player Speed Too High**
- **Location:** Line 119
- **Severity:** HIGH
- **Description:** Running speed multiplier set to 3.5x (should be 1.8x)
- **Impact:** Player moves too fast to control properly
- **Progression:** Started at 2.5x, increased to 3.0x, then 3.5x trying to make game "harder"
- **Code:**
  ```python
  self.speed = PLAYER_SPEED * 3.5  # Tried 2.5, 3.0, now 3.5 - too fast!
  ```

### 8. **Acceleration Too Aggressive**
- **Location:** Lines 126-129
- **Severity:** MEDIUM
- **Description:** Acceleration value increased from 0.5 to 1.2
- **Impact:** Player movement feels twitchy and hard to control
- **Code:**
  ```python
  self.vel_x = max(self.vel_x - 1.2, -self.speed)  # Should be 0.5
  ```

### 9. **Friction Barely Works**
- **Location:** Line 132
- **Severity:** HIGH
- **Description:** Friction coefficient set to 0.98 (should be 0.8)
- **Impact:** Player slides forever after stopping input, like moving on ice
- **Attempted Values:** 0.95, 0.97, 0.98 - all wrong
- **Code:**
  ```python
  self.vel_x *= 0.98  # Tried 0.95, 0.97, 0.98 - still wrong
  ```

---

## Collision Detection Failures

### 10. **Players Fall Through Moving Platforms**
- **Location:** Lines 252-280
- **Severity:** CRITICAL
- **Description:** Collision detection has gaps, especially with moving platforms
- **Impact:** Most game-breaking bug - makes moving platforms unusable
- **Root Cause:** Platform position updates don't sync with player position
- **Status:** Tried fixing for hours, still broken

### 11. **Platform Doesn't Carry Player**
- **Location:** Lines 277-280
- **Severity:** CRITICAL
- **Description:** Player doesn't move with moving platform (no platform velocity transfer)
- **Impact:** Player stays in place while platform moves beneath them, then falls off
- **Attempted Fixes (Failed):**
  - `player.rect.x += self.speed * self.direction` - didn't work
  - Storing last_x and calculating delta - also failed
- **Status:** Gave up, left commented out

### 12. **No Side Collision Detection**
- **Location:** Lines 148-158
- **Severity:** HIGH
- **Description:** Only checks vertical collision (vel_y > 0), ignores horizontal
- **Impact:** Player can phase through platforms from the sides
- **TODO Comments:** "Add side collision", "Add top collision (bonk head)"

### 13. **Collision Has Gaps**
- **Location:** Lines 145-159
- **Severity:** HIGH
- **Description:** Collision detection is unreliable with fast movement
- **Impact:** Player sometimes passes through solid objects
- **Code Comments:** "Tried multiple approaches, none work perfectly"

### 14. **Position Correction Causes Jitter**
- **Location:** Line 153
- **Severity:** MEDIUM
- **Description:** Snapping player to platform top causes visual stuttering
- **Impact:** Player appears to vibrate when landing on platforms
- **Code:**
  ```python
  self.rect.bottom = platform.rect.top  # FIXME: Position correction causes jitter
  ```

---

## Camera System Issues

### 15. **Camera Smoothing Too Slow**
- **Location:** Line 603
- **Severity:** HIGH
- **Description:** Camera lerp value reduced from 0.1 to 0.05, then to 0.02
- **Impact:** Camera lags far behind player movement, disorienting gameplay
- **Code:**
  ```python
  self.camera_offset += (target_offset - self.camera_offset) * 0.02  # Was 0.05, made even slower
  ```

### 16. **Random Camera Jitter**
- **Location:** Lines 606-608
- **Severity:** CRITICAL
- **Description:** Added "stabilization" that randomly offsets camera by ±5 pixels (10% chance per frame)
- **Impact:** Camera shakes randomly, causes motion sickness
- **Code:**
  ```python
  if random.random() < 0.1:  # 10% chance each frame - WHY?!
      self.camera_offset += random.randint(-5, 5)
  ```
- **Question in Code:** "WHY?!" (developer doesn't remember why they added this)

### 17. **Screen Shake Too Intense**
- **Location:** Lines 611-615
- **Severity:** HIGH
- **Description:** Screen shake effect doubled (multiplied by 2)
- **Impact:** When damaged, screen shakes violently, hard to see
- **Values:** Shake amount set to 30 (should be 15), then multiplied by 2 = 60 pixel shake
- **Code:**
  ```python
  shake_amount = self.screen_shake * 2  # Doubled for "effect"
  ```

---

## Enemy and Obstacle Problems

### 18. **Enemy Speed Doubled**
- **Location:** Line 305
- **Severity:** HIGH
- **Description:** All enemy speeds multiplied by 2 to make game "harder"
- **Impact:** Enemies move too fast to dodge, game becomes unfair
- **Code:**
  ```python
  self.speed = speed * 2  # Doubled it to make game "harder" - now unfair
  ```

### 19. **Enemy Movement Stutters**
- **Location:** Lines 319-321
- **Severity:** MEDIUM
- **Description:** Enemies only move every 3rd frame instead of every frame
- **Impact:** Jerky, unpredictable movement patterns
- **Code:**
  ```python
  if self.frame_count % 3 == 0:  # Why did I add this?
      self.rect.x += self.speed * self.direction
  ```

### 20. **Hit Detection Too Sensitive**
- **Location:** Lines 311-312, 721-722
- **Severity:** HIGH
- **Description:** Hit boxes inflated by 10 pixels padding
- **Impact:** Player gets hit from further away than visually appears
- **Code:**
  ```python
  self.hit_padding = 10  # Makes enemies hit from further away
  hit_rect = self.player.rect.inflate(obstacle.hit_padding, obstacle.hit_padding)
  ```

### 21. **Patrol Range Too Large**
- **Location:** Line 324
- **Severity:** MEDIUM
- **Description:** Enemy patrol range increased from 200 to 300 pixels
- **Impact:** Enemies patrol too far, sometimes disappear off screen
- **Code:**
  ```python
  if abs(self.rect.x - self.original_x) > 300:  # Was 200
  ```

### 22. **No Break After Hit**
- **Location:** Lines 742-743
- **Severity:** HIGH
- **Description:** Missing `break` statement after processing enemy collision
- **Impact:** Can hit multiple enemies in one frame, lose multiple lives instantly
- **Code Comment:** "Should break after hit but doesn't"

---

## Boss Fight Bugs

### 23. **Projectile Hit Detection Broken**
- **Location:** Lines 792-812
- **Severity:** CRITICAL
- **Description:** Projectile collision doesn't account for camera offset or boss movement
- **Impact:** Nearly impossible to hit Lord Zing with projectiles
- **Code:**
  ```python
  distance = abs(proj['x'] - self.lord_zing.rect.x)
  # Forgot to account for camera offset AND boss is moving
  ```

### 24. **Hit Box Too Small**
- **Location:** Line 801
- **Severity:** HIGH
- **Description:** Boss hit box radius reduced from 50 to 20 pixels
- **Impact:** Extremely difficult to land hits, frustrating boss fight
- **Code:**
  ```python
  if distance < 20:  # Should be 50 and use camera offset
  ```

### 25. **Projectiles Pass Through Boss**
- **Location:** Lines 810-812
- **Severity:** HIGH
- **Description:** Hit detection only checks x-axis distance, not proper collision
- **Impact:** Projectiles sometimes visually hit but don't register
- **TODO:** "Use proper collision detection", "Fix the camera offset issue"

---

## Power-Up System Failures

### 26. **Speed Boost Permanent and Too Strong**
- **Location:** Lines 760-763
- **Severity:** CRITICAL
- **Description:** Speed power-up multiplies speed by 4x and never resets
- **Impact:** After collecting one speed boost, player becomes uncontrollable permanently
- **Code:**
  ```python
  self.player.speed = PLAYER_SPEED * 4  # Never resets!
  print("SPEED BOOST!")  # Debug print left in
  ```

### 27. **Jump Power-Up Doesn't Work**
- **Location:** Lines 764-767
- **Severity:** HIGH
- **Description:** Jump power-up just makes player jump once instead of boosting jump height
- **Impact:** Power-up feels useless, doesn't match expected behavior
- **Code:**
  ```python
  self.player.jump()  # Just makes you jump, not boost
  # TODO: Should increase jump height for duration
  ```

### 28. **Attack Power-Up Does Nothing**
- **Location:** Lines 768-770
- **Severity:** HIGH
- **Description:** Attack power-up has no implementation
- **Code:**
  ```python
  elif power_up.type == "attack":
      # TODO: Attack power-up does nothing
      pass
  ```

### 29. **No Duration Tracking**
- **Location:** Lines 772-773
- **Severity:** HIGH
- **Description:** Power-ups have no expiration time, effects are permanent
- **Impact:** Game balance completely broken after collecting power-ups
- **FIXME:** "No duration tracking - permanent effects"

### 30. **Wrong Score Value**
- **Location:** Line 757
- **Severity:** LOW
- **Description:** Power-ups give 50 points instead of 200
- **Impact:** Score progression feels unrewarding
- **Code:**
  ```python
  self.player.score += 50  # Should be 200, giving way less
  ```

---

## Level Design Issues

### 31. **Level 2 Nearly Impossible**
- **Location:** Lines 579-619
- **Severity:** CRITICAL
- **Description:** Level 2 was "balanced" to be harder but became unplayable
- **Issues:**
  - Platforms too far apart after jump nerf
  - Too many enemies (4 instead of 2)
  - Moving platforms way too fast (speed 3 and 2.5 instead of 2 and 1.5)
  - Platform ranges too large (200 and 150 instead of 120 and 100)
  - Missing critical platforms (line 587 commented out by accident)
  - Collectibles too spread out, many unreachable
  - Boss moved higher, harder to reach

### 32. **Missing Critical Platforms**
- **Location:** Line 587
- **Severity:** HIGH
- **Description:** Platform at (750, 280) commented out by accident
- **Impact:** Creates impossible gap in Level 2
- **Code:**
  ```python
  # Platform(750, 280, 80, 20),  # Commented out by accident
  ```

### 33. **Moving Platforms Too Fast**
- **Location:** Lines 591-594
- **Severity:** HIGH
- **Description:** Platform speeds increased to 3 and 2.5 (were 2 and 1.5)
- **Impact:** Combined with player not being carried, makes platforms impossible to use

### 34. **Too Many Enemies**
- **Location:** Lines 597-602
- **Severity:** HIGH
- **Description:** Level 2 has 4 ground enemies instead of 2
- **Impact:** With no invincibility frames and sensitive hit detection, nearly impossible to survive

### 35. **Coins in Impossible Locations**
- **Location:** Lines 605-608
- **Severity:** MEDIUM
- **Description:** Collectibles spread 150 pixels apart with 40 pixel vertical gaps
- **Impact:** Many coins unreachable with weakened jump

---

## Moving Platform Specific Issues

### 36. **Random Speed Variation**
- **Location:** Line 261
- **Severity:** HIGH
- **Description:** Platform speed randomized between 0.8x and 1.2x each frame
- **Impact:** Completely unpredictable platform movement
- **Code:**
  ```python
  actual_speed = self.speed * random.uniform(0.8, 1.2)  # WHY DID I ADD RANDOM?!
  ```
- **Question in Code:** Developer doesn't understand why random was added

### 37. **Platform Teleporting**
- **Location:** Lines 266-273
- **Severity:** HIGH
- **Description:** Position clamping logic causes platforms to "jump" to boundary
- **Impact:** Visual glitches, platforms disappear and reappear
- **Issue:** `new_x` not updated after clamping (line 273)

### 38. **Range Check Wrong**
- **Location:** Line 266
- **Severity:** MEDIUM
- **Description:** Uses `>=` instead of `>` for range limit check
- **Impact:** Platform reverses direction too early

---

## Performance Problems

### 39. **Collision Checks Not Optimized**
- **Location:** Lines 814-818
- **Severity:** MEDIUM
- **Description:** All collision checks run 60 times per second even when paused
- **Impact:** Unnecessary CPU usage
- **TODO:** "Optimize collision detection", "Add spatial partitioning"

### 40. **Random FPS Drops**
- **Location:** Lines 1207-1208
- **Severity:** MEDIUM
- **Description:** Game sometimes runs at 30fps instead of 60fps
- **Cause:** Unknown, possibly related to gradient background drawing
- **Performance Comments:** "Random lag spikes every few seconds"

### 41. **Gradient Background Performance**
- **Location:** Multiple draw functions (lines 959-964, 1003-1008, etc.)
- **Severity:** LOW
- **Description:** Drawing gradient line-by-line every frame
- **Impact:** Could be optimized by pre-rendering to surface

### 42. **No Culling Optimization**
- **Location:** Line 1089
- **Severity:** LOW
- **Description:** Collectible culling range too narrow (-30 to +30 instead of -50 to +50)
- **Impact:** Items pop in/out of view abruptly

---

## Missing Features

### 43. **Shooting Controls Don't Work**
- **Location:** Lines 641-645
- **Severity:** HIGH
- **Description:** Enter key shooting functionality commented out
- **Impact:** Player can't shoot projectiles reliably
- **Code:**
  ```python
  # BUG: Enter key not working for shooting
  # if event.key == pygame.K_RETURN:
  #     if self.state == "game":
  #         self.player.shoot()
  ```

### 44. **No Shooting Cooldown**
- **Location:** Line 195
- **Severity:** MEDIUM
- **Description:** No cooldown timer on shooting
- **Impact:** Can spam projectiles, but they don't work anyway

### 45. **Missing Shooting Instruction**
- **Location:** Line 989
- **Severity:** LOW
- **Description:** Menu doesn't tell players how to shoot
- **Code Comment:** "BUG: Missing shooting instruction"

### 46. **Time Not Recorded on Game Over**
- **Location:** Line 734
- **Severity:** LOW
- **Description:** `time_taken` not added to stats dictionary when player dies
- **Impact:** Can't show play time on game over screen
- **Code Comment:** "BUG: Not recording time_taken"

### 47. **Incomplete Game Stats**
- **Location:** Line 507
- **Severity:** LOW
- **Description:** Game stats dictionary missing `time_taken` field
- **Impact:** Victory/game over screens have incomplete stats

### 48. **Sound Effects Not Implemented**
- **Location:** Line 516
- **Severity:** LOW
- **Description:** Attempted to add sound system but never finished
- **Code:**
  ```python
  # self.sound_effects = {}  # Tried to add sounds - didn't finish
  ```

### 49. **Music Not Implemented**
- **Location:** Line 517
- **Severity:** LOW
- **Description:** Music player planned but never started
- **Code:**
  ```python
  # self.music_player = None  # Music not implemented
  ```

### 50. **Particle System Abandoned**
- **Location:** Line 515
- **Severity:** LOW
- **Description:** Particle system attempted but removed due to performance
- **Code:**
  ```python
  # self.particles = []  # Tried to add particle system - too slow
  ```

### 51. **Save System Abandoned**
- **Location:** Line 15
- **Severity:** LOW
- **Description:** Attempted JSON-based save system, gave up
- **Code:**
  ```python
  # import json  # Was trying to use this for save system - gave up
  ```

---

## Code Quality Issues

### 52. **Debug Print Statements Everywhere**
- **Location:** Multiple (lines 109, 159, 522, 729, 734, 763, 805, 808)
- **Severity:** LOW
- **Description:** Console spam from forgotten debug prints
- **Examples:**
  - `print(f"DEBUG: platforms count: {len(platforms)}")`
  - `print("GAME OVER!")`
  - `print("SPEED BOOST!")`
  - `print(f"HIT BOSS! Health: {self.lord_zing.health}")`

### 53. **Commented Out Failed Code**
- **Location:** Throughout file
- **Severity:** LOW
- **Description:** Many commented sections showing failed implementation attempts
- **Examples:**
  - Multiple gravity value attempts (lines 43-44)
  - Various friction values (line 132)
  - Platform carrying player attempts (lines 277-280)
  - Procedural generation code (lines 535-545)

### 54. **Magic Numbers Everywhere**
- **Location:** Throughout
- **Severity:** LOW
- **Description:** Hard-coded values with no named constants
- **Examples:** 3.5, 1.2, 0.98, 300, 20, etc.

### 55. **Over 100 TODO/FIXME Comments**
- **Location:** Throughout entire file
- **Severity:** LOW
- **Description:** Extensive list of known issues documented in comments
- **Count:**
  - TODO: ~50+ comments
  - FIXME: ~30+ comments
  - BUG: ~40+ comments

### 56. **No Error Handling**
- **Location:** Line 1226-1238
- **Severity:** MEDIUM
- **Description:** Minimal try-catch, crashes close immediately
- **Impact:** No useful error messages for debugging

### 57. **Unused Variables**
- **Location:** Multiple
- **Examples:**
  - `collision_count` (line 144) - only used for debug
  - `frame_count` (line 1168) - only for debug comments
  - `move_timer` (line 250) - added but not used

### 58. **Inconsistent Respawn Position**
- **Location:** Lines 170-173, 737-740
- **Severity:** MEDIUM
- **Description:** Player respawns at (50, 500) which might be inside obstacles
- **Impact:** Can respawn and immediately take damage again


