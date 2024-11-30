
from pydantic import BaseModel
from typing import Dict, List, Optional

class Address(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class Student(BaseModel):
    name: str
    age: int
    address: Address
    
class StudentFilter(BaseModel):
    name:str
    age:int
    
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None
    
    
class StudentListResponse(BaseModel):
    data: List[StudentFilter]