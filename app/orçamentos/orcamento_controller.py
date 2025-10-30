# app/orcamentos/orcamento_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal, get_db
from . import orcamento_service, orcamento_model
from auth.auth_service import get_current_orcamento

router = APIRouter(
    prefix="/orcamentos",
    tags=["orcamentos"],
    dependencies=[Depends(get_current_orcamento)]
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

@router.put("/{orcamento_id}", response_model=orcamento_model.OrcamentoPublic)
def update_orcamento(orcamento_id: int, orcamento: orcamento_model.OrcamentoUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um orcamento."""
    return orcamento_service.update_existing_orcamento(db=db, orcamento_id=orcamento_id, orcamento_in=orcamento)

@router.delete("/{orcamento_id}", response_model=orcamento_model.OrcamentoPublic)
def delete_orcamento(orcamento_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um orcamento."""
    return orcamento_service.delete_orcamento_by_id(db=db, orcamento_id=orcamento_id)