"""
Meta-Progression System for Phase 3

This module handles persistent progression that carries over between runs:
- Legacy system for equipment and skill inheritance
- Meta currencies (Soul Essence, Knowledge Crystals, Fate Tokens)
- Unlock progression for new content
- Mastery systems for weapons and magic
- Prestige system for advanced players
"""

import pygame
import json
import logging
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from config import META_PROGRESSION_CONFIG
from utils.constants import *

logger = logging.getLogger(__name__)


@dataclass
class MetaCurrency:
    """Represents a meta-progression currency"""
    name: str
    amount: int = 0
    lifetime_earned: int = 0
    
    def add(self, amount: int) -> None:
        """Add currency amount"""
        self.amount += amount
        self.lifetime_earned += amount
        
    def spend(self, amount: int) -> bool:
        """Spend currency if available"""
        if self.amount >= amount:
            self.amount -= amount
            return True
        return False


@dataclass
class MasteryProgress:
    """Represents mastery progress in a specific area"""
    mastery_type: str
    level: int = 0
    experience: int = 0
    unlocked_abilities: List[str] = None
    
    def __post_init__(self):
        if self.unlocked_abilities is None:
            self.unlocked_abilities = []


@dataclass
class LegacyItem:
    """Represents an item that can be inherited"""
    item_type: str
    item_data: Dict[str, Any]
    inheritance_chance: float
    source_run: int
    
    
