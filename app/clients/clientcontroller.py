# app/clients/controller.py
from fastapi import APIRouter, HTTPException, status
from .clientmodels import ClientCreate, ClientPublic, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])

# Simulação de um banco de dados em memória
fake_db = {
    1: {"id": 1, "email": "client1@example.com", "full_name": "client One", "password": "password1"},
    2: {"id": 2, "email": "client2@example.com", "full_name": "client Two", "password": "password2"},
}

@router.post("/", response_model=ClientPublic, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate):
    new_id = max(fake_db.keys() or [0]) + 1
    new_client_data = client.model_dump()
    new_client_data["id"] = new_id
    fake_db[new_id] = new_client_data
    return ClientPublic(**new_client_data)

@router.get("/", response_model=list[ClientPublic])
def list_clients():
    # Converte os dicionários do 'banco de dados' para o modelo público
    return [ClientPublic(**client_data) for client_data in fake_db.values()]

@router.put("/{client_id}", response_model=ClientPublic)
def update_client(client_id: int, client_update: ClientUpdate):
    if client_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")

    stored_client_data = fake_db[client_id]
    update_data = client_update.model_dump(exclude_unset=True) # Apenas campos enviados

    updated_client = stored_client_data.copy()
    updated_client.update(update_data)
    fake_db[client_id] = updated_client

    return ClientPublic(**updated_client)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int):
    if client_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")

    del fake_db[client_id]
    # Com status 204, a resposta não deve ter corpo. O FastAPI cuida disso.