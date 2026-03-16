from api import moodle_call

def get_all_categories():
    return moodle_call("core_course_get_categories")

def get_category_by_id(categoryid):
    return moodle_call(
        "core_course_get_categories",
        {"criteria[0][key]": "id", "criteria[0][value]": categoryid}
    )

def view_categories():
    for category in get_all_categories():
        print(f"ID: {category.get('id')} - Name: {category.get('name')}")