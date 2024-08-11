import sys
import torch
import json
import numpy as np

class NPCEnhancer:
    def __init__(self, model):
        self.model = model

    def enhance_behavior(self, npc_data):
        """
        Enhances the behavior of NPCs using the pre-trained model.
        Args:
            npc_data (dict): The NPC data from the game.
        
        Returns:
            dict: Enhanced NPC data.
        """
        enhanced_data = npc_data.copy()

        for npc in enhanced_data['npcs']:
            state = self.extract_state_features(npc)
            action_probabilities = self.model(state)
            npc['behavior'] = self.select_action(action_probabilities)

        return enhanced_data

    def extract_state_features(self, npc):
        """
        Extract relevant features from the NPC's current state.
        Args:
            npc (dict): The NPC data.
        
        Returns:
            torch.Tensor: The state features as a tensor.
        """
        # Example: Extract position, health, and goal as features
        position = np.array([npc['x'], npc['y']])
        health = np.array([npc['health']])
        goal = np.array([npc['goal_x'], npc['goal_y']])
        state_features = np.concatenate([position, health, goal])
        return torch.tensor(state_features, dtype=torch.float32)

    def select_action(self, action_probabilities):
        """
        Selects an action based on the model's output probabilities.
        Args:
            action_probabilities (torch.Tensor): Probabilities of each action.
        
        Returns:
            str: The selected action.
        """
        actions = ['move_left', 'move_right', 'attack', 'defend']
        action_index = torch.argmax(action_probabilities).item()
        return actions[action_index]

def load_game_data(game_path):
    """
    Load the game data, including NPC behavior.
    Args:
        game_path (str): Path to the game's NPC data file.
    
    Returns:
        dict: Loaded NPC data.
    """
    with open(game_path, 'r') as f:
        data = json.load(f)
    return data

def save_game_data(game_path, data):
    """
    Save the enhanced game data back to the file.
    Args:
        game_path (str): Path to the game's NPC data file.
        data (dict): The enhanced NPC data.
    """
    with open(game_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    game_path = sys.argv[1]
    npc_model = torch.load('npc_model.pth')  # Load your pre-trained NPC model
    enhancer = NPCEnhancer(npc_model)

    game_data = load_game_data(game_path)
    enhanced_data = enhancer.enhance_behavior(game_data)
    save_game_data(game_path, enhanced_data)
