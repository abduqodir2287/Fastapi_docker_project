from pydantic import BaseModel

class PUser(BaseModel):
    first_name: str
    last_name: str
    age: int

class Organization(BaseModel):
    org_id: int
    org_name: str


