# EXPLAINME.md

## LOGS
Los sensores de la red EcoWatch generan continuamente registros ambientales que pueden provenir de múltiples fuentes y en diferentes formatos.

Tu desafío será implementar una solución que permita leer y validar datos de logs provenientes de distintas fuentes potenciales, considerando que estos pueden llegar en distintos formatos. Además, deberás establecer reglas claras de validación para asegurar que los datos que ingresan al sistema tengan la calidad necesaria para ser procesados.

### Requisitos funcionales:
- Simula al menos una fuente de logs (por ejemplo, .csv, .json o datos en memoria). 
    - Implementación: 
        - La clase [`LogReader`](src/log_reader.py) está diseñada para leer y validar logs desde archivos CSV, pero su estructura permite extender fácilmente el soporte a otros formatos (como JSON o datos en memoria) agregando nuevos métodos de lectura. Esto cumple con el requerimiento de soportar múltiples fuentes y formatos de logs, y deja el sistema preparado para futuras extensiones sin modificar el resto del código.
        - Referencia: [`src/log_reader.py`](src/log_reader.py)
- Valida que cada entrada contenga los campos clave esperados: timestamp, tipo, sala, métricas ambientales.
    - Implementación:
        - La clase [`LogReader`](src/log_reader.py) define los campos requeridos en la constante `REQUIRED_FIELDS` y valida que cada fila del archivo contenga estos campos y que no sean nulos antes de crear un objeto `Log`. Si falta algún campo o hay un valor nulo, la fila se descarta automáticamente.
        - Además, durante la creación de cada objeto `Log`, si ocurre un error de tipo o de valor (por ejemplo, un formato de fecha inválido o un valor no convertible a float), el sistema captura la excepción específica (`ValueError`, `TypeError`), imprime una advertencia indicando el índice de la fila y el motivo, y continúa procesando el resto de los registros. Esto mejora la trazabilidad y el debugging de datos problemáticos, evitando silenciar errores inesperados.
        - Referencia: [`src/log_reader.py`](src/log_reader.py), métodos `read_logs` y `_is_valid_row`, manejo de excepciones y logging de advertencias.
- Piensa cómo podrías manejar registros mal formados, o cómo se adaptarían nuevas fuentes en el futuro (no es necesario implementarlo).
    - Implementación:
        - Los registros mal formados (con datos faltantes o tipos incorrectos) son descartados durante la lectura y validación en [`LogReader`](src/log_reader.py). Además, la arquitectura permite extender fácilmente la clase para soportar nuevas fuentes de datos (por ejemplo, agregando un método para leer JSON o datos en memoria), sin modificar el resto del sistema.
        - Referencia: [`src/log_reader.py`](src/log_reader.py), métodos `read_logs` y `_is_valid_row`.

## CACHÉ TEMPORAL
El sistema de EcoWatch debe garantizar el acceso rápido a registros recientes (últimos 5 minutos), ya que muchas decisiones operativas se toman con base en datos en tiempo real. Sin embargo, no todos los registros llegan en orden o a tiempo, lo que implica desafíos adicionales de consistencia y rendimiento.

El reto para ti será diseñar una solución que permita mantener en memoria solo los registros relevantes más recientes, considerando que algunos pueden llegar con retraso ("late events") y que los usuarios necesitarán hacer consultas rápidas por sala o por timestamp.

### Requisitos funcionales
- Implementa una estructura que mantenga en memoria los registros correspondientes a los últimos 5 minutos.
    - Implementación:
        - Se implementó la clase [`TemporalCache`](src/cache.py), que utiliza una estructura `deque` para almacenar en memoria solo los registros de los últimos 5 minutos. Cada vez que se agrega un nuevo log, se purgan automáticamente los registros que quedan fuera de la ventana temporal.
        - Referencia: [`src/cache.py`](src/cache.py), métodos `add_log` y `_purge_old_logs`.
- Permite consultas rápidas por sala o por timestamp.
    - Implementación:
        - La clase [`TemporalCache`](src/cache.py) provee los métodos `get_logs_by_room` y `get_logs_by_timestamp`, que permiten filtrar y recuperar rápidamente los registros en memoria según la sala o el timestamp.
        - Referencia: [`src/cache.py`](src/cache.py), métodos `get_logs_by_room` y `get_logs_by_timestamp`.
- Si quieres ir un paso más allá, considera cómo se comportaría el sistema si llegaran eventos con retraso (“late events”).
    - Implementación:
        - La lógica de purgado en [`TemporalCache`](src/cache.py) se basa en el timestamp de los logs, no en el orden de llegada. Esto permite que, aunque un evento llegue tarde, si su timestamp está dentro de la ventana de 5 minutos, será incluido en la caché; si no, será descartado en el siguiente purgado.
        - Referencia: [`src/cache.py`](src/cache.py), métodos `add_log` y `_purge_old_logs`.

