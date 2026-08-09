from pydantic import BaseModel,model_validator

class User(BaseModel):
    password:str
    confirm_password:str
    @model_validator(mode='after')
    def chk_password(self):
        if self.password!=self.confirm_password:
            raise ValueError("Passwords not match")
        return self
ps={'password':'abcd123','confirm_password':'abcd123'}
u1=User(**ps)
print(u1)

class UniStudent(BaseModel):
    dep_name:str
    age:int
    @model_validator(mode='after')
    def chk_stinfo(self):
        if self.dep_name=="BSCS" and self.age<18:
            raise ValueError("Bs student must be 18+")
        return self
uinfo={'dep_name':'SoftwareEngineering','age':19}
u1=UniStudent(**uinfo)
print(u1)