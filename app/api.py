from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .test_agent import agent_executor

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/query")
async def process_query(query: Query):
    try:
        result = agent_executor.invoke({"input": query.query})
        return {"response": result["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