### PROCESAMIENTO MODULARIZADO Y ORIENTADO A OBJETOS
El sistema debe ser flexible y fácil de mantener a medida que crece la complejidad del monitoreo ambiental. Para ello, es clave que el diseño del software represente correctamente las entidades del dominio (sensores, salas, registros, reportes) y que se puedan agregar nuevas funcionalidades sin reescribir grandes partes del código.

De esta manera, se espera que diseñes un sistema que refleje de manera coherente el modelo de datos de EcoWatch utilizando los principios de la Programación Orientada a Objetos (POO). Identifica las entidades clave del dominio y desarrolla clases que encapsulan sus datos y comportamientos. Tu solución debe facilitar la reutilización, la extensión de funcionalidades y el mantenimiento a lo largo del tiempo.

### Requisitos funcionales
- Usa clases para representar las entidades del dominio, como Log, Sensor, Sala, Reporte.
    - Implementación:
        - Se crearon clases específicas para cada entidad del dominio: [`Log`](src/log.py) para los registros, [`Room`](src/room.py) para las salas, y [`Report`](src/report.py) como clase base para los reportes. Esto permite modelar de forma clara y coherente cada concepto del sistema.
        - Referencia: [`src/log.py`](src/log.py), [`src/room.py`](src/room.py), [`src/report.py`](src/report.py)
- Encapsula atributos y comportamientos para organizar mejor tu sistema.
    - Implementación:
        - Cada clase encapsula sus atributos y métodos, por ejemplo, `Room` tiene un método `add_log` para agregar registros, y `Log` almacena todos los datos relevantes de un registro ambiental. Esto mejora la organización y la mantenibilidad del código.
        - Referencia: [`src/log.py`](src/log.py), [`src/room.py`](src/room.py)
- Diseña tu código pensando en que pueda crecer con el tiempo (ej. agregar nuevos sensores, nuevas reglas).
    - Implementación:
        - El diseño orientado a objetos y el uso de patrones como Factory y Strategy permiten agregar nuevas entidades, sensores, reglas o reportes sin modificar el código existente, solo extendiendo las clases o registrando nuevos tipos en la fábrica.
        - Referencia: [`src/report_factory.py`](src/report_factory.py), [`src/report_strategy.py`](src/report_strategy.py), explicación en la sección de extensibilidad.

## REPORTES
El equipo directivo de EcoWatch necesita acceder a reportes diarios y personalizados para tomar decisiones rápidas. Estos reportes deben poder adaptarse fácilmente a diferentes necesidades: monitorear zonas específicas, identificar alertas críticas o analizar el desempeño ambiental general. Además, a futuro se prevé que se soliciten nuevos tipos de reportes, por lo que la solución debe facilitar su extensión sin reescribir el sistema completo.

Se te solicita diseñar una arquitectura que permita generar reportes ejecutivos adaptables, donde cada tipo de reporte pueda tener una lógica de procesamiento diferente. La solución debe ser modular, fácil de extender y capaz de integrar nuevos tipos de reportes sin modificar el código existente. Se espera que apliques patrones de diseño apropiados para desacoplar la lógica de creación y la lógica de ejecución de los reportes.

### Requisitos funcionales
- Implementa, al menos, dos tipos de reportes (por ejemplo: estado por sala, alertas críticas).
    - Implementación:
        - Se implementaron dos tipos de reportes: [`StateByRoomReport`](src/reports_state_by_room.py) (estado por sala) y [`CriticalAlertsReport`](src/reports_critical_alerts.py) (alertas críticas), cada uno con su propia lógica de procesamiento y estrategia.
        - Referencia: [`src/reports_state_by_room.py`](src/reports_state_by_room.py), [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)
- Aplicá al menos dos patrones de diseño. Uno debe ser Factory, el otro puede ser Strategy o Decorator, según lo que te resulte más claro y útil.
    - Implementación:
        - Se aplicó el patrón Factory en la clase [`ReportFactory`](src/report_factory.py) para la creación desacoplada de reportes, y el patrón Strategy en las clases [`StateByRoomStrategy`](src/reports_state_by_room.py) y [`CriticalAlertsStrategy`](src/reports_critical_alerts.py) para desacoplar la lógica de generación de reportes.
        - Referencia: [`src/report_factory.py`](src/report_factory.py), [`src/report_strategy.py`](src/report_strategy.py), [`src/reports_state_by_room.py`](src/reports_state_by_room.py), [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)
