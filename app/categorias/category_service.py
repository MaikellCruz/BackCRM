# app/categorys/category_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import category_model, category_repository
from utils.image_processor import process_image_base64

def create_new_category(db: Session, category: category_model.CategoryCreate):
    db_category = category_repository.get_category_by_name(db, nome=category.nome)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome already registered")

    return category_repository.create_category(db=db, category=category, role_id=category.role_id)

def get_all_categorys(db: Session):
    """Serviço para listar todas as categorias. Neste caso, apenas repassa a chamada."""
    return category_repository.get_categorys(db)

def get_category_by_id(db: Session, category_id: int):
    """Serviço para buscar uma categoria pelo ID, com tratamento de erro."""
    db_category = category_repository.get_category(db, category_id=category_id)
    # REGRA DE NEGÓCIO: Se a categoriaa não for encontrada, retornar um erro 404.
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
    return db_category

def update_existing_category(db: Session, category_id: int, category_in: category_model.CategoryUpdate):
    """Serviço para atualizar uma categoria, com tratamento de erro."""
    db_category = get_category_by_id(db, category_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return category_repository.update_category(db=db, db_category=db_category, category_in=category_in)

def delete_category_by_id(db: Session, category_id: int):
    """Serviço para deletar uma categoria, com tratamento de erro."""
    db_category = get_category_by_id(db, category_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return category_repository.delete_category(db=db, db_category=db_category)
