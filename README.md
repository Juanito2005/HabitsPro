# Sistema de Gestión de Tareas y Hábitos (CLI)

Aplicación de consola desarrollada en Python puro (sin librerías externas) para gestionar productividad personal.

## Aclaración Importante

**Sin persistencia: al salir se pierde todo.**
El sistema funciona con un modelo de datos en memoria. Si el programa se cierra, se pierde toda la información generada en esa sesión.

## Cómo ejecutar

El proyecto no requiere gestores de dependencias ni entornos virtuales complejos. Solo necesitas tener Python 3.10 o superior instalado.

Abre tu terminal en la carpeta raíz del proyecto y ejecuta: **python3 main.py**

Menús disponibles
La aplicación cuenta con una navegación clara mediante menús y submenús numerados:

Gestión de tareas: Permite crear, listar (con ordenamiento y paginación), ver detalle, cambiar estado, editar, eliminar y ver el plan del día.

Gestión de hábitos: Permite crear hábitos (diarios o semanales), listarlos, marcarlos como realizados y ver estadísticas de cumplimiento.

Búsqueda y filtros: Motor de búsqueda combinable para encontrar tareas por estado, prioridad, etiquetas, texto en título o fechas de vencimiento.

Estadísticas: Muestra métricas calculadas en tiempo real sobre los estados, prioridades, tiempos estimados vs reales, etiquetas más usadas y progreso de hábitos.

Registro de sesión: Historial paginado de todas las acciones que el usuario realiza en el sistema durante la sesión actual (creaciones, ediciones, cambios de estado).

Salir: Cierra la aplicación (con aviso previo de pérdida de datos).

Qué datos maneja
El sistema gestiona tres entidades principales en memoria (estructuradas en diccionarios de Python dentro del módulo memory_db.py):

Tareas: Mantienen un ID único, título, descripción, prioridad (1-3), estado (pendiente, en_progreso, hecha, cancelada), fecha de creación, vencimiento, lista de etiquetas y seguimiento de tiempo (estimado y real).

Hábitos: Acciones repetibles con ID, nombre, frecuencia (diaria/semanal), objetivo numérico por periodo y un registro de las fechas en las que se cumplió.

Log de Sesión: Lista de eventos que guarda la fecha/hora exacta (timestamp), la acción realizada y los detalles del cambio.

**Decisiones técnicas y estructura:**

* El formato Markdown (`.md`) es el estándar en repositorios de código. Es lo mismo que ves cuando clonas un proyecto de Java en GitHub y lees las instrucciones de compilación de Maven/Gradle.
* Se agregó la aclaración de "Sin persistencia" justo debajo del título, ya que el documento PDF lo solicita como un punto específico a resaltar.
* Las descripciones son directas y explican el modelo de datos en memoria, lo cual ayuda a cualquier desarrollador que revise tu entrega a entender cómo reemplazaste la base de datos tradicional.
