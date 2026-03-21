from dotenv import load_dotenv
import os
import logging
import ast

load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/app.log', encoding='utf-8'),
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

# Helper para parsear listas de .env
def _parse_env_list(env_var: str, default: list | None = None) -> list:
    try:
        value = os.getenv(env_var, "").strip()
        if not value:
            return default or []
        return ast.literal_eval(value)
    except (ValueError, SyntaxError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error al parsear {env_var}: {e}. Usando lista vacía.")
        return default or []

# Estudiantes a inscribir en los cursos nuevos (por ciclo lectivo)
COURSE_ID_WITH_STUDENTS_CORRECTLY: list = _parse_env_list("COURSE_ID_WITH_STUDENTS_CORRECTLY")
COURSE_DIVITION: list = _parse_env_list("COURSE_DIVITION")

# Validación de variables críticas
if not MOODLE_URL or not MOODLE_TOKEN or not OLD_SCHOOL_YEAR or not NEW_SCHOOL_YEAR:
    raise ValueError(
        "Recuerda configurar las variables de entorno MOODLE_URL, MOODLE_TOKEN, OLD_SCHOOL_YEAR y NEW_SCHOOL_YEAR en el archivo .env"
    )