class MetaProgressionManager:
    """Manages all meta-progression systems"""
    
    def __init__(self, save_file: str = "meta_progression.json"):
        self.save_file = save_file
        self.config = META_PROGRESSION_CONFIG
        
        # Meta currencies
        self.currencies: Dict[str, MetaCurrency] = {}
        self._initialize_currencies()
        
        # Mastery systems
        self.masteries: Dict[str, MasteryProgress] = {}
        self._initialize_masteries()
        
        # Legacy system
        self.legacy_items: List[LegacyItem] = []
        self.memory_fragments: List[Dict[str, Any]] = []
        
        # Unlock progression
        self.unlocked_biomes: List[str] = []
        self.unlocked_enemies: List[str] = []
        self.unlocked_features: List[str] = []
        
        # Prestige system
        self.prestige_level: int = 0
        self.prestige_experience: int = 0
        
        # Statistics
        self.total_runs: int = 0
        self.successful_runs: int = 0
        self.total_playtime: int = 0  # in seconds
        self.deepest_level_reached: int = 0
        
        # Load existing data
        self.load_meta_progression()
        
    def _initialize_currencies(self) -> None:
        """Initialize meta currencies"""
        currency_configs = self.config.get('meta_currencies', {})
        
        for currency_name in currency_configs:
            if currency_name not in self.currencies:
                self.currencies[currency_name] = MetaCurrency(currency_name)
                
    def _initialize_masteries(self) -> None:
        """Initialize mastery systems"""
        mastery_configs = self.config.get('mastery_system', {})
        
        for mastery_type in mastery_configs:
            if mastery_type not in self.masteries:
                self.masteries[mastery_type] = MasteryProgress(mastery_type)
                
    def add_currency(self, currency_type: str, amount: int, reason: str = "") -> None:
        """Add meta currency"""
        if currency_type in self.currencies:
            self.currencies[currency_type].add(amount)
            logger.info(f"Added {amount} {currency_type} ({reason})")
            
    def spend_currency(self, currency_type: str, amount: int, purpose: str = "") -> bool:
        """Spend meta currency"""
        if currency_type in self.currencies:
            success = self.currencies[currency_type].spend(amount)
            if success:
                logger.info(f"Spent {amount} {currency_type} ({purpose})")
            return success
        return False
        
    def get_currency_amount(self, currency_type: str) -> int:
        """Get current amount of a currency"""
        return self.currencies.get(currency_type, MetaCurrency(currency_type)).amount
        
    def add_mastery_experience(self, mastery_type: str, experience: int) -> bool:
        """Add experience to a mastery and check for level up"""
        if mastery_type not in self.masteries:
            return False
            
        mastery = self.masteries[mastery_type]
        mastery.experience += experience
        
        # Check for level up
        mastery_config = self.config.get('mastery_system', {}).get(mastery_type, {})
        max_level = mastery_config.get('max_level', 100)
        
        if mastery.level < max_level:
            # Simple linear progression: level * 100 experience per level
            required_exp = (mastery.level + 1) * 100
            
            if mastery.experience >= required_exp:
                mastery.level += 1
                mastery.experience -= required_exp
                
                # Check for special unlocks
                special_unlocks = mastery_config.get('special_unlocks', {})
                if mastery.level in special_unlocks:
                    unlock_name = special_unlocks[mastery.level]
                    if unlock_name not in mastery.unlocked_abilities:
                        mastery.unlocked_abilities.append(unlock_name)
                        logger.info(f"Unlocked {unlock_name} for {mastery_type} mastery level {mastery.level}")
                
                logger.info(f"{mastery_type} mastery leveled up to {mastery.level}")
                return True
                
        return False
        
    def get_mastery_bonuses(self, mastery_type: str) -> Dict[str, float]:
        """Get current bonuses from a mastery"""
        if mastery_type not in self.masteries:
            return {}
            
        mastery = self.masteries[mastery_type]
        mastery_config = self.config.get('mastery_system', {}).get(mastery_type, {})
        bonuses_per_level = mastery_config.get('bonuses_per_level', {})
        
        bonuses = {}
        for bonus_type, bonus_per_level in bonuses_per_level.items():
            bonuses[bonus_type] = bonus_per_level * mastery.level
            
        return bonuses
        
    def add_legacy_item(self, item_type: str, item_data: Dict[str, Any], 
                       inheritance_chance: float = None) -> None:
        """Add an item to the legacy system"""
        if not self.config.get('legacy_system', {}).get('enabled', False):
            return
            
        if inheritance_chance is None:
            inheritance_chance = self.config.get('legacy_system', {}).get('equipment_inheritance_chance', 0.1)
            
        legacy_item = LegacyItem(
            item_type=item_type,
            item_data=item_data,
            inheritance_chance=inheritance_chance,
            source_run=self.total_runs
        )
        
        self.legacy_items.append(legacy_item)
        
        # Limit legacy items to prevent bloat
        max_legacy_items = 50
        if len(self.legacy_items) > max_legacy_items:
            # Remove oldest items with lowest inheritance chance
            self.legacy_items.sort(key=lambda x: (x.inheritance_chance, -x.source_run))
            self.legacy_items = self.legacy_items[-max_legacy_items:]
            
    def get_inherited_items(self) -> List[Dict[str, Any]]:
        """Get items that should be inherited for the new run"""
        inherited = []
        
        for legacy_item in self.legacy_items:
            if random.random() < legacy_item.inheritance_chance:
                inherited.append(legacy_item.item_data.copy())
                
        return inherited
        
    def unlock_content(self, content_type: str, content_name: str, cost: int = 0) -> bool:
        """Unlock new content using meta currencies"""
        unlock_configs = self.config.get('unlock_progression', {})
        
        if content_type == 'biome_unlocks':
            if content_name in self.unlocked_biomes:
                return False
                
            unlock_config = unlock_configs.get('biome_unlocks', {}).get(content_name, {})
            required_cost = unlock_config.get('cost', cost)
            
            # For now, use knowledge_crystals as the primary unlock currency
            if self.spend_currency('knowledge_crystals', required_cost, f"unlock {content_name}"):
                self.unlocked_biomes.append(content_name)
                logger.info(f"Unlocked biome: {content_name}")
                return True
                
        elif content_type == 'enemy_unlocks':
            if content_name in self.unlocked_enemies:
                return False
                
            unlock_config = unlock_configs.get('enemy_unlocks', {}).get(content_name, {})
            required_cost = unlock_config.get('cost', cost)
            
            if self.spend_currency('soul_essence', required_cost, f"unlock {content_name}"):
                self.unlocked_enemies.append(content_name)
                logger.info(f"Unlocked enemy: {content_name}")
                return True
                
        return False
        
    def add_prestige_experience(self, amount: int) -> bool:
        """Add prestige experience and check for prestige level up"""
        if not self.config.get('prestige_system', {}).get('enabled', False):
            return False
            
        self.prestige_experience += amount
        
        prestige_config = self.config.get('prestige_system', {})
        requirements = prestige_config.get('requirements_per_level', [])
        max_prestige = len(requirements)
        
        if self.prestige_level < max_prestige:
            required_exp = requirements[self.prestige_level]
            
            if self.prestige_experience >= required_exp:
                self.prestige_level += 1
                self.prestige_experience -= required_exp
                logger.info(f"Prestige level increased to {self.prestige_level}")
                return True
                
        return False
        
    def get_prestige_bonuses(self) -> Dict[str, float]:
        """Get bonuses from prestige levels"""
        if self.prestige_level == 0:
            return {}
            
        prestige_config = self.config.get('prestige_system', {})
        bonuses_per_prestige = prestige_config.get('bonuses_per_prestige', {})
        
        bonuses = {}
        for bonus_type, bonus_per_level in bonuses_per_prestige.items():
            bonuses[bonus_type] = bonus_per_level * self.prestige_level
            
        return bonuses
        
    def on_run_start(self) -> None:
        """Called when a new run starts"""
        self.total_runs += 1
        
    def on_run_end(self, successful: bool, level_reached: int, playtime: int) -> None:
        """Called when a run ends"""
        if successful:
            self.successful_runs += 1
            
        self.total_playtime += playtime
        self.deepest_level_reached = max(self.deepest_level_reached, level_reached)
        
        # Award currencies based on performance
        self._award_run_completion_currencies(successful, level_reached, playtime)
        
        # Add prestige experience
        prestige_exp = level_reached * 10
        if successful:
            prestige_exp *= 2
        self.add_prestige_experience(prestige_exp)
        
    def _award_run_completion_currencies(self, successful: bool, level_reached: int, playtime: int) -> None:
        """Award currencies at the end of a run"""
        # Soul essence based on level reached
        soul_essence = level_reached * 5
        if successful:
            soul_essence *= 2
        self.add_currency('soul_essence', soul_essence, "run completion")
        
        # Knowledge crystals for discoveries and bosses
        knowledge_crystals = level_reached // 5  # Every 5 levels
        if successful:
            knowledge_crystals += 10  # Bonus for completion
        self.add_currency('knowledge_crystals', knowledge_crystals, "discoveries and bosses")
        
        # Fate tokens for exceptional performance
        if successful and level_reached >= 20:
            self.add_currency('fate_tokens', 1, "exceptional run")
        elif level_reached >= 50:
            self.add_currency('fate_tokens', 1, "deep exploration")
            
    def get_meta_progression_summary(self) -> Dict[str, Any]:
        """Get a summary of all meta progression"""
        return {
            'currencies': {name: currency.amount for name, currency in self.currencies.items()},
            'masteries': {name: {'level': mastery.level, 'experience': mastery.experience} 
                         for name, mastery in self.masteries.items()},
            'prestige_level': self.prestige_level,
            'prestige_experience': self.prestige_experience,
            'unlocked_content': {
                'biomes': len(self.unlocked_biomes),
                'enemies': len(self.unlocked_enemies),
                'features': len(self.unlocked_features)
            },
            'statistics': {
                'total_runs': self.total_runs,
                'successful_runs': self.successful_runs,
                'success_rate': self.successful_runs / max(1, self.total_runs) * 100,
                'total_playtime': self.total_playtime,
                'deepest_level': self.deepest_level_reached
            }
        }
        
    def save_meta_progression(self) -> bool:
        """Save meta progression to file"""
        try:
            data = {
                'currencies': {name: asdict(currency) for name, currency in self.currencies.items()},
                'masteries': {name: asdict(mastery) for name, mastery in self.masteries.items()},
                'legacy_items': [asdict(item) for item in self.legacy_items],
                'memory_fragments': self.memory_fragments,
                'unlocked_biomes': self.unlocked_biomes,
                'unlocked_enemies': self.unlocked_enemies,
                'unlocked_features': self.unlocked_features,
                'prestige_level': self.prestige_level,
                'prestige_experience': self.prestige_experience,
                'total_runs': self.total_runs,
                'successful_runs': self.successful_runs,
                'total_playtime': self.total_playtime,
                'deepest_level_reached': self.deepest_level_reached,
                'version': '3.0'
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info("Meta progression saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save meta progression: {e}")
            return False
            
    def load_meta_progression(self) -> bool:
        """Load meta progression from file"""
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                
            # Load currencies
            currencies_data = data.get('currencies', {})
            for name, currency_data in currencies_data.items():
                self.currencies[name] = MetaCurrency(**currency_data)
                
            # Load masteries
            masteries_data = data.get('masteries', {})
            for name, mastery_data in masteries_data.items():
                self.masteries[name] = MasteryProgress(**mastery_data)
                
            # Load legacy items
            legacy_items_data = data.get('legacy_items', [])
            self.legacy_items = [LegacyItem(**item_data) for item_data in legacy_items_data]
            
            # Load other data
            self.memory_fragments = data.get('memory_fragments', [])
            self.unlocked_biomes = data.get('unlocked_biomes', [])
            self.unlocked_enemies = data.get('unlocked_enemies', [])
            self.unlocked_features = data.get('unlocked_features', [])
            self.prestige_level = data.get('prestige_level', 0)
            self.prestige_experience = data.get('prestige_experience', 0)
            self.total_runs = data.get('total_runs', 0)
            self.successful_runs = data.get('successful_runs', 0)
            self.total_playtime = data.get('total_playtime', 0)
            self.deepest_level_reached = data.get('deepest_level_reached', 0)
            
            logger.info("Meta progression loaded successfully")
            return True
            
        except FileNotFoundError:
            logger.info("No meta progression file found, starting fresh")
            return True
        except Exception as e:
            logger.error(f"Failed to load meta progression: {e}")
            return False
