from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.ERROR)
load_dotenv()

with open("prompt/martinho.xml", "r", encoding="utf-8") as f:
    prompt_lutero = f.read()

with open("prompt/agostinho.xml", "r", encoding="utf-8") as f:
    prompt_agostinho = f.read()

with open("prompt/spurgeon.xml", "r", encoding="utf-8") as f:
    prompt_spurgeon = f.read()

with open("prompt/billy.xml", "r", encoding="utf-8") as f:
    prompt_billy = f.read()

with open("prompt/paulo.xml", "r", encoding="utf-8") as f:
    prompt_paulo = f.read()

# Shared database
db = SqliteDb(db_file="agent_memory.db")

# Tavily search tools for web research
tavily_tools = TavilyTools()

lutero = Agent(
    name="Martinho Lutero",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_lutero,
    description="Teólogo da Reforma Protestante, especialista em graça e fé",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

agostinho = Agent(
    name="Agostinho de Hipona",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_agostinho,
    description="Padre da Igreja, filósofo e teólogo, especialista em pecado e redenção",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

spurgeon = Agent(
    name="Charles Spurgeon",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_spurgeon,
    description="Príncipe dos Pregadores, especialista em evangelismo e vida devocional",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

billy = Agent(
    name="Billy Graham",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_billy,
    description="Grande evangelista contemporâneo, especialista em decisões de fé e evangelismo",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

paulo = Agent(
    name="Apóstolo Paulo",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_paulo,
    description="Apóstolo dos gentios, especialista em doutrina, graça e vida cristã prática",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

agent = Team(
    name="Mesa dos Conselheiros",
    members=[lutero, agostinho, spurgeon, billy, paulo],
    instructions=[
        "Vocês são um conselho de grandes líderes cristãos da história, reunidos para aconselhar pessoas com sabedoria bíblica.",
        "Cada conselheiro deve contribuir com sua perspectiva única baseada em sua época, experiência e ênfase teológica.",
        "As respostas devem ser práticas, acolhedoras e fundamentadas nas Escrituras.",
        "Usem formatação para WhatsApp: *negrito*, _itálico_, e quebras de linha para facilitar a leitura.",
        "Mantenham um tone de amor e encorajamento, como pastores cuidando de suas ovelhas."])
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.ERROR)
load_dotenv()

with open("prompt/martinho.xml", "r", encoding="utf-8") as f:
    prompt_lutero = f.read()

with open("prompt/agostinho.xml", "r", encoding="utf-8") as f:
    prompt_agostinho = f.read()

with open("prompt/spurgeon.xml", "r", encoding="utf-8") as f:
    prompt_spurgeon = f.read()

with open("prompt/billy.xml", "r", encoding="utf-8") as f:
    prompt_billy = f.read()

with open("prompt/paulo.xml", "r", encoding="utf-8") as f:
    prompt_paulo = f.read()

# Shared database
db = SqliteDb(db_file="agent_memory.db")

# Tavily search tools for web research
tavily_tools = TavilyTools()

lutero = Agent(
    name="Martinho Lutero",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_lutero,
    description="Teólogo da Reforma Protestante, especialista em graça e fé",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

agostinho = Agent(
    name="Agostinho de Hipona",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_agostinho,
    description="Padre da Igreja, filósofo e teólogo, especialista em pecado e redenção",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

spurgeon = Agent(
    name="Charles Spurgeon",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_spurgeon,
    description="Príncipe dos Pregadores, especialista em evangelismo e vida devocional",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

billy = Agent(
    name="Billy Graham",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_billy,
    description="Grande evangelista contemporâneo, especialista em decisões de fé e evangelismo",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

paulo = Agent(
    name="Apóstolo Paulo",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=prompt_paulo,
    description="Apóstolo dos gentios, especialista em doutrina, graça e vida cristã prática",
    db=db,
    add_history_to_context=True,
    tools=[tavily_tools],
)

agent = Team(
    name="Mesa dos Conselheiros",
    members=[lutero, agostinho, spurgeon, billy, paulo],
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

# IMPORTANTE: Esse bloco só roda se executar python agent.py diretamente
if __name__ == "__main__":
    response = agent.run("Teste")
    print(response.content)