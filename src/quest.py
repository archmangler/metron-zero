class Quest:
    def __init__(self, quest_id, title, description, objectives, rewards):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # List of objectives
        self.rewards = rewards  # Dictionary of rewards
        self.completed = False
        self.active = False
    
    def check_completion(self, player):
        if self.completed:
            return True
            
        all_complete = True
        for objective in self.objectives:
            if not objective.is_complete():
                all_complete = False
                break
        
        if all_complete:
            self.completed = True
            self.give_rewards(player)
        
        return all_complete
    
    def give_rewards(self, player):
        for reward_type, value in self.rewards.items():
            if reward_type == 'gold':
                player.gold += value
            elif reward_type == 'item':
                player.inventory.add_item(value)
            elif reward_type == 'experience':
                player.add_experience(value)

class QuestObjective:
    def __init__(self, description, required_amount=1):
        self.description = description
        self.required_amount = required_amount
        self.current_amount = 0
    
    def update(self, amount=1):
        self.current_amount = min(self.current_amount + amount, self.required_amount)
    
    def is_complete(self):
        return self.current_amount >= self.required_amount

class QuestManager:
    def __init__(self):
        self.available_quests = {}
        self.active_quests = {}
        self.completed_quests = {}
        self.setup_quests()
    
    def setup_quests(self):
        # Example quest setup
        kill_enemies_quest = Quest(
            "QUEST_001",
            "Clear the Area",
            "Defeat enemies in the area to make it safe.",
            [QuestObjective("Defeat enemies", 5)],
            {'gold': 100, 'experience': 50}
        )
        
        collect_items_quest = Quest(
            "QUEST_002",
            "Gather Resources",
            "Collect weapon parts for the merchant.",
            [QuestObjective("Collect weapon parts", 3)],
            {'gold': 150, 'item': InventoryItem("Steel Sword", "weapon", {'damage': 25})}
        )
        
        self.available_quests = {
            "QUEST_001": kill_enemies_quest,
            "QUEST_002": collect_items_quest
        }
    
    def accept_quest(self, quest_id):
        if quest_id in self.available_quests:
            quest = self.available_quests.pop(quest_id)
            quest.active = True
            self.active_quests[quest_id] = quest
            return True
        return False
    
    def update_quest_progress(self, quest_id, objective_index, amount=1):
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.objectives[objective_index].update(amount)
    
    def check_quest_completion(self, player):
        for quest_id, quest in list(self.active_quests.items()):
            if quest.check_completion(player):
                self.active_quests.pop(quest_id)
                self.completed_quests[quest_id] = quest
    
    def get_save_data(self):
        return {
            'available': [q.quest_id for q in self.available_quests.values()],
            'active': {
                q.quest_id: [obj.current_amount for obj in q.objectives]
                for q in self.active_quests.values()
            },
            'completed': list(self.completed_quests.keys())
        }
    
    def load_save_data(self, data):
        # Reset current state
        self.setup_quests()
        
        # Restore quest states
        for quest_id in data['completed']:
            if quest_id in self.available_quests:
                quest = self.available_quests.pop(quest_id)
                quest.completed = True
                self.completed_quests[quest_id] = quest
        
        for quest_id, objectives_progress in data['active'].items():
            if quest_id in self.available_quests:
                quest = self.available_quests.pop(quest_id)
                quest.active = True
                for obj, progress in zip(quest.objectives, objectives_progress):
                    obj.current_amount = progress
                self.active_quests[quest_id] = quest