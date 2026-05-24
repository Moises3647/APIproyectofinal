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
    #1. Checar si el usuario estaba registrado anteriormente
    if db.query(models.Usuario).filter(models.Usuario.username == from_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exist",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
    #2. si no intenta crear el nuevo usuario
    try:
        from models import Usuario
        from auth import obtener_password_hasheado
        #si el nombre y contraseña esta vacio marca una excepcion
        if from_data.username.strip() == "" or from_data.password.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campos vacios",
                headers={"WWW-Authenticate": "Bearer"},
            )
        #3. crea el objeto usuario
        nuevo_usuario = Usuario(
            username = from_data.username,
            hashed_password = obtener_password_hasheado(from_data.password)
        )
        #4. lo guarda en la base de datos
        db.add(nuevo_usuario)
        db.commit()
        return {
            "mensaje": "Usuario creado exitosamente"
        }
    except Exception as e:
        #5. si da error regresa la base de datos a un estado anterior y levanta una exepcion
        db.rollback()
        print(f"Error al crear usuario: {e}")
        raise HTTPException(
            status_code=500,
            detail=e
        )
        

