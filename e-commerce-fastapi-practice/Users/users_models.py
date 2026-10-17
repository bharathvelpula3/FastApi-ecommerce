#create a database
#AUthentication
#JWT
#FileUpload
from .user_database import  UserBase
from sqlalchemy import Column,Integer,String

class User(UserBase):
    __tablename__ = "user_database"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashPassword = Column(String)
    email = Column(String)
