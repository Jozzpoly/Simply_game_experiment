"""
Tutorial Manager for Phase 4

This module provides comprehensive player onboarding and tutorial systems:
- Progressive feature introduction
- Interactive tutorials for advanced systems
- Contextual help and tooltips
- Achievement-based learning
- Skip options for experienced players
"""

import pygame
import time
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class TutorialState(Enum):
    """States of tutorial progression"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TutorialTrigger(Enum):
    """Triggers for tutorial activation"""
    GAME_START = "game_start"
    FIRST_ENEMY = "first_enemy"
    FIRST_ITEM = "first_item"
    LEVEL_COMPLETE = "level_complete"
    FIRST_DEATH = "first_death"
    LEVEL_3_REACHED = "level_3_reached"
    FIRST_ENHANCED_ENEMY = "first_enhanced_enemy"
    FIRST_SECRET_AREA = "first_secret_area"
    META_CURRENCY_EARNED = "meta_currency_earned"
    MASTERY_LEVEL_UP = "mastery_level_up"
    DIFFICULTY_ADJUSTMENT = "difficulty_adjustment"
    SETTINGS_OPENED = "settings_opened"


@dataclass
class TutorialStep:
    """Individual step in a tutorial"""
    step_id: str
    title: str
    description: str
    instruction: str
    highlight_element: Optional[str] = None
    wait_for_action: Optional[str] = None
    auto_advance_delay: Optional[float] = None
    can_skip: bool = True


@dataclass
class Tutorial:
    """Complete tutorial definition"""
    tutorial_id: str
    name: str
    description: str
    trigger: TutorialTrigger
    priority: int
    prerequisites: List[str] = field(default_factory=list)
    steps: List[TutorialStep] = field(default_factory=list)
    repeatable: bool = False
    category: str = "basic"


class TutorialManager:
    """Manages player onboarding and tutorial systems"""
    
    def __init__(self):
        self.tutorials: Dict[str, Tutorial] = {}
        self.tutorial_progress: Dict[str, TutorialState] = {}
        self.current_tutorial: Optional[str] = None
        self.current_step: int = 0
        self.tutorial_enabled = True
        self.show_hints = True
        
        # Tutorial state
        self.active_highlights: List[str] = []
        self.pending_tutorials: List[str] = []
        self.tutorial_history: List[Dict[str, Any]] = []
        
        # Timing
        self.last_tutorial_time = 0
        self.tutorial_cooldown = 5.0  # seconds between tutorials
        
        # Initialize tutorials
        self._initialize_tutorials()
        
        logger.info("Tutorial Manager initialized")
    
    def _initialize_tutorials(self) -> None:
        """Initialize all tutorial definitions"""
        
        # Basic Game Tutorial
        basic_tutorial = Tutorial(
            tutorial_id="basic_gameplay",
            name="Basic Gameplay",
            description="Learn the fundamentals of the game",
            trigger=TutorialTrigger.GAME_START,
            priority=1,
            category="basic",
            steps=[
                TutorialStep(
                    step_id="welcome",
                    title="Welcome to the Rouge-like Adventure!",
                    description="This tutorial will teach you the basics",
                    instruction="Click anywhere to continue",
                    auto_advance_delay=3.0
                ),
                TutorialStep(
                    step_id="movement",
                    title="Movement",
                    description="Use WASD or arrow keys to move your character",
                    instruction="Try moving around",
                    wait_for_action="player_moved",
                    highlight_element="player"
                ),
                TutorialStep(
                    step_id="combat",
                    title="Combat",
                    description="Click to attack enemies",
                    instruction="Defeat your first enemy",
                    wait_for_action="enemy_killed",
                    highlight_element="enemies"
                ),
                TutorialStep(
                    step_id="items",
                    title="Items",
                    description="Collect items to improve your character",
                    instruction="Pick up an item",
                    wait_for_action="item_collected",
                    highlight_element="items"
                )
            ]
        )
        
        # Advanced Features Tutorial
        advanced_tutorial = Tutorial(
            tutorial_id="advanced_features",
            name="Advanced Features",
            description="Learn about enhanced enemies and special abilities",
            trigger=TutorialTrigger.LEVEL_3_REACHED,
            priority=2,
            prerequisites=["basic_gameplay"],
            category="advanced",
            steps=[
                TutorialStep(
                    step_id="enhanced_enemies",
                    title="Enhanced Enemies",
                    description="Starting from level 3, you'll encounter enhanced enemies with special abilities",
                    instruction="Be careful of their unique attack patterns",
                    auto_advance_delay=4.0
                ),
                TutorialStep(
                    step_id="elemental_damage",
                    title="Elemental Damage",
                    description="Enhanced enemies use elemental attacks: fire, ice, lightning, and more",
                    instruction="Watch for visual indicators of their element type",
                    auto_advance_delay=4.0
                ),
                TutorialStep(
                    step_id="status_effects",
                    title="Status Effects",
                    description="Some attacks can inflict status effects like burn, freeze, or poison",
                    instruction="Check your status bar for active effects",
                    highlight_element="status_bar"
                )
            ]
        )
        
        # Meta-Progression Tutorial
        meta_tutorial = Tutorial(
            tutorial_id="meta_progression",
            name="Meta-Progression",
            description="Learn about persistent progression between runs",
            trigger=TutorialTrigger.META_CURRENCY_EARNED,
            priority=3,
            prerequisites=["basic_gameplay"],
            category="progression",
            steps=[
                TutorialStep(
                    step_id="currencies",
                    title="Meta Currencies",
                    description="You've earned Soul Essence! This currency persists between runs",
                    instruction="Open the meta-progression panel to see your currencies",
                    wait_for_action="meta_panel_opened",
                    highlight_element="meta_panel"
                ),
                TutorialStep(
                    step_id="mastery",
                    title="Mastery System",
                    description="Gain experience in weapon and magic mastery for permanent bonuses",
                    instruction="Check your mastery progress",
                    highlight_element="mastery_panel"
                ),
                TutorialStep(
                    step_id="legacy",
                    title="Legacy Items",
                    description="Some items may carry over to your next run as legacy items",
                    instruction="Legacy items appear with a special glow",
                    auto_advance_delay=3.0
                )
            ]
        )
        
        # Dynamic Difficulty Tutorial
        difficulty_tutorial = Tutorial(
            tutorial_id="dynamic_difficulty",
            name="Dynamic Difficulty",
            description="Learn how the game adapts to your skill level",
            trigger=TutorialTrigger.DIFFICULTY_ADJUSTMENT,
            priority=4,
            category="systems",
            steps=[
                TutorialStep(
                    step_id="adaptive_system",
                    title="Adaptive Difficulty",
                    description="The game automatically adjusts difficulty based on your performance",
                    instruction="Check the difficulty indicator in the top-right",
                    highlight_element="difficulty_indicator"
                ),
                TutorialStep(
                    step_id="performance_tracking",
                    title="Performance Tracking",
                    description="The system tracks your accuracy, completion time, and survival rate",
                    instruction="Play naturally - the system will find the right challenge level",
                    auto_advance_delay=4.0
                ),
                TutorialStep(
                    step_id="challenge_modes",
                    title="Challenge Modes",
                    description="You can also enable special challenge modes for extra difficulty",
                    instruction="Access challenge modes through the settings menu",
                    highlight_element="settings_button"
                )
            ]
        )
        
        # Settings Tutorial
        settings_tutorial = Tutorial(
            tutorial_id="settings_overview",
            name="Settings Overview",
            description="Customize your game experience",
            trigger=TutorialTrigger.SETTINGS_OPENED,
            priority=5,
            category="interface",
            steps=[
                TutorialStep(
                    step_id="categories",
                    title="Settings Categories",
                    description="Settings are organized into categories: Graphics, Audio, Gameplay, and more",
                    instruction="Browse through the different categories",
                    auto_advance_delay=3.0
                ),
                TutorialStep(
                    step_id="accessibility",
                    title="Accessibility Options",
                    description="The game includes colorblind support, high contrast mode, and other accessibility features",
                    instruction="Check the Accessibility category for options",
                    highlight_element="accessibility_category"
                ),
                TutorialStep(
                    step_id="controls",
                    title="Control Customization",
                    description="You can customize controls and key bindings to your preference",
                    instruction="Visit the Controls category to customize",
                    highlight_element="controls_category"
                )
            ]
        )
        
        # Register all tutorials
        tutorials = [basic_tutorial, advanced_tutorial, meta_tutorial, 
                    difficulty_tutorial, settings_tutorial]
        
        for tutorial in tutorials:
            self.tutorials[tutorial.tutorial_id] = tutorial
            self.tutorial_progress[tutorial.tutorial_id] = TutorialState.NOT_STARTED
    
    def trigger_tutorial(self, trigger: TutorialTrigger, context: Dict[str, Any] = None) -> bool:
        """Trigger tutorials based on game events"""
        if not self.tutorial_enabled:
            return False
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_tutorial_time < self.tutorial_cooldown:
            return False
        
        # Find tutorials for this trigger
        triggered_tutorials = []
        for tutorial_id, tutorial in self.tutorials.items():
            if (tutorial.trigger == trigger and 
                self.tutorial_progress[tutorial_id] == TutorialState.NOT_STARTED and
                self._check_prerequisites(tutorial)):
                triggered_tutorials.append(tutorial)
        
        if not triggered_tutorials:
            return False
        
        # Sort by priority and start the highest priority tutorial
        triggered_tutorials.sort(key=lambda t: t.priority)
        tutorial_to_start = triggered_tutorials[0]
        
        return self.start_tutorial(tutorial_to_start.tutorial_id, context)
    
    def start_tutorial(self, tutorial_id: str, context: Dict[str, Any] = None) -> bool:
        """Start a specific tutorial"""
        if tutorial_id not in self.tutorials:
            logger.warning(f"Unknown tutorial: {tutorial_id}")
            return False
        
        tutorial = self.tutorials[tutorial_id]
        
        # Check if already in progress or completed
        if self.tutorial_progress[tutorial_id] in [TutorialState.IN_PROGRESS, TutorialState.COMPLETED]:
            if not tutorial.repeatable:
                return False
        
        # Check prerequisites
        if not self._check_prerequisites(tutorial):
            logger.info(f"Prerequisites not met for tutorial: {tutorial_id}")
            return False
        
        # Start tutorial
        self.current_tutorial = tutorial_id
        self.current_step = 0
        self.tutorial_progress[tutorial_id] = TutorialState.IN_PROGRESS
        self.last_tutorial_time = time.time()
        
        # Record in history
        self.tutorial_history.append({
            'tutorial_id': tutorial_id,
            'started_time': time.time(),
            'context': context or {}
        })
        
        logger.info(f"Started tutorial: {tutorial_id}")
        return True
    
    def advance_tutorial(self) -> bool:
        """Advance to the next step in the current tutorial"""
        if not self.current_tutorial:
            return False
        
        tutorial = self.tutorials[self.current_tutorial]
        
        # Check if we're at the last step
        if self.current_step >= len(tutorial.steps) - 1:
            return self.complete_tutorial()
        
        # Advance to next step
        self.current_step += 1
        logger.debug(f"Advanced tutorial {self.current_tutorial} to step {self.current_step}")
        return True
    
    def complete_tutorial(self) -> bool:
        """Complete the current tutorial"""
        if not self.current_tutorial:
            return False
        
        tutorial_id = self.current_tutorial
        self.tutorial_progress[tutorial_id] = TutorialState.COMPLETED
        
        # Update history
        for entry in reversed(self.tutorial_history):
            if entry['tutorial_id'] == tutorial_id and 'completed_time' not in entry:
                entry['completed_time'] = time.time()
                entry['duration'] = entry['completed_time'] - entry['started_time']
                break
        
        # Clear current tutorial
        self.current_tutorial = None
        self.current_step = 0
        self.active_highlights.clear()
        
        logger.info(f"Completed tutorial: {tutorial_id}")
        return True
    
    def skip_tutorial(self) -> bool:
        """Skip the current tutorial"""
        if not self.current_tutorial:
            return False
        
        tutorial_id = self.current_tutorial
        tutorial = self.tutorials[tutorial_id]
        current_step = tutorial.steps[self.current_step] if self.current_step < len(tutorial.steps) else None
        
        # Check if current step can be skipped
        if current_step and not current_step.can_skip:
            return False
        
        self.tutorial_progress[tutorial_id] = TutorialState.SKIPPED
        
        # Update history
        for entry in reversed(self.tutorial_history):
            if entry['tutorial_id'] == tutorial_id and 'completed_time' not in entry:
                entry['skipped_time'] = time.time()
                entry['duration'] = entry['skipped_time'] - entry['started_time']
                break
        
        # Clear current tutorial
        self.current_tutorial = None
        self.current_step = 0
        self.active_highlights.clear()
        
        logger.info(f"Skipped tutorial: {tutorial_id}")
        return True
    
    def _check_prerequisites(self, tutorial: Tutorial) -> bool:
        """Check if tutorial prerequisites are met"""
        for prereq in tutorial.prerequisites:
            if (prereq not in self.tutorial_progress or 
                self.tutorial_progress[prereq] != TutorialState.COMPLETED):
                return False
        return True
    
    def get_current_tutorial_step(self) -> Optional[TutorialStep]:
        """Get the current tutorial step"""
        if not self.current_tutorial:
            return None
        
        tutorial = self.tutorials[self.current_tutorial]
        if self.current_step >= len(tutorial.steps):
            return None
        
        return tutorial.steps[self.current_step]
    
    def get_current_tutorial_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current tutorial"""
        if not self.current_tutorial:
            return None
        
        tutorial = self.tutorials[self.current_tutorial]
        current_step = self.get_current_tutorial_step()
        
        return {
            'tutorial_id': self.current_tutorial,
            'tutorial_name': tutorial.name,
            'current_step': self.current_step,
            'total_steps': len(tutorial.steps),
            'step_info': {
                'title': current_step.title,
                'description': current_step.description,
                'instruction': current_step.instruction,
                'can_skip': current_step.can_skip
            } if current_step else None,
            'progress_percentage': (self.current_step / len(tutorial.steps)) * 100
        }
    
    def handle_game_event(self, event_type: str, event_data: Dict[str, Any] = None) -> None:
        """Handle game events for tutorial progression"""
        current_step = self.get_current_tutorial_step()
        if not current_step:
            return
        
        # Check if this event advances the tutorial
        if current_step.wait_for_action == event_type:
            self.advance_tutorial()
    
    def update(self, delta_time: float) -> None:
        """Update tutorial system"""
        current_step = self.get_current_tutorial_step()
        if not current_step:
            return
        
        # Handle auto-advance
        if current_step.auto_advance_delay:
            # This would need to track timing for auto-advance
            pass
    
    def set_tutorial_enabled(self, enabled: bool) -> None:
        """Enable or disable tutorials"""
        self.tutorial_enabled = enabled
        if not enabled and self.current_tutorial:
            self.skip_tutorial()
    
    def reset_tutorial_progress(self, tutorial_id: Optional[str] = None) -> None:
        """Reset tutorial progress"""
        if tutorial_id:
            if tutorial_id in self.tutorial_progress:
                self.tutorial_progress[tutorial_id] = TutorialState.NOT_STARTED
        else:
            # Reset all tutorials
            for tutorial_id in self.tutorial_progress:
                self.tutorial_progress[tutorial_id] = TutorialState.NOT_STARTED
        
        # Clear current tutorial if it was reset
        if tutorial_id == self.current_tutorial or tutorial_id is None:
            self.current_tutorial = None
            self.current_step = 0
            self.active_highlights.clear()
    
    def get_tutorial_statistics(self) -> Dict[str, Any]:
        """Get tutorial completion statistics"""
        total_tutorials = len(self.tutorials)
        completed = sum(1 for state in self.tutorial_progress.values() 
                       if state == TutorialState.COMPLETED)
        skipped = sum(1 for state in self.tutorial_progress.values() 
                     if state == TutorialState.SKIPPED)
        
        return {
            'total_tutorials': total_tutorials,
            'completed': completed,
            'skipped': skipped,
            'completion_rate': (completed / total_tutorials) * 100 if total_tutorials > 0 else 0,
            'tutorials_seen': completed + skipped,
            'current_tutorial': self.current_tutorial,
            'tutorial_enabled': self.tutorial_enabled
        }
    
    def export_progress(self) -> Dict[str, Any]:
        """Export tutorial progress for saving"""
        return {
            'tutorial_progress': {k: v.value for k, v in self.tutorial_progress.items()},
            'tutorial_history': self.tutorial_history,
            'tutorial_enabled': self.tutorial_enabled,
            'show_hints': self.show_hints
        }
    
    def import_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Import tutorial progress from save data"""
        try:
            # Import progress states
            if 'tutorial_progress' in progress_data:
                for tutorial_id, state_value in progress_data['tutorial_progress'].items():
                    if tutorial_id in self.tutorial_progress:
                        self.tutorial_progress[tutorial_id] = TutorialState(state_value)
            
            # Import history
            if 'tutorial_history' in progress_data:
                self.tutorial_history = progress_data['tutorial_history']
            
            # Import settings
            if 'tutorial_enabled' in progress_data:
                self.tutorial_enabled = progress_data['tutorial_enabled']
            
            if 'show_hints' in progress_data:
                self.show_hints = progress_data['show_hints']
            
            logger.info("Tutorial progress imported successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import tutorial progress: {e}")
            return False
