# Guía de Troubleshooting - Email Report Bot

Soluciones a los problemas más comunes que puedas encontrar al usar el Email Report Bot.

---

## "Failed to Authenticate with Outlook"

### Síntomas
- Error: `401 Unauthorized` o `Invalid Credentials`
- El bot no puede conectarse a Outlook/Microsoft 365
- Mensaje: `Authentication failed for...`

### Causas Comunes

#### 1. Contraseña Incorrecta
**Solución:**
- Verifica que estés usando una **App Password** (contraseña de aplicación), NO tu contraseña normal de Microsoft 365
- La App Password tiene 16 caracteres: `xxxx-xxxx-xxxx-xxxx`
- Cópiala nuevamente desde [Azure Portal](https://myaccount.microsoft.com/security-info)
- Actualiza `.env` con la nueva contraseña

#### 2. MFA No Activado
**Solución:**
- La autenticación por App Password requiere MFA (Multi-Factor Authentication) activado
- Ve a [Azure Security Info](https://myaccount.microsoft.com/security-info)
- Haz clic en "Add Sign-in method"
- Selecciona "Authenticator app" o "Phone"
- Completa la verificación
- Luego genera una nueva App Password

#### 3. Cuenta Antigua de Outlook.com
**Solución:**
- Si usas una cuenta antigua de outlook.com sin Microsoft 365:
  - Actualiza a una cuenta de Microsoft 365
  - O usa una cuenta de Gmail en su lugar
- En `.env`, cambia: `EMAIL_PROVIDER=gmail`

#### 4. Dirección de Email Incorrecta
**Solución:**
```env
# En .env, verifica que coincida con:
EMAIL_ADDRESS=tu_email_registrado@outlook.com
```

### Verificación Paso a Paso

```bash
# 1. Verifica que las variables estén configuradas
python -c "from src.config import Config; c = Config(); print(f'Email: {c.EMAIL_ADDRESS}')"

# 2. Prueba la conexión de red al servidor
python -c "
import socket
try:
    socket.create_connection(('outlook.office365.com', 993), timeout=5)
    print('✓ Conexión de red OK')
except:
    print('✗ No se puede conectar al servidor (firewall/red)')
"

# 3. Prueba la autenticación
python -c "
from src.email_service import OutlookService
from src.config import Config
try:
    service = OutlookService(Config())
    service.test_connection()
    print('✓ Autenticación OK')
except Exception as e:
    print(f'✗ Error: {e}')
"
```

---

## "Gmail Credentials File Not Found"

### Síntomas
- Error: `FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'`
- El bot no encuentra las credenciales de Google
- Cuando intentas ejecutar: `No credentials file`

### Soluciones

#### 1. Archivo en Ubicación Incorrecta
**Solución:**
```bash
# El archivo DEBE estar en la raíz del proyecto:
email-report-bot/
├── credentials.json    ← AQUÍ
├── main.py
├── .env
├── requirements.txt
└── src/
```

- Descargó el archivo desde Google Cloud Console
- Renómbralo a exactamente: `credentials.json`
- Muévelo a la carpeta raíz del proyecto (donde está `main.py`)

#### 2. Credenciales No Generadas
**Solución (crear credenciales):**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Asegúrate de tener el proyecto correcto seleccionado
3. Ve a "APIs y servicios" → "Biblioteca"
4. Busca "Gmail API" y haz clic en "Habilitar"
5. Ve a "Credenciales" → "Crear Credenciales"
6. Selecciona:
   - Tipo: `ID de cliente de OAuth`
   - Tipo de aplicación: `Aplicación de escritorio`
7. Haz clic en "Crear"
8. Descarga el archivo JSON
9. Renómbralo a `credentials.json` y ponlo en la raíz

#### 3. Permisos Insuficientes
**Solución:**
```bash
# Elimina el token antiguo para re-autenticar
rm token.pickle

# Ejecuta el bot nuevamente
python main.py

# Se abrirá navegador pidiendo permiso
# Asegúrate de hacer clic en "Permitir" o "Allow"
```

### Verificación

```bash
# Verifica que el archivo existe
test -f credentials.json && echo "✓ Archivo encontrado" || echo "✗ Archivo no encontrado"

# Verifica que es un JSON válido
python -c "
import json
with open('credentials.json') as f:
    data = json.load(f)
    print('✓ JSON válido')
    print(f'  Client ID: {data.get(\"installed\", {}).get(\"client_id\", \"?\")[:20]}...')
"
```

---

## "No Emails Found"

### Síntomas
- El bot ejecuta sin errores pero no encuentra correos
- Mensaje: `No emails found` o reportes vacíos
- `len(emails) == 0`

### Causas y Soluciones

#### 1. Rango de Fechas Incorrecto
**Solución:**
```env
# En .env, verifica:
EMAIL_START_DATE=2024-01-01
EMAIL_END_DATE=2024-12-31
```

```bash
# Prueba con un rango más amplio
python -c "
from src.email_service import EmailService
from src.config import Config
from datetime import datetime, timedelta

config = Config()
service = EmailService.factory(config)

# Últimos 30 días
end = datetime.now()
start = end - timedelta(days=30)

emails = service.get_emails(start, end)
print(f'Encontrados: {len(emails)} correos')
"
```

#### 2. Filtros de Búsqueda Demasiado Restrictivos
**Solución:**
```env
# En .env, simplifica los filtros:

# NO recomendado:
EMAIL_FILTER=from:ejemplo@empresa.com AND subject:(importante OR urgente) AND has:attachment

# Recomendado para testing:
EMAIL_FILTER=
```

#### 3. Carpeta Incorrecta
**Solución:**
```bash
# Verifica qué carpetas tienes
python -c "
from src.email_service import EmailService
from src.config import Config

config = Config()
service = EmailService.factory(config)
folders = service.get_folders()
for folder in folders:
    print(f'- {folder}')
"

# En .env, asegúrate que FOLDER esté en la lista:
# FOLDER=INBOX  # o Bandeja de entrada, Spam, etc.
```

#### 4. Permiso de Lectura Denegado
**Solución (Gmail):**
```bash
# Elimina el token y re-autentica
rm token.pickle
python main.py

# Verifica que autorizaste el acceso a Gmail
```

### Debugging

```bash
# Modo verbose para ver detalles
DEBUG_MODE=True python -c "
from src.email_service import EmailService
from src.config import Config
import logging

logging.basicConfig(level=logging.DEBUG)

config = Config()
service = EmailService.factory(config)
emails = service.get_recent_emails(limit=10)

print(f'Encontrados: {len(emails)}')
for email in emails:
    print(f'  {email.date} - {email.sender}: {email.subject}')
"
```

---

## "Module Not Found Errors"

### Síntomas
- `ModuleNotFoundError: No module named '...'`
- Errores como: `No module named 'exchangelib'`, `No module named 'google'`
- Ocurren al ejecutar el bot

### Soluciones

#### 1. Dependencias No Instaladas
**Solución:**
```bash
# Asegúrate de que el venv está activado
# En Windows:
.\venv\Scripts\Activate.ps1
# En macOS/Linux:
source venv/bin/activate

# Reinstala todas las dependencias
pip install -r requirements.txt --upgrade --force-reinstall
```

#### 2. Virtual Environment No Activado
**Solución:**
```bash
# Verifica que ves (venv) al inicio de tu línea de comandos

# En Windows PowerShell:
.\venv\Scripts\Activate.ps1

# En cmd.exe:
venv\Scripts\activate.bat

# En macOS/Linux Bash:
source venv/bin/activate

# En macOS/Linux Zsh:
source venv/bin/activate
```

#### 3. pip Instalando en Lugar Equivocado
**Solución:**
```bash
# Verifica que pip está usando el venv correcto
which pip  # macOS/Linux
where pip  # Windows (PowerShell)

# Debería mostrar ruta con 'venv'

# Si no, desinstala globalmente e instala en venv:
pip uninstall -y paquete
./venv/Scripts/pip install paquete
```

#### 4. requirements.txt Desactualizado
**Solución:**
```bash
# Actualiza manualmente las dependencias principales:
pip install --upgrade pip setuptools wheel
pip install exchangelib google-auth-oauthlib google-auth-httplib2 openpyxl python-dotenv schedule
```

### Verificación

```bash
# Lista todos los módulos instalados
pip list

# Verifica módulos específicos
python -c "
import exchangelib; print('✓ exchangelib')
import google.auth; print('✓ google.auth')
import openpyxl; print('✓ openpyxl')
import dotenv; print('✓ dotenv')
"
```

---

## "Connection Timeout"

### Síntomas
- Mensaje: `Connection timed out` o `timeout: timed out`
- El bot se congela al intentar conectar
- Tardanza extrema (>60 segundos) sin respuesta
- Error: `[Errno 110] Connection timed out`

### Causas y Soluciones

#### 1. Firewall o Proxy Bloqueando
**Solución:**
```bash
# Verifica conectividad a los servidores
# Para Outlook:
python -c "
import socket
try:
    s = socket.create_connection(('outlook.office365.com', 993), timeout=10)
    print('✓ Outlook accesible')
    s.close()
except socket.timeout:
    print('✗ Timeout - Firewall/proxy bloqueando')
except Exception as e:
    print(f'✗ Error: {e}')
"

# Para Gmail:
python -c "
import socket
try:
    s = socket.create_connection(('imap.gmail.com', 993), timeout=10)
    print('✓ Gmail accesible')
    s.close()
except socket.timeout:
    print('✗ Timeout - Firewall/proxy bloqueando')
except Exception as e:
    print(f'✗ Error: {e}')
"
```

#### 2. Conexión de Internet Lenta
**Solución:**
- Verifica que tu conexión de Internet esté estable
- Reinicia tu router/conexión
- Prueba con otra red (hotspot móvil)

#### 3. Servidores de Email Experimentando Problemas
**Solución:**
- Verifica el estado de los servidores:
  - Outlook: [Microsoft 365 Service Health](https://status.office365.com/)
  - Gmail: [Google Cloud Status](https://www.google.com/appsstatus/dashboard/)
- Espera a que se resuelvan los problemas
- Reintenta en unos minutos

#### 4. Timeout Demasiado Bajo en Configuración
**Solución (en `.env` o código):**
```env
# Aumenta el timeout (en segundos)
CONNECTION_TIMEOUT=30
```

```python
# En src/email_service.py (si tienes acceso):
# Outlook:
CREDENTIAL.exchange_server.timeout = 30

# Gmail:
imap.timeout = 30
```

### Debug Avanzado

```bash
# Verifica la latencia
ping outlook.office365.com    # Windows
ping -c 4 outlook.office365.com  # macOS/Linux

# Prueba la conexión segura
python -c "
import ssl
import socket
hostname = 'outlook.office365.com'
port = 993
context = ssl.create_default_context()
with socket.create_connection((hostname, port), timeout=10) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(f'✓ Conexión SSL exitosa')
        print(f'  Certificado: {ssock.getpeercert()}')
"
```

---

## "SSL Certificate Error"

### Síntomas
- Error: `SSL: CERTIFICATE_VERIFY_FAILED`
- Mensaje: `ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`
- `CERTIFICATE_SELF_SIGNED`
- `unable to get local issuer certificate`

### Causas y Soluciones

#### 1. Certificados de Python No Actualizados (macOS)
**Solución:**
```bash
# En macOS, ejecuta:
/Applications/Python\ 3.x/Install\ Certificates.command

# O manualmente:
python -m pip install --upgrade certifi
```

#### 2. Firewall/Antivirus Interceptando SSL
**Solución:**
- Temporalmente desactiva el antivirus/firewall
- Reintenta la conexión
- Si funciona, configura una excepción para:
  - `outlook.office365.com`
  - `imap.gmail.com`
  - `smtp.gmail.com`

#### 3. Certificado Expirado o Inválido
**Solución:**
```bash
# Verifica la validez del certificado
python -c "
import ssl
import socket
hostname = 'outlook.office365.com'
try:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 993), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            print('✓ Certificado válido')
            print(f'  Subject: {cert}')
except ssl.SSLError as e:
    print(f'✗ Error SSL: {e}')
"
```

#### 4. Desactivar Verificación SSL (NO RECOMENDADO para producción)
**Solución de Emergencia:**
```python
# En src/email_service.py
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

**Nota:** Esto NO es seguro. Úsalo solo para debugging. Resuelve el problema subyacente.

---

## "Permission Denied"

### Síntomas
- Error: `PermissionError: [Errno 13] Permission denied`
- Mensaje: `Access is denied`
- No puede leer/escribir archivos o carpetas

### Causas y Soluciones

#### 1. Permisos de Archivo de Credenciales (Linux/macOS)
**Solución:**
```bash
# Verifica permisos
ls -l credentials.json
ls -l token.pickle

# Cambia permisos si es necesario
chmod 600 credentials.json
chmod 600 token.pickle
```

#### 2. Archivo .env No Legible
**Solución:**
```bash
# Verifica permisos
ls -l .env

# Cambia si es necesario
chmod 644 .env
```

#### 3. Directorio de Reportes Sin Permisos de Escritura
**Solución:**
```bash
# Crea la carpeta si no existe
mkdir -p reports

# Cambia permisos en Linux/macOS
chmod 755 reports

# En Windows (PowerShell), verifica que el usuario tenga permiso:
Get-Acl reports | Format-List
```

#### 4. Archivo Abierto en Otro Programa
**Solución:**
```bash
# En Windows, un reporte puede estar abierto en Excel
# Solución: Cierra el archivo Excel

# En bash/Linux, verifica qué proceso tiene el archivo:
lsof | grep nombre_del_archivo
```

---

## Cómo Leer y Debuggear Logs

### Configurar Logging Detallado

En `.env`:
```env
DEBUG_MODE=True
LOG_LEVEL=DEBUG
LOG_FILE=logs/email_report_bot.log
```

### Ejecutar en Modo Debug

```bash
# Activa logging detallado
python -u main.py 2>&1 | tee debug.log

# O con timestamp
python -u main.py 2>&1 | while IFS= read -r line; do echo "[$(date +'%H:%M:%S')] $line"; done
```

### Interpretar Errores Comunes en Logs

```
[ERROR] Authentication failed: 401 Unauthorized
  → Ver sección "Failed to Authenticate with Outlook"

[ERROR] No module named 'exchangelib'
  → Ver sección "Module Not Found Errors"

[ERROR] Connection timeout
  → Ver sección "Connection Timeout"

[ERROR] File not found: credentials.json
  → Ver sección "Gmail Credentials File Not Found"

[WARNING] Slow response from server
  → Problema de red o servidor sobrecargado
```

### Archivos de Log

```bash
# Ver los últimos 50 líneas del log
tail -50 logs/email_report_bot.log

# Ver logs en tiempo real
tail -f logs/email_report_bot.log

# Buscar errores
grep ERROR logs/email_report_bot.log

# Buscar por timestamp
grep "2024-01-15" logs/email_report_bot.log
```

---

## No se Resolvió tu Problema?

1. **Consulta la documentación:**
   - [INSTALLATION.md](INSTALLATION.md) - Pasos de instalación
   - [README.md](README.md) - Información general

2. **Abre un Issue en GitHub:**
   - Ve a [Reportar un Bug](https://github.com/tuusuario/email-report-bot/issues/new?labels=bug)
   - Incluye:
     ```
     - Versión de Python: (ejecuta: python --version)
     - Sistema Operativo: (Windows/macOS/Linux)
     - Proveedor de email: (Outlook/Gmail)
     - Error exacto:
     - Pasos para reproducir:
     - Logs relevantes:
     ```

3. **Contacta a Soporte:**
   - Email: support@example.com
   - Discord: https://discord.gg/example
   - Foro: https://forum.example.com

---

## Solución Rápida: Reset Completo

Si todo falla, prueba esto (perderás configuración local):

```bash
# Desactiva el venv
deactivate

# Elimina el venv
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows cmd

# Recomienza desde cero
python -m venv venv
# Activa venv según tu SO
pip install -r requirements.txt

# Vuelve a configurar
rm token.pickle credentials.json
# Sigue la guía de instalación nuevamente
```

¡Esperamos que estos troubleshooting te ayuden! 🚀
