from fastapi import FastAPI
from .routers.router import router as app_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.title = "InventariX"
app.version = "0.1.2"
app.description = """
Inventory and Logistics Management System\n

InventariX is a comprehensive solution for efficient inventory and logistics management, designed to streamline business processes and enhance operational visibility. With an intuitive interface powered by the robustness of FastAPI, InventariX provides a complete set of tools enabling businesses to maintain precise control over their stock and optimize the supply chain.
"""

# Configuracion de CORS para permitir todas las solicitudes
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los metodos (GET, POST, PUT y DELETE)
    allow_headers=["*"],  # Permitir todos los encabezados, incluyendo 'Authorization'
)

app.include_router(app_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)