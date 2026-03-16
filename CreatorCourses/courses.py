from api import moodle_call

def get_courses():
    try:
        return moodle_call('core_course_get_courses')
    except Exception as e:
        print(f"Error al obtener cursos: {e}")
        return []

def filter_courses_by_age(courses, year_suffix):
    filtered_courses = []
    for course in courses:
        shortname = course.get('shortname','').strip()
        if shortname.endswith(year_suffix):
            filtered_courses.append(course)
    return filtered_courses

def create_course(fullname, shortname, description, categoryid):
    try:
        response = moodle_call('core_course_create_courses', {
            'courses[0][fullname]': fullname,
            'courses[0][shortname]': shortname,
            'courses[0][summary]': description,
            'courses[0][categoryid]': categoryid
        })
        return response
    except Exception as e:
        print(f"Error al crear curso: {e}")
        return None

def view_course_details(courses):
    for course in sorted(courses, key=lambda x: x.get('shortname','')):
        print(f"ShortName: {course.get('shortname')} - Fullname: ({course.get('fullname')}) - Categoría ID: {course.get('categoryid')}")
        
# def comparated(a, b):
#     ca=0
#     cb=0
#     for ab in a:
#         if ab.get('shortname','').strip()[:-3] in [bb.get('shortname','').strip()[:-3] for bb in b]:
#             ca += 1
#             print(f"Curso existente: {ab.get('shortname')} - {ab.get('fullname')}")
#         else:
#             print(f"Curso nuevo a crear: {ab.get('shortname')} - {ab.get('fullname')}")
#             cb += 1
#     print(f"Total cursos existentes: {ca}")
#     print(f"Total cursos nuevos a crear: {cb}")