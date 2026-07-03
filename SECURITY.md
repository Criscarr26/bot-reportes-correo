# Política de Seguridad - Email Report Bot

## Introducción

La seguridad es una prioridad en el Email Report Bot. Este documento describe cómo reportar vulnerabilidades de seguridad y las prácticas recomendadas para usar el bot de forma segura.

---

## Reportar Vulnerabilidades de Seguridad

### ⚠️ NO HAGAS ESTO

❌ **No** abras un GitHub Issue público para reportar vulnerabilidades
❌ **No** publiques detalles de seguridad en redes sociales
❌ **No** envíes detalles de seguridad en correos normales
❌ **No** compartas credenciales en los reportes

### ✓ HAZ ESTO EN SU LUGAR

#### Opción 1: GitHub Security Advisory (Recomendado)

1. Ve a [GitHub Security Advisories](https://github.com/tuusuario/email-report-bot/security/advisories)
2. Haz clic en "Report a vulnerability"
3. Completa el formulario:
   - **Título:** Descripción breve de la vulnerabilidad
   - **Descripción:** Detalles técnicos
   - **Severidad:** Crítica/Alta/Media/Baja
   - **Affected versions:** Qué versiones están afectadas
   - **Fixed version (if known):** Si sabes cómo arreglarlo

#### Opción 2: Email Privado

Envía un correo a: **security@example.com**

Incluye:
```
Asunto: [SECURITY] Vulnerabilidad en Email Report Bot

Cuerpo:
- Descripción de la vulnerabilidad
- Pasos para reproducir
- Impacto potencial
- Sugiere parches (si tienes)
- Información de contacto para seguimiento
```

#### Opción 3: Contacto de Emergencia

Para vulnerabilidades críticas que requieren respuesta inmediata:

**Email:** emergency-security@example.com
**Teléfono:** +1-XXX-XXX-XXXX (contacta primero por email)

---

## Timeline de Respuesta

Nos comprometemos a:

| Severidad | Confirmación | Patch | Lanzamiento |
|-----------|-------------|-------|-------------|
| Crítica 🔴 | 24 horas | 48 horas | 72 horas |
| Alta 🟠 | 48 horas | 7 días | 14 días |
| Media 🟡 | 5 días | 14 días | 30 días |
| Baja 🟢 | 10 días | 30 días | Próxima versión |

### Proceso

1. **Recibimiento:** Confirmamos que recibimos tu reporte
2. **Investigación:** Verificamos la vulnerabilidad
3. **Desarrollo:** Trabajamos en un parche
4. **Testing:** Probamos exhaustivamente
5. **Lanzamiento:** Publicamos la corrección
6. **Disclosure:** Creditamos al reportador (si lo deseas)

---

## Vulnerabilidades Cubiertas

Consideramos vulnerabilidades de seguridad:

✓ Inyección de código (SQL, Command, etc.)
✓ Autenticación/autorización débil
✓ Exposición de credenciales
✓ Cross-Site Scripting (XSS) - si aplica
✓ Cross-Site Request Forgery (CSRF) - si aplica
✓ Insecure deserialization
✓ Broken cryptography
✓ Information disclosure
✓ Privilege escalation
✓ Remote Code Execution (RCE)

NO Consideramos:

- Errores de tipografía
- Características incompletas
- Problemas de UI/UX
- Issues de rendimiento menores

---

## Buenas Prácticas para Usar el Bot

### 1. Credenciales y Contraseñas

#### ✓ Haz

```bash
# Usar variables de entorno
export EMAIL_PASSWORD="app-password-de-16-caracteres"

# Usar .env con permisos restringidos
chmod 600 .env

# Usar App Passwords para Outlook
# Usar OAuth para Gmail
```

#### ✗ No Hagas

```bash
# Nunca hardcodees contraseñas
EMAIL_PASSWORD = "micontraseña"

# Nunca los guardes en git
git add .env  # ❌

# Nunca las compartas en código
os.getenv("EMAIL_PASSWORD", "fallback_password")  # ❌

# No uses tu contraseña normal
# Usa siempre App Passwords (Outlook) u OAuth (Gmail)
```

### 2. Almacenamiento de Credenciales

```bash
# Configuración segura de .env

# 1. Crea el archivo
touch .env

# 2. Restrige permisos (Linux/macOS)
chmod 600 .env

# 3. Añade a .gitignore
echo ".env" >> .gitignore
echo "credentials.json" >> .gitignore
echo "token.pickle" >> .gitignore

# 4. Verifica que NO está en git
git status  # .env no debe aparecer
```

### 3. Archivos de Credenciales

```python
# ✓ Bueno - verificar permisos
import os
import stat

credentials_file = "credentials.json"
stat_info = os.stat(credentials_file)
mode = stat_info.st_mode & 0o777

if mode != 0o600:  # Permisos muy abiertos
    print("⚠️ ADVERTENCIA: Permisos inseguros en credentials.json")
    os.chmod(credentials_file, 0o600)

# ✗ Malo - no verificar permisos
with open("credentials.json") as f:
    creds = json.load(f)
```

### 4. Logging Seguro

```python
# ✓ Bueno - no loguear credenciales
def authenticate(email, password):
    logger.info(f"Autenticando usuario: {email}")  # OK
    result = login_service.auth(email, password)
    logger.info("Autenticación exitosa")  # OK

# ✗ Malo - loguear información sensible
logger.debug(f"Contraseña: {password}")  # ❌
logger.info(f"Token: {auth_token}")      # ❌
logger.error(f"Fallo: {full_error}")     # Podría contener secretos
```

### 5. Manejo de Datos Sensibles

```python
# ✓ Bueno - encriptar datos sensibles
from cryptography.fernet import Fernet

cipher = Fernet(encryption_key)
encrypted_token = cipher.encrypt(token.encode())

# ✓ Bueno - usar conexiones SSL/TLS
IMAP_CONNECTION = imaplib.IMAP4_SSL(
    host="imap.gmail.com",
    port=993,
    ssl_context=ssl.create_default_context()
)

# ✗ Malo - almacenar tokens en plaintext
token_file = open("token.txt", "w")
token_file.write(auth_token)  # ❌
```

### 6. Actualizaciones de Seguridad

```bash
# Mantén las dependencias actualizadas
pip list --outdated
pip install --upgrade -r requirements.txt

# Verifica vulnerabilidades conocidas
pip install safety
safety check
```

---

## Datos Sensibles que el Bot Maneja

⚠️ **El bot puede procesar:**

- **Direcciones de email** - De usuarios y contactos
- **Contenido de correos** - Asuntos, cuerpo, adjuntos
- **Información personal** - Nombres, empresas, ubicaciones
- **Información financiera** - Si está en los correos
- **Credenciales de acceso** - Contraseñas de app, tokens OAuth
- **Metadatos** - Fechas, tamaños, carpetas

### Responsabilidades del Usuario

- ✓ Cumple con leyes de privacidad (GDPR, CCPA, etc.)
- ✓ Obtén consentimiento de las personas cuyos datos procesas
- ✓ Almacena los reportes de forma segura
- ✓ No compartas reportes que contengan información personal
- ✓ Elimina datos cuando ya no sea necesarios

---

## Dependencias de Seguridad

El bot usa estas librerías críticas para seguridad:

```
exchangelib==4.x        - Comunicación segura con Outlook
google-auth==2.x        - Autenticación OAuth de Google
cryptography==41.x      - Operaciones criptográficas
python-dotenv==1.x      - Gestión de variables de entorno
```

### Mantener Dependencias Seguras

```bash
# Verifica vulnerabilidades
pip install safety
safety check --json > safety_report.json

# Audita dependencias
pip audit

# Usa versionamiento explícito
pip freeze > requirements.txt
```

---

## Seguridad del Repositorio

### Para Mantenedores

- ✓ Habilita Two-Factor Authentication (2FA)
- ✓ Usa branch protection rules
- ✓ Requiere code reviews antes de merge
- ✓ Ejecuta tests automáticos (CI/CD)
- ✓ Escanea código con SAST tools
- ✓ Verifica dependencias regularmente

### Para Contribuidores

- ✓ Usa SSH keys en lugar de HTTPS
- ✓ Firma tus commits con GPG (opcional pero recomendado)
- ✓ No commitees secretos (usa pre-commit hooks)
- ✓ Verifica que no hay keys en tu PR

```bash
# Pre-commit hook para evitar secretos
pip install detect-secrets
detect-secrets scan > .secrets.baseline

# Antes de push
detect-secrets scan --baseline .secrets.baseline
```

---

## Reporting de Otros Problemas de Seguridad

### Seguridad del Proyecto

Si encuentras problemas en:
- Documentación de seguridad
- Configuración insegura por defecto
- Mejoras de seguridad
- Prácticas no documentadas

Puedes:
1. Abrir un GitHub Issue con etiqueta `security`
2. Iniciar una Discusión en GitHub
3. Contactar a los mantenedores

---

## Reconnaissance & Penetration Testing

Si realizas testing de seguridad (pen testing):

1. **Contacta primero:** Envía email a security@example.com
2. **Obtén permiso explícito** antes de cualquier testing
3. **Define el alcance:** Qué sistemas puedes testear
4. **Timeline:** Cuándo quieres hacerlo
5. **Confidencialidad:** Resultados bajo NDA

---

## FAQs de Seguridad

### P: ¿El bot almacena mis correos?
**R:** No. El bot los lee para generar reportes, pero no los almacena (a menos que configures un cache local).

### P: ¿Puedo confiar en mis credenciales?
**R:** Tus credenciales se almacenan localmente en tu archivo `.env`. No se envían a servidores nuestros. Usa App Passwords (Outlook) u OAuth (Gmail) para máxima seguridad.

### P: ¿Qué pasa si alguien obtiene acceso a mi máquina?
**R:** Pueden leer tus archivos `.env` y `credentials.json`. Protege tu máquina con password fuerte y encriptación de disco.

### P: ¿Está el bot auditado por terceros?
**R:** Actualmente no. Estamos abiertos a auditorías de seguridad.

### P: ¿Qué debo hacer si encuentro un agujero de seguridad?
**R:** Reporta según las instrucciones en "Reportar Vulnerabilidades de Seguridad".

---

## Contactos de Seguridad

| Rol | Email | Respuesta |
|-----|-------|----------|
| **Coordinador de Seguridad** | security@example.com | 24-48h |
| **Contacto de Emergencia** | emergency-security@example.com | 4h |
| **Privacidad/GDPR** | privacy@example.com | 48h |

---

## Changelog de Seguridad

| Fecha | Issue | Severidad | Descripción | Estado |
|-------|-------|-----------|-------------|--------|
| 2024-06-03 | N/A | N/A | Lanzamiento inicial | ✓ Seguro |

---

## Licencia

Esta política está bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Agradecimientos

Gracias a todos los reportadores de seguridad que han ayudado a mantener este proyecto seguro.

**Última actualización:** 2024-06-03

---

Para más información, consulta:
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Código de conducta
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [README.md](README.md) - Documentación general