- La solución debe ser extensible: debería poder agregarse un nuevo tipo de reporte sin reescribir lo anterior.
    - Implementación:
        - Gracias a la arquitectura basada en Factory y Strategy, se puede agregar un nuevo tipo de reporte creando una nueva clase de reporte y su estrategia, y registrándola en la fábrica, sin modificar el código existente. Esto está documentado en la sección de extensibilidad y demostrado en el archivo [`src/report_factory.py`](src/report_factory.py).
        - Referencia: explicación en la sección de extensibilidad, [`src/report_factory.py`](src/report_factory.py)

## Extras
- Uso de @decorators para logging, validaciones o benchmarking
    - Implementación:
        - Se implementó un decorador de logging llamado `log_execution` en [`src/log_reader.py`](src/log_reader.py), que permite registrar en consola la ejecución de métodos clave, como la lectura de logs. Esto facilita el monitoreo y debugging del flujo de datos.
        - Referencia: [`src/log_reader.py`](src/log_reader.py), decorador `log_execution` y su uso en el método `read_logs`.
- Uso de pandas para generar reportes tabulares
    - Implementación:
        - Todos los reportes (`StateByRoomReport`, `CriticalAlertsReport`) generan su salida en formato `pandas.DataFrame`, lo que permite un manejo eficiente y flexible de los datos tabulares.
        - Referencia: [`src/reports_state_by_room.py`](src/reports_state_by_room.py), [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)
- Exportación automática a .csv o .xlsx
    - Implementación:
        - Se agregó un método utilitario `export_report` en [`src/report_factory.py`](src/report_factory.py) que permite exportar cualquier reporte generado (en formato DataFrame) a archivos `.csv` o `.xlsx` de manera automática, facilitando la integración con herramientas externas y la distribución de reportes.
        - Referencia: [`src/report_factory.py`](src/report_factory.py), función `export_report`.
