"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================ 
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================ 

def create_character(name, character_class):
    """
    Create a new character with stats based on class.
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns:
        Dictionary with character data including:
        - name, class, level, health, max_health, strength, magic
        - experience, gold, inventory, active_quests, completed_quests
    
    Raises:
        InvalidCharacterClassError: if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    # Before creating the character, check if the class exists
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    stats = valid_classes[character_class]
    # Build the character as a dictionary
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ============================================================================ 
# SAVE / LOAD FUNCTIONS
# ============================================================================ 

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file.
    
    Filename format: {character_name}_save.txt
    
    Returns:
        True if successful
    
    Raises:
        PermissionError, IOError: if file cannot be written
    """
    # TODO: Implement save functionality
    # Make sure the save folder exists. If it doesn't, Python creates it.
    # 'exist_ok=True' prevents errors if the folder is already there.
    validate_character_data(character)
    os.makedirs(save_directory, exist_ok=True)  # used ai to import directories


    # Create a file name using the character's name.
    filename = f"{character['name']}_save.txt"

    # Join the folder path and file name into a full file path.
    filepath = os.path.join(save_directory, filename)

    # Convert lists into simple comma-separated text.
    # Text files can't store lists directly, so I turn them into strings.
    inventory_str = ",".join(character["inventory"])
    active_quests_str = ",".join(character["active_quests"])
    completed_quests_str = ",".join(character["completed_quests"])

    # Open the file in write mode ("w"). If the file doesn't exist, Python creates it.
    # Using 'with' automatically closes the file when we're done.
    with open(filepath, "w") as f:
        f.write(f"NAME: {character['name']}\n")
        f.write(f"CLASS: {character['class']}\n")
        f.write(f"LEVEL: {character['level']}\n")
        f.write(f"HEALTH: {character['health']}\n")
        f.write(f"MAX_HEALTH: {character['max_health']}\n")
        f.write(f"STRENGTH: {character['strength']}\n")
        f.write(f"MAGIC: {character['magic']}\n")
        f.write(f"EXPERIENCE: {character['experience']}\n")
        f.write(f"GOLD: {character['gold']}\n")
        f.write(f"INVENTORY: {inventory_str}\n")
        f.write(f"ACTIVE_QUESTS: {active_quests_str}\n")
        f.write(f"COMPLETED_QUESTS: {completed_quests_str}\n")

    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file.
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns:
        Character dictionary
    
    Raises: 
        CharacterNotFoundError: if save file doesn't exist
        SaveFileCorruptedError: if file cannot be read
        InvalidSaveDataError: if data format is wrong
    """
    # TODO: Implement load functionality
    # Build the full path to the character's save file
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # Check if the file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file for '{character_name}' not found.")

    # Try to read the file
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(f"Could not read save file: {e}")

    # List of all fields we expect to find in a save file
    expected_keys = {
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
    }

    data = {}  # empty dictionary for key values

    # check for mistakes
    for line in lines:
        if ":" not in line:
            # If a line doesn't have a colon, the file is broken
            raise InvalidSaveDataError("Malformed line in save file.")

        # Split the line into key and value at the first colon
        key, value = line.strip().split(":", 1)
        key, value = key.strip(), value.strip()  # Remove extra spaces

        # Check if the key is one of the expected fields
        if key not in expected_keys:
            raise InvalidSaveDataError(f"Unexpected key in save file: {key}")

        data[key] = value  # Store the value in the dictionary

    # Make sure all required fields are present
    missing_fields = expected_keys - data.keys()
    if missing_fields:
        raise InvalidSaveDataError(f"Missing fields in save data: {missing_fields}")

    # Convert text values to the correct types
    try:
        character = {
            "name": data["NAME"],  # Already text
            "class": data["CLASS"],  # Already text
            "level": int(data["LEVEL"]),  # Convert string to integer
            "health": int(data["HEALTH"]),  # Convert string to integer
            "max_health": int(data["MAX_HEALTH"]),  # Convert string to integer
            "strength": int(data["STRENGTH"]),  # Convert string to integer
            "magic": int(data["MAGIC"]),  # Convert string to integer
            "experience": int(data["EXPERIENCE"]),  # Convert string to integer
            "gold": int(data["GOLD"]),  # Convert string to integer
            # Convert comma-separated strings back to lists. If empty, use empty list
            "inventory": data["INVENTORY"].split(",") if data["INVENTORY"] else [],
            "active_quests": data["ACTIVE_QUESTS"].split(",") if data["ACTIVE_QUESTS"] else [],
            "completed_quests": data["COMPLETED_QUESTS"].split(",") if data["COMPLETED_QUESTS"] else []
        }
    except ValueError:
        # If conversion fails, the save file has bad numbers
        raise InvalidSaveDataError("Numeric fields in save data contain invalid values.")

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names.
    
    Returns:
        List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    import os  # Needed to work with folders and files

    # If the save folder does not exist, return an empty list
    if not os.path.exists(save_directory):
        return []

    # List all files in the save folder
    files = os.listdir(save_directory)

    # Filter only files that end with "_save.txt" and remove that suffix
    character_names = [f[:-9] for f in files if f.endswith("_save.txt")]

    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file.
    
    Returns:
        True if deleted successfully
    
    Raises:
        CharacterNotFoundError: if character doesn't exist
    """
    # TODO: Implement character deletion
    import os  # Needed to work with files

    # Build the path to the character's save file
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # Check if the file exists
    if not os.path.exists(filepath):
        # Raise an error if the character save does not exist
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")

    # Delete the file
    os.remove(filepath)

    return True  # Return True to indicate deletion was successful



# ============================================================================ 
# CHARACTER OPERATIONS
# ============================================================================ 

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups.
    
    Level up formula: level_up_xp = current_level * 100
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain XP.")

    character['experience'] += xp_amount
    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['health'] = character['max_health']


def add_gold(character, amount):
    """
    Add gold to character's inventory.
    
    Args:
        amount: Amount of gold to add (negative to spend)
    
    Returns:
        New gold total
    
    Raises:
        ValueError: if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_gold = character['gold'] + amount
    if new_gold < 0:
        raise ValueError("Not enough gold to spend.")
    character['gold'] = new_gold
    return new_gold


def heal_character(character, amount):
    """
    Heal character by specified amount.
    
    Health cannot exceed max_health.
    
    Returns:
        Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot be healed.")
    heal_amount = min(amount, character['max_health'] - character['health'])
    character['health'] += heal_amount
    return heal_amount

def is_character_dead(character):
    """
    Check if character's health is 0 or below.
    
    Returns:
        True if dead, False if alive
    """
    # TODO: Implement death check
    return character['health'] <= 0


def revive_character(character):
    """
    Revive a dead character with 50% health.
    
    Returns:
        True if revived, False if already alive
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if character['health'] > 0:
        return False
    character['health'] = max(1, character['max_health'] // 2)
    return True


# ============================================================================ 
# VALIDATION
# ============================================================================ 

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields.
    
    Returns:
        True if valid
    
    Raises:
        InvalidSaveDataError: if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    for key in required_fields:
        if key not in character:
            raise InvalidSaveDataError(f"Missing required field: {key}")

    numeric_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for key in numeric_fields:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"Field {key} must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for key in list_fields:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"Field {key} must be a list")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

