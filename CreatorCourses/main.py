from config import OLD_SCHOOL_YEAR, NEW_SCHOOL_YEAR
from courses import *
from categories import *
from enrolments import *
from api import moodle_test_connection

def main():
    if moodle_test_connection():
        print("Conexión a Moodle exitosa. Iniciando proceso de creación de cursos...")
        get_courses_list = get_courses()
        
        old_courses = filter_courses_by_age(get_courses_list, OLD_SCHOOL_YEAR)
        old_courses = sorted(old_courses, key=lambda x: x.get('shortname',''))
        print(f"Se encontraron {len(old_courses)} cursos del año {OLD_SCHOOL_YEAR}.")
        
        new_created_courses = filter_courses_by_age(get_courses_list, NEW_SCHOOL_YEAR)
        new_created_courses = sorted(new_created_courses, key=lambda x: x.get('shortname',''))
        print(f"Se encontraron {len(new_created_courses)} cursos del año {NEW_SCHOOL_YEAR}.")
        
        view_course_details(new_created_courses)
        view_course_details(old_courses)
        
        # old_courses.pop(4)
        # view_course_details(old_courses)
        
    else:
        print("No se pudo conectar a Moodle. Verifique la configuración y vuelva a intentarlo.")
    return

if __name__ == "__main__":
    main()