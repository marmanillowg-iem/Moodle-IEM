from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Conexion a Moodle
MOODLE_URL: str | None = os.getenv("MOODLE_URL")
MOODLE_TOKEN: str | None = os.getenv("MOODLE_TOKEN")
MOODLE_FORMAT: str = os.getenv("MOODLE_FORMAT", "json")
REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

# Ciclos Lectivos a Trabajar
OLD_SCHOOL_YEAR: str | None = os.getenv("OLD_SCHOOL_YEAR")
NEW_SCHOOL_YEAR: str | None = os.getenv("NEW_SCHOOL_YEAR")

# Roles ID 
STUDENT_ROLE_ID: int = int(os.getenv("STUDENT_ROLE_ID", "5"))
TEACHER_ROLE_ID: int = int(os.getenv("TEACHER_ROLE_ID", "3"))

# Validación de variables críticas
if not MOODLE_URL or not MOODLE_TOKEN:
    raise ValueError(
        "Recuerda configurar las variables de entorno MOODLE_URL y MOODLE_TOKEN en el archivo .env"
    )