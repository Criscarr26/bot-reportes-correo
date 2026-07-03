# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Planeado
- [ ] Soporte para más proveedores de email (ProtonMail, Thunderbird)
- [ ] Dashboard web para visualizar reportes
- [ ] Integración con Slack para notificaciones
- [ ] Filtrado avanzado por múltiples criterios
- [ ] Exportación a múltiples formatos (PDF, HTML, JSON)
- [ ] Caché de correos para mejorar rendimiento
- [ ] API REST para acceso programático

---

## [1.0.0] - 2024-06-03

### Lanzamiento Inicial (Initial Release)

#### Añadido (Added)
- **Integración con Outlook/Microsoft 365**
  - Autenticación con Exchange Server
  - Soporte para App Passwords
  - Lectura de correos desde cualquier carpeta
  - Filtrado por rango de fechas

- **Integración con Gmail**
  - Autenticación OAuth 2.0
  - Lectura de correos mediante Gmail API
  - Soporte para búsqueda avanzada (Gmail Query Language)
  - Token caching para acceso rápido

- **Generación de Reportes**
  - Exportación a formato Excel (.xlsx)
  - Exportación a formato CSV (.csv)
  - Reportes con estadísticas básicas
  - Agrupación por remitente/asunto/fecha
  - Resumen de actividad por período

- **Programación de Tareas**
  - Ejecución diaria automática
  - Ejecución semanal
  - Ejecución mensual
  - Programa personalizado mediante cron/Task Scheduler

- **Configuración**
  - Variables de entorno (.env)
  - Archivo de configuración YAML
  - Múltiples perfiles de ejecución
  - Logging configurable

- **Documentación**
  - [INSTALLATION.md](INSTALLATION.md) - Guía de instalación paso a paso
  - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas
  - [README.md](README.md) - Documentación general
  - [CONTRIBUTING.md](CONTRIBUTING.md) - Guía para contribuidores
  - [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Código de conducta
  - [SECURITY.md](SECURITY.md) - Política de seguridad

#### Característica Técnica
- Python 3.8+
- Uso de libraries:
  - `exchangelib` - Acceso a Outlook
  - `google-auth-oauthlib` - Autenticación Gmail
  - `openpyxl` - Generación de Excel
  - `python-dotenv` - Gestión de variables de entorno
  - `schedule` - Programación de tareas

#### Bug Fixes
- N/A (Lanzamiento inicial)

#### Seguridad
- Encriptación de credenciales locales
- Uso de App Passwords para Outlook (recomendado por Microsoft)
- OAuth 2.0 para Gmail (sin almacenar contraseña)
- Validación de archivos de configuración

---

## Guía para Futuras Versiones

### Cuando Contribuyas con Cambios

Actualiza el `CHANGELOG.md` siguiendo este formato:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Categoría

#### Subcategoría
- Descripción del cambio
```

### Categorías de Cambios

1. **Added** (Añadido) - Nuevas características
2. **Changed** (Cambiado) - Cambios en funcionalidad existente
3. **Deprecated** (Deprecado) - Funcionalidad que será removida
4. **Removed** (Removido) - Funcionalidad removida
5. **Fixed** (Corregido) - Corrección de bugs
6. **Security** (Seguridad) - Cambios de seguridad

### Formato de Versión

- **MAJOR** (X.0.0) - Cambios incompatibles con versiones anteriores
- **MINOR** (0.Y.0) - Nuevas características compatibles hacia atrás
- **PATCH** (0.0.Z) - Corrección de bugs y ajustes menores

### Ejemplos

#### Ejemplo 1: Nuevo Feature
```markdown
## [1.1.0] - 2024-07-15

### Added
- Soporte para exportación a PDF
- Dashboard web básico
- Notificaciones por email de reportes generados
```

#### Ejemplo 2: Bug Fix
```markdown
## [1.0.1] - 2024-06-10

### Fixed
- Corrección: Email con caracteres especiales causaba crash
- Corrección: Timeout en conexión a Outlook con Internet lenta
- Corrección: Reportes vacíos cuando el filtro no encontraba coincidencias
```

#### Ejemplo 3: Versión Mayor
```markdown
## [2.0.0] - 2024-12-01

### Added
- Dashboard interactivo con gráficos
- API REST completa
- Integración con Slack

### Changed
- Estructura de configuración completamente refactorizada
- Cambio de formato de logs

### Removed
- Soporte para Python 3.7 (ahora requiere 3.8+)
- Formato CSV deprecated (usar Excel o JSON)
```

---

## Notas de Desarrollo

### Cómo Generar el Changelog Automático

Si usas `git` y `conventional commits`:

```bash
# Instalar herramienta changelog
npm install -g auto-changelog

# Generar changelog desde commits
auto-changelog --package
```

### Archivos Relacionados

- [CONTRIBUTING.md](CONTRIBUTING.md) - Guidelines para contribuciones
- [SECURITY.md](SECURITY.md) - Política de vulnerabilidades
- [README.md](README.md) - Información del proyecto

---

## Historial de Versiones Archivado

Para versiones anteriores a la v1.0.0, consulta:
- [Releases en GitHub](https://github.com/tuusuario/email-report-bot/releases)
- [Commits en GitHub](https://github.com/tuusuario/email-report-bot/commits)

---

**Última actualización:** 2024-06-03
