"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager 
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================ 
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================ 
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid input. Please select 1, 2, or 3.")

def new_game():
    """
    Start a new game by creating a character
    """
    global current_character
    
    print("\n=== NEW GAME ===")
    name = input("Enter character name: ").strip()
    
    # Loop until a valid class is selected
    while True:
        char_class = input("Choose class (Warrior/Mage/Rogue/Cleric): ").strip()
        try:
            current_character = character_manager.create_character(name, char_class)
            print(f"Character '{name}' ({char_class}) created successfully!")
            break
        except InvalidCharacterClassError as e:
            print(f"Error: {e}. Please choose a valid class.")
    
    # Start game loop for the new character
    game_loop()

def load_game():
    """
    Load an existing saved game
    """
    global current_character
    
    print("\n=== LOAD GAME ===")
    
    saved_chars = character_manager.list_saved_characters()
    if not saved_chars:
        print("No saved characters found.")
        return
    
    # Display saved characters
    print("Saved Characters:")
    for i, char_name in enumerate(saved_chars, start=1):
        print(f"{i}. {char_name}")
    
    while True:
        choice = input(f"Select character to load (1-{len(saved_chars)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved_chars):
            idx = int(choice) - 1
            char_name = saved_chars[idx]
            try:
                current_character = character_manager.load_character(char_name)
                print(f"Character '{char_name}' loaded successfully!")
                break
            except (CharacterNotFoundError, SaveFileCorruptedError) as e:
                print(f"Error loading character: {e}")
        else:
            print("Invalid selection. Please choose a valid number.")
    
    game_loop()

# ============================================================================ 
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - displays game menu and processes player actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select 1-6.")

def game_menu():
    """
    Display in-game menu and get player choice
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in [str(i) for i in range(1, 7)]:
            return int(choice)
        else:
            print("Invalid input. Please select a number between 1 and 6.")

# ============================================================================ 
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """
    Display character information
    """
    global current_character
    
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character.get('level', 1)}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character.get('strength', 0)}")
    print(f"Magic: {current_character.get('magic', 0)}")
    print(f"Gold: {current_character.get('gold', 0)}")
    
    # Display quest progress
    active_quests = quest_handler.get_active_quests(current_character)
    print(f"Active Quests: {len(active_quests)}")
    for q in active_quests:
        print(f"- {q['title']}")

def view_inventory():
    """
    Display and manage inventory
    """
    global current_character, all_items
    
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)
    
    print("\nOptions:")
    print("1. Use item")
    print("2. Equip weapon")
    print("3. Equip armor")
    print("4. Drop item")
    print("5. Back")
    
    choice = input("Select an option: ").strip()
    
    if choice == '1':
        item_id = input("Enter item ID to use: ").strip()
        try:
            print(inventory_system.use_item(current_character, item_id, all_items[item_id]))
        except (ItemNotFoundError, InvalidItemTypeError) as e:
            print(f"Error: {e}")
    elif choice == '2':
        item_id = input("Enter weapon ID to equip: ").strip()
        try:
            print(inventory_system.equip_weapon(current_character, item_id, all_items[item_id]))
        except (ItemNotFoundError, InvalidItemTypeError) as e:
            print(f"Error: {e}")
    elif choice == '3':
        item_id = input("Enter armor ID to equip: ").strip()
        try:
            print(inventory_system.equip_armor(current_character, item_id, all_items[item_id]))
        except (ItemNotFoundError, InvalidItemTypeError) as e:
            print(f"Error: {e}")
    elif choice == '4':
        item_id = input("Enter item ID to drop: ").strip()
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
            print(f"Dropped {item_id}.")
        except ItemNotFoundError as e:
            print(f"Error: {e}")
    else:
        print("Returning to game menu.")

def quest_menu():
    """
    Quest management menu
    """
    global current_character, all_quests
    
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest")
    print("7. Back")
    
    choice = input("Select an option: ").strip()
    
    try:
        if choice == '1':
            quest_handler.display_active_quests(current_character)
        elif choice == '2':
            quest_handler.display_available_quests(current_character, all_quests)
        elif choice == '3':
            quest_handler.display_completed_quests(current_character)
        elif choice == '4':
            quest_id = input("Enter quest ID to accept: ").strip()
            quest_handler.accept_quest(current_character, quest_id, all_quests)
        elif choice == '5':
            quest_id = input("Enter quest ID to abandon: ").strip()
            quest_handler.abandon_quest(current_character, quest_id)
        elif choice == '6':
            quest_id = input("Enter quest ID to complete: ").strip()
            quest_handler.complete_quest(current_character, quest_id)
    except QuestError as e:
        print(f"Quest Error: {e}")

def explore():
    """
    Find and fight random enemies
    """
    global current_character
    
    print("\nExploring the world...")
    
    try:
        # Generate random enemy based on character level
        enemy = combat_system.get_random_enemy_for_level(current_character.get('level', 1))
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()
        
        if result['winner'] == 'player':
            print(f"You defeated {enemy['name']}! Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
        elif result['winner'] == 'enemy':
            print("You were defeated!")
            handle_character_death()
        elif result['winner'] == 'escaped':
            print("You successfully escaped!")
            
    except (CharacterDeadError, CombatNotActiveError) as e:
        print(f"Combat Error: {e}")

def shop():
    """
    Shop menu for buying/selling items
    """
    global current_character, all_items
    
    print("\n=== SHOP ===")
    print(f"Gold: {current_character.get('gold', 0)}")
    print("Available items:")
    
    for item_id, data in all_items.items():
        print(f"- {data['name']} ({data['type']}) - Cost: {data['cost']} gold")
    
    print("\nOptions:")
    print("1. Buy item")
    print("2. Sell item")
    print("3. Back")
    
    choice = input("Select an option: ").strip()
    
    if choice == '1':
        item_id = input("Enter item ID to buy: ").strip()
        try:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            print(f"Purchased {all_items[item_id]['name']}.")
        except (InsufficientResourcesError, InventoryFullError) as e:
            print(f"Error: {e}")
    elif choice == '2':
        item_id = input("Enter item ID to sell: ").strip()
        try:
            gold_received = inventory_system.sell_item(current_character, item_id, all_items[item_id])
            print(f"Sold {all_items[item_id]['name']} for {gold_received} gold.")
        except ItemNotFoundError as e:
            print(f"Error: {e}")

# ============================================================================ 
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """
    Save current game state
    """
    global current_character
    try:
        character_manager.save_character(current_character)
        print(f"Character '{current_character['name']}' saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """
    Load all quest and item data from files
    """
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating default files...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Invalid data format: {e}")
        raise

def handle_character_death():
    """
    Handle character death
    """
    global current_character, game_running
    
    print("\nYour character has died!")
    print("Options:")
    print("1. Revive (costs gold)")
    print("2. Quit")
    
    choice = input("Select an option: ").strip()
    
    if choice == '1':
        try:
            character_manager.revive_character(current_character)
            print("Character revived! Continue your adventure.")
        except InsufficientResourcesError as e:
            print(f"Cannot revive: {e}")
            game_running = False
    else:
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!\n")

# ============================================================================ 
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except (MissingDataFileError, InvalidDataFormatError):
        print("Game data could not be loaded. Exiting.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break

if __name__ == "__main__":
    main()
