import requests
import logging
from config import MOODLE_URL, MOODLE_TOKEN, MOODLE_FORMAT, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

'''
    Llamada a la API de Moodle
    @Param function: Nombre de la función del servicio web de Moodle
    @Param params: Diccionario con parámetros adicionales para la función
    @Return: Respuesta de Moodle (dict o list) si es exitosa, None si hay error
'''

def moodle_call(function: str, params: dict | None = None) -> dict | list | None:
    payload = {
        **(params or {}),
        'wstoken': MOODLE_TOKEN,
        'moodlewsrestformat': MOODLE_FORMAT,
        'wsfunction': function
    }
    try:
        response = requests.post(
            f'{MOODLE_URL}/webservice/rest/server.php',
            data=payload,
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and ('exception' in data or 'errorcode' in data):
            error_msg = data.get('message', data.get('debuginfo', str(data)))
            logger.error(f"Error de Moodle: {error_msg}")
            return None

        return data
    except requests.exceptions.Timeout:
        logger.error('Error en la llamada a Moodle: tiempo de espera agotado.')
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la llamada a Moodle: {e}")
        return None
    except ValueError:
        logger.error('Error en la llamada a Moodle: la respuesta no es JSON válido.')
        return None
    
# Verifica la conexión a Moodle
def moodle_test_connection() -> bool:
    try:
        return isinstance(moodle_call('core_webservice_get_site_info'), dict)
    except Exception as e:
        logger.error(f"Error al conectar a Moodle: {e}")
        return False