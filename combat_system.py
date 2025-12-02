"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================  
# ENEMY DEFINITIONS  
# ============================================================================  

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    if enemy_type.lower() == "goblin":
        enemy = {
            'name': 'Goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type.lower() == "orc":
        enemy = {
            'name': 'Orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type.lower() == "dragon":
        enemy = {
            'name': 'Dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        # Raise error if the enemy type is not recognized
        raise InvalidTargetError(f"Enemy type '{enemy_type}' is invalid.")
    
    # Return the created enemy dictionary
    return enemy
    

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    
    # Create and return enemy using create_enemy()
    return create_enemy(enemy_type)
    

# ============================================================================  
# COMBAT SYSTEM  
# ============================================================================  

class SimpleBattle:
    """
    Simple turn-based combat system
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        self.character = character  # Store reference to player's character
        self.enemy = enemy          # Store reference to enemy
        self.combat_active = True   # Flag to track if battle is ongoing
        self.turn_counter = 0       # Count turns to manage abilities or AI
        # Track special ability cooldowns
        self.character.setdefault('special_cooldown', 0)
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is already dead!")
        
        # Battle loop continues until someone dies or player escapes
        while self.combat_active:
            # Decrement cooldowns at start of turn
            if self.character.get('special_cooldown', 0) > 0:
                self.character['special_cooldown'] -= 1
            
            # Player acts first
            self.player_turn()
            if not self.combat_active:  # Could have escaped
                break
            winner = self.check_battle_end()
            if winner:
                break
            
            # Enemy acts next
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                break
            
            self.turn_counter += 1  # Increment turn counter for tracking purposes
        
        # Determine outcome
        winner = self.check_battle_end()
        if winner == 'player':
            rewards = get_victory_rewards(self.enemy)
            self.character['xp'] = self.character.get('xp', 0) + rewards['xp']
            self.character['gold'] = self.character.get('gold', 0) + rewards['gold']
            return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
        elif winner == 'enemy':
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
        else:
            return {'winner': 'escaped', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self, action=None):
        """
        Handle player's turn
        action: 'attack', 'special', 'run' (deterministic for testing)
        """
        # TODO: Implement player turn
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take a turn, combat is not active.")
        
        # Display combat stats
        display_combat_stats(self.character, self.enemy)
        
        # For deterministic behavior during tests
        if action is None:
            action = 'attack'  # default action for non-demo purposes
        
        if action == 'attack':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage!")
        elif action == 'special':
            if self.character.get('special_cooldown', 0) > 0:
                raise AbilityOnCooldownError("Ability is on cooldown.")
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
            self.character['special_cooldown'] = 3  # Example: 3-turn cooldown
        elif action == 'run':
            if self.attempt_escape(force_result=True):  # force success in deterministic mode
                display_battle_log(f"{self.character['name']} successfully escaped!")
            else:
                display_battle_log(f"{self.character['name']} failed to escape.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        """
        # TODO: Implement enemy turn
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take a turn, combat is not active.")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        """
        # TODO: Implement damage calculation
        # Formula: attacker's strength minus 1/4 of defender's strength
        damage = attacker['strength'] - (defender['strength'] // 4)
        return max(1, damage)  # Minimum damage is always 1
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        """
        # TODO: Implement damage application
        target['health'] = max(0, target['health'] - damage)  # Prevent negative HP
    
    def check_battle_end(self):
        """
        Check if battle is over
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        elif self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        return None
    
    def attempt_escape(self, force_result=None):
        """
        Try to escape from battle
        force_result: True/False for deterministic testing
        """
        # TODO: Implement escape attempt
        if force_result is not None:
            success = force_result
        else:
            success = random.random() < 0.5  # 50% chance normally
        if success:
            self.combat_active = False
        return success

# ============================================================================  
# SPECIAL ABILITIES  
# ============================================================================  

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    """
    # TODO: Implement special abilities
    char_class = character['class'].lower()
    if char_class == 'warrior':
        return warrior_power_strike(character, enemy)
    elif char_class == 'mage':
        return mage_fireball(character, enemy)
    elif char_class == 'rogue':
        return rogue_critical_strike(character, enemy)
    elif char_class == 'cleric':
        return cleric_heal(character)
    else:
        return f"{character['name']} has no special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    damage = character['strength'] * 2
    enemy['health'] = max(0, enemy['health'] - damage)
    return f"{character['name']} uses Power Strike on {enemy['name']} for {damage} damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    damage = character['magic'] * 2
    enemy['health'] = max(0, enemy['health'] - damage)
    return f"{character['name']} casts Fireball on {enemy['name']} for {damage} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    damage = character['strength'] * 3
    enemy['health'] = max(0, enemy['health'] - damage)
    return f"{character['name']} lands a Critical Strike on {enemy['name']} for {damage} damage!"

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    heal_amount = 30
    character['health'] = min(character['max_health'], character['health'] + heal_amount)
    return f"{character['name']} heals for {heal_amount} HP!"

# ============================================================================  
# COMBAT UTILITIES  
# ============================================================================  

def can_character_fight(character):
    """
    Check if character is in condition to fight
    """
    # TODO: Implement fight check
    return character['health'] > 0  # Simple check, could add battle flag

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    """
    # TODO: Implement reward calculation
    return {'xp': enemy.get('xp_reward', 0), 'gold': enemy.get('gold_reward', 0)}

def display_combat_stats(character, enemy):
    """
    Display current combat status
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================  
# TESTING  
# ============================================================================  

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        # deterministic testing: always attack
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")


