from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os
import logging
from agent_manager import AgentManager

logging.basicConfig(level=logging.ERROR)
load_dotenv()

# Shared database
db = SqliteDb(db_file="agent_memory.db")

# Tavily search tools for web research
tavily_tools = TavilyTools()

def get_team() -> Team:
    manager = AgentManager()
    active_agents_data = manager.get_active_agents()
    
    agent_instances = []
    for agent_data in active_agents_data:
        agent_instance = Agent(
            name=agent_data["name"],
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=agent_data["prompt"],
            description=agent_data.get("description", ""),
            db=db,
            add_history_to_context=True,
            tools=[tavily_tools],
        )
        agent_instances.append(agent_instance)
        
    return Team(
        name="Mesa dos Conselheiros",
        members=agent_instances,
        instructions=[
            "Vocês são um conselho de grandes líderes cristãos da história, reunidos para aconselhar pessoas com sabedoria bíblica.",
            "Cada conselheiro deve contribuir com sua perspectiva única baseada em sua época, experiência e ênfase teológica.",
            "As respostas devem ser práticas, acolhedoras e fundamentadas nas Escrituras.",
            "Usem formatação para WhatsApp: *negrito*, _itálico_, e quebras de linha para facilitar a leitura.",
            "Mantenham um tone de amor e encorajamento, como pastores cuidando de suas ovelhas."
        ],
        db=db,
        add_history_to_context=True,
    )

# Initialize the team
agent = get_team()

# IMPORTANTE: Esse bloco só roda se executar python agent.py diretamente
if __name__ == "__main__":
    response = agent.run("Teste")
    print(response.content)