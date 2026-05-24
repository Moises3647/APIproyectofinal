# AeroStat API 🚀

**AeroStat API** es una solución robusta desarrollada con **FastAPI** diseñada para el monitoreo ambiental. Permite recolectar datos de temperatura y humedad, junto con capturas visuales, integrando almacenamiento en la nube y persistencia de datos local.

Este proyecto está diseñado para trabajar en conjunto con una **Raspberry Pi 2** y una aplicación Android (`gonzalez.moises.apptemphumed`).

## ✨ Características

- **Autenticación JWT**: Seguridad mediante tokens de acceso de larga duración, ideales para dispositivos IoT como la Raspberry Pi.
- **Integración con Cloudinary**: Las imágenes capturadas se suben automáticamente a la nube para garantizar su disponibilidad.
- **Persistencia de Datos**: Uso de SQLAlchemy con SQLite para el almacenamiento de registros históricos.
- **Auto-Seeding**: Creación automática de usuarios base (`admin` y `raspberry_pi`) al iniciar la aplicación por primera vez.
- **Documentación Interactiva**: Acceso inmediato a Swagger UI y ReDoc.

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI
- **Base de Datos**: SQLite & SQLAlchemy (ORM)
- **Seguridad**: Passlib (Bcrypt) & Python-Jose (JWT)
- **Almacenamiento**: Cloudinary API
- **Servidor**: Uvicorn

## ⚙️ Configuración

Antes de ejecutar la aplicación, debes configurar tus credenciales en los archivos correspondientes (o preferiblemente mediante variables de entorno):

1.  **Cloudinary** (`routers/sensors.py`):
    Actualiza `cloud_name`, `api_key` y `api_secret` con tus credenciales de Cloudinary.
2.  **JWT Secret** (`auth.py`):
    Cambia `SECRET_TOKEN` por una cadena aleatoria y segura.

## 🚀 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <tu-repositorio>
   cd APIproyectofinal
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la API**:
   ```bash
   python main.py
   ```
   La API estará disponible en `http://localhost:8000`.

## 📖 Documentación de la API

Puedes interactuar con los endpoints directamente desde el navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

| Método | Endpoint | Descripción | Autenticación |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/login` | Obtener token de acceso (OAuth2). | No |
| `POST` | `/users/register` | Registrar un nuevo usuario. | No |
| `POST` | `/sensors/s1` | Registrar temperatura, humedad y foto. | **Sí (JWT)** |
| `GET` | `/sensors/s1/latest` | Obtener el registro más reciente. | **Sí (JWT)** |
| `GET` | `/sensors/s1/history` | Obtener historial de registros. | **Sí (JWT)** |

## 🔑 Usuarios por Defecto

El sistema crea automáticamente dos usuarios si no existen:
- **Administrador**: `admin` / `password123`
- **Dispositivo (RPi)**: `raspberry_pi` / `rasberrypi2`

## Creacion de nuevos usuarios

Puedes crear nuevos usuarios de tipo User para visualizar los datos por la app
- **Nombre de usuario** debe ser unico para cada usuario

## 📂 Estructura del Proyecto

```text
├── main.py              # Punto de entrada de la aplicación
├── auth.py              # Lógica de seguridad y JWT
├── database.py          # Configuración de DB y creación de usuarios
├── models.py            # Modelos de SQLAlchemy
├── routers/             # Endpoints divididos por módulos
│   ├── sensors.py       # Gestión de datos de sensores e imágenes
│   └── users.py         # Gestión de login y usuarios
└── requirements.txt     # Dependencias del proyecto
```