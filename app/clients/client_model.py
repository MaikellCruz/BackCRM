# users/user_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from app.database import Base
from app.roles.role_model import RolePublic # Importa o schema público de Role
from typing import Optional

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class Client(Base):
    __tablename__ = "Clients"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True, nullable=True)
    enterprise_name = Column(String, index=True, nullable=True)
    cel_number = Column(String, index=True, nullable=True)
    adress = Column(String, index=True, nullable=True)
    profile_image_url = Column(String, nullable=True)
    profile_image_base64 = Column(Text, nullable=True)
    # Chave estrangeira que aponta para a tabela 'roles'
    role_id = Column(Integer, ForeignKey("roles.id"))
    # Cria a relação para que possamos acessar o objeto Role a partir de um User
    role = relationship("Role")

    # Relacionamentos
    category = relationship("Category", back_populates="clients")
    orcamentos = relationship("Orcamento", back_populates="client", cascade="all, delete-orphan")

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class ClientCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    enterprise_name : str | None = Field(default=None, min_length=3)
    cel_number: Optional[str] = None
    adress : Optional[str] = None
    profile_image_url: Optional[str] = None
    profile_image_base64: Optional[str] = Field(None, description="Imagem em Base64")
    role_id: int = Field(description="ID do role a ser associado ao client")
    orcamento_id: int = Field(..., example=1)
    category_id: int = Field(..., example=3)

class ClientUpdate(BaseModel):
    email: EmailStr
    full_name: str | None = Field(default=None, min_length=3)
    enterprise_name: str | None = Field(default=None, min_length=3)
    cel_number: Optional[str] = None
    address: Optional[str] = None
    profile_image_url: Optional[str] = None
    profile_image_base64: Optional[str] = Field(None, description="Imagem em Base64")
    orcamento_id: int = Field(..., example=1)
    category_id: int = Field(..., example=3)

class ClientPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    full_name: str | None = None
    enterprise_name: str | None = None
    cel_number: Optional[str] = None
    address: Optional[str] = None
    profile_image_url: Optional[str] = None
    profile_image_base64: Optional[str] = None
    role: RolePublic # O perfil agora é um objeto aninhado
    orcamento_id: int
    category_id: int