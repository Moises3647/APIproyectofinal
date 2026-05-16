from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./sensores.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FUNCIÓN PARA GENERAR USUARIOS POR DEFECTO ---
def crear_usuarios_por_defecto():
    from models import Usuario # Importación local para evitar imports cíclicos
    from auth import obtener_password_hasheado # Tu función de encriptación
    
    db = SessionLocal()
    try:
        # 1. Verificar si ya existe el usuario admin para no duplicarlo
        admin_existe = db.query(Usuario).filter(Usuario.username == "admin").first()
        
        if not admin_existe:
            print("Generando usuarios por defecto en la base de datos...")
            
            # Usuario para ti (Monitorear en la App `gonzalez.moises.apptemphumed`)
            usuario_admin = Usuario(
                username="admin",
                hashed_password=obtener_password_hasheado("password123"), # Cambia esto por algo seguro
                role="admin"
            )
            
            # Usuario exclusivo para la Raspberry Pi 2
            usuario_rasp = Usuario(
                username="raspberry_pi",
                hashed_password=obtener_password_hasheado("rasberrypi2"),
                role="device"
            )
            
            db.add(usuario_admin)
            db.add(usuario_rasp)
            db.commit()
            print(" Usuarios creados exitosamente (admin y raspberry_pi).")
        else:
            print(" Los usuarios por defecto ya existen en la base de datos.")
            
    except Exception as e:
        print(f"Error al crear usuarios por defecto: {e}")
    finally:
        db.close()