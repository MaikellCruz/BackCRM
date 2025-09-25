from pydantic import BaseModel, EmailStr, Field

# Schema para os dados que o cliente envia ao CRIAR um usuário
class ClientCreate(BaseModel):
    email: EmailStr | None = None
    cpf: str | None = Field(default=None, min_length=11)
    telefone: str | None = Field(default=None, min_length=11)
    #cpf: str = Field(default=None, min_length=11) | None
    #telefone: str = Field(default=None, min_length=11) | None
    # full_name: str = Field(min_length=3)
    full_name: str | None = Field(min_length=3) 

# Schema para os dados que o cliente envia ao ATUALIZAR um usuário
# Todos os campos são opcionais
class ClientUpdate(BaseModel):
    email: EmailStr | None
    cpf: str | None = Field(default=None, min_length=11)
    telefone: str | None = Field(default=None, min_length=11)
    # cpf: str = Field(default=None, min_length=11) | None
    # telefone: str = Field(default=None, min_length=11) | None
    full_name: str | None = Field(min_length=3) 

# Schema para os dados que a API RETORNA ao cliente (público)
class ClientPublic(BaseModel):
    id: int
    email: EmailStr | None
    cpf: str | None
    telefone: str | None
    full_name: str
