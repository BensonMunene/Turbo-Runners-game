# Turbo Runners - Blippo's Epic Adventure

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the game files** to your local machine

2. **Navigate to the game directory**:
   ```bash
   cd "Game 2"
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

After completing the installation steps, run the game with:
```bash
python main.py
```

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.7 or higher
- **Display**: 1200x700 minimum screen resolution
- **Input**: Mouse and keyboard required
- **RAM**: 512MB minimum
- **Storage**: 50MB free space

## Game Overview

**Turbo Runners** is an action-packed 2D platformer where you control Blippo, a cheerful yellow character on a mission to rescue his friend from the evil Lord Zing. Navigate through three challenging levels filled with obstacles, collectibles, and power-ups in this fast-paced adventure game.

## Game Objective

Help Blippo traverse dangerous platforms, defeat the menacing Lord Zing, and rescue his captured friend. Each level presents increasing difficulty with time constraints, moving obstacles, and complex platforming challenges.

## Controls

### Basic Movement

- **Arrow Keys / WASD**: Move left and right
- **Space Bar / Left Mouse Click**: Jump
- **Hold Left Mouse Button**: Run faster (Turbo Mode)
- **Enter Key**: Shoot projectiles (for boss battles)
- **Escape**: Return to main menu

### Advanced Controls

- **Mouse Movement**: Influences camera and targeting
- **Click Title/Space**: Start game from menu
- **R Key**: Restart level (on game over)

## Game Features

### Character System

- **Blippo**: The main protagonist with animated expressions
  - Smooth movement with acceleration/deceleration
  - Animated running with speed boost
  - Blinking eyes and dynamic smile
  - Jump particles and landing effects
  - Projectile shooting capability

### Level Design

- **3 Progressive Difficulty Levels**:
  - **Level 1 (Easy)**: 120 seconds, basic platforms and obstacles
  - **Level 2 (Medium)**: 90 seconds, more complex layouts
  - **Level 3 (Hard)**: 60 seconds, challenging precision platforming

### Platform Types

- **Static Platforms**: Solid green platforms for basic navigation
- **Moving Platforms**: Horizontally moving platforms with customizable speed and range
- **Ground Platform**: Base level safety platform

### Enemy System

- **Patrol Enemies**: Red creatures that move back and forth with glowing eyes
- **Floating Spikes**: Dark red triangular hazards that float vertically
- **Lord Zing**: The main boss with 3 health points and size-scaling damage system

### Collectibles & Power-ups

- **Golden Coins**: Spinning collectibles worth 100 points each
- **Speed Power-up**: Blue power-up that doubles movement speed
- **Jump Power-up**: Yellow power-up that provides instant jump boost
- **Attack Power-up**: Red power-up for enhanced combat abilities

### Visual Effects

- **Animated Background**: Moving clouds and twinkling stars
- **Particle Systems**: Jump particles, landing effects, and sparkles
- **Dynamic Lighting**: Glowing effects on platforms, enemies, and UI
- **Screen Shake**: Impact feedback during combat and collisions
- **Smooth Camera**: Following camera with offset for better visibility

### Audio-Visual Polish

- **Color-coded Difficulty**: Visual indicators for level complexity
- **Pulsating Animations**: Dynamic UI elements and character animations
- **Gradient Backgrounds**: Smooth color transitions for different game states
- **Interactive Buttons**: Hover effects and visual feedback

## Game Mechanics

### Physics System

- **Gravity**: Realistic falling physics (0.8 units)
- **Jump Mechanics**: -15 velocity jump speed with ground detection
- **Collision Detection**: Precise rectangle-based collision system
- **Friction**: Smooth deceleration when not moving

### Health & Lives System

- **3 Lives**: Player starts with 3 lives (displayed as hearts)
- **Damage Sources**: Contact with enemies or falling off screen
- **Respawn System**: Return to safe position after taking damage

### Scoring System

- **Coins**: 100 points each
- **Power-ups**: 200 points each
- **Time Bonus**: Remaining time contributes to final score

### Boss Battle Mechanics

- **Lord Zing Health**: 3 hit points with visual size reduction
- **Projectile Combat**: Shoot projectiles using Enter key
- **Proximity Attacks**: Close-range combat with mouse clicks
- **Victory Condition**: Defeat Lord Zing to rescue the friend

## Game States

### Main Menu

- Interactive animated title
- Floating background elements
- Comprehensive control instructions
- Click-to-start functionality

### Level Selection

- Visual difficulty indicators
- Time limit displays
- Animated level buttons with hover effects
- Progress tracking

### Gameplay

- Real-time UI with lives, score, and timer
- Dynamic camera following
- Particle effects and animations
- Progressive difficulty scaling

### Game Over Screen

- Performance analytics
- Death counter and statistics
- Restart and menu options
- Animated background effects

### Victory Screen

- Celebration animations
- Complete game statistics
- Performance rating system
- Rainbow text effects

## Performance Ratings

Based on deaths during gameplay:

- **LEGENDARY!**: Less than 2 deaths
- **EXCELLENT!**: 2-4 deaths
- **GOOD EFFORT!**: 5+ deaths

## Art Style

- **Color Palette**: Forest greens, deep blues, bright yellows, and vibrant reds
- **Character Design**: Rounded, friendly sprites with expressive features
- **Environment**: Fantasy platformer aesthetic with glowing effects
- **UI Design**: Modern, clean interface with animated elements

## Technical Features

### Performance Optimizations

- **60 FPS Target**: Smooth gameplay experience
- **Efficient Rendering**: Only draw on-screen objects
- **Memory Management**: Proper sprite and particle cleanup
- **Responsive Controls**: Low-latency input handling

### Code Architecture

- **Object-Oriented Design**: Modular class structure
- **State Management**: Clean separation of game states
- **Event Handling**: Comprehensive input system
- **Animation System**: Frame-based animation timing


## Tips & Strategies

### Level 1 (Easy)

- Take your time to learn the controls
- Collect all coins for maximum score
- Use moving platforms to reach higher areas
- Practice jump timing on moving obstacles

### Level 2 (Medium)

- Master the turbo run for difficult jumps
- Time your movements with platform cycles
- Use power-ups strategically
- Watch for increased enemy speed

### Level 3 (Hard)

- Precision jumping is essential
- Memorize enemy patrol patterns
- Utilize all available power-ups
- Plan routes to minimize backtracking

### Boss Battle Tips

- Maintain distance while shooting projectiles
- Use the Enter key for ranged attacks
- Watch Lord Zing's movement patterns
- Time close-range attacks carefully

## Known Features

- Smooth difficulty progression
- Responsive control scheme
- Comprehensive visual feedback
- Detailed performance tracking
- Multiple input methods support

## Fun Facts

- Blippo changes color when running (orange in turbo mode)
- Lord Zing shrinks with each hit taken
- The friend shows different expressions when caged vs. rescued
- Background stars twinkle at different rates
- Coins have realistic spinning physics
- Screen shake intensity varies with impact force

## Replayability

- **Time Attack Mode**: Beat your best completion times
- **Perfect Run Challenge**: Complete without losing lives
- **Coin Collection**: Gather all collectibles in each level
- **Speed Run**: Complete all levels as quickly as possible

---

*Turbo Runners combines classic platformer gameplay with modern visual effects and responsive controls, creating an engaging experience for players of all skill levels. Master the mechanics, defeat Lord Zing, and become the ultimate Turbo Runner!*