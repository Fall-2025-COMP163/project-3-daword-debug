"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
import character_manager

# ============================================================================ 
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    # Check that quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]
    
    # Check character level
    if character.get('level', 1) < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required to accept this quest.")
    
    # Check prerequisite quest
    prereq = quest.get('prerequisite', 'NONE')
    if prereq != 'NONE' and prereq not in character.get('completed_quests', []):
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq}' not completed.")
    
    # Check if already completed
    if quest_id in character.get('completed_quests', []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")
    
    # Check if already active
    if quest_id in character.get('active_quests', []):
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")
    
    # Add quest to active quests
    character.setdefault('active_quests', []).append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    quest = quest_data_dict[quest_id]
    
    # Remove from active quests
    character['active_quests'].remove(quest_id)
    
    # Add to completed quests
    character.setdefault('completed_quests', []).append(quest_id)
    
    # Grant rewards
    character_manager.gain_experience(character, quest['reward_xp'])
    character['gold'] = character.get('gold', 0) + quest['reward_gold']
    
    return {'xp': quest['reward_xp'], 'gold': quest['reward_gold']}


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    """
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    """
    return [quest_data_dict[qid] for qid in character.get('active_quests', []) if qid in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    """
    return [quest_data_dict[qid] for qid in character.get('completed_quests', []) if qid in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    """
    available = []
    for qid, quest in quest_data_dict.items():
        if can_accept_quest(character, qid, quest_data_dict):
            available.append(quest)
    return available


# ============================================================================ 
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character.get('completed_quests', [])


def is_quest_active(character, quest_id):
    return quest_id in character.get('active_quests', [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements without raising exceptions
    """
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    
    if character.get('level', 1) < quest['required_level']:
        return False
    
    prereq = quest.get('prerequisite', 'NONE')
    if prereq != 'NONE' and prereq not in character.get('completed_quests', []):
        return False
    
    if quest_id in character.get('completed_quests', []):
        return False
    
    if quest_id in character.get('active_quests', []):
        return False
    
    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    chain = []
    current_id = quest_id
    
    while current_id != 'NONE':
        chain.insert(0, current_id)
        prereq = quest_data_dict[current_id].get('prerequisite', 'NONE')
        if prereq == current_id:
            break  # Avoid infinite loop
        current_id = prereq
    
    return chain


# ============================================================================ 
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    if total == 0:
        return 0.0
    completed = len(character.get('completed_quests', []))
    return (completed / total) * 100.0


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0
    for qid in character.get('completed_quests', []):
        quest = quest_data_dict.get(qid)
        if quest:
            total_xp += quest['reward_xp']
            total_gold += quest['reward_gold']
    return {'total_xp': total_xp, 'total_gold': total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [q for q in quest_data_dict.values() if min_level <= q['required_level'] <= max_level]


# ============================================================================ 
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Reward XP: {quest_data['reward_xp']}, Gold: {quest_data['reward_gold']}")
    print(f"Required Level: {quest_data['required_level']}")
    prereq = quest_data.get('prerequisite', 'NONE')
    print(f"Prerequisite: {prereq}")


def display_quest_list(quest_list):
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']}) | XP: {quest['reward_xp']}, Gold: {quest['reward_gold']}")


def display_character_quest_progress(character, quest_data_dict):
    active = len(character.get('active_quests', []))
    completed = len(character.get('completed_quests', []))
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print("\n=== QUEST PROGRESS ===")
    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed}")
    print(f"Completion: {percentage:.1f}%")
    print(f"Total XP Earned: {rewards['total_xp']}, Total Gold Earned: {rewards['total_gold']}")


# ============================================================================ 
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for qid, quest in quest_data_dict.items():
        prereq = quest.get('prerequisite', 'NONE')
        if prereq != 'NONE' and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{qid}' has invalid prerequisite '{prereq}'")
    return True


# ============================================================================ 
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }

    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }

    # Accepting the first quest
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
        display_character_quest_progress(test_char, test_quests)
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept quest: {e}") 
