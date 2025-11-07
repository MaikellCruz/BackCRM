# app/categorys/category_repository.py

from sqlalchemy.orm import Session
from app.categorias import category_model
from security import get_password_hash

# --- FUNÇÕES DE LEITURA (READ) ---

def get_category(db: Session, category_id: int):
    """
    Busca uma única categoria pelo seu ID.
    db.query(categoria_model.Category): Inicia uma consulta na tabela Category.
    .filter(categoria_model.Category.id == category_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(category_model.Category).filter(category_model.Category.id == category_id).first()

def get_category_by_name(db: Session, nome: str):
    """Busca uma única categoria pelo seu e-mail."""
    return db.query(category_model.Category).filter(category_model.Category.nome == nome).first()

def get_categorys(db: Session):
    """
    Busca todas as categorias cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(category_model.Category).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_category(db: Session, category: category_model.CategoryCreate, role_id: int = None):
    """
    Cria uma nova categoria no banco de dados.
    """

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_category = category_model.Category(
        nome=category.nome, 
        tipo=category.tipo,
        descricao=category.descrição,
        role_id=role_id
    )

    db.add(db_category)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_category) # Atualiza o objeto db_category com os dados do banco (como o ID gerado).
    return db_category

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_category(db: Session, db_category: category_model.Category, category_in: category_model.CategoryUpdate):
    """Atualiza os dados de uma categoria existente."""
    update_data = category_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.add(db_category) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_category) # Atualiza o objeto com os dados do banco.
    return db_category

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_category(db: Session, db_category: category_model.Category):
    """Deleta uma categoria do banco de dados."""
    db.delete(db_category) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_category


