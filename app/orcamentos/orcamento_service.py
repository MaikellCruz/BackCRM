# app/orcamentos/orcamento_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.orcamentos import orcamento_repository, orcamento_model
from utils.image_processor import process_image_base64

def create_new_orcamento(db: Session, orcamento: orcamento_model.OrcamentoCreate):
    db_orcamento = orcamento_repository.get_orcamento_by_name(db, email=orcamento.name)
    if db_orcamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already registered")

    return orcamento_repository.create_orcamento(db=db, orcamento=orcamento_in, role_id=orcamento.role_id)

def get_all_orcamentos(db: Session):
    """Serviço para listar todos os orcamentos. Neste caso, apenas repassa a chamada."""
    return orcamento_repository.get_orcamentos(db)

def get_orcamento_by_id(db: Session, orcamento_id: int):
    """Serviço para buscar um orcamento pelo ID, com tratamento de erro."""
    db_orcamento = orcamento_repository.get_orcamento(db, orcamento_id=orcamento_id)
    # REGRA DE NEGÓCIO: Se o orcamento não for encontrado, retornar um erro 404.
    if db_orcamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orcamento not found")
    return db_orcamento

def get_orcamento_by_client(self, client_id: int):
       return self.repository.get_by_client(client_id)

def update_existing_orcamento(db: Session, orcamento_id: int, orcamento_in: orcamento_model.OrcamentoUpdate):
    """Serviço para atualizar um orcamento, com tratamento de erro."""
    db_orcamento = get_orcamento_by_id(db, orcamento_id) # Reutiliza a lógica para buscar e checar se o orcamento existe.
    return orcamento_repository.update_orcamento(db=db, db_orcamento=db_orcamento, orcamento_in=orcamento_in)

def delete_orcamento_by_id(db: Session, orcamento_id: int):
    """Serviço para deletar um orcamento, com tratamento de erro."""
    db_orcamento = get_orcamento_by_id(db, orcamento_id) # Reutiliza a lógica para buscar e checar se o orcamento existe.
    return orcamento_repository.delete_orcamento(db=db, db_orcamento=db_orcamento)