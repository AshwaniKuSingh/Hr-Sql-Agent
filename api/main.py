import os
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    rows: str
    sql: str = ""
    error: str = None

AGENT_HOST = os.getenv("AGENT_HOST", "http://localhost:8001")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API starting up...")
    yield
    print("API shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
async def query(request: QueryRequest):
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{AGENT_HOST}/query",
                json={"question": request.question}
            )
            data = response.json()
            return QueryResponse(rows=data["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))