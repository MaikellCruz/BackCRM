# app/clients/client_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.clients import client_repository, client_model
from app.utils.image_processor import process_image_base64

def create_new_client(db: Session, client: client_model.ClientCreate):
    db_client = client_repository.get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Processa a imagem se fornecida (converte AVIF para JPEG automaticamente)
    try:
        processed_image = process_image_base64(client.profile_image_base64)
        # Cria uma cópia dos dados do cliente com a imagem processada
        client_data = client.model_copy()
        client_data.profile_image_base64 = processed_image
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro no processamento da imagem: {e}"
        )

    return client_repository.create_client(db=db, client=client_data, role_id=client.role_id)

def get_all_clients(db: Session):
    """Serviço para listar todos os clientes. Neste caso, apenas repassa a chamada."""
    return client_repository.get_clients(db)

def get_client_by_id(db: Session, client_id: int):
    """Serviço para buscar um cliente pelo ID, com tratamento de erro."""
    db_client = client_repository.get_client(db, client_id=client_id)
    # REGRA DE NEGÓCIO: Se o cliente não for encontrado, retornar um erro 404.
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
    return db_client

def update_existing_client(db: Session, client_id: int, client_in: client_model.ClientUpdate):
    """Serviço para atualizar um cliente, com tratamento de erro."""
    db_client = get_client_by_id(db, client_id) # Reutiliza a lógica para buscar e checar se o cliente existe.
    
    # Processa a imagem se fornecida (converte AVIF para JPEG automaticamente)
    if client_in.profile_image_base64:
        try:
            processed_image = process_image_base64(client_in.profile_image_base64)
            # Cria uma cópia dos dados com a imagem processada
            client_data = client_in.model_copy()
            client_data.profile_image_base64 = processed_image
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Erro no processamento da imagem: {e}"
            )
    else:
        client_data = client_in
    
    return client_repository.update_client(db=db, db_client=db_client, client_in=client_data)

def delete_client_by_id(db: Session, client_id: int):
    """Serviço para deletar um cliente, com tratamento de erro."""
    db_client = get_client_by_id(db, client_id) # Reutiliza a lógica para buscar e checar se o cliente existe.
    return client_repository.delete_client(db=db, db_client=db_client)