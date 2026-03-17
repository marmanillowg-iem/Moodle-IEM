from api import moodle_call

diccionary_categories = {
    1: "Sin categoría",
    2: "Primaria",
    3: "Secundaria",
    4: "Superior",
    5: "Administración",
    6: "Docentes",
    7: "Alumnos",
    8: "Otros"
}

def get_all_categories():
    return moodle_call("core_course_get_categories")

def get_category_by_id(categoryid):
    return moodle_call(
        "core_course_get_categories",
        {"criteria[0][key]": "id", "criteria[0][value]": categoryid}
    )

def view_categories():
    for category in sorted(get_all_categories(), key=lambda x: x.get('id', 0)):
        print(f"ID: {category.get('id')} - Name: {category.get('name')} - Parent ID: {category.get('parent')} - Description: {category.get('description')}")

def view_only_category_with_parent_id():
    for category in sorted(get_all_categories(), key=lambda x: x.get('id', 0)):
        if category.get('parent') != 0:
            print(f"ID: {category.get('id')} - Name: {category.get('name')} - Parent ID: {category.get('parent')} - Description: {category.get('description')}")
            
def category_with_parent_id():
    diccionary_categories_with_parent_id = {}
    for category in sorted(get_all_categories(), key=lambda x: x.get('id', 0)):
        if category.get('parent') != 0:
            diccionary_categories_with_parent_id[category.get('parent')] = category.get('id')
    return diccionary_categories_with_parent_id