from api import moodle_call

def get_enrolled_users(courseid):
    try:
        return moodle_call('core_enrol_get_enrolled_users', {
            'courseid': courseid
        })
    except Exception as e:
        print(f"Error al obtener usuarios inscritos: {e}")
        return []

def get_enrolled_students(courseid):
    try:
        users = get_enrolled_users(courseid)
        students = [user for user in users if any(role['roleid'] == 5 for role in user.get('roles', []))]
        return students
    except Exception as e:
        print(f"Error al filtrar estudiantes inscritos: {e}")
        return []
    
def get_enrolled_teachers(courseid):
    try:
        users = get_enrolled_users(courseid)
        teachers = [user for user in users if any(role['roleid'] == 3 for role in user.get('roles', []))]
        return teachers
    except Exception as e:
        print(f"Error al filtrar docentes inscritos: {e}")
        return []
    
def enrol_user(courseid, userid, roleid):
    try:
        response = moodle_call('enrol_manual_enrol_users', {
            'enrolments[0][roleid]': roleid,
            'enrolments[0][userid]': userid,
            'enrolments[0][courseid]': courseid
        })
        return response
    except Exception as e:
        print(f"Error al inscribir usuario: {e}")
        return None  