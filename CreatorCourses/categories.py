from api import moodle_call
import logging

logger = logging.getLogger(__name__)

# Obtiene todas las categorías de Moodle
def get_all_categories() -> list:
    try:
        result = moodle_call('core_course_get_categories')
        return result if isinstance(result, list) else []
    except Exception as e:
        logger.error(f"Error al obtener categorías: {e}")
        return []
    

# Obtiene una categoría específica por su ID
def get_category_by_id(categoryid: int) -> list:
    try:
        result = moodle_call(
            "core_course_get_categories",
            {"criteria[0][key]": "id", "criteria[0][value]": categoryid}
        )
        return result if isinstance(result, list) else []
    except Exception:
        return []
            
# Muestra todas las categorías ordenadas por ID
def view_categories() -> None:
    categories = get_all_categories() or []
    for category in sorted(categories, key=lambda x: x.get('id', 0)):
        logger.info(
            f"ID: {category.get('id')} - "
            f"Name: {category.get('name')} - "
            f"Parent ID: {category.get('parent')} - "
            f"Description: {category.get('description')}"
        )

# Muestra solo las categorías que tienen una categoría padre (by parent != 0)
def view_categories_with_parent() -> None:
    categories = get_all_categories() or []
    for category in sorted(categories, key=lambda x: x.get('id', 0)):
        if category.get('parent') != 0:
            logger.info(
                f"ID: {category.get('id')} - "
                f"Name: {category.get('name')} - "
                f"Parent ID: {category.get('parent')} - "
                f"Description: {category.get('description')}"
            )
            
# Retorna un diccionario mapeando parent_id -> category_id para categorías con padre (parent != 0)
# Ejemplo de retorno: { 10: 15, 20: 25 } donde 10 y 20 son parent_id y 15 y 25 son category_id correspondientes
def get_categories_by_parent() -> dict:
    categories = get_all_categories() or []
    return {
        category.get('parent'): category.get('id')
        for category in categories
        if category.get('parent') != 0
    }