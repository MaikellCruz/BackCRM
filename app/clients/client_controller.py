# app/clients/client_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal, get_db
from . import client_service, client_model
from auth.auth_service import get_current_client

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    dependencies=[Depends(get_current_client)]
)

@router.post("/", response_model=client_model.ClientPublic, status_code=status.HTTP_201_CREATED)
def create_client(client: client_model.ClientCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo cliente. Recebe os dados validados (client)
    e a sessão do banco (db) através da injeção de dependência."""
    return client_service.create_new_client(db=db, client=client)

@router.get("/", response_model=List[client_model.ClientPublic])
def read_clients(db: Session = Depends(get_db)):
    """Endpoint para listar todos os clientes."""
    return client_service.get_all_clients(db)

@router.get("/{client_id}", response_model=client_model.ClientPublic)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um cliente pelo ID."""
    return client_service.get_client_by_id(db, client_id=client_id)

@router.put("/{client_id}", response_model=client_model.ClientPublic)
def update_client(client_id: int, client: client_model.ClientUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um cliente."""
    return client_service.update_existing_client(db=db, client_id=client_id, client_in=client)

@router.delete("/{client_id}", response_model=client_model.ClientPublic)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um cliente."""
    return client_service.delete_client_by_id(db=db, client_id=client_id)