# Guía de Contribución - Email Report Bot

¡Gracias por tu interés en contribuir al Email Report Bot! Este documento proporciona directrices para que el proceso de contribución sea claro y eficiente para todos.

---

## Código de Conducta

Este proyecto y todos los que participan en él están regulados por nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, se espera que mantengas este código. Por favor, reporta comportamiento inaceptable a [conduct@example.com](mailto:conduct@example.com).

---

## ¿Cómo Puedo Contribuir?

### 1. Reportar Bugs

Antes de crear un reporte de bug, por favor **revisa el Changelog y la sección de Issues** para evitar duplicados.

#### Cómo Reportar un Bug

1. **Abre un nuevo Issue** en [GitHub Issues](https://github.com/tuusuario/email-report-bot/issues)

2. **Usa este template:**
   ```
   ## Descripción del Bug
   Descripción clara y concisa de cuál es el problema.

   ## Pasos para Reproducir
   1. Ir a...
   2. Hacer clic en...
   3. Ver error...

   ## Comportamiento Esperado
   Qué debería haber ocurrido.

   ## Comportamiento Actual
   Qué sucedió en su lugar.

   ## Información del Sistema
   - OS: [Windows/macOS/Linux]
   - Python: [3.8/3.9/3.10/3.11]
   - Versión del Bot: [v1.0.0]
   - Proveedor de Email: [Outlook/Gmail]

   ## Logs Relevantes
   ```
   Pega los logs aquí
   ```

   ## Información Adicional
   Cualquier otra información que consideres relevante.
   ```

3. **Etiqueta el Issue** con `bug`

4. **Sé paciente** - Los mantenedores responderán cuando sea posible

### 2. Sugerir Features (Mejoras)

¿Tienes una idea para una nueva característica? ¡Nos encantaría escucharla!

#### Cómo Sugerir una Feature

1. **Abre un nuevo Issue** con el título: `[FEATURE] Tu sugerencia aquí`

2. **Proporciona contexto:**
   ```
   ## Descripción
   Descripción clara de la característica que te gustaría.

   ## Motivación
   ¿Qué problema resuelve? ¿Por qué es útil?

   ## Ejemplo de Uso
   Cómo te gustaría usar esta característica.

   ## Alternativas Consideradas
   ¿Hay otras formas de abordar esto?
   ```

3. **Etiqueta el Issue** con `enhancement` o `feature-request`

### 3. Enviar Pull Requests (PRs)

Los PRs son la mejor forma de proponer cambios en el código.

#### Antes de Comenzar

1. **Haz Fork** del repositorio
2. **Clona tu fork** localmente:
   ```bash
   git clone https://github.com/tu-usuario/email-report-bot.git
   cd email-report-bot
   ```
3. **Crea una rama** para tu feature/fix:
   ```bash
   git checkout -b feature/descripcion-concisa
   ```

#### Proceso de Desarrollo

1. **Configura el entorno local:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # o .\venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # dependencias de desarrollo
   ```

2. **Haz los cambios:**
   - Un commit por característica/fix
   - Código limpio y documentado
   - Pruebas para nuevas características

3. **Ejecuta las pruebas:**
   ```bash
   pytest
   pytest --cov=src  # ver cobertura
   ```

4. **Verifica el linting:**
   ```bash
   flake8 src/
   black --check src/
   pylint src/
   ```

5. **Formatea el código:**
   ```bash
   black src/
   isort src/
   ```

#### Enviar el PR

1. **Push a tu fork:**
   ```bash
   git push origin feature/descripcion-concisa
   ```

2. **Abre un Pull Request** en GitHub

3. **Completa el template de PR:**
   ```markdown
   ## Descripción
   Breve descripción de los cambios.

   ## Tipo de Cambio
   - [ ] Bug fix (no-breaking change que corrige un issue)
   - [ ] Feature nueva (no-breaking change que añade funcionalidad)
   - [ ] Breaking change (fix o feature que causaría cambios existentes)
   - [ ] Cambio de documentación

   ## ¿Cómo ha sido probado?
   Describe los tests que ejecutaste:
   - [ ] Test local completado
   - [ ] Nueva prueba añadida
   - [ ] Pruebas existentes pasan

   ## Checklist
   - [ ] Mi código sigue el estilo de este proyecto
   - [ ] He ejecutado `black` y `isort` en mi código
   - [ ] He actualizado la documentación
   - [ ] He añadido pruebas unitarias
   - [ ] Las pruebas nuevas y existentes pasan
   - [ ] He actualizado CHANGELOG.md

   ## Issues Relacionados
   Cierra #XXX (el número del issue que resuelve)
   ```

---

## Guía de Estilo de Código

### PEP 8 y Recomendaciones Python

Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/) estrictamente.

#### Formatting Automático

Usamos herramientas para mantener el código consistente:

```bash
# Black - formateador de código
black src/ tests/

# isort - organizador de imports
isort src/ tests/

# Verificar linting
flake8 src/ tests/
pylint src/
```

#### Convenciones de Código

```python
# ✓ Bueno - nombres descriptivos
def get_emails_by_date_range(start_date, end_date):
    """Obtiene correos dentro del rango de fechas especificado."""
    pass

# ✗ Malo - nombres poco claros
def get_mails(s, e):
    pass
```

```python
# ✓ Bueno - comentarios útiles
def calculate_report_statistics(emails):
    """
    Calcula estadísticas del reporte.
    
    Args:
        emails: Lista de objetos Email
        
    Returns:
        dict: Estadísticas con conteos y promedios
    """
    pass

# ✗ Malo - comentarios obvios
def calculate_report_statistics(emails):
    # calcula estadísticas
    pass
```

```python
# ✓ Bueno - usar type hints
def filter_emails(emails: list[Email], keyword: str) -> list[Email]:
    """Filtra correos por palabra clave."""
    return [e for e in emails if keyword in e.subject]

# ✗ Malo - sin type hints
def filter_emails(emails, keyword):
    pass
```

#### Estructura de Archivos

```
email-report-bot/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración global
│   ├── email_service.py       # Servicio base de email
│   ├── outlook_service.py     # Implementación Outlook
│   ├── gmail_service.py       # Implementación Gmail
│   ├── report_generator.py    # Generación de reportes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── email.py           # Modelo Email
│   │   └── report.py          # Modelo Report
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging
│       └── validators.py      # Validaciones
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_email_service.py
│   └── test_report_generator.py
└── main.py
```

---

## Setup Local para Desarrollo

### Instalación de Herramientas de Desarrollo

```bash
# Crea el virtual environment
python -m venv venv

# Activa el venv
source venv/bin/activate  # macOS/Linux
# o .\venv\Scripts\Activate.ps1  # Windows

# Instala dependencias regulares
pip install -r requirements.txt

# Instala dependencias de desarrollo
pip install -r requirements-dev.txt

# Incluyen:
# - pytest (testing)
# - pytest-cov (code coverage)
# - black (formatting)
# - isort (import sorting)
# - flake8 (linting)
# - pylint (linting avanzado)
# - sphinx (documentación)
```

### Verificación Inicial

```bash
# Verifica que todo está instalado
python -c "
import pytest
import black
import isort
import flake8
print('✓ Todas las herramientas instaladas')
"
```

---

## Cómo Correr Tests

### Ejecutar Todas las Pruebas

```bash
# Ejecución simple
pytest

# Con output verboso
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html

# Generar reporte HTML
open htmlcov/index.html
```

### Ejecutar Pruebas Específicas

```bash
# Archivo específico
pytest tests/test_config.py

# Función específica
pytest tests/test_config.py::test_load_env_file

# Con patrón
pytest -k "test_email" -v
```

### Test Driven Development (TDD)

Para nuevas características:

1. **Escribe la prueba primero:**
   ```bash
   pytest -k "test_new_feature" -v  # Falla
   ```

2. **Implementa la funcionalidad:**
   ```python
   def new_feature():
       """Tu implementación aquí."""
       pass
   ```

3. **Ejecuta la prueba nuevamente:**
   ```bash
   pytest -k "test_new_feature" -v  # Pasa
   ```

### Cobertura de Código

Apunta a cobertura >80%:

```bash
# Ver cobertura
pytest --cov=src --cov-report=term-missing

# Generar reporte
pytest --cov=src --cov-report=html
# Abre htmlcov/index.html
```

---

## Commit Message Guidelines

Seguimos el estándar [Conventional Commits](https://www.conventionalcommits.org/):

### Formato

```
<tipo>(<scope>): <resumen>

<descripción (opcional)>

<footer (opcional)>
```

### Tipos de Commits

- `feat` - Nuevas características
- `fix` - Corrección de bugs
- `docs` - Cambios en documentación
- `style` - Cambios de formato (no afecta lógica)
- `refactor` - Refactorización de código
- `test` - Añadir o actualizar tests
- `chore` - Cambios en build/dependencias

### Ejemplos de Commits

```bash
# Feature
git commit -m "feat(outlook): add support for shared mailboxes"

# Bug fix
git commit -m "fix(gmail): handle special characters in subject line

Fixes #123"

# Documentation
git commit -m "docs(installation): update Outlook setup instructions"

# Refactor
git commit -m "refactor(report): simplify statistics calculation"

# Test
git commit -m "test(email_service): add unit tests for filtering"
```

---

## Documentación

### Comentarios de Código

```python
def get_emails(self, start_date: datetime, end_date: datetime) -> list[Email]:
    """
    Obtiene correos dentro del rango de fechas especificado.
    
    Este método realiza una búsqueda IMAP en el servidor
    y retorna los correos ordenados por fecha descendente.
    
    Args:
        start_date: Fecha de inicio (inclusive)
        end_date: Fecha de fin (inclusive)
        
    Returns:
        List[Email]: Lista de correos encontrados, ordenados por fecha
        
    Raises:
        ConnectionError: Si no hay conexión al servidor
        ValueError: Si start_date > end_date
        
    Examples:
        >>> service = GmailService(config)
        >>> emails = service.get_emails(
        ...     datetime(2024, 1, 1),
        ...     datetime(2024, 12, 31)
        ... )
        >>> len(emails)
        42
    """
    pass
```

### Docstrings

Usa [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

```python
class EmailService:
    """
    Servicio base para lectura de correos.
    
    Proporciona interfaz común para diferentes proveedores
    de email (Outlook, Gmail, etc).
    """
    
    def authenticate(self) -> bool:
        """Autentica el servicio con las credenciales configuradas."""
        pass
```

### Actualizar Documentación

Si tu cambio afecta la funcionalidad pública:

1. Actualiza [README.md](README.md) si es necesario
2. Actualiza [CHANGELOG.md](CHANGELOG.md)
3. Actualiza docstrings del código
4. Actualiza [TROUBLESHOOTING.md](TROUBLESHOOTING.md) si aplica

---

## Revisión de PRs

### Lo que Revisamos

- ✓ Código limpio y bien estructurado
- ✓ Tests unitarios para nuevas funcionalidades
- ✓ Documentación actualizada
- ✓ Sin breaking changes sin justificación
- ✓ Cumple con PEP 8 y el estilo del proyecto
- ✓ CHANGELOG.md actualizado
- ✓ Commits con mensajes claros

### Tiempo de Revisión

- PRs pequeños (<100 líneas): 1-3 días
- PRs medianos (100-500 líneas): 3-7 días
- PRs grandes (>500 líneas): 7-14 días

### Después de Feedback

Si se solicitan cambios:

1. Haz los cambios solicitados
2. Haz commit: `git commit -m "refactor: address review feedback"`
3. Push nuevamente
4. NO hace falta abrir un nuevo PR

---

## Preguntas Frecuentes

### ¿Puedo trabajar en el código antes de comentar?

Sí, pero es mejor abrir un Issue primero para evitar trabajo duplicado.

### ¿Cómo me contacto con los mantenedores?

1. GitHub Issues - para bugs/features públicos
2. Email: developers@example.com - para asuntos privados
3. Discord: https://discord.gg/example - para chat casual

### ¿Qué pasa si mi PR no es aceptado?

Aprenderás sobre los requisitos del proyecto. Es normal.
Puedes:
- Preguntar feedback detallado
- Mejorar según comentarios
- Re-enviar

### ¿Puedo traducir la documentación?

¡Por supuesto! Crea un PR con:
- Documentación traducida en carpeta `docs/{idioma}`
- Ej: `docs/es/README.md`, `docs/fr/README.md`

---

## Recursos Útiles

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## Reconocimiento

Todos los contribuidores serán reconocidos en:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) (será creado)
- Página de GitHub del proyecto
- Lanzamientos/releases

---

## Conclusión

¡Gracias por contribuir! Tus aportes hacen que este proyecto sea mejor para todos.

¿Alguna pregunta? Abre un Issue o contacta a los mantenedores.

**Happy coding! 🚀**
