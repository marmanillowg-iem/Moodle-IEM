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
            'courses[0][categoryid]': categoryid,
        })
        return response
    except Exception as e:
        print(f"Error al crear curso: {e}")
        return None

def view_course_details(courses):
    i = 0
    for course in sorted(courses, key=lambda x: x.get('shortname','')):
        print(f"Indice: {i} - ShortName: {course.get('shortname')} - Fullname: ({course.get('fullname')}) - Categoría ID: {course.get('categoryid')} - summary: {course.get('summary')}")
        i += 1

def create_list_courses(courses):
    results = []
    for course in courses:
        results.append(create_course( course.get('fullname'), course.get('shortname'), course.get('summary'), course.get('categoryid')))
    return results

def course_to_create(course, year_suffix):
    courses_to_create = []
    for course in course:
        courses_to_create.append({
            'shortname': course.get('shortname')[:-2] + year_suffix,
            'fullname': course.get('fullname')[:-2] + year_suffix,
            'categoryid': course.get('categoryid'),
            'summary': 'Aula Virtual de ' + course.get('fullname')[:-2] + year_suffix,
            'displayname': course.get('fullname')[:-2] + year_suffix,
        })
    return courses_to_create

def modify_course_category(courseid, new_categoryid):
    try:
        response = moodle_call('core_course_update_courses', {
            'courses[0][id]': courseid,
            'courses[0][categoryid]': new_categoryid,
        })
        return response
    except Exception as e:
        print(f"Error al modificar curso: {e}")
        return None

def modify_courses_categories(courses, new_categories):
    results = []
    for course in courses:
        course_category_id = course.get('categoryid')
        if course_category_id in new_categories:
            results.append(modify_course_category(course.get('id'), new_categories[course_category_id]))
    return results