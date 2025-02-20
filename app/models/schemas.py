from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from pydantic import BaseModel
from database import Base

# SQLAlchemy Models
class ConstructionMaterial(Base):
    __tablename__ = "construction_materials"

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String, index=True)
    weight = Column(Float)
    date_added = Column(DateTime, default=datetime.utcnow)

class Debris(Base):
    __tablename__ = "debris"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    date_added = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class MaterialBase(BaseModel):
    material_name: str
    weight: float

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    date_added: datetime

    class Config:
        orm_mode = True

class DebrisBase(BaseModel):
    weight: float

class DebrisCreate(DebrisBase):
    pass

class Debris(DebrisBase):
    id: int
    date_added: datetime

    class Config:
        orm_mode = True