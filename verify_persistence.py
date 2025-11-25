import logging
from agent import agent

logging.basicConfig(level=logging.INFO)

def test_persistence():
    session_id = "test_user_123"
    print(f"--- Testando persistência para sessão: {session_id} ---")
    
    # Pergunta sobre o contexto (deve lembrar da execução anterior)
    msg = "Qual é o meu nome?"
    print(f"User: {msg}")
    resp = agent.run(msg, session_id=session_id)
    print(f"Agent: {resp.content}\n")
    
    if "Guilherme" in resp.content:
        print("✅ SUCESSO: O agente lembrou o nome da sessão anterior!")
    else:
        print("❌ FALHA: O agente esqueceu o nome.")

if __name__ == "__main__":
    test_persistence()
