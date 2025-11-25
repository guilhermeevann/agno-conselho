import os
import json
import logging
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import agent  # importa o Agent já configurado
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Modelo para mensagem do chat
class ChatMessage(BaseModel):
    message: str
    session_id: str = None

# API Endpoint para chat
@app.post("/api/chat")
async def chat_endpoint(chat_msg: ChatMessage):
    try:
        user_message = chat_msg.message
        # Se não vier session_id, gera um novo (embora o ideal seja o front manter)
        session_id = chat_msg.session_id or str(uuid.uuid4())
        
        logger.info(f"Recebendo mensagem: {user_message} (Session: {session_id})")
        
        # Executar agente
        response = agent.run(user_message, session_id=session_id)
        
        # Extrair conteúdo da resposta
        reply_content = response.content if hasattr(response, "content") else str(response)
        
        return {"response": reply_content, "session_id": session_id}
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Servir arquivos estáticos (Frontend)
# Monta a pasta 'static' na raiz '/'
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Porta padrão do Render é 10000, mas localmente pode ser 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)