import os
import json
import logging
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import agent as initial_agent, get_team  # importa o Agent inicial e a função para recarregar
from agent_manager import AgentManager
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Variável global para manter a instância do time atual
current_agent_team = initial_agent
agent_manager = AgentManager()

# Modelo para mensagem do chat
class ChatMessage(BaseModel):
    message: str
    session_id: str = None

# Modelo para Agente
class AgentModel(BaseModel):
    id: str
    name: str
    description: str
    prompt: str
    is_active: bool = True

# API Endpoint para chat
@app.post("/api/chat")
async def chat_endpoint(chat_msg: ChatMessage):
    try:
        user_message = chat_msg.message
        # Se não vier session_id, gera um novo (embora o ideal seja o front manter)
        session_id = chat_msg.session_id or str(uuid.uuid4())
        
        logger.info(f"Recebendo mensagem: {user_message} (Session: {session_id})")
        
        # Executar agente (usando a instância atual)
        response = current_agent_team.run(user_message, session_id=session_id)
        
        # Extrair conteúdo da resposta
        reply_content = response.content if hasattr(response, "content") else str(response)
        
        return {"response": reply_content, "session_id": session_id}
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoints de Gerenciamento de Agentes ---

@app.get("/api/agents")
async def get_agents():
    return agent_manager.get_all_agents()

@app.post("/api/agents")
async def create_agent(agent: AgentModel):
    success = agent_manager.add_agent(agent.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Agent ID already exists")
    return {"status": "success", "agent": agent}

@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: str, agent: AgentModel):
    success = agent_manager.update_agent(agent_id, agent.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "success", "agent": agent}

@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str):
    success = agent_manager.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "success"}

@app.post("/api/team/refresh")
async def refresh_team():
    global current_agent_team
    try:
        current_agent_team = get_team()
        return {"status": "success", "message": "Team reloaded successfully"}
    except Exception as e:
        logger.error(f"Error reloading team: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Servir arquivos estáticos (Frontend)
# Monta a pasta 'static' na raiz '/'
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Porta padrão do Render é 10000, mas localmente pode ser 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)