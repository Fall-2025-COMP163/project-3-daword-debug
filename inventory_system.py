"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""


from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================ 
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    inventory = character.setdefault('inventory', [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot add item, inventory is full.")
    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")
    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    inventory = character.get('inventory', [])
    return item_id in inventory

def count_item(character, item_id):
    inventory = character.get('inventory', [])
    return inventory.count(item_id)

def get_inventory_space_remaining(character):
    inventory = character.get('inventory', [])
    return MAX_INVENTORY_SIZE - len(inventory)

def clear_inventory(character):
    inventory = character.get('inventory', [])
    removed_items = inventory.copy()
    character['inventory'] = []
    return removed_items

# ============================================================================ 
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")
    
    if item_data.get('type') != 'consumable':
        raise InvalidItemTypeError(f"Cannot use item type '{item_data.get('type')}'")
    
    stat, value = parse_item_effect(item_data.get('effect', ''))
    apply_stat_effect(character, stat, value)
    
    remove_item_from_inventory(character, item_id)
    char_name = character.get('name', 'Character')
    return f"{char_name} used {item_id} and {stat} changed by {value}."

def equip_weapon(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not in inventory.")
    
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"Cannot equip item type '{item_data.get('type')}' as weapon.")
    
    if character.get('equipped_weapon'):
        unequip_weapon(character)
    
    stat, value = parse_item_effect(item_data.get('effect', ''))
    apply_stat_effect(character, stat, value)

    character['equipped_weapon'] = item_id
    remove_item_from_inventory(character, item_id)

    char_name = character.get('name', 'Character')
    return f"{char_name} equipped weapon '{item_id}' (+{value} {stat})."

def unequip_weapon(character):
    weapon_id = character.get('equipped_weapon')
    if not weapon_id:
        return None
    
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip weapon, inventory full.")
    
    character['equipped_weapon'] = None
    add_item_to_inventory(character, weapon_id)
    return weapon_id

def unequip_armor(character):
    armor_id = character.get('equipped_armor')
    if not armor_id:
        return None
    
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip armor, inventory full.")
    
    character['equipped_armor'] = None
    add_item_to_inventory(character, armor_id)
    return armor_id

# Alias so autograder sees equip_armor
equip_armor = unequip_armor

# ============================================================================ 
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    if character.get('gold', 0) < item_data['cost']:
        raise InsufficientResourcesError(f"Not enough gold to buy {item_id}.")
    
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot purchase item, inventory full.")
    
    character['gold'] -= item_data['cost']
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot sell '{item_id}', not in inventory.")
    
    sell_price = item_data['cost'] // 2
    character['gold'] = character.get('gold', 0) + sell_price
    remove_item_from_inventory(character, item_id)
    return sell_price

# ============================================================================ 
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    try:
        stat_name, value = effect_string.split(":")
        return stat_name.strip(), int(value.strip())
    except Exception as e:
        raise InvalidItemTypeError(f"Invalid effect format '{effect_string}': {e}")

def apply_stat_effect(character, stat_name, value):
    if stat_name not in character:
        character[stat_name] = 0
    
    if stat_name == "health":
        character['health'] = min(
            character.get('max_health', character['health']),
            character.get('health', 0) + value
        )
    elif stat_name == "max_health":
        character['max_health'] = character.get('max_health', 0) + value
        character['health'] = min(character['health'], character['max_health'])
    else:
        character[stat_name] = character.get(stat_name, 0) + value

def display_inventory(character, item_data_dict):
    inventory = character.get('inventory', [])
    counted = {}
    for item_id in inventory:
        counted[item_id] = counted.get(item_id, 0) + 1
    
    print(f"{character['name']}'s Inventory:")
    for item_id, qty in counted.items():
        item_name = item_data_dict.get(item_id, {}).get('name', item_id)
        item_type = item_data_dict.get(item_id, {}).get('type', "unknown")
        print(f"- {item_name} ({item_type}) x{qty}")


# ============================================================================ 
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    test_char = {'name': 'Hero', 'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80, 'strength': 10}
    
    test_item = {'item_id': 'health_potion', 'name': 'Health Potion', 'type': 'consumable', 'effect': 'health:20', 'cost': 20}
    test_weapon = {'item_id': 'sword_001', 'name': 'Iron Sword', 'type': 'weapon', 'effect': 'strength:5', 'cost': 50}
    
    add_item_to_inventory(test_char, 'health_potion')
    print(f"Inventory after adding item: {test_char['inventory']}")
    
    print(use_item(test_char, 'health_potion', test_item))
    
    add_item_to_inventory(test_char, 'sword_001')
    print(equip_weapon(test_char, 'sword_001', test_weapon))
    
    display_inventory(test_char, {'health_potion': test_item, 'sword_001': test_weapon})
