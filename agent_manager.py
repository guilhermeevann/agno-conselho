import json
import os
from typing import List, Dict, Optional

class AgentManager:
    def __init__(self, config_file: str = "agents.json"):
        self.config_file = config_file
        self.agents = self._load_agents()

    def _load_agents(self) -> List[Dict]:
        if not os.path.exists(self.config_file):
            return []
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading agents: {e}")
            return []

    def _save_agents(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.agents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving agents: {e}")

    def get_all_agents(self) -> List[Dict]:
        return self.agents

    def get_active_agents(self) -> List[Dict]:
        return [agent for agent in self.agents if agent.get("is_active", True)]

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        for agent in self.agents:
            if agent["id"] == agent_id:
                return agent
        return None

    def add_agent(self, agent_data: Dict) -> bool:
        if self.get_agent(agent_data["id"]):
            return False  # Agent with this ID already exists
        self.agents.append(agent_data)
        self._save_agents()
        return True

    def update_agent(self, agent_id: str, agent_data: Dict) -> bool:
        for i, agent in enumerate(self.agents):
            if agent["id"] == agent_id:
                self.agents[i] = {**agent, **agent_data}
                self._save_agents()
                return True
        return False

    def delete_agent(self, agent_id: str) -> bool:
        initial_len = len(self.agents)
        self.agents = [agent for agent in self.agents if agent["id"] != agent_id]
        if len(self.agents) < initial_len:
            self._save_agents()
            return True
        return False
