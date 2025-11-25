"""
Script para testar as ferramentas Tavily de pesquisa web nos agentes.
"""
from agent import agent

# Teste 1: Pergunta que pode requerer pesquisa web
print("=" * 80)
print("TESTE 1: Pergunta sobre eventos atuais")
print("=" * 80)
response = agent.run(
    "Quais são as notícias mais recentes sobre a igreja evangélica no Brasil?",
    session_id="test_tavily_1"
)
print(response.content)
print("\n")

# Teste 2: Pergunta teológica que pode se beneficiar de pesquisa
print("=" * 80)
print("TESTE 2: Pergunta teológica com contexto atual")
print("=" * 80)
response = agent.run(
    "O que vocês pensam sobre as discussões atuais sobre teologia da prosperidade?",
    session_id="test_tavily_2"
)
print(response.content)
print("\n")

print("=" * 80)
print("Testes concluídos!")
print("=" * 80)
