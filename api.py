from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import classifying_model.main
import main as RAG

app = FastAPI(
    title="Legal Assistant API",
    description="API for legal case analysis and chat",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# Case categorization request model
class CaseRequest(BaseModel):
    case_description: str
    language: Optional[str] = "en"  # Default to English

class CaseResponse(BaseModel):
    category: str
    #confidence: float
    #subcategories: Optional[List[str]] = None

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                # Parse the received data if it's JSON
                try:
                    parsed_data = json.loads(data)
                    user_message = parsed_data.get("message", data)
                except json.JSONDecodeError:
                    user_message = data
                
                # Call RAG system
                articles, rag_response = RAG.query_rag(user_message)
                
                # Prepare response with sources
                response_data = {
                    "type": "response",
                    "content": rag_response,
                    "sources": [
                        {
                            "article_number": f"Article {i+1}",
                            "preview": article[:200] + "..." if len(article) > 200 else article
                        } for i, article in enumerate(articles[:3])  # Limit to top 3 sources
                    ] if articles else []
                }
                
                await manager.send_message(json.dumps(response_data, ensure_ascii=False), websocket)
                
            except Exception as e:
                # Send error response
                error_response = {
                    "type": "error",
                    "content": f"خطأ في معالجة الطلب: {str(e)}",
                    "sources": []
                }
                await manager.send_message(json.dumps(error_response, ensure_ascii=False), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/categorize-case", response_model=CaseResponse)
async def categorize_case(case: CaseRequest):
    return CaseResponse(
        category=classifying_model.main.classify_case_description(case.case_description),
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test RAG endpoint
@app.post("/test-rag")
async def test_rag(question: str):
    try:
        articles, response = RAG.query_rag(question)
        return {
            "response": response,
            "sources_count": len(articles),
            "sources": [
                {
                    "article_number": f"Article {i+1}",
                    "preview": article[:200] + "..." if len(article) > 200 else article
                } for i, article in enumerate(articles[:3])
            ] if articles else []
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    # Get host from environment variable or use default
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=False  # Set to False in production
    )
