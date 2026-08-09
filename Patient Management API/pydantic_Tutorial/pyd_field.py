from pydantic import BaseModel,Field
from typing import Optional
class Student(BaseModel):
    name:str=Field(min_length=3,max_length=20,description="Student full name")
    age:int=Field(gt=18,le=60)
    country:str=Field(default="Pakistan")
    rollno:str=Field(pattern=r"^SE-\d{3}$")
info={'name':'Zaid','age':34,'rollno':'SE-483'}
Student1=Student(**info)
print(Student1)