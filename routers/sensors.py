from fastapi import APIRouter, Depends, File, UploadFile, Form, Query, HTTPException
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
import database, models, auth
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Identificador de tu App de Android en Jetpack Compose
PACKAGE_NAME = "gonzalez.moises.apptemphumed"

# CONFIGURACIÓN DE CLOUDINARY
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/s1")
async def recibir_y_subir_foto(
    temperatura: float = Form(...),
    humedad: float = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(auth.verificar_token)
):
    try:
        # 1. Subir la imagen a Cloudinary (Evita que se borre en Render)
        resultado_subida = cloudinary.uploader.upload(
            await foto.read(), 
            folder="aerostat_capturas"
        )
        url_publica = resultado_subida['secure_url'] 

        # 2. Guardar la URL y los datos en la base de datos SQLite
        ahora = datetime.datetime.now()
        nuevo_registro = models.SensorRegistro(
            temperatura=temperatura,
            humedad=humedad,
            foto_path=url_publica, 
            timestamp=ahora
        )
        db.add(nuevo_registro)
        db.commit()
        
        return {
            "status": "success",
            "url_generada": url_publica,
            "fecha": ahora.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar datos: {str(e)}")

@router.get("/s1/latest")
def obtener_ultimo_registro(
    db: Session = Depends(database.get_db),
    token: str = Depends(auth.verificar_token) 
):
    ultimo = db.query(models.SensorRegistro).order_by(models.SensorRegistro.id.desc()).first()
    
    if not ultimo:
        raise HTTPException(status_code=404, detail="No hay datos registrados aún")
        
    return ultimo  


@router.get("/s1/history")
def obtener_historial(
    limit: int = Query(default=20, le=100), 
    db: Session = Depends(database.get_db),
    token: str = Depends(auth.verificar_token)
):
    historial = db.query(models.SensorRegistro).order_by(models.SensorRegistro.id.desc()).limit(limit).all()
    
    return historial