# app/orcamentos/orcamento_repository.py

from sqlalchemy.orm import Session
from app.orcamentos import orcamento_model

# --- FUNÇÕES DE LEITURA (READ) ---

def get_orcamento(db: Session, orcamento_id: int):
    """
    Busca um único orcamento pelo seu ID.
    db.query(orcamento_model.orcamento): Inicia uma consulta na tabela orcamento.
    .filter(orcamento_model.orcamento.id == orcamento_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(orcamento_model.Orcamento).filter(orcamento_model.Orcamento.id == orcamento_id).first()

def get_all(db: Session):
    """
    Busca todos os orcamentos cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(orcamento_model.Orcamento).all()

def get_by_client(db: Session, client_id: int):
    """
    Busca todos os orcamentos de um cliente específico.
    """
    return db.query(orcamento_model.Orcamento).filter(orcamento_model.Orcamento.client_id == client_id).all()


# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_orcamento(db: Session, orcamento: orcamento_model.OrcamentoCreate, role_id: int = None):
    """
    Cria um novo orcamento no banco de dados.
    """

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_orcamento = orcamento_model.Orcamento(
        name=orcamento.name,
        value=orcamento.value,
        date=orcamento.date,
        descr=orcamento.descr,
        client_id=orcamento.client_id,
        category_id=orcamento.category_id
    )

    db.add(db_orcamento)
    db.commit()
    db.refresh(db_orcamento)
    return db_orcamento


# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_orcamento(db: Session, db_orcamento: orcamento_model.Orcamento, orcamento_in: orcamento_model.OrcamentoUpdate):
    """Atualiza os dados de um orcamento existente."""
    update_data = orcamento_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_orcamento, key, value)

    db.add(db_orcamento)
    db.commit()
    db.refresh(db_orcamento)
    return db_orcamento


# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_orcamento(db: Session, db_orcamento: orcamento_model.Orcamento):
    """Deleta um orcamento do banco de dados."""
    db.delete(db_orcamento)
    db.commit()
    return db_orcamento