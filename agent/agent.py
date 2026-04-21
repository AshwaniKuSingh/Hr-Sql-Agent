import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from schema import get_schema

class QueryRequest(BaseModel):
    question: str

agent_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_instance
    print("Starting up — creating agent...")
    agent_instance = create_agent()
    print("Agent ready!")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

def create_agent():
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER', 'admin')}:{os.getenv('POSTGRES_PASSWORD', 'password123')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'hrdb')}"
    )
    llm = Ollama(
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama3.2")
    )
    return create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(request: QueryRequest):
    schema = get_schema()
    prompt = f"""You are an HR data analyst.
    Use this database schema as context:
    {schema}
    
    Answer this question by generating and executing SQL: {request.question}
    
    Return the results in a clear format."""
    
    result = agent_instance.invoke({"input": prompt})
    return {"output": result["output"]}