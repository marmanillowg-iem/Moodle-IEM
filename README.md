# Moodle-IEM

Script en Python para trabajar con la API web de Moodle y automatizar tareas relacionadas con cursos, categorías e inscripciones.

## Objetivo del proyecto

Este código está orientado a consultar un sitio Moodle mediante servicios web REST y preparar procesos de gestión académica, especialmente para revisar cursos por año escolar y dejar lista la base para crear cursos nuevos o matricular usuarios.

En el estado actual del proyecto, el flujo principal:

- comprueba la conexión con Moodle,
- obtiene el listado completo de cursos,
- filtra los cursos por sufijo de año académico,
- ordena los resultados por `shortname`,
- muestra por consola los cursos encontrados para el año anterior y el nuevo año.

## Estructura del código

El código principal está dentro de la carpeta `CreatorCourses/`.

### `main.py`

Es el punto de entrada del programa.

Su responsabilidad es coordinar la ejecución general:

1. validar que la conexión con Moodle funciona,
2. recuperar todos los cursos disponibles,
3. filtrar cursos del año anterior (`OLD_SCHOOL_YEAR`),
4. filtrar cursos del nuevo año (`NEW_SCHOOL_YEAR`),
5. mostrar por consola los detalles de los cursos del nuevo año.

Actualmente no crea cursos de forma automática desde `main.py`, pero sí deja preparados los datos necesarios para revisar el estado actual antes de automatizar más acciones.

### `api.py`

Contiene la capa de comunicación con Moodle.

- `moodle_call(function, params=None)`: hace una petición `POST` al endpoint REST de Moodle y devuelve la respuesta en formato JSON.
- `moodle_test_connection()`: verifica que el token y la URL funcionan haciendo una llamada a `core_webservice_get_site_info`.

Este módulo centraliza el acceso a la API para que el resto del proyecto no repita lógica de conexión.

### `config.py`

Carga la configuración desde variables de entorno usando `python-dotenv`.

Variables utilizadas:

- `MOODLE_URL`: URL base del sitio Moodle.
- `MOODLE_TOKEN`: token del servicio web.
- `MOODLE_FORMAT`: formato de respuesta, por defecto `json`.
- `OLD_SCHOOL_YEAR`: sufijo usado para identificar cursos del año anterior.
- `NEW_SCHOOL_YEAR`: sufijo usado para identificar cursos del nuevo año.

Si `MOODLE_URL` o `MOODLE_TOKEN` no existen, el programa lanza un error para evitar ejecuciones mal configuradas.

### `courses.py`

Agrupa funciones relacionadas con cursos.

- `get_courses()`: obtiene todos los cursos desde Moodle.
- `filter_courses_by_age(courses, year_suffix)`: filtra cursos cuyo `shortname` termina con un sufijo concreto.
- `create_course(fullname, shortname, description, categoryid)`: crea un curso nuevo en Moodle.
- `view_course_details(courses)`: imprime nombre corto, nombre completo y categoría de cada curso.

La lógica de filtrado actual asume que el año académico está codificado al final del `shortname`.

### `categories.py`

Gestiona la consulta de categorías de Moodle.

- `get_all_categories()`: obtiene todas las categorías.
- `get_category_by_id(categoryid)`: busca una categoría concreta por su identificador.
- `view_categories()`: muestra por consola el listado de categorías.

### `enrolments.py`

Incluye utilidades para trabajar con usuarios inscritos en un curso.

- `get_enrolled_users(courseid)`: recupera todos los usuarios inscritos.
- `get_enrolled_students(courseid)`: filtra usuarios con rol de estudiante (`roleid == 5`).
- `get_enrolled_teachers(courseid)`: filtra usuarios con rol de profesor (`roleid == 3`).
- `enrol_user(courseid, userid, roleid)`: matricula manualmente a un usuario en un curso.

Este módulo todavía no está conectado directamente al flujo principal, pero ya ofrece la base para automatizar matrículas en pasos posteriores del proyecto.

## Flujo actual de ejecución

Cuando se ejecuta el programa:

1. se cargan las variables desde el archivo `.env`,
2. se prueba la conexión con Moodle,
3. se solicitan todos los cursos mediante la API,
4. se separan los cursos del año antiguo y del nuevo año,
5. se imprimen estadísticas y detalles de los cursos detectados.

## Configuración necesaria

Antes de ejecutar el script, debe existir un archivo `.env` con valores similares a estos:

```env
MOODLE_URL=https://tu-moodle.example.com
MOODLE_TOKEN=tu_token_de_servicio_web
MOODLE_FORMAT=json
OLD_SCHOOL_YEAR=25
NEW_SCHOOL_YEAR=26
```

## Dependencias

El proyecto usa principalmente estas librerías:

- `requests`
- `python-dotenv`

Si necesitas instalarlas manualmente:

```bash
pip install requests python-dotenv
```

## Ejecución

Desde la raíz del proyecto:

```bash
python CreatorCourses/main.py
```

## Estado actual del desarrollo

En este momento el proyecto está centrado en inspeccionar y preparar la información de Moodle antes de automatizar acciones más sensibles.

Lo que ya está implementado:

- conexión autenticada a la API de Moodle,
- lectura de cursos,
- filtrado por año académico,
- consulta de categorías,
- consulta de matrículas,
- funciones para crear cursos y matricular usuarios.

Lo que todavía no está automatizado desde el flujo principal:

- clonación o creación masiva de cursos basada en cursos anteriores,
- migración completa de estudiantes o docentes entre cursos,
- sincronización integral entre cursos antiguos y nuevos.

## Resumen

Este repositorio está construyendo una herramienta de automatización para Moodle. La base ya permite conectarse al campus, analizar cursos por año y reutilizar funciones para crear cursos, consultar categorías y gestionar matrículas. El siguiente paso natural sería unir esas piezas en un flujo principal que compare cursos antiguos y nuevos y ejecute acciones automáticamente con validaciones previas.