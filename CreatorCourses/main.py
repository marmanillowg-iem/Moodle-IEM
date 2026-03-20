from config import OLD_SCHOOL_YEAR, NEW_SCHOOL_YEAR
from courses import *
from categories import *
from enrolments import *
from api import moodle_test_connection
import logging

logger = logging.getLogger(__name__)

# posiciones = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 92, 93, 94, 101, 120, 121, 122, 123, 124, 125, 126, 127, 128, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162]

# coursos_referencia_estudiantes = {
#     21: get_students_id(1352),
#     22: get_students_id(1353),
#     23: get_students_id(1354),
#     31: get_students_id(1355),
#     32: get_students_id(1356),
#     33: get_students_id(1357),
#     41: get_students_id(1278),
#     42: get_students_id(1279),
#     43: get_students_id(1280),
#     51: get_students_id(1358),
#     52: get_students_id(1359),
#     53: get_students_id(1360),
#     61: get_students_id(1361),
#     62: get_students_id(1362),
#     63: get_students_id(1363),
# }

# docentes_faltantes = {
# 1108: 1355,
# 1109: 1356,
# 1110: 1357,
# 1111: 1358,
# 1112: 1359,
# 1113: 1360,
# 1115: 1361,
# 1116: 1363,
# 1135: 1295,
# 1162: 1302,
# 1161: 1303,
# 1160: 1304,
# 1159: 1305,
# 1158: 1306,
# 1157: 1307,
# 1156: 1308,
# 1155: 1309,
# 1154: 1310,
# 1153: 1311,
# 1152: 1312,
# 1151: 1313,
# 1208: 1335,
# 1243: 1332,
# 1238: 1317,
# 1240: 1323,
# 1267: 1326,
# 1268: 1336,
# 1269: 1328,
# 1242: 1329,
# 1144: 1430,
# 1142: 1432,
# 1139: 1435,
# 1138: 1436,
# 1137: 1437,
# 1136: 1438,
# 1245: 1297,
# 1246: 1298,
# 1247: 1299,
# 1248: 1300,
# 1249: 1301
# }

def main():
    if moodle_test_connection():
        logger.info("Conexión a Moodle exitosa. Iniciando proceso de creación de cursos...")
        get_courses_list = get_courses()
        
        old_courses = filter_courses_by_age(get_courses_list, OLD_SCHOOL_YEAR)
        old_courses = sorted(old_courses, key=lambda x: x.get('shortname',''))        
        new_created_courses = filter_courses_by_age(get_courses_list, NEW_SCHOOL_YEAR)
        new_created_courses = sorted(new_created_courses, key=lambda x: x.get('shortname',''))
        
        #for i in sorted(set(posiciones), reverse=True):
        #    if 0 <= i < len(old_courses):
        #        old_courses.pop(i)
        
        #courses_create_list = course_to_create(old_courses, NEW_SCHOOL_YEAR)
        #print(create_list_courses(courses_create_list))
        #Ya se crearon los cursos
        #print(modify_courses_categories(old_courses,category_with_parent_id()))
        #view_course_details(new_created_courses)
    
        # for course in new_created_courses:
        #     if get_enrolled_students(course.get('id')) == []:
        #         if course.get('shortname').strip('').endswith('21-26'):
        #             for student_id in coursos_referencia_estudiantes[21]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('22-26'):
        #             for student_id in coursos_referencia_estudiantes[22]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('23-26'):
        #             for student_id in coursos_referencia_estudiantes[23]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('31-26'):
        #             for student_id in coursos_referencia_estudiantes[31]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('32-26'):
        #             for student_id in coursos_referencia_estudiantes[32]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('33-26'):
        #             for student_id in coursos_referencia_estudiantes[33]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('4-26'):
        #             for student_id in coursos_referencia_estudiantes[41]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[42]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[43]:
        #                 enrol_user(course.get('id'), student_id, 5)
                    
        #         elif course.get('shortname').strip('').endswith('41-26'):
        #             for student_id in coursos_referencia_estudiantes[41]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('42-26'):
        #             for student_id in coursos_referencia_estudiantes[42]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('43-26'):
        #             for student_id in coursos_referencia_estudiantes[43]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('5-26'):
        #             for student_id in coursos_referencia_estudiantes[51]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[52]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[53]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
                        
        #         elif course.get('shortname').strip('').endswith('51-26'):
        #             for student_id in coursos_referencia_estudiantes[51]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('52-26'):
        #             for student_id in coursos_referencia_estudiantes[52]:
        #                 enrol_user(course.get('id'), student_id, 5) 
                        
        #         elif course.get('shortname').strip('').endswith('53-26'):
        #             for student_id in coursos_referencia_estudiantes[53]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('6-26'):
        #             for student_id in coursos_referencia_estudiantes[61]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[62]:
        #                 enrol_user(course.get('id'), student_id, 5)
        #             for student_id in coursos_referencia_estudiantes[63]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
                        
        #         elif course.get('shortname').strip('').endswith('61-26'):
        #             for student_id in coursos_referencia_estudiantes[61]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('62-26'):
        #             for student_id in coursos_referencia_estudiantes[62]:
        #                 enrol_user(course.get('id'), student_id, 5)
                        
        #         elif course.get('shortname').strip('').endswith('63-26'):
        #             for student_id in coursos_referencia_estudiantes[63]:
        #                 enrol_user(course.get('id'), student_id, 5)
        
        # for student_id in coursos_referencia_estudiantes[21]:
        #     enrol_user(1369, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[22]:
        #     enrol_user(1369, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[23]:
        #     enrol_user(1369, student_id, 5)
            
        # for student_id in coursos_referencia_estudiantes[31]:
        #     enrol_user(1370, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[32]:
        #     enrol_user(1370, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[33]:
        #     enrol_user(1370, student_id, 5)
        
        # for student_id in coursos_referencia_estudiantes[61]:
        #     enrol_user(1425, student_id, 5)
        #     enrol_user(1440, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[62]:
        #     enrol_user(1425, student_id, 5)
        #     enrol_user(1440, student_id, 5)
        # for student_id in coursos_referencia_estudiantes[63]:
        #     enrol_user(1425, student_id, 5)
        #     enrol_user(1440, student_id, 5)
        # for course in new_created_courses:
        #     if get_enrolled_students(course.get('id')) == []:
        #         print(f"Curso {course.get('shortname')} sin estudiantes inscritos. Inscribiendo estudiantes de referencia...")
        # for course in new_created_courses:
        #     if get_enrolled_teachers(course.get('id')) == []:
        #        for old_course in old_courses:
        #            if old_course.get('shortname')[:-2] == course.get('shortname')[:-2]:
        #                teachers = get_enrolled_teachers(old_course.get('id'))
        #                for teacher in teachers:
        #                     enrol_user(course.get('id'), teacher.get('id'), 3)
        for course in new_created_courses:
            if get_enrolled_teachers(course.get('id')) == []:
                logger.warning(f"Curso {course.get('shortname')} - ID: {course.get('id')} sin docentes inscritos. Inscribiendo docentes de referencia...")
        # for course in old_courses:
        #     logger.debug(f"Curso antiguo: ID: {course.get('id')} - ShortName: {course.get('shortname')}")
    #     for old_id, new_id in docentes_faltantes.items():
    #         teachers = get_enrolled_teachers(old_id)
    #         for teacher in teachers:
    #             enrol_user(new_id, teacher.get('id'), 3)
    else:
        logger.error("No se pudo conectar a Moodle. Verifique la configuración y vuelva a intentarlo.")
    return

if __name__ == "__main__":
    main()