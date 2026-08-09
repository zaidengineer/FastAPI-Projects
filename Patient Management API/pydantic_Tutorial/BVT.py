from pydantic import BaseModel,HttpUrl,SecretStr,EmailStr,Field
from pathlib import Path
from ipaddress import IPv4Address
from datetime import date
from typing import Annotated

class allF(BaseModel):
    email:Annotated[EmailStr,Field(description="Student email")]
    user:Annotated[str,Field(min_length=3,max_length=20)]
    password:Annotated[SecretStr,Field(min_length=8)]
    file:Annotated[Path,Field(description="File-Format")]
    address:Annotated[IPv4Address,Field(description="Address")]
    url:Annotated[HttpUrl,Field(description="URL-LINK")]
    time:date

info={'email':'zaid@gmail.com','user':'zaid','password':'zaid2344','file':'image.jpg','address':'192.168.0.1','url':'https://www.google.com','time':'2004-10-15'}
a1=allF(**info)
print(a1)