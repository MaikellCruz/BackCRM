# app/clients/client_repository.py

from sqlalchemy.orm import Session
from . import client_model
from security import get_password_hash

# --- FUNÇÕES DE LEITURA (READ) ---

def get_client(db: Session, client_id: int):
    """
    Busca um único cliente pelo seu ID.
    db.query(client_model.client): Inicia uma consulta na tabela client.
    .filter(client_model.client.id == client_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(client_model.client).filter(client_model.client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    """Busca um único cliente pelo seu e-mail."""
    return db.query(client_model.client).filter(client_model.client.email == email).first()

def get_clients(db: Session):
    """
    Busca todos os clientes cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(client_model.client).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_client(db: Session, client: client_model.clientCreate, role_id: int = None):
    """
    Cria um novo cliente no banco de dados.
    """
    # Agora a senha é hasheada corretamente
    hashed_password = get_password_hash(client.password)

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_client = client_model.client(
        email=client.email, 
        hashed_password=hashed_password, 
        full_name=client.full_name,
        profile_image_url=client.profile_image_url,
        profile_image_base64=client.profile_image_base64,
        role_id=role_id
    )

    db.add(db_client)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_client) # Atualiza o objeto db_client com os dados do banco (como o ID gerado).
    return db_client

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_client(db: Session, db_client: client_model.client, client_in: client_model.clientUpdate):
    """Atualiza os dados de um cliente existente."""
    update_data = client_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
        # Se o campo for 'password', precisa mapear para 'hashed_password' no modelo SQLAlchemy
        if key == "password":
            setattr(db_client, "hashed_password", value) # AVISO: A senha ainda não está sendo hasheada!
        else:
            setattr(db_client, key, value) # Atualiza cada campo no objeto do banco (db_client).

    db.add(db_client) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_client) # Atualiza o objeto com os dados do banco.
    return db_client

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_client(db: Session, db_client: client_model.client):
    """Deleta um cliente do banco de dados."""
    db.delete(db_client) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_client