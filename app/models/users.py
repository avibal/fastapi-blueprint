from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Users(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    email = Column(String)
