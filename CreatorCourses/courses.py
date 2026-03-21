from api import moodle_call
import logging

logger = logging.getLogger(__name__)

# Devuelve todos los cursos disponibles en Moodle
def get_courses() -> list:
    try:
        result = moodle_call('core_course_get_courses')
        return result if isinstance(result, list) else []
    except Exception as e:
        logger.error(f"Error al obtener cursos: {e}")
        return []

'''
    Filtra los cursos por el sufijo del año en el shortname.
    @Param courses: Lista de cursos a filtrar
    @Param year_suffix: Sufijo del año a buscar (OLD_SCHOOL_YEAR o NEW_SCHOOL_YEAR)
    @Return: Lista de cursos que coinciden con el sufijo del año
'''
def filter_courses_by_age(courses: list, year_suffix: str) -> list:
    return [
        course for course in courses
        if course.get('shortname', '').strip().endswith(year_suffix)
    ]

'''
    Creador de curso en la Plataforma Moodle
    @Param fullname: Nombre completo del curso
    @Param shortname: Nombre corto del curso
    @Param description: Descripción del curso
    @Param categoryid: ID de la categoría a la que pertenece el curso
    @Return: Respuesta de Moodle con los detalles del curso creado o None si hay error
'''
def create_course(fullname: str, shortname: str, description: str, categoryid: int) -> dict | None:
    try:
        response = moodle_call('core_course_create_courses', {
            'courses[0][fullname]': fullname,
            'courses[0][shortname]': shortname,
            'courses[0][summary]': description,
            'courses[0][categoryid]': categoryid,
        })
        return response
    except Exception as e:
        logger.error(f"Error al crear curso: {e}")
        return None

# Muestra los detalles de los cursos ordenados por shortname
def view_course_details(courses: list) -> None:
    sorted_courses = sorted(courses, key=lambda x: x.get('shortname', ''))
    for i, course in enumerate(sorted_courses):
        logger.info(
            f"Indice: {i} - ID: {course.get('id')} - "
            f"ShortName: {course.get('shortname')} - "
            f"Fullname: ({course.get('fullname')}) - "
            f"Categoría ID: {course.get('categoryid')} - "
            f"summary: {course.get('summary')}"
        )


'''
    Creador de múltiples cursos en lote
    @Param courses: Lista de diccionarios con los detalles de cada curso a crear
    @Return: Lista de respuestas de Moodle para cada curso creado o None si hay error (Log del evento)
'''
def create_list_courses(courses: list) -> list:
    return [
        create_course(
            course.get('fullname'),
            course.get('shortname'),
            course.get('summary'),
            course.get('categoryid')
        )
        for course in courses
    ]

'''
    Prepara cursos para creación reemplazando los últimos 2 caracteres (que contiene el año lectivo anterior) con el sufijo del nuevo año lectivo.
    @Param courses: Lista de cursos a preparar
    @Param year_suffix: Nuevo sufijo de año a aplicar (NEW_SCHOOL_YEAR)
    @Return: Lista de cursos con shortname y fullname modificados para  la creación
'''
def courses_to_create(courses: list, year_suffix: str) -> list:
    return [
        {
            'shortname': item.get('shortname', '')[:-2] + year_suffix,
            'fullname': item.get('fullname', '')[:-2] + year_suffix,
            'categoryid': item.get('categoryid'),
            'summary': f"Aula Virtual de {item.get('fullname', '')[:-2]}{year_suffix}",
        }
        for item in courses
    ]

'''
    Modifica la categoría de un curso específico.
    @Param courseid: ID del curso a modificar
    @Param new_categoryid: ID de la nueva categoría a asignar al curso
    @Return: Respuesta de Moodle con los detalles del curso modificado o None si hay error (Log del evento)
'''
def modify_course_category(courseid: int, new_categoryid: int) -> dict | None:
    try:
        response = moodle_call('core_course_update_courses', {
            'courses[0][id]': courseid,
            'courses[0][categoryid]': new_categoryid,
        })
        return response
    except Exception as e:
        logger.error(f"Error al modificar curso: {e}")
        return None

'''
    Modifica la categoría de un listado de cursos según un mapeo de categoryid actual -> new_categoryid.
    @Param courses: Lista de cursos a modificar
    @Param new_categories: Diccionario mapeando categoryid actual -> new_categoryid para las categorías a asignar
    @Return: Lista de respuestas de Moodle para cada curso modificado o None si hay error (Log del evento)
'''
def modify_courses_categories(courses: list, new_categories: dict) -> list:
    return [
        modify_course_category(course.get('id'), new_categories[course_category_id])
        for course in courses
        if (course_category_id := course.get('categoryid')) in new_categories
    ]