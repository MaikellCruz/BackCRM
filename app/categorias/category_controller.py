# app/category/category_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal, get_db
from . import category_model, category_service
from auth.auth_service import get_current_category

router = APIRouter(
    prefix="/category",
    tags=["Categorys"],
    dependencies=[Depends(get_current_category)]
)

@router.post("/", response_model=category_model.CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(category: category_model.CategoryCreate, db: Session = Depends(get_db)):
    """Endpoint para criar uma nova categoria. Recebe os dados validados (category)
    e a sessão do banco (db) através da injeção de dependência."""
    return category_service.create_new_category(db=db, category=category)

@router.get("/", response_model=List[category_model.CategoryPublic])
def read_category(db: Session = Depends(get_db)):
    """Endpoint para listar todas as categorias."""
    return category_service.get_all_category(db)

@router.get("/{category_id}", response_model=category_model.CategoryPublic)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar uma categoria pelo ID."""
    return category_service.get_category_by_id(db, category_id=category_id)

@router.put("/{category_id}", response_model=category_model.CategoryPublic)
def update_category(category_id: int, category: category_model.CategoryUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar uma categoria."""
    return category_service.update_existing_category(db=db, category_id=category_id, category_in=category)

@router.delete("/{category_id}", response_model=category_model.CategoryPublic)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_to_delete = category_service.get_category_by_id(db, category_id)
    category_data = category_model.CategoryPublic.model_validate(category_to_delete)
    category_service.delete_category_by_id(db=db, category_id=category_id)
    return category_data