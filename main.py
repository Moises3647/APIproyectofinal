from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import models, database
from routers import users, sensors  # Busca correctamente dentro de la carpeta routers
import os

# 1. Crear las tablas en la base de datos SQLite si no existen
models.Base.metadata.create_all(bind=database.engine)

# 2. Generar automáticamente los usuarios por defecto (admin y raspberry_pi)
database.crear_usuarios_por_defecto()

app = FastAPI(title="AeroStat API")

# Carpetas y estáticos
if not os.path.exists("capturas"): 
    os.makedirs("capturas")
app.mount("/static/capturas", StaticFiles(directory="capturas"), name="capturas")

# Incluir los módulos separados de la carpeta routers
app.include_router(users.router)
app.include_router(sensors.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)