- Diseño de una API con FastAPI para consultar logs o reportes
    - Implementación:
        - Se implementó una API básica utilizando FastAPI en [`src/api.py`](src/api.py`). Esta API permite consultar los logs validados y generar reportes (por ejemplo, estado por sala o alertas críticas) a través de endpoints HTTP, facilitando la integración con otros sistemas o dashboards.
        - Referencia: [`src/api.py`](src/api.py)
- Pruebas unitarias con unittest o pytest
    - Implementación:
        - Se implementaron pruebas unitarias básicas utilizando `pytest` en el archivo [`tests/test_log_reader.py`](tests/test_log_reader.py). Estas pruebas validan la correcta lectura y validación de logs, asegurando que el sistema maneje correctamente los datos válidos y descarte los inválidos.
        - Referencia: [`tests/test_log_reader.py`](tests/test_log_reader.py)
- Configuración de variables sensibles con .env
    - Implementación:
        - Se implementó el uso de variables de entorno sensibles mediante un archivo `.env` y la librería `python-dotenv`. Ahora, por ejemplo, la ruta del archivo de logs puede configurarse desde el entorno, facilitando la portabilidad y seguridad del sistema.
        - Referencia: [`src/api.py`](src/api.py), uso de `os.getenv` y carga de `.env`.

---

This document explains the key design and implementation decisions made for the EcoWatch project. Each section references the relevant code and the requirement it addresses.

---

## Design Patterns Used: Factory & Strategy
**Requirement:** Apply at least two design patterns. One must be Factory, the other can be Strategy or Decorator.

### Factory Pattern
- **Where:** [`src/report_factory.py`](src/report_factory.py)
- **How:**
  - The `ReportFactory` class allows for the registration and creation of report objects by type, decoupling the instantiation logic from the usage logic.
  - Example usage in [`src/__main__.py`](src/__main__.py):
    ```python
    factory = ReportFactory()
    factory.register_default_reports()
    state_report = factory.create_report("state_by_room")
    alerts_report = factory.create_report("critical_alerts")
    ```
- **Why:** This enables easy extensibility and maintenance, as new report types can be added without modifying existing code.

### Strategy Pattern
- **Where:**
  - [`src/report_strategy.py`](src/report_strategy.py)
  - [`src/reports_state_by_room.py`](src/reports_state_by_room.py)
  - [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)
- **How:**
  - Each report class (e.g., `StateByRoomReport`, `CriticalAlertsReport`) delegates its report generation logic to a strategy class (`StateByRoomStrategy`, `CriticalAlertsStrategy`).
  - This allows for different processing logic to be swapped in or extended without changing the report interface.
  - Example:
    ```python
    # src/reports_state_by_room.py
    class StateByRoomReport(Report):
        def __init__(self, strategy=None):
            self.strategy = strategy or StateByRoomStrategy()
        def generate(self, logs):
            return self.strategy.generate(logs)
    ```
- **Why:** This supports the open/closed principle and makes it easy to add new report types or change logic without modifying existing code.

---

## 1. Log Ingestion and Validation
**Requirement:** Simulate at least one log source (CSV), validate required fields, and ensure data quality.

- **Decision:** Used `pandas` for robust CSV reading and validation, as it simplifies handling missing data and type conversion.
- **Why:** `pandas` is efficient for tabular data and easily extensible to other formats (e.g., JSON).
- **Where:** [`src/log_reader.py`](src/log_reader.py)
- **How:** The `LogReader` class checks for required fields and parses each row into a `Log` object, skipping invalid rows.

---

## 2. In-Memory Temporal Cache
**Requirement:** Keep only the last 5 minutes of logs in memory, support fast queries by room or timestamp, and handle late events.

- **Decision:** Used a `deque` to store logs and a sliding window approach to purge old entries.
- **Why:** `deque` allows efficient appends and pops from both ends, ideal for time-based sliding windows.
- **Where:** [`src/cache.py`](src/cache.py)
- **How:** The `TemporalCache` class manages log addition and purging, with methods for querying by room or timestamp.

---

## 3. Object-Oriented Domain Modeling
**Requirement:** Use classes to represent domain entities (Log, Room, Report), encapsulate data and behavior, and ensure extensibility.

- **Decision:** Defined clear classes for each entity, with attributes and methods encapsulated.
- **Why:** OOP makes the system modular, maintainable, and easy to extend (e.g., new sensors, new reports).
- **Where:**
  - [`src/log.py`](src/log.py) — `Log` class
  - [`src/room.py`](src/room.py) — `Room` class
  - [`src/report.py`](src/report.py) — `Report` abstract base class

---

## 4. Report Generation with Design Patterns
**Requirement:** Implement at least two report types, use Factory and Strategy patterns, and ensure extensibility.

- **Decision:**
  - **Factory Pattern:** Used for report creation, decoupling report instantiation from usage.
  - **Strategy Pattern:** Each report delegates its logic to a strategy class, allowing easy addition of new report types.
- **Why:**
  - Factory allows new reports to be registered without changing existing code.
  - Strategy enables different processing logic for each report, supporting open/closed principle.
- **Where:**
  - Factory: [`src/report_factory.py`](src/report_factory.py)
  - Strategy: [`src/report_strategy.py`](src/report_strategy.py), [`src/reports_state_by_room.py`](src/reports_state_by_room.py), [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)
- **How:**
  - Register new reports in the factory with `register_report` or `register_default_reports`.
  - Each report (e.g., `StateByRoomReport`, `CriticalAlertsReport`) uses a strategy for its logic.

---

## 5. Tabular Reporting with pandas
**Requirement:** Generate tabular reports for executive use.

- **Decision:** Used `pandas.DataFrame` for report output.
- **Why:** `pandas` provides powerful aggregation, filtering, and export capabilities.
- **Where:**
  - [`src/reports_state_by_room.py`](src/reports_state_by_room.py)
  - [`src/reports_critical_alerts.py`](src/reports_critical_alerts.py)

---

## 6. Extensibility and Maintainability
**Requirement:** System should be easy to extend (new log sources, new reports, new rules).

- **Decision:**
  - All core logic is modular and separated by responsibility.
  - Adding a new report or log source requires minimal changes.
- **Why:** Follows SOLID principles and best practices for scalable software.
- **Where:**
  - New log sources: extend `LogReader` ([`src/log_reader.py`](src/log_reader.py))
  - New reports: add a new report and strategy, register in factory ([`src/report_factory.py`](src/report_factory.py))

---

## 7. Example Usage
**Requirement:** Provide a clear entry point for running the system.

- **Decision:** Added a main script that demonstrates reading logs and generating reports.
- **Where:** [`src/__main__.py`](src/__main__.py)

---

## 8. Why Not...?
- **Why not use a database for cache?** For the 5-minute window and real-time needs, in-memory is faster and simpler.
- **Why not hardcode report logic?** Using patterns makes it easier to add new reports without modifying existing code.
- **Why not use only functions?** Classes and OOP make the system more maintainable and extensible for future growth.

---

## 9. Further Improvements
- Add decorators for logging, validation, or benchmarking.
- Export reports to CSV/XLSX.
- Add API endpoints (e.g., with FastAPI).
- Add unit tests (e.g., with pytest).
- Use environment variables for configuration.

---

## Extensibility: Adding New Report Types Without Rewriting Existing Code
**Requirement:** The solution must be extensible: it should be possible to add a new report type without rewriting existing code.

- **How is this achieved?**
  - The use of the **Factory** pattern ([`src/report_factory.py`](src/report_factory.py)) allows you to register new report types dynamically.
  - The **Strategy** pattern ([`src/report_strategy.py`](src/report_strategy.py)) lets you encapsulate new report logic in a new strategy class.
  - Existing code (other reports, the main script, etc.) does **not** need to be modified to support new reports.

- **Example:**
  1. Create a new strategy class (e.g., `MyNewReportStrategy`) in a new file or in `src/`.
  2. Create a new report class (e.g., `MyNewReport`) that uses your strategy.
  3. Register your new report in the factory:
     ```python
     factory.register_report("my_new_report", MyNewReport)
     ```
  4. Now you can create and use your new report type:
     ```python
     my_report = factory.create_report("my_new_report")
     my_report.generate(logs)
     ```

- **Why does this work?**
  - The main script and the rest of the system interact with reports only through the factory and the common interface (`Report`).
  - No existing report or factory code needs to be changed—just register the new type.

- **References:**
  - Factory: [`src/report_factory.py`](src/report_factory.py)
  - Strategy: [`src/report_strategy.py`](src/report_strategy.py)
  - Example usage: [`src/__main__.py`](src/__main__.py)

For any questions or suggestions, see the code comments and docstrings, or contact the author.

## Ejecución de la API (FastAPI)

Para ejecutar la API de EcoWatch desarrollada con FastAPI:

### 1. Instala FastAPI y Uvicorn (si aún no lo hiciste):
```bash
pip install fastapi uvicorn
```

### 2. Ejecuta el servidor con Uvicorn
Desde la raíz del proyecto, ejecuta:
```bash
uvicorn src.api:app --reload
```
- `src.api:app` indica que el objeto `app` está en el archivo `src/api.py`.
- `--reload` permite recargar automáticamente el servidor cuando cambias el código (útil para desarrollo).

### 3. Accede a la API
- **Documentación interactiva:**  [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc (otra doc):**  [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Ejemplos de endpoints disponibles
- `GET /logs`  — Devuelve los logs validados (puedes limitar la cantidad con el parámetro `limit`).
- `GET /report/state_by_room`  — Devuelve el reporte de estado por sala.
- `GET /report/critical_alerts`  — Devuelve el reporte de alertas críticas.

### Exportación de reportes vía API
- `GET /report/state_by_room/export?format=csv|xlsx` — Descarga el reporte de estado por sala como CSV o XLSX.
- `GET /report/critical_alerts/export?format=csv|xlsx` — Descarga el reporte de alertas críticas como CSV o XLSX.

Ejemplo URLs:
- Descargar estado por sala como CSV: `http://localhost:8000/report/state_by_room/export?format=csv`
- Descargar alertas críticas como XLSX: `http://localhost:8000/report/critical_alerts/export?format=xlsx`

Ejemplo de solicitudes cURL:
```bash
curl -o state_by_room_report.csv "http://localhost:8000/report/state_by_room/export?format=csv"
curl -o state_by_room_report.xlsx "http://localhost:8000/report/state_by_room/export?format=xlsx"
curl -o critical_alerts_report.csv "http://localhost:8000/report/critical_alerts/export?format=csv"
curl -o critical_alerts_report.xlsx "http://localhost:8000/report/critical_alerts/export?format=xlsx"
```

### Consulta de logs por rango de fechas, sala y sensor
- `GET /logs/query?start_time_date=YYYY-MM-DD HH:MM:SS&end_time_date=YYYY-MM-DD HH:MM:SS&room=RoomName[&sensor=SensorName]` — Devuelve los logs filtrados por rango de fechas, sala y opcionalmente sensor.

Ejemplo URL:
- `http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1`

Ejemplos de solicitudes cURL:
```bash
curl "http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1"
curl "http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room2&sensor=SensorA"
```

#### Exportación de resultados de la consulta
- `GET /logs/query/export?start_time_date=...&end_time_date=...&room=...&sensor=...&format=csv|xlsx` — Descarga los logs filtrados como CSV o XLSX.

Ejemplo:
```bash
curl -o filtered_logs.csv "http://localhost:8000/logs/query/export?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1&format=csv"
curl -o filtered_logs.xlsx "http://localhost:8000/logs/query/export?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room2&sensor=SensorA&format=xlsx"
```

---
