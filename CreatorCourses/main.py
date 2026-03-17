from config import OLD_SCHOOL_YEAR, NEW_SCHOOL_YEAR
from courses import *
from categories import *
from enrolments import *
from api import moodle_test_connection

posiciones = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 92, 93, 94, 101, 120, 121, 122, 123, 124, 125, 126, 127, 128, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162]

def main():
    if moodle_test_connection():
        print("Conexión a Moodle exitosa. Iniciando proceso de creación de cursos...")
        get_courses_list = get_courses()
        
        old_courses = filter_courses_by_age(get_courses_list, OLD_SCHOOL_YEAR)
        old_courses = sorted(old_courses, key=lambda x: x.get('shortname',''))        
        #new_created_courses = filter_courses_by_age(get_courses_list, NEW_SCHOOL_YEAR)
        #new_created_courses = sorted(new_created_courses, key=lambda x: x.get('shortname',''))
        
        #for i in sorted(set(posiciones), reverse=True):
        #    if 0 <= i < len(old_courses):
        #        old_courses.pop(i)
        
        #courses_create_list = course_to_create(old_courses, NEW_SCHOOL_YEAR)
        #print(create_list_courses(courses_create_list))
        #Ya se crearon los cursos
        print(modify_courses_categories(old_courses,category_with_parent_id()))

    else:
        print("No se pudo conectar a Moodle. Verifique la configuración y vuelva a intentarlo.")
    return

if __name__ == "__main__":
    main()