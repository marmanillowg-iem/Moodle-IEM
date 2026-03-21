from config import OLD_SCHOOL_YEAR, NEW_SCHOOL_YEAR
from courses import *
from categories import *
from enrolments import *
from api import moodle_test_connection
import logging

logger = logging.getLogger(__name__)

#TODO!: La funcion no contemplan los estudiantes de un unico curso de 2do y 3ro pues tenemos que diferenciar de otra forma a dichos cursos pues endwith no es suficiente, ya que traerá a las segundas y terceras divisiones de todos los años.
'''
    Inscribe a los estudiantes en los cursos nuevos según su sección y división de referencia
    @Param courses_to_enrol: Lista de cursos nuevos a los cuales se les deben inscribir estudiantes
    @Return: None
'''
def enroll_students_in_new_courses(courses_to_enrol: list) -> None:
    try:
        STUDENTS_TO_ENROL = create_list_students_enrolments()
        section_to_divisions = {
            '21': [21],
            '22': [22],
            '23': [23],
            '31': [31],
            '32': [32],
            '33': [33],
            '4': [41, 42, 43],
            '41': [41],
            '42': [42],
            '43': [43],
            '5': [51, 52, 53],
            '51': [51],
            '52': [52],
            '53': [53],
            '6': [61, 62, 63],
            '61': [61],
            '62': [62],
            '63': [63],
        }

        for course in courses_to_enrol:
            if len(get_enrolled_students(course.get('id'))) == 0:
                logger.info(f"Curso {course.get('shortname')} sin estudiantes inscritos. Inscribiendo estudiantes de referencia...")
                shortname = (course.get('shortname') or '').strip()
                course_id = course.get('id')
                for section_suffix, divisions in section_to_divisions.items():
                    if shortname.endswith(f"{section_suffix}-{NEW_SCHOOL_YEAR}"):
                        for division in divisions:
                            for student_id in STUDENTS_TO_ENROL.get(division, []):
                                enrol_user(course_id, student_id, STUDENT_ROLE_ID)
                        break
                        
    except Exception as e:
        logger.error(f"Error al inscribir estudiantes en los cursos nuevos: {e}")

'''
    Inscribe a los docentes en los cursos nuevos según su sección y división de referencia
    @Param courses_to_enrol: Lista de cursos nuevos a los cuales se les deben inscribir docentes
    @Param old_courses_school_year: Lista de cursos antiguos del año escolar anterior
    @Return: None
'''
def enroll_teachers_in_new_courses(courses_to_enrol: list, old_courses_school_year: list) -> None:
    try:
        for course in courses_to_enrol:
            if len(get_enrolled_teachers(course.get('id'))) == 0:
                logger.warning(f"Curso {course.get('shortname')} - ID: {course.get('id')} sin docentes inscritos. Inscribiendo docentes de referencia...")
                for old_course in old_courses_school_year:
                    if old_course.get('shortname')[:-2] == course.get('shortname')[:-2]:
                        teachers = get_enrolled_teachers(old_course.get('id'))
                        for teacher in teachers:
                             enrol_user(course.get('id'), teacher.get('id'), TEACHER_ROLE_ID)
                        break
    except Exception as e:
        logger.error(f"Error al inscribir docentes en los cursos nuevos: {e}")

# Migracion de cursos: Crea los cursos nuevos, modifica sus categorias y luego inscribe a los estudiantes y docentes de referencia en los cursos nuevos.
def main():
    if moodle_test_connection():
        try:
            logger.info("Conexión a Moodle exitosa. Iniciando la migración...")
            courses_list_in_moodle = get_courses()
            
            # Obtengo los cursos del año lectivo anterior
            old_courses_school_year = sorted(filter_courses_by_age(courses_list_in_moodle, OLD_SCHOOL_YEAR), key=lambda x: x.get('shortname',''))

            # Creo los cursos nuevos reemplazando el año lectivo anterior por el nuevo en el shortname y fullname
            output = create_list_courses(courses_to_create(old_courses_school_year, NEW_SCHOOL_YEAR))
            logger.info(f"Migración de cursos completada: {output}")
            
            # Modifico las categorias de los cursos nuevos para que correspondan a las categorias del año lectivo anterior
            output = modify_courses_categories(old_courses_school_year, get_categories_by_parent())
            logger.info(f"Modificación de categorías completada: {output}")
            
            # Obtengo los cursos nuevos para inscribir a los estudiantes y docentes
            courses_to_enrol = sorted(filter_courses_by_age(courses_list_in_moodle, NEW_SCHOOL_YEAR), key=lambda x: x.get('shortname',''))
            enroll_students_in_new_courses(courses_to_enrol)
            enroll_teachers_in_new_courses(courses_to_enrol, old_courses_school_year)
            
        except Exception as e:
            logger.error(f"Error durante la ejecución: {e}")
    else:
        logger.error("No se pudo conectar a Moodle. Verifique la configuración y vuelva a intentarlo.")
    return  

if __name__ == "__main__":
    main()