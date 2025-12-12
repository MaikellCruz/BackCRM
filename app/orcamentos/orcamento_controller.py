# app/orcamentos/orcamento_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from app.database import SessionLocal, get_db
from app.orcamentos import orcamento_service, orcamento_model
from app.auth.auth_service import get_current_user

router = APIRouter(
    prefix="/orcamentos",
    tags=["Orcamentos"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=orcamento_model.OrcamentoPublic, status_code=status.HTTP_201_CREATED)
def create_orcamento(orcamento: orcamento_model.OrcamentoCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo orcamento. Recebe os dados validados (orcamento)
    e a sessão do banco (db) através da injeção de dependência."""
    return orcamento_service.create_new_orcamento(db=db, orcamento=orcamento)

@router.get("/", response_model=List[orcamento_model.OrcamentoPublic])
def read_orcamentos(db: Session = Depends(get_db)):
    """Endpoint para listar todos os orcamentos."""
    return orcamento_service.get_all_orcamentos(db)

@router.get("/{orcamento_id}", response_model=orcamento_model.OrcamentoPublic)
def read_orcamento(orcamento_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um orcamento pelo ID."""
    return orcamento_service.get_orcamento_by_id(db, orcamento_id=orcamento_id)

@router.get("/client/{client_id}", response_model=list[orcamento_model.OrcamentoPublic])
def get_orcamento_by_client(client_id: int, db: Session = Depends(get_db)):
    return orcamento_service.get_orcamento_by_client(db, client_id=client_id)

@router.put("/{orcamento_id}", response_model=orcamento_model.OrcamentoPublic)
def update_orcamento(orcamento_id: int, orcamento: orcamento_model.OrcamentoUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um orcamento."""
    return orcamento_service.update_existing_orcamento(db=db, orcamento_id=orcamento_id, orcamento_in=orcamento)

@router.delete("/{orcamento_id}", response_model=orcamento_model.OrcamentoPublic)
def delete_orcamento(orcamento_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um orcamento."""
    return orcamento_service.delete_orcamento_by_id(db=db, orcamento_id=orcamento_id)