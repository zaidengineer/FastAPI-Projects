from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated,Optional


class Patient(BaseModel):
    id:Annotated[str,Field(..., examples=["P001"])]
    name:Annotated[str,Field(..., description="Patient name")]
    age:Annotated[int,Field(..., gt=0,lt=120,description="Patient Age")]
    city:Annotated[str,Field(..., description="City name")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Select gender")]
    height:Annotated[float,Field(..., description="Height in meters")]
    weight:Annotated[float,Field(..., description="weight in kgs")]
    @computed_field
    @property
    def bmi(self)->float:
        bmi=self.weight/(self.height**2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        else :
            return 'Obese'


class patient_update(BaseModel):
    name:Optional[str]=None
    age:Optional[int] = Field(default=None, gt=0, lt=120)
    city:Optional[str]=None
    gender:Optional[Literal["male","female","others"]] = None
    height:Optional[float]=None
    weight:Optional[float]=None