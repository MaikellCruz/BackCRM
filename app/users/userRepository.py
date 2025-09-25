from sqlalchemy.orm import Session
from . import user_model
from security import get_password_hash # [NOVO] Importa a função de hash

# --- FUNÇÕES DE LEITURA (READ) ---
def get_user(db: Session, user_id: int):
    """
    Busca um único usuário pelo seu ID.
    db.query(user_model.User): Inicia uma consulta na tabela User.
    .filter(user_model.User.id == user_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Busca um único usuário pelo seu e-mail."""
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_users(db: Session):
    """
    Busca todos os usuários cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(user_model.User).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_user(db: Session, user: user_model.UserCreate, role_id: int):
    """
    Cria um novo usuário no banco de dados.
    """
    # [CORRIGIDO] A senha agora é hasheada antes de salvar
    hashed_password = get_password_hash(user.password)

    db_user = user_model.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role_id=role_id # [NOVO] Atribui o ID do perfil
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_user(db: Session, db_user: user_model.User, user_in: user_model.UserUpdate):
    """Atualiza os dados de um usuário existente."""
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        # [CORRIGIDO] Hasheia a senha se ela estiver sendo atualizada
        if key == "password" and value:
            setattr(db_user, "hashed_password", get_password_hash(value))
        else:
            setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_user(db: Session, db_user: user_model.User):
    """Deleta um usuário do banco de dados."""
    db.delete(db_user)
    db.commit()
    return db_user
