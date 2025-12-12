# Orcamentos/Orcamento_model.py
from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from app.database import Base
from app.roles.role_model import RolePublic # Importa o schema público de Role
from typing import Optional

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class Orcamento(Base):
    __tablename__ = "Orcamentos"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    value = Column(Float, nullable=False, default=0.0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    descr= Column(String, index=True, nullable=True)

    #  Relacionamentos
    client_id = Column(Integer, ForeignKey("Clients.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("Categorys.id"), nullable=False)

    client = relationship("Client", back_populates="orcamentos")
    category = relationship("Category", back_populates="orcamentos")

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class OrcamentoCreate(BaseModel):
    name: str = Field(min_length=8)
    value:float = Field(default=None, min_length=3)
    date: int = Field(..., example="2025-10-30")
    descr: str | None = Field(default=None, min_length=3)
    client_id: int = Field(..., example=1)
    category_id: int = Field(..., example=3)

class OrcamentoUpdate(BaseModel):
    name: str = Field(min_length=8)
    value:float = Field(default=None, min_length=3)
    date: int = Field(..., example="2025-10-30")
    descr: str | None = Field(default=None, min_length=3)
    client_id: int = Field(..., example=1)
    category_id: int = Field(..., example=3)

class OrcamentoPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    value: float
    date: int | None = None
    descr: str
    client_id: int
    category_id: int
