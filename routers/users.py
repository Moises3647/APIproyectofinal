from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, models, auth

# Manteniendo tu prefijo original /users
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    # 1. Buscar al usuario en la base de datos por su username
    usuario = db.query(models.Usuario).filter(models.Usuario.username == form_data.username).first()
    
    # Si el usuario no existe en la base de datos
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Verificar si la contraseña coincide con el hash guardado
    password_correcto = auth.verificar_password(form_data.password, usuario.hashed_password)
    
    # Si la contraseña está mal
    if not password_correcto:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar el token dinámico JWT usando tu auth.py
    access_token = auth.crear_token_acceso(data={"sub": usuario.username})
    
    # 4. Retornar el token en el formato estándar OAuth2
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/register")
def register(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    try:
        if db.query(models.Usuario).filter(models.Usuario.username == from_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exist",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
        else:
            from models import Usuario
            from auth import obtener_password_hasheado
            
            if from_data.username.strip() == "" or from_data.password.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Campos vacios",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            nuevo_usuario = Usuario(
                username = from_data.username,
                hashed_password = obtener_password_hasheado(from_data.password)
            )
            db.add(nuevo_usuario)
            db.commit()
            return {
                "mensaje": "Usuario creado exitosamente"
            }
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        raise HTTPException(
            status_code=500,
            detail=e
        )
        

