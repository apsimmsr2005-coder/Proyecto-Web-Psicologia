"""
Archivo principal de la API SaludMente Comunitaria.

Crea la aplicacion FastAPI, habilita CORS, inicializa la base de datos y
registra los controladores REST del sistema.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db, seed_db
from app.controller.auth_controller_api import router as auth_router
from app.controller.beneficiario_controller_api import router as beneficiario_router
from app.controller.reporte_controller_api import router as reporte_router
from app.controller.seguimiento_controller_api import router as seguimiento_router
from app.controller.sesion_controller_api import router as sesion_router
from app.controller.usuario_controller_api import router as usuario_router


app = FastAPI(
    title="SaludMente Comunitaria API",
    description="API REST para gestion de atencion psicologica comunitaria.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
seed_db()

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(beneficiario_router)
app.include_router(sesion_router)
app.include_router(seguimiento_router)
app.include_router(reporte_router)


@app.get("/")
def root():
    return {
        "message": "SaludMente Comunitaria API",
        "docs": "/docs",
        "credenciales_demo": {
            "correo": "admin@sistema.com",
            "contrasena": "admin123",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
