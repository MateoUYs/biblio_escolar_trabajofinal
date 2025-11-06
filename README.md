# BiblioEscolar – MATEO INDART, JAVIER FERNDANDEZ

## Objetivo general

El proyecto BiblioEscolar tiene como objetivo desarrollar una aplicación en **Python** con interfaz gráfica de escritorio utilizando **Tkinter**, que permita gestionar una biblioteca escolar.  
Su propósito es brindar una herramienta que facilite el registro, la consulta y la administración de libros, usuarios y préstamos, integrando visualización de datos y automatización de tareas de mantenimiento.

Esta aplicación fue diseñada dentro del marco del **Proyecto de Contexto Abierto en Python 2025**, cumpliendo con los requerimientos establecidos:  
- Interfaz gráfica.  
- Persistencia de datos.  
- Visualización mediante gráficos.  
- Automatización de procesos.  
- Pruebas unitarias.  

---

**BiblioEscolar** es una aplicación de escritorio orientada al ámbito educativo, pensada para instituciones que deseen organizar y gestionar su biblioteca de manera digital y sencilla.  
Permite registrar libros, usuarios y préstamos, visualizar la información almacenada y automatizar ciertas acciones, como la eliminación de préstamos vencidos.

Las principales características de la aplicación son:

- **Gestión de libros**: alta, baja y modificación de registros, con información sobre ISBN, título, autor, género y disponibilidad.  
- **Gestión de usuarios**: registro de docentes y estudiantes, con identificación por tipo de usuario.  
- **Préstamos y devoluciones**: registro de préstamos activos y devolución de ejemplares.  
- **Automatización de mantenimiento**: eliminación automática de préstamos vencidos cada 24 horas mediante la librería APScheduler.  
- **Visualización de datos**: gráfico de barras con la cantidad de libros por género utilizando Matplotlib.  
- **Roles diferenciados**: ciertas funciones (como eliminar préstamos o usuarios) solo están disponibles para el rol docente.  

---

## Instalación y ejecución

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/MateoUYs/biblio_escolar_trabajofinal
cd biblio_escolar
```

### 2. Crear un entorno virtual (opcional)

```bash
python -m venv venv
```

Activar el entorno virtual:

- En Windows:
  ```bash
  venv\Scripts\activate
  ```
- En Linux o macOS:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## Estructura del proyecto

```
biblio_escolar/
│
├── ui/
│   ├── ventana_principal.py
│   ├── formulario_libro.py
│   ├── formulario_usuario.py
│   ├── tabla_prestamos.py
│   └── form_login.py
│
├── data/
│   ├── base_datos.py
│   └── seed_demo.py
│
├── tests/
│   ├── test_db_conexion.py
│   ├── test_libros.py
│   ├── test_usuarios.py
│   ├── test_prestamos_flujo.py
│   └── test_historial.py
│
├── requirements.txt
├── README.md
└── main.py
```

---

## Persistencia de datos

La base de datos **SQLite3** se crea automáticamente al iniciar el programa.  
Contiene tres tablas principales: **libros**, **usuarios** y **prestamos**.

---

## Automatización con APScheduler

Se integró la librería **APScheduler** para programar tareas automáticas.  
El sistema elimina préstamos vencidos cada 24 horas.

```python
from apscheduler.schedulers.background import BackgroundScheduler
from data.base_datos import eliminar_prestamos_vencidos

def iniciar_tareas_automaticas():
    scheduler = BackgroundScheduler()
    scheduler.add_job(eliminar_prestamos_vencidos, 'interval', hours=24)
    scheduler.start()
```

---

## Visualización de datos

Se utiliza **Matplotlib** para mostrar un gráfico de libros agrupados por género, accesible desde el menú principal.

---

## Pruebas automatizadas

Se implementaron pruebas unitarias con **Pytest**, ubicadas en `/tests`, para validar:  
1. Creación de tablas.  
2. Registro de libros y usuarios.  
3. Flujo de préstamos y devoluciones.  
4. Eliminación del historial de devoluciones.  

Ejecutar con:

```bash
pytest -v
```

---

## Librerías utilizadas y justificación

| Categoría | Librería | Descripción |
|------------|-----------|-------------|
| Interfaz gráfica | Tkinter | Interfaz gráfica nativa de Python. |
| Persistencia | sqlite3 | Base de datos local y ligera. |
| Visualización | Matplotlib | Gráficos de libros por género. |
| Automatización | APScheduler | Elimina préstamos vencidos automáticamente. |
| Testing | Pytest | Pruebas unitarias del sistema. |

---

## Fundamento didáctico

El desarrollo del proyecto permitió aplicar conocimientos de programación, persistencia, automatización y pruebas en un contexto educativo real.  
La automatización mediante APScheduler promueve la reflexión sobre la eficiencia y el mantenimiento de los sistemas, alineándose con el enfoque de **Paulo Freire (1970)** sobre el uso crítico de la tecnología como medio para el aprendizaje significativo.

---

## Evaluación esperada

| Criterio | Ponderación |
|-----------|--------------|
| Funcionalidad y requisitos cumplidos | 25 |
| Interfaz y experiencia de usuario | 5 |
| Persistencia y automatización | 15 |
| Calidad y estructura del código | 15 |
| Pruebas automatizadas | 10 |
| Documentación | 10 |
| Fundamento didáctico | 5 |
| **Total** | **85 puntos** |

---

## Autoría y licencia

**Autor:** Mateo Indart Vega, Javier Fernandez.  
**Instituto:** Instituto de Formación Docente “José Pedro Varela” – Rosario, Uruguay  
**Versión:** v1.0.2  
**Licencia:** Uso educativo libre.
