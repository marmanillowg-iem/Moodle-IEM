import requests
from config import MOODLE_URL, MOODLE_TOKEN, MOODLE_FORMAT

def moodle_call(function, params = None):
    if params is None:
        params = {}
    params.update({
        'wstoken': MOODLE_TOKEN,
        'moodlewsrestformat': MOODLE_FORMAT,
        'wsfunction': function
    })
    try:
        response = requests.post(MOODLE_URL + '/webservice/rest/server.php', data=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la llamada a Moodle: {e}")
        return None
    
def moodle_test_connection():
    try:
        if isinstance(moodle_call('core_webservice_get_site_info'), dict):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al conectar a Moodle: {e}")
        return False