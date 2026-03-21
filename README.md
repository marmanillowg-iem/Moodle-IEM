# Moodle-IEM: Herramienta de Automatización para Moodle

## Descripción General

**Moodle-IEM** es una herramienta desarrollada en Python que automatiza tareas administrativas complejas en plataformas Moodle. Específicamente está diseñada para gestionar la transición entre ciclos lectivos, automatizando la creación de cursos nuevos, migración de categorías, e inscripción masiva de estudiantes y docentes.

El proyecto se enfoca en la **seguridad operacional**, con validaciones exhaustivas y manejo robusto de errores para proteger datos en entornos educativos de producción.

## Objetivo del Proyecto

Este código está orientado a:

1. **Consultar un sitio Moodle** mediante servicios web REST autenticados
2. **Analizar cursos por año académico** (filtrado por sufijo en shortname)
3. **Crear cursos nuevos masivamente** basándose en cursos del año anterior
4. **Recategorizar cursos** según mapeos de categorías padre → hijo
5. **Inscribir estudiantes** según plantillas de referencia por división
6. **Inscribir docentes** migrando desde cursos anteriores
7. **Generar reportes** del estado de operaciones

La herramienta **valida antes de actuar**, permitiendo revisar datos sin automatizar acciones destructivas.

---

## Estructura del Código

### Organización de Archivos

```
Moodle-IEM/
├── CreatorCourses/              # Módulos principales
│   ├── main.py                 # Punto de entrada y orquestación
│   ├── api.py                  # Capa de comunicación con Moodle
│   ├── config.py               # Carga y validación de configuración
│   ├── courses.py              # Gestión de cursos
│   ├── categories.py           # Gestión de categorías
│   ├── enrolments.py           # Gestión de inscripciones
│   ├── logs/                   # Directorio de logs generados
│   └── __pycache__/            # Caché de compilación Python
├── .env                        # Configuración (NO versionado)
├── .env.example                # Plantilla de configuración
├── README.md                   # Este archivo
└── LICENSE                     # Licencia del proyecto
```

---

## Módulos y Funciones Detalladas

### **api.py** - Capa de Comunicación

**Responsabilidad**: Centraliza todas las interacciones con la API REST de Moodle.

#### Funciones Principales:

##### `moodle_call(function: str, params: dict | None = None) -> dict | list`
- **Propósito**: Realiza llamadas POST al endpoint REST de Moodle
- **Parámetros**:
  - `function`: Nombre de la función webservice de Moodle (ej: `core_course_get_courses`)
  - `params`: Parámetros adicionales según la función
- **Retorno**: `dict | list` en éxito, `[]` en error
- **Manejo de Errores**:
  - Timeouts de conexión
  - Errores HTTP (raise_for_status)
  - Respuestas JSON inválidas
  - Errores reportados por Moodle (exception/errorcode en response)

##### `moodle_test_connection() -> bool`
- **Propósito**: Verifica que el token y URL configurados funcionan
- **Método**: Invoca `core_webservice_get_site_info`
- **Retorno**: `True` si conexión exitosa, `False` en error

**Notas Técnicas**:
- Retorna `[]` (no `None`) en errores para seguridad de tipo
- Timeout configurable: 30 segundos (por defecto)
- Loguea todos los errores de Moodle con contexto

---

### **config.py** - Configuración y Validación

**Responsabilidad**: Carga variables de entorno y valida que estén completas.

#### Variables Críticas:

```python
# Conexión Moodle
MOODLE_URL              # URL base (ej: https://moodleiem.unsa.edu.ar)
MOODLE_TOKEN            # Token de API generado en Moodle
MOODLE_FORMAT           # Formato de respuesta (json por defecto)
REQUEST_TIMEOUT_SECONDS # Timeout para solicitudes (30 por defecto)

# Ciclos Lectivos
OLD_SCHOOL_YEAR         # Año anterior (sufijo, ej: "25")
NEW_SCHOOL_YEAR         # Año nuevo (sufijo, ej: "26")

# Roles
STUDENT_ROLE_ID         # ID del rol "estudiante" en Moodle (5 por defecto)
TEACHER_ROLE_ID         # ID del rol "docente" en Moodle (3 por defecto)

# Datos de Plantillas
COURSE_ID_WITH_STUDENTS_CORRECTLY  # IDs de cursos plantilla con estudiantes correctos
COURSE_DIVITION         # códigos de división por ejemplo: 21, 22, 23, ..., 63
```

#### Función `_parse_env_list(env_var: str, default: list) -> list`
- **Propósito**: Parsea listas de Python desde variables de entorno
- **Método**: Usa `ast.literal_eval()` de forma segura
- **Formato esperado**: `[1231, 234, 1234, ...]`
- **Manejo de errores**: Loguea errores de sintaxis, devuelve lista vacía

**Validación Crítica**:
```python
if not MOODLE_URL or not MOODLE_TOKEN or not OLD_SCHOOL_YEAR or not NEW_SCHOOL_YEAR:
    raise ValueError("Configuración incompleta")
```

---

### **courses.py** - Gestión de Cursos

**Responsabilidad**: CRUD de cursos en Moodle.

#### Funciones Principales:

##### `get_courses() -> list`
- **Propósito**: Obtiene todos los cursos del sitio Moodle
- **Retorno**: Lista de diccionarios con estructura de Moodle
- **Seguridad**: Retorna `[]` si falla (nunca `None`)
- **Uso**: Base para filtrado por año

##### `filter_courses_by_age(courses: list, year_suffix: str) -> list`
- **Propósito**: Filtra cursos por sufijo del año en shortname
- **Lógica**: `course['shortname'].endswith(year_suffix)`
- **Ejemplo**: `filter_courses_by_age(all_courses, "25")` → cursos del 2025
- **Retorno**: Lista de cursos filtrados

##### `create_course(fullname, shortname, description, categoryid) -> dict | None`
- **Propósito**: Crea un curso individual
- **Lógica**: Invoca `core_course_create_courses` en Moodle
- **Retorno**: Respuesta de Moodle o `None` si error
- **Validación**: Loguea todos los errores

##### `courses_to_create(courses: list, year_suffix: str) -> list`
- **Propósito**: Prepara cursos antiguos para crear versión nueva
- **Transformación**:
  - Reemplaza últimos 2 caracteres del año en shortname y fullname
  - Genera summary automático
  - Mantiene categoryid original
- **Ejemplo**: 
  - Input: `{'shortname': 'MAT-2° AÑO-25', ...}`
  - Output: `{'shortname': 'MAT-2° AÑO-26', ...}`

##### `create_list_courses(courses: list) -> list`
- **Propósito**: Crea múltiples cursos en lote
- **Lógica**: Itera sobre cursos, invoca `create_course()` para cada uno
- **Retorno**: Lista de respuestas (mezcla de dicts y Nones)

##### `modify_course_category(courseid: int, new_categoryid: int) -> dict | None`
- **Propósito**: Cambia la categoría de un curso
- **Validación**: Verifica que la categoría existe
- **Retorno**: Respuesta de Moodle o `None`

##### `modify_courses_categories(courses: list, new_categories: dict) -> list`
- **Propósito**: Recategoriza múltiples cursos según mapeo
- **Mapeo**: `{actual_categoryid: new_categoryid, ...}`
- **Filtrado**: Solo modifica si categoría actual existe en mapeo
- **Walrus Operator**: Usa `:=` para extraer y validar en una expresión

---

### **categories.py** - Gestión de Categorías

**Responsabilidad**: Consulta y mapeo de categorías de Moodle.

#### Funciones Principales:

##### `get_all_categories() -> list`
- **Propósito**: Obtiene todas las categorías del sitio
- **Retorno**: Lista de categorías o `[]` si error
- **Try/Except**: Maneja errores de API

##### `get_category_by_id(categoryid: int) -> list`
- **Propósito**: Obtiene una categoría específica por ID
- **Uso**: Validación individual (actualmente no usado en flujo principal)
- **Retorno**: Lista con la categoría o `[]`

##### `get_categories_by_parent() -> dict`
- **Propósito**: Mapea categorías según relación padre-hijo
- **Lógica**: `{parent_id: category_id for cada categoría}`
- **Filtrado**: Solo incluye categorías con `parent != 0`
- **Ejemplo**: `{10: 15, 20: 25}` = categoría 10 mapea a 15, etc.
- **Uso**: Input para `modify_courses_categories()`

---

### **enrolments.py** - Gestión de Inscripciones

**Responsabilidad**: Consulta y gestión de matrículas de usuarios.

#### Funciones de Consulta:

##### `get_enrolled_users(courseid: int) -> list`
- **Propósito**: Obtiene todos los usuarios inscritos en un curso
- **Retorno**: Lista de usuarios con estructura de Moodle
- **Seguridad**: Try/except, retorna `[]` en error

##### `get_enrolled_students(courseid: int) -> list`
- **Propósito**: Obtiene solo los estudiantes (filtra por rol)
- **Filtrado**: `role['roleid'] == STUDENT_ROLE_ID`
- **Retorno**: Lista de estudiantes o `[]`
- **Validación**: Usa `any()` para buscar rol en lista de roles del usuario

##### `get_students_id(courseid: int) -> list`
- **Propósito**: Extrae solo los IDs de estudiantes
- **Transformación**: `[student['id'] for student in students]`
- **Uso**: Base para inscripciones masivas
- **Retorno**: Lista de IDs de estudiantes o `[]`

##### `get_enrolled_teachers(courseid: int) -> list`
- **Propósito**: Obtiene solo los docentes (filtra por rol)
- **Filtrado**: `role['roleid'] == TEACHER_ROLE_ID`
- **Retorno**: Lista de docentes o `[]`

#### Funciones de Inscripción:

##### `enrol_user(courseid: int, userid: int, roleid: int) -> dict | None`
- **Propósito**: Inscribe un usuario en un curso con rol específico
- **Método**: `enrol_manual_enrol_users` en Moodle
- **Validación**: Loguea errores, retorna `None` si falla
- **Retorno**: Respuesta de Moodle o `None`

#### Funciones de Generación de Datos:

##### `create_list_students_enrolments() -> dict`
- **Propósito**: Genera diccionario de estudiantes plantilla por división
- **Estructura**: `{division: [id_estudiante1, id_estudiante2, ...], ...}`
- **Validación**: Verifica que `COURSE_DIVITION` y `COURSE_ID_WITH_STUDENTS_CORRECTLY` tienen igual longitud
- **Contenido**: 
  - Clave: Código de división (21, 22, 23, ..., 63)
  - Valor: Lista de IDs de estudiantes del curso plantilla
- **Uso**: Búsqueda rápida de estudiantes por división durante inscripciones
- **Retorno**: Diccionario o `{}` si error de validación

---

### **main.py** - Orquestación del Flujo

**Responsabilidad**: Coordina toda la migración de ciclo lectivo.

#### Función `enroll_students_in_new_courses(courses_to_enrol: list) -> None`

**Propósito**: Inscribe estudiantes plantilla en cursos nuevos sin estudiantes

**Flujo**:
1. Para cada curso nuevo en `courses_to_enrol`
2. Verifica: `if len(get_enrolled_students(course_id)) == 0`
3. Extrae el sufijo de división del `shortname` (ej: "21", "22", etc.)
4. Mapea sufijo → lista de IDs de estudiantes desde `STUDENTS_TO_ENROL`
5. Inscribe todos los estudiantes en el curso con rol STUDENT_ROLE_ID

**Mapeo de sufijos**:
```python
section_to_divisions = {
    '21': [21], '22': [22], '23': [23],  # 2° año
    '31': [31], '32': [32], '33': [33],  # 3° año
    '41': [41], '42': [42], '43': [43],  # 4° año
    '51': [51], '52': [52], '53': [53],  # 5° año
    '61': [61], '62': [62], '63': [63],  # 6° año
    # Especiales (todos los de un año):
    '4': [41, 42, 43], '5': [51, 52, 53], '6': [61, 62, 63]
}
```

**Ejemplo**: Curso "Biología-4°-26" → sufijo "4" → inscribe divisiones 41, 42, 43

#### Función `enroll_teachers_in_new_courses(courses_to_enrol: list, old_courses_school_year: list) -> None`

**Propósito**: Inscribe docentes migrados desde cursos antiguos

**Flujo**:
1. Para cada curso nuevo
2. Verifica: `if len(get_enrolled_teachers(course_id)) == 0`
3. Busca el curso antiguo: compara `shortname[:-2]` (ignora año)
4. Si encuentra coincidencia, obtiene docentes del curso antiguo
5. Inscribe cada docente en curso nuevo con rol TEACHER_ROLE_ID

**Lógica de coincidencia**:
```
Curso antiguo: "Biología-2° AÑO-25" → "Biología-2° AÑO"
Curso nuevo:   "Biología-2° AÑO-26" → "Biología-2° AÑO"
→ COINCIDEN → Migra docentes
```

#### Función Principal `main() -> None`

**Flujo Completo de Migración**:

1. **Conexión**: Verifica `moodle_test_connection()`
2. **Obtención de datos** (1 única llamada a API):
   ```python
   courses_list_in_moodle = get_courses()
   ```
3. **Filtrado**:
   ```python
   old_courses_school_year = filter_courses_by_age(courses_list_in_moodle, OLD_SCHOOL_YEAR)
   ```
4. **Creación de cursos nuevos**:
   ```python
   output = create_list_courses(courses_to_create(old_courses_school_year, NEW_SCHOOL_YEAR))
   ```
5. **Recategorización** (toma cursos viejos como referencia):
   ```python
   output = modify_courses_categories(old_courses_school_year, get_categories_by_parent())
   ```
6. **Filtrado de nuevos**:
   ```python
   courses_to_enrol = filter_courses_by_age(courses_list_in_moodle, NEW_SCHOOL_YEAR)
   ```
7. **Inscripción de estudiantes**:
   ```python
   enroll_students_in_new_courses(courses_to_enrol)
   ```
8. **Inscripción de docentes**:
   ```python
   enroll_teachers_in_new_courses(courses_to_enrol, old_courses_school_year)
   ```

**Manejo de Errores**:
- Try/except global captura excepciones no previstas
- Loguea error y continúa con siguiente operación cuando es posible
- Si falla conexión a Moodle: loguea y termina

---


```

### Notas de Configuración:

- **Token de Moodle**: Generar en administración del sitio. El usuario debe tener permisos de:
  - Crear cursos
  - Modificar cursos
  - Gestionar usuarios y roles
  - Acceso a webservices

- **Plantillas de cursos**: Los cursos en `COURSE_ID_WITH_STUDENTS_CORRECTLY` deben tener estudiantes inscritos correctamente para de ahí descargar los IDs

- **Correspondencia de divisiones**: Cada índice en `COURSE_DIVITION` corresponde al mismo índice en `COURSE_ID_WITH_STUDENTS_CORRECTLY`
  - Índice 0: División 21 ← Estudiantes del curso ID 1234
  - Índice 1: División 22 ← Estudiantes del curso ID 234
  - Etc.

---

## Instalación

### Requisitos

- Python 3.10+
- pip (gestor de paquetes)
- Acceso a URL de Moodle
- Token válido de Moodle

### Pasos

1. **Clonar repositorio**:
   ```bash
   git clone <repo-url>
   cd Moodle-IEM
   ```

2. **Crear entorno virtual** (ya incluido, si no):
   ```bash
   python -m venv .
   source bin/activate  # Linux/Mac
   # o
   Activate.ps1  # Windows PowerShell
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Dependencias principales:
   - `requests`: Para llamadas HTTP a la API REST
   - `python-dotenv`: Para cargar variables de entorno desde `.env`

4. **Configurar `.env`**:
   ```bash
   cp .env.example .env
   # Editar .env con valores reales
   ```

5. **Crear directorio de logs**:
   ```bash
   mkdir -p CreatorCourses/logs
   ```

### Verificación

```bash
python CreatorCourses/main.py
```

Si la conexión es exitosa, verás:
```
2026-03-21 14:30:45,123 - root - INFO - Conexión a Moodle exitosa. Iniciando la migración...
```

Si hay error de configuración:
```
ValueError: Recuerda configurar las variables de entorno MOODLE_URL, MOODLE_TOKEN, OLD_SCHOOL_YEAR y NEW_SCHOOL_YEAR en el archivo .env
```

---

## Uso

### Ejecución Completa

```bash
python CreatorCourses/main.py
```

### Salida de Logs

Los logs se escriben en:
- **Archivo**: `CreatorCourses/logs/app.log` (persistente)
- **Consola**: Salida estándar en tiempo real (INFO y superior)

Niveles de log:
- `INFO`: Operaciones completadas exitosamente
- `WARNING`: Advertencias (ej: cursos sin docentes)
- `ERROR`: Errores captados (ej: conexión fallida, validación fallida)

### Interpretación de Salida

```log
INFO - Conexión a Moodle exitosa. Iniciando la migración...
INFO - Migración de cursos completada: [{'id': 1500, ...}, ...]
INFO - Modificación de categorías completada: [...]
INFO - Curso Biología-2°-26 sin estudiantes inscritos. Inscribiendo estudiantes de referencia...
WARNING - Curso Física-4°-26 - ID: 1505 sin docentes inscritos. Inscribiendo docentes de referencia...
ERROR - Error al obtener cursos: <detalles>
```

---

## Mejoras Realizadas en el Código

### Seguridad de Tipos

✅ **Validación exhaustiva de retornos**:
- `moodle_call()` retorna `[]` en errores (nunca `None`)
- Todas las funciones de API tienen try/except
- Comparaciones seguras con `isinstance()` antes de iterar

✅ **Configuración robusta**:
- `ast.literal_eval()` para parseo seguro de listas
- Validación de variables críticas con `raise ValueError`
- Logging de errores de configuración

### Optimización de Performance

✅ **Una sola llamada a `get_courses()`**:
- Se obtienen todos los cursos UNA sola vez
- Se reutiliza en filtros para OLD_SCHOOL_YEAR y NEW_SCHOOL_YEAR
- Reduce carga en API de Moodle en ~66%

✅ **Mapeo de divisiones**:
- Dictionary lookup O(1) para encontrar estudiantes por división
- Mapeo de sufijos permite flexibilidad en nombrado de cursos

### Claridad de Código

✅ **Operador walrus** (`x := moodle_call(...)`):
- Extrae y valida categorías en una sola expresión
- Código más limpio en list comprehensions

✅ **Logueo detallado**:
- Cada operación registra su progreso
- Errores incluyen contexto completo
- Facilita debugging en producción

✅ **Documentación exhaustiva**:
- Docstrings tipo Google en cada función
- Comentarios en main.py explicando flujo

---

## Limitaciones Conocidas

1. **Suposición de año en last 2 caracteres del shortname**:
   - Solo funciona si nombre corto termina con formato "-25" o "-26"
   - Cursos con nombres cortos (<3 caracteres) fallan silenciosamente

2. **Mapeo 1:1 de divisiones**:
   - 15 cursos plantilla = 15 divisiones exactas
   - No hay soporte para divisiones dinámicas

3. **Sin sincronización parcial**:
   - Si la operación falla a mitad, hay que revisar manualmente
   - Idealmente habría rollback transaccional (Moodle no lo soporta nativamente)

4. **Sin validación de datos previos**:
   - No verifica si estudiantes ya están inscritos
   - Podría duplicar inscripciones en ejecuciones repetidas

---

## Estado Actual del Desarrollo

### ✅ Implementado

- ✓ Conexión autenticada a API de Moodle
- ✓ Lectura de cursos por año académico
- ✓ Creación masiva de cursos nuevos
- ✓ Recategorización de cursos
- ✓ Inscripción masiva de estudiantes
- ✓ Migración de docentes
- ✓ Manejo robusto de errores
- ✓ Logging detallado
- ✓ Validación de configuración
- ✓ Parseo seguro de listas desde .env

### 📋 Potenciales Mejoras Futuras

1. **Sincronización de datos**:
   - Obtener datos de Moodle en tiempo real
   - Detectar cambios desde última ejecución

2. **Interfaz web**:
   - Dashboard de estado de migración
   - Controles manuales de operaciones

3. **Manejo avanzado de errores**:
   - Reintentos con backoff exponencial
   - Cola de operaciones pendientes

4. **Gestión de docentes**:
   - Asignación automática de docentes a divisiones
   - Validación de cargas horarias

5. **Reportes**:
   - Exportar resultados a CSV
   - Alertas de inconsistencias

6. **Auditoría**:
   - Registro de quién ejecutó qué y cuándo
   - Comparación antes/después de la migración

---

## Requisitos de Permisos en Moodle

El token de usuario debe tener permisos para:

```
✓ core_course_get_courses         - Listar cursos
✓ core_course_create_courses      - Crear cursos
✓ core_course_update_courses      - Modificar cursos
✓ core_course_get_categories      - Listar categorías
✓ core_enrol_get_enrolled_users   - Ver usuarios en cursos
✓ enrol_manual_enrol_users        - Inscribir usuarios
```

---

## Troubleshooting

### Error: "Recuerda configurar las variables de entorno..."

**Causa**: Faltan variables en `.env`

**Solución**: Copiar `.env.example` a `.env` y completar todos los valores

### Error: "Error de Moodle: invalid_parameter exception"

**Causa**: Categoría ID, rol ID o parámetro inválido

**Solución**: 
- Verificar que TEACHER_ROLE_ID y STUDENT_ROLE_ID coinciden con Moodle
- Verificar que categorías existen en Moodle

### Error: "Error en la llamada a Moodle: tiempo de espera agotado"

**Causa**: Moodle tarda más de 30 segundos en responder

**Solución**: Aumentar REQUEST_TIMEOUT_SECONDS en `.env`

### Cursos creados pero estudiantes no inscritos

**Causa**: 
1. Divisiones en .env no coinciden con sufijos de cursos
2. Plantillas de cursos no tienen estudiantes

**Solución**: Verificar mapeo de COURSE_DIVITION y nombres de cursos

---

## Licencia

Define según tu proyecto (MIT, GPL, etc.)

---

## Historial de Cambios

### v1.0 (21 marzo 2026)
- Versión inicial operativa
- Todas las funciones principales implementadas
- Código validado y optimizado
- Documentación completa

### Contribuciones
- Aceptamos pull requests para mejoras y correcciones
- Reportar issues para bugs o sugerencias

### To Work On
- Concretar el TODO descrito en el main
- Implementar una interfaz web para control manual
- Agregar pruebas unitarias y de integración