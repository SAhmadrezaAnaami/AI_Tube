from pydantic import BaseModel

class searchSchema(BaseModel):
    searchText: str
    