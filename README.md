# Actividad A6.2 – Reservation System (Hotel / Customer / Reservation)

Este repositorio implementa un sistema simple de **Hoteles**, **Clientes** y **Reservas** con:

- Persistencia en archivos **JSON**
- Servicios con operaciones CRUD y lógica de negocio
- Manejo de datos inválidos sin detener la ejecución
- Pruebas unitarias con `unittest`
- Flujo funcional manual (`manual_run.py`) usando `data/*.json`
- Evidencia de ejecución y análisis estático (`flake8`, `pylint`, `coverage`) en `results/`


---

## 1) Requisitos y herramientas

- Python 3
- Dependencias en `requirements.txt`

Herramientas:

- `unittest` (incluido en Python)
- `flake8`
- `pylint`
- `coverage`

Instalación:

```bash
pip install -r requirements.txt
```

---

## 2) Estructura del proyecto

```text
.
├── data/
│   ├── customers.json
│   ├── hotels.json
│   └── reservations.json
├── results/
│   ├── coverage_final.txt
│   ├── coverage.txt
│   ├── flake8_final.txt
│   ├── flake8.txt
│   ├── functional_run.txt
│   ├── pylint_src_final.txt
│   ├── pylint_src.txt
│   ├── pylint_tests_final.txt
│   ├── pylint_tests.txt
│   ├── unittest_final.txt
│   └── unittest.txt
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── storage.py
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_hotels.py
│   ├── test_reservations.py
│   └── test_storage.py
├── manual_run.py
├── requirements.txt
└── README.md
```

**Notas importantes:**

- `data/` contiene los JSON reales usados para el flujo manual.
- `results/` contiene evidencia (ejecuciones y análisis).
- `manual_run.py` ejecuta un flujo funcional real **sin unittest**, usando `data/`.

---

## 3) Ejecución de pruebas unitarias

Ejecutar toda la suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Guardar evidencia en `results/`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v | tee results/unittest.txt
```

> En la ejecución aparecen mensajes `[ERROR]` y `[WARN]` en consola.  
> Esto es esperado: hay pruebas **negativas** (no existe registro, JSON inválido, etc.) y los servicios imprimen esos mensajes por diseño.

---

## 4) Análisis estático

### 4.1 flake8

Revisar todo:

```bash
flake8 src tests
```

Guardar evidencia:

```bash
flake8 src tests | tee results/flake8.txt
```

### 4.2 pylint

Revisar código fuente:

```bash
pylint src
```

Guardar evidencia:

```bash
pylint src | tee results/pylint_src.txt
```

Revisar pruebas:

```bash
pylint tests
```

Guardar evidencia:

```bash
pylint tests | tee results/pylint_tests.txt
```

---

## 5) Cobertura (coverage)

Ejecutar coverage con unittest:

```bash
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
```

Guardar evidencia:

```bash
coverage report -m | tee results/coverage.txt
```

Generar reporte HTML:

```bash
coverage html
```

---

## 6) Flujo funcional manual (manual_run.py)

Este repo incluye un flujo manual para demostrar el comportamiento real del sistema con persistencia en JSON, sin depender de pruebas.

### 6.1 Ejecutar

```bash
python manual_run.py
```

### 6.2 Guardar evidencia del flujo manual

```bash
python manual_run.py | tee results/functional_run.txt
```

### 6.3 ¿Qué hace exactamente manual_run.py?

El script:

1. Crea/verifica carpetas `data/` y `results/`.
2. Usa persistencia real en:
   - `data/hotels.json`
   - `data/customers.json`
   - `data/reservations.json`
3. Genera IDs únicos con UUID para no “romper” datos existentes.
4. Ejecuta el flujo:
   - Crear Hotel
   - Crear Customer
   - Crear Reservation (reserva un cuarto)
   - Validar que `rooms_available` disminuyó
   - Cancelar Reservation (libera cuarto)
   - Validar que `rooms_available` se restauró
   - Validar que el `status` queda en `CANCELED` en el store

---

## 7) Principales errores encontrados y correcciones aplicadas

Durante el desarrollo se corrigieron fallas típicas de integración entre modelos/servicios/tests:

- **IndentationError en tests:** se reestructuraron archivos y se validó con `py_compile`.
- **Firma de modelos vs tests:** tests construían `Customer(..., email)` pero el modelo final usa los campos reales del dataclass. Se ajustaron tests al constructor correcto.
- **Bug en cancelación de reserva:** se pasaba `hotel_id` dos veces al `update()` (posicional y keyword) causando:

  ```text
  TypeError: got multiple values for argument 'hotel_id'
  ```

  Se eliminó el duplicado.

- **flake8 (W292/W293/E501):** se agregaron newlines finales y se ajustaron líneas largas.
- **pylint en tests:** se agregaron docstrings en módulos/clases/métodos donde fue necesario para subir el score sin “disables”.

---

## 8) Evidencia incluida


En la carpeta `results/` se incluyen los archivos generados durante la ejecución del proyecto y el análisis estático.

### Pruebas unitarias
- `unittest.txt`
- `unittest_final.txt`
<img width="1439" height="590" alt="image" src="https://github.com/user-attachments/assets/e114f322-2bea-47fa-a40f-d20fa02090f1" />

### Análisis estático — flake8
- `flake8.txt`
<img width="1150" height="360" alt="image" src="https://github.com/user-attachments/assets/81978100-843b-4744-be8f-58290435ce73" />

- `flake8_final.txt`
<img width="1618" height="318" alt="image" src="https://github.com/user-attachments/assets/6e192313-e0a2-4c82-a3d7-bed803cf1667" />
*NOTA: No se muestra ningun resultado ya que al no haber errores con flake8 no arroja ningún valor.

### Análisis estático — pylint
- `pylint_src.txt`
<img width="1431" height="679" alt="image" src="https://github.com/user-attachments/assets/a072994a-fcd4-42f7-9d31-921b24712043" />

- `pylint_src_final.txt`
<img width="1242" height="548" alt="image" src="https://github.com/user-attachments/assets/53ea8ef5-8661-4a76-b382-05198b7ee701" />

- `pylint_tests.txt`
<img width="1661" height="692" alt="image" src="https://github.com/user-attachments/assets/d1b5680c-8ceb-47dc-b55f-11de03230296" />

- `pylint_tests_final.txt`
<img width="1466" height="553" alt="image" src="https://github.com/user-attachments/assets/a172cfd7-0298-4d43-a929-4c6ea5b6f0db" />


### Cobertura
- `coverage.txt`
- `coverage_final.txt`
<img width="1833" height="843" alt="image" src="https://github.com/user-attachments/assets/3582835c-44de-4e18-878a-2d09f0200b43" />

### Flujo funcional manual
- `functional_run.txt`
<img width="1834" height="757" alt="image" src="https://github.com/user-attachments/assets/7a1c0e80-43e8-4d35-af32-6a0ecadf6b16" />

---

### ¿Qué documentan estos archivos?

- Ejecución de pruebas unitarias  
- Revisión de estilo del código (PEP8)  
- Revisión de calidad del código  
- Cobertura de pruebas  
- Ejecución funcional real del sistema
---

## 9) Cómo guardar evidencia del flujo manual 

## Generación de evidencia

Para regenerar toda la evidencia del proyecto:

```bash
mkdir -p results

# Pruebas unitarias
python -m unittest discover -s tests -p "test_*.py" -v | tee results/unittest.txt
python -m unittest discover -s tests -p "test_*.py" -v | tee results/unittest_final.txt

# Análisis estático — flake8
flake8 src tests | tee results/flake8.txt
flake8 src tests | tee results/flake8_final.txt

# Análisis estático — pylint
pylint src | tee results/pylint_src.txt
pylint src | tee results/pylint_src_final.txt

pylint tests | tee results/pylint_tests.txt
pylint tests | tee results/pylint_tests_final.txt

# Cobertura
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m | tee results/coverage.txt
coverage report -m | tee results/coverage_final.txt

# Flujo funcional manual
python manual_run.py | tee results/functional_run.txt
```
