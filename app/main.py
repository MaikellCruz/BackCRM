import uvicorn
from fastapi import FastAPI


from clients import clientcontroller
from users import usercontroller

# 1. Cria a instância principal da nossa aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

app.include_router(usercontroller.router)
app.include_router(clientcontroller.router)

@app.get("/")
def read_root():
    return {"message": "API está no ar!"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)