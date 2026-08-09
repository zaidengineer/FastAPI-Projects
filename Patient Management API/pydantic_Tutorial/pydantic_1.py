from pydantic import BaseModel
from typing import Optional
class Student(BaseModel):
    name:str
    age:Optional[int]=None
    university:str="University of Lahore"
    cgpa:float
data={'name':'zaid','age':34,'cgpa':3.8}
student=Student(**data)
print(student.name,student.age,student.university,student.cgpa)
print(student)