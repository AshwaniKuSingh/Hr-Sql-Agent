import os
import psycopg2

CACHE_FILE = "./schema_cache.txt"

def get_schema():
    if os.path.exists(CACHE_FILE):
        print("Loading schema from cache...")
        with open(CACHE_FILE, "r") as f:
            return f.read()
    
    print("Fetching schema from database...")
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "hrdb"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "password123"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'employees'
        ORDER BY ordinal_position
    """)
    
    columns = cursor.fetchall()
    
    schema = "CREATE TABLE employees (\n"
    schema += ",\n".join([f"    {col[0]} {col[1]}" for col in columns])
    schema += "\n);"
    
    with open(CACHE_FILE, "w") as f:
        f.write(schema)
    
    print("Schema cached successfully")
    cursor.close()
    conn.close()
    return schema

if __name__ == "__main__":
    print(get_schema())