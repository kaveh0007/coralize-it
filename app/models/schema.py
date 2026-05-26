from pydantic import BaseModel

class SQLQueryFromGenAI(BaseModel):
    thinking_process: str
    query: str
    is_possible: bool