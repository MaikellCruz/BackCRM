# Categorys/user_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.database import Base
from app.roles.role_model import RolePublic # Importa o schema público de Role
from typing import Optional

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class Category(Base):
    __tablename__ = "Categorys"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(String, unique=True, index=True, nullable=True)
    descricao = Column(String, nullable=True)
    # Chave estrangeira que aponta para a tabela 'roles'
    role_id = Column(Integer, ForeignKey("roles.id"))
    # Cria a relação para que possamos acessar o objeto Role a partir de um Category
    role = relationship("Role")

    # Relacionamentos
    clients = relationship("Client", back_populates="category", cascade="all, delete-orphan")
    orcamentos = relationship("Orcamento", back_populates="category", cascade="all, delete-orphan")

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class CategoryCreate(BaseModel):
    nome: str | None = Field(default=None, min_length=3,  description="Nome da categoria")
    tipo: str | None = Field(default=None, min_length=3)
    descrição: str | None = Field(default=None, min_length=3)
    role_id: int = Field(description="ID do role a ser associado a categoria")
    orcamento_id: int = Field(..., example=1)
    client_id: int = Field(..., example=3)

class CategoryUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3,  description="Nome da categoria")
    tipo: str | None = Field(default=None, min_length=3)
    descrição: str | None = Field(default=None, min_length=3)
    orcamento_id: int = Field(..., example=1)
    client_id: int = Field(..., example=3)

class CategoryPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nome: str
    tipo: str
    descrição: str
    role: RolePublic # O perfil agora é um objeto aninhado
    orcamento_id: int
    client_id: int
