# app/orcamentos/orcamento_repository.py

from sqlalchemy.orm import Session
from . import orcamento_model
from security import get_password_hash

# --- FUNÇÕES DE LEITURA (READ) ---

def get_orcamento(db: Session, orcamento_id: int):
    """
    Busca um único orcamento pelo seu ID.
    db.query(orcamento_model.orcamento): Inicia uma consulta na tabela orcamento.
    .filter(orcamento_model.orcamento.id == orcamento_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(orcamento_model.orcamento).filter(orcamento_model.Orcamento.id == orcamento_id).first()

def get_orcamento_by_email(db: Session, email: str):
    """Busca um único orcamento pelo seu e-mail."""
    return db.query(orcamento_model.orcamento).filter(orcamento_model.Orcamento.email == email).first()

def get_orcamentos(db: Session):
    """
    Busca todos os orcamentos cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(orcamento_model.orcamento).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_orcamento(db: Session, orcamento: orcamento_model.OrcamentoCreate, role_id: int = None):
    """
    Cria um novo orcamento no banco de dados.
    """
    # Agora a senha é hasheada corretamente
    hashed_password = get_password_hash(orcamento.password)

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_orcamento = orcamento_model.Orcamento(
        name=orcamento.name,
        value=orcamento.value, 
        hashed_password=hashed_password, 
        date=orcamento.date,
        descr=orcamento.descr,
        profile_image_url=orcamento.profile_image_url,
        profile_image_base64=orcamento.profile_image_base64,
        role_id=role_id
    )

    db.add(db_orcamento)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_orcamento) # Atualiza o objeto db_orcamento com os dados do banco (como o ID gerado).
    return db_orcamento

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_orcamento(db: Session, db_orcamento: orcamento_model.Orcamento, orcamento_in: orcamento_model.OrcamentoUpdate):
    """Atualiza os dados de um orcamento existente."""
    update_data = orcamento_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
        # Se o campo for 'password', precisa mapear para 'hashed_password' no modelo SQLAlchemy
        if key == "password":
            setattr(db_orcamento, "hashed_password", value) # AVISO: A senha ainda não está sendo hasheada!
        else:
            setattr(db_orcamento, key, value) # Atualiza cada campo no objeto do banco (db_orcamento).

    db.add(db_orcamento) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_orcamento) # Atualiza o objeto com os dados do banco.
    return db_orcamento

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_orcamento(db: Session, db_orcamento: orcamento_model.Orcamento):
    """Deleta um orcamento do banco de dados."""
    db.delete(db_orcamento) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_orcamento