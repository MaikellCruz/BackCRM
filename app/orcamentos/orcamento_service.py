# app/orcamentos/orcamento_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.orcamentos import orcamento_repository, orcamento_model
from app.utils.image_processor import process_image_base64


def create_new_orcamento(db: Session, orcamento: orcamento_model.OrcamentoCreate):
    # garante que não exista outro orcamento com mesmo nome (se esse for o requisito)
    existing = next((o for o in orcamento_repository.get_all(db) if o.name == orcamento.name), None)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already registered")

    return orcamento_repository.create_orcamento(db=db, orcamento=orcamento)


def get_all_orcamentos(db: Session):
    """Serviço para listar todos os orcamentos."""
    return orcamento_repository.get_all(db)


def get_orcamento_by_id(db: Session, orcamento_id: int):
    """Serviço para buscar um orcamento pelo ID, com tratamento de erro."""
    db_orcamento = orcamento_repository.get_orcamento(db, orcamento_id=orcamento_id)
    if db_orcamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orcamento not found")
    return db_orcamento


def get_orcamento_by_client(db: Session, client_id: int):
    return orcamento_repository.get_by_client(db, client_id)


def update_existing_orcamento(db: Session, orcamento_id: int, orcamento_in: orcamento_model.OrcamentoUpdate):
    db_orcamento = get_orcamento_by_id(db, orcamento_id)
    return orcamento_repository.update_orcamento(db=db, db_orcamento=db_orcamento, orcamento_in=orcamento_in)


def delete_orcamento_by_id(db: Session, orcamento_id: int):
    db_orcamento = get_orcamento_by_id(db, orcamento_id)
    return orcamento_repository.delete_orcamento(db=db, db_orcamento=db_orcamento)