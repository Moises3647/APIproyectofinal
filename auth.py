from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración del algoritmo de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de seguridad JWT (Cambia la firma por algo secreto en producción)
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "una_llave_por_defecto_muy_larga_y_segura_123")
ALGORITHM = "HS256"

# Permite a FastAPI extraer automáticamente el token de las cabeceras HTTP (Bearer Token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# =====================================================================
# 1. FUNCIONES PARA CONTRASENAS (Hasheo y Verificación)
# =====================================================================

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con el hash guardado en la DB."""
    return pwd_context.verify(plain_password, hashed_password)

def obtener_password_hasheado(password: str) -> str:
    """Genera un hash seguro a partir de una contraseña. Se usa para las Seeds/Semillas."""
    return pwd_context.hash(password)

# =====================================================================
# 2. FUNCIONES PARA TOKENS JWT (Creación y Validación)
# =====================================================================

def crear_token_acceso(data: dict) -> str:
    """Genera un token JWT firmado con un tiempo de expiración de 1 año."""
    to_encode = data.copy()
    # Expiración larga (365 días) para evitar que la Raspberry pierda conexión constantemente
    expiracion = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expiracion})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependencia de FastAPI para proteger rutas. 
    Verifica que el token sea válido y no haya expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acceso inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token usando nuestra clave secreta
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username # Retorna el usuario autenticado si todo está bien
    except JWTError:
        raise credentials_exception