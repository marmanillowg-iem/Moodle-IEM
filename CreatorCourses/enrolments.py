from api import moodle_call
from config import STUDENT_ROLE_ID, TEACHER_ROLE_ID, COURSE_ID_WITH_STUDENTS_CORRECTLY, COURSE_DIVITION
import logging

logger = logging.getLogger(__name__)

'''
    Obtiene todos los usuarios inscriptos en un curso (by Course ID)
    @Param courseid: ID del curso
    @Return: Lista de usuarios inscriptos en el curso o vacia en caso de error
'''
def get_enrolled_users(courseid: int) -> list:
    try:
        return moodle_call('core_enrol_get_enrolled_users', {
            'courseid': courseid
        })
    except Exception as e:
        logger.error(f"Error al obtener usuarios inscritos: {e}")
        return []

'''    
    Obtiene solo los estudiantes inscritos en un curso
    @Param courseid: ID del curso
    @Return: Lista de estudiantes inscriptos en el curso o vacia en caso de error
'''
def get_enrolled_students(courseid: int) -> list:
    try:
        users = get_enrolled_users(courseid)
        return [
            user for user in users
            if any(role['roleid'] == STUDENT_ROLE_ID for role in user.get('roles', []))
        ]
    except Exception as e:
        logger.error(f"Error al filtrar estudiantes inscritos: {e}")
        return []

'''
    Obtiene solo los IDs de los estudiantes inscritos en un curso
    @Param courseid: ID del curso
    @Return: Lista de IDs de estudiantes inscriptos en el curso o vacia en caso de error
'''
def get_students_id(courseid: int) -> list:
    try:
        students = get_enrolled_students(courseid)
        return [student['id'] for student in students]
    except Exception as e:
        logger.error(f"Error al obtener IDs de estudiantes inscritos: {e}")
        return []   
   
'''
    Obtiene solo los docentes inscritos en un curso
    @Param courseid: ID del curso
    @Return: Lista de docentes inscriptos en el curso o vacia en caso de error
''' 
def get_enrolled_teachers(courseid: int) -> list:
    try:
        users = get_enrolled_users(courseid)
        return [
            user for user in users
            if any(role['roleid'] == TEACHER_ROLE_ID for role in user.get('roles', []))
        ]
    except Exception as e:
        logger.error(f"Error al filtrar docentes inscritos: {e}")
        return []

'''
    Inscribe un usuario en un curso con un rol específico
    @Param courseid: ID del curso
    @Param userid: ID del usuario a inscribir
    @Param roleid: ID del rol con el que se inscribirá al usuario (estudiante, docente, etc.)
    @Return: Respuesta de la API o None en caso de error (Log de eventos)
'''    
def enrol_user(courseid: int, userid: int, roleid: int) -> dict | None:
    try:
        response = moodle_call('enrol_manual_enrol_users', {
            'enrolments[0][roleid]': roleid,
            'enrolments[0][userid]': userid,
            'enrolments[0][courseid]': courseid
        })
        return response
    except Exception as e:
        logger.error(f"Error al inscribir usuario: {e}")
        return None   

'''
    Crea un diccionario con la division como clave y una lista de IDs de estudiantes (que toman funcion de plantillas) para luego ser inscriptos en los cursos correspondientes a esa division.
    @Return: Diccionario con la division como clave y una lista de IDs de estudiantes como valor o vacio en caso de error (Log de eventos)
'''
def create_list_students_enrolments() -> dict:
    if len(COURSE_DIVITION) != len(COURSE_ID_WITH_STUDENTS_CORRECTLY):
        logger.error(
            "Longitudes desiguales: COURSE_DIVITION=%s, COURSE_ID_WITH_STUDENTS_CORRECTLY=%s",
            len(COURSE_DIVITION),
            len(COURSE_ID_WITH_STUDENTS_CORRECTLY),
        )
        return {}

    return {
        division: get_students_id(course_id)
        for division, course_id in zip(COURSE_DIVITION, COURSE_ID_WITH_STUDENTS_CORRECTLY)
    }
