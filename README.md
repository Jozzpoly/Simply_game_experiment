# Professional Rouge-like Game

A sophisticated 2D rouge-like game featuring advanced procedural generation, dynamic difficulty adaptation, comprehensive progression systems, and modern UI design. This professional-grade game has evolved through 4 major development phases to deliver a commercial-quality gaming experience.

## 🎮 **Game Overview**

**Genre**: Action Rouge-like with Real-time Combat
**Perspective**: Top-down 2D with dynamic camera system
**Combat Style**: Projectile-based attacks with elemental damage types
**Progression**: Deep character advancement with meta-progression
**Generation**: Advanced procedural level creation with architectural themes

## ✨ **Core Features**

### **🎯 Advanced Combat System**
- **Real-time projectile combat** with mouse aiming and continuous firing
- **7 Elemental damage types**: Physical, Fire, Ice, Lightning, Poison, Dark, Holy
- **Status effects system**: Burning, freezing, stunning, poisoning, and more
- **Tactical positioning**: Flanking bonuses, cover mechanics, high ground advantages
- **Combo system**: Chain attacks for increased damage multipliers

### **🏰 Sophisticated Level Generation**
- **8 Unique biomes**: Dungeon, Forest, Cave, Ruins, Swamp, Volcanic, Crystal Cavern, Necropolis
- **6 Architectural themes**: Cathedral, Fortress, Cavern, Ruins, Laboratory, Temple
- **Dynamic difficulty zones**: Safe zones, challenge areas, elite encounters, puzzle rooms
- **Progressive scaling**: Maps grow larger and more complex with each level
- **Environmental hazards**: Interactive elements that affect gameplay

### **⚔️ Enhanced Enemy System**
- **8 Distinct enemy types**: Normal, Fast, Tank, Sniper, Berserker, Mage, Assassin, Necromancer, Golem, Archer, Shaman, Berserker Elite, Shadow
- **Advanced AI coordination**: Group tactics, formations, and role-based behaviors
- **Special abilities**: Each enemy type has unique skills and attack patterns
- **Dynamic spawning**: Enemy density and types adapt to player performance
- **Boss encounters**: Challenging multi-phase boss fights with unique mechanics

### **🎯 Deep Progression Systems**
- **Skill tree system**: 3 specialization paths (Combat, Survival, Utility) with 15+ unique skills
- **Equipment system**: 6 rarity tiers from Common to Artifact with set bonuses
- **Achievement system**: 20+ achievements with meaningful rewards
- **Meta-progression**: Persistent advancement across runs with soul essence, knowledge crystals, and fate tokens
- **Mastery systems**: Weapon and magic mastery with 100 levels each

### **🎨 Modern User Experience**
- **Professional UI**: Modern interface with smooth animations and transitions
- **Accessibility features**: Colorblind support, high contrast mode, keyboard navigation
- **Comprehensive settings**: 25+ configuration options for graphics, audio, gameplay
- **Tutorial system**: Progressive onboarding with 5 comprehensive tutorials
- **Real-time feedback**: Dynamic HUD, damage numbers, visual effects

### **🧠 Intelligent Systems**
- **Dynamic difficulty**: AI-driven difficulty adaptation based on player performance
- **Performance optimization**: Automatic quality adjustments to maintain 60 FPS
- **Advanced save system**: Comprehensive persistence with backup and migration
- **Weather system**: Dynamic environmental effects affecting gameplay
- **Challenge modes**: Daily/weekly challenges with special modifiers

## 🎮 **Controls**

### **Basic Controls**
- **Movement**: WASD or Arrow Keys
- **Shooting**: Left Mouse Button, Space Key (aim with mouse, holding fires continuously)
- **Camera Zoom**: Mouse Wheel (zoom in/out for tactical overview)

### **Advanced Controls**
- **Inventory**: I key - Access equipment and items
- **Skills**: K key - View and upgrade skill tree
- **Achievements**: O key - Track progress and rewards
- **Character Stats**: C key - Detailed character information
- **Upgrade Menu**: U key - Spend upgrade and skill points
- **Pause**: P key or ESC - Pause/resume game
- **Fullscreen**: F11 or Alt+Enter - Toggle fullscreen mode

## 💻 **System Requirements**

### **Minimum Requirements**
- **OS**: Windows 7/10/11, macOS 10.12+, or Linux
- **Python**: 3.7 or higher
- **Memory**: 512 MB RAM
- **Storage**: 100 MB available space
- **Graphics**: DirectX 9.0c compatible

### **Recommended Requirements**
- **Python**: 3.9 or higher
- **Memory**: 1 GB RAM
- **Graphics**: Dedicated graphics card for optimal performance

## 🚀 **Installation & Setup**

### **Quick Start (Recommended)**

#### **Windows PowerShell**
```powershell
# Navigate to the game directory
cd "path\to\simple_rouge_like"

# Set up development environment (installs dependencies)
.\scripts\dev_utils.ps1 setup

# Launch the game
.\scripts\run_game.ps1
```

#### **Cross-Platform**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### **Manual Installation**

1. **Install Python 3.7+** from [python.org](https://python.org)
2. **Install dependencies:**
   ```bash
   pip install pygame>=2.0.0 numpy>=1.20.0
   ```
3. **Launch the game:**
   - **Windows**: `.\scripts\run_game_simple.ps1`
   - **Cross-platform**: `python main.py`

### **Development Setup**

For developers and contributors:

```powershell
# System requirements check
.\scripts\dev_utils.ps1 check

# Install all development dependencies
.\scripts\dev_utils.ps1 install

# Run comprehensive test suite
.\scripts\run_tests_simple.ps1

# Run specific test categories
.\scripts\run_tests_simple.ps1 -TestFile progression

# Clean up cache and temporary files
.\scripts\dev_utils.ps1 clean
```

## 🏗️ **Project Architecture**

### **Core Game Files**
- **`main.py`**: Game entry point and initialization
- **`game.py`**: Main game loop, state management, and event handling
- **`config.py`**: Comprehensive configuration system with 1300+ settings

### **Game Systems** (`/systems`)
- **`integrated_game_manager.py`**: Coordinates all advanced systems
- **`meta_progression.py`**: Persistent progression across runs
- **`dynamic_difficulty.py`**: AI-driven difficulty adaptation
- **`enhanced_save_manager.py`**: Advanced save/load with backups
- **`settings_manager.py`**: Professional settings system
- **`tutorial_manager.py`**: Progressive player onboarding

### **Game Modules**
- **`/entities`**: Player, enemies, projectiles, items, environmental objects
- **`/level`**: Advanced procedural generation with architectural themes
- **`/progression`**: Skill trees, equipment, achievements, character advancement
- **`/ui`**: Modern interface with animations and accessibility features
- **`/utils`**: Animation, audio, visual effects, constants, save management

### **Quality Assurance & Development**
- **`/tests`**: Organized test suite (unit, functional, integration, performance)
- **`/scripts`**: PowerShell utilities for development and deployment
- **`/docs`**: Complete documentation of all 4 development phases
- **`/assets`**: Game resources (images, sounds, UI elements)

## 🎯 **How to Play**

### **Getting Started**
1. **Launch the game** and click "New Game" or "Continue" for existing saves
2. **Complete the tutorial** - 5 progressive lessons teach all game mechanics
3. **Choose your playstyle** - Combat, Survival, or Utility specialization paths
4. **Explore procedurally generated levels** with unique biomes and themes

### **Core Gameplay Loop**
1. **Navigate levels** using WASD/arrow keys with mouse-wheel zoom
2. **Engage enemies** with projectile combat (mouse aim + left click/spacebar)
3. **Collect loot** - Equipment, consumables, and upgrade materials
4. **Progress through levels** by finding and using stairs (defeat 50% of enemies first)
5. **Advance your character** through multiple progression systems

### **Character Progression**
- **Gain XP** from defeating enemies (varies by enemy type and difficulty)
- **Level up** to earn upgrade points and skill points
- **Spend points** in the comprehensive upgrade system:
  - **Stats Tab** (U key): Core attributes (health, damage, speed, fire rate)
  - **Skills Tab** (K key): 15+ skills across 3 specialization trees
  - **Equipment Tab** (I key): Manage weapons, armor, accessories with set bonuses
  - **Achievements Tab** (O key): Track 20+ achievements with meaningful rewards
  - **Character Stats** (C key): Detailed character information and statistics

### **Advanced Systems**
- **Meta-progression**: Earn soul essence, knowledge crystals, and fate tokens
- **Dynamic difficulty**: Game adapts to your skill level automatically
- **Equipment mastery**: Gain weapon and magic mastery through use
- **Challenge modes**: Daily and weekly challenges with special rewards
- **Prestige system**: Advanced progression for experienced players

### **Pro Tips**
- **Experiment with builds** - Skills and equipment synergize in powerful ways
- **Use the environment** - Hazards can damage enemies too
- **Master elemental damage** - Different enemies have resistances and weaknesses
- **Explore thoroughly** - Secret areas contain valuable rewards
- **Adapt your strategy** - Each biome and enemy type requires different tactics

## 🛠️ **Troubleshooting**

### **Common Installation Issues**

#### **PowerShell Execution Policy (Windows)**
```powershell
# Check current policy
Get-ExecutionPolicy

# Enable script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Python/Dependency Issues**
- **"Python not recognized"**: Install Python from [python.org](https://python.org) and add to PATH
- **"Pygame not found"**: Run `pip install pygame>=2.0.0`
- **"NumPy not found"**: Run `pip install numpy>=1.20.0`
- **Permission errors**: Run terminal/PowerShell as administrator

### **Performance Issues**
- **Low FPS**: Game automatically adjusts quality - check settings menu
- **High memory usage**: Restart game periodically for long sessions
- **Slow loading**: Ensure adequate storage space (100MB+ free)

### **Getting Support**
- **Game Help**: Press F1 in-game for contextual help
- **Script Help**: Run `.\scripts\dev_utils.ps1 help` for development utilities
- **Documentation**: Check `/docs` folder for comprehensive guides (25+ files)
- **Testing**: Run `.\scripts\run_tests_simple.ps1` to verify installation
- **Project Analysis**: See `PROJECT_ORGANIZATION_SUMMARY.md` for complete overview

## 🏆 **Development Credits**

### **Project Attribution**
- **Author**: sb (System Builder/Developer)
- **Prompter/Designer**: Jozzpoly (Game Design & Direction)
- **Engine**: Python 3.x with Pygame 2.x
- **Architecture**: Modular object-oriented design with type annotations

### **Development Journey**
This professional rouge-like game evolved through **4 major development phases**:

- **Phase 1**: Core mechanics and basic systems foundation
- **Phase 2**: Enhanced enemies, elemental combat, equipment system
- **Phase 3**: Meta-progression, dynamic difficulty, advanced generation
- **Phase 4**: Polish, integration, settings, tutorials, launch preparation

### **Technical Excellence**
- **Code Quality**: Type annotations, comprehensive testing, modular architecture
- **Performance**: 60 FPS target with automatic optimization
- **Accessibility**: Colorblind support, keyboard navigation, high contrast modes
- **Compatibility**: Cross-platform support with backward save compatibility

## 🚀 **Project Status: Launch Ready**

This rouge-like game represents a **professional-grade gaming experience** that has achieved commercial launch readiness through systematic development and comprehensive testing. The game offers hundreds of hours of engaging gameplay with deep progression systems and intelligent difficulty adaptation.
