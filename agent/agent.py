import os
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from schema import get_schema

def create_agent():
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER', 'admin')}:{os.getenv('POSTGRES_PASSWORD', 'password123')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'hrdb')}"
    )

    llm = Ollama(
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama3.2")
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20
    )

    return agent

def query(question: str):
    schema = get_schema()
    agent = create_agent()
    
    prompt = f"""You are an HR data analyst. 
    Use this database schema as context:
    {schema}
    
    Answer this question by generating and executing SQL: {question}
    
    Return the results in a clear format."""
    
    result = agent.invoke({"input": prompt})
    return result["output"]

if __name__ == "__main__":
    print("Testing agent...")
    result = query("How many employees left the company? Show attrition rate by department")
    print(f"\nResult: {result}")