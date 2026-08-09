from pydantic import BaseModel,Field,field_validator
from typing import List,Dict

class Address(BaseModel):
    city:str
    district:str
    zipcode:int
class Course(BaseModel):
    name:str
    crhrs:int
class Student(BaseModel):
    @field_validator("name")
    @classmethod
    def clean_name(cls,value):
        value= value.title()
        value= value.strip()
        return value
    @field_validator("age")
    @classmethod
    def chk_age(cls,value):
        if value<18:
            raise ValueError("Age must be above 18")
        return value
    name:str=Field(description="Student name")
    books:List[str]
    address:Address
    course:Course
    certificates:Dict[str,str]
    age:int
adrs={'city':'Lahore','district':'Bahawalnagar','zipcode':5500}
corse={'name':'Python','crhrs':4}
stinfo={'name':'Zaid','books':['pF','AICT','DB','py'],'address':adrs,'course':corse,'certificates':{'c1':'HEC','c2':'Coursera'},'age':24}
st1=Student(**stinfo)
print(st1)