import logging
from agent import agent

# Configurar logging para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_memory():
    session_id = "test_user_123"
    
    print(f"--- Testando memória para sessão: {session_id} ---")
    
    # 1. Primeira mensagem: Apresentação
    msg1 = "Olá, meu nome é Guilherme."
    print(f"User: {msg1}")
    resp1 = agent.run(msg1, session_id=session_id)
    print(f"Agent: {resp1.content}\n")
    
    # 2. Segunda mensagem: Pergunta sobre o contexto
    msg2 = "Qual é o meu nome?"
    print(f"User: {msg2}")
    resp2 = agent.run(msg2, session_id=session_id)
    print(f"Agent: {resp2.content}\n")
    
    # Verificação
    if "Guilherme" in resp2.content:
        print("✅ SUCESSO: O agente lembrou o nome!")
    else:
        print("❌ FALHA: O agente não lembrou o nome.")

if __name__ == "__main__":
    test_memory()
