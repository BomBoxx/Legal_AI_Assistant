from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Tuple
import uvicorn
from main import query_rag, collection, existing

app = FastAPI(
    title="Legal RAG System",
    description="A RAG system for legal document querying using FastAPI",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str
    n_results: int = 40

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "ما هي الجرائم التي يعاقب عليها القانون",
                "n_results": 40
            }
        }
    )

class QueryResponse(BaseModel):
    chunks: List[str]
    answer: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "chunks": ["Article 1: ...", "Article 2: ..."],
                "answer": "Based on the legal texts provided, the crimes punishable by law include..."
            }
        }
    )

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Legal RAG System API",
        "status": "active",
        "documents_indexed": existing
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        chunks, answer = query_rag(request.question, request.n_results)
        return QueryResponse(chunks=chunks, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 