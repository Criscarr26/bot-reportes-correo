# Guía de Instalación - Email Report Bot

Una guía paso a paso para instalar y configurar el Email Report Bot en tu sistema.

## Requisitos del Sistema

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

### Software Requerido
- **Python 3.8+** - [Descargar desde python.org](https://www.python.org/downloads/)
- **pip** - Gestor de paquetes de Python (incluido con Python 3.4+)
- **Git** - Control de versiones (opcional, pero recomendado) - [Descargar desde git-scm.com](https://git-scm.com/)
- **Visual C++ Build Tools** (Windows) - Requerido para compilar algunas dependencias

### Requisitos de Red
- Conexión a Internet estable
- Acceso a los servidores de Outlook/Microsoft 365 o Gmail
- Puerto 587 (SMTP) y 993 (IMAP) abiertos si tienes firewall

### Requisitos de Cuenta
- Una cuenta de correo electrónico de **Outlook/Microsoft 365** o **Gmail**
- Acceso para crear aplicaciones en:
  - [Azure Portal](https://portal.azure.com/) (para Outlook)
  - [Google Cloud Console](https://console.cloud.google.com/) (para Gmail)

---

## Paso 1: Clonar el Repositorio

```bash
# Abre tu terminal/PowerShell
cd tu_carpeta_de_proyectos

# Clona el repositorio
git clone https://github.com/tuusuario/email-report-bot.git
cd email-report-bot
```

Si no usas Git, descarga el repositorio como ZIP desde GitHub y extrae el contenido.

---

## Paso 2: Crear Virtual Environment

Un virtual environment aísla las dependencias de tu proyecto del resto del sistema.

### En Windows (PowerShell)
```powershell
# Crear el virtual environment
python -m venv venv

# Activar el virtual environment
.\venv\Scripts\Activate.ps1
```

Si obtienes un error de ejecución, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### En macOS/Linux (Bash)
```bash
# Crear el virtual environment
python3 -m venv venv

# Activar el virtual environment
source venv/bin/activate
```

**Deberías ver `(venv)` al inicio de tu línea de comandos**, indicando que el virtual environment está activo.

---

## Paso 3: Instalar Dependencias con pip

Con el virtual environment activo, instala todas las dependencias del proyecto:

```bash
# Actualizar pip (recomendado)
pip install --upgrade pip

# Instalar las dependencias desde requirements.txt
pip install -r requirements.txt
```

**Dependencias principales:**
- `python-dotenv` - Gestión de variables de entorno
- `exchangelib` - Integración con Outlook/Exchange
- `google-auth-oauthlib` - Autenticación OAuth para Gmail
- `openpyxl` - Generación de reportes Excel
- `schedule` - Programación de tareas

---

## Paso 4: Configurar Variables de Entorno

### Copiar archivo .env.example a .env

```bash
# Windows (PowerShell)
Copy-Item .env.example -Destination .env

# macOS/Linux
cp .env.example .env
```

Luego, abre el archivo `.env` en tu editor de texto favorito y configura los valores:

```env
# Configuración de Email
EMAIL_PROVIDER=outlook  # o 'gmail'
EMAIL_ADDRESS=tu_email@outlook.com
EMAIL_PASSWORD=tu_contraseña_o_app_password

# Configuración de Outlook (si la usas)
OUTLOOK_EXCHANGE_SERVER=outlook.office365.com
OUTLOOK_USE_SSL=True

# Configuración de Gmail (si la usas)
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.pickle

# Configuración de Reportes
REPORT_OUTPUT_DIR=reports
REPORT_FORMAT=xlsx  # o 'csv'
REPORT_FREQUENCY=daily  # 'daily', 'weekly', 'monthly'

# Opciones Avanzadas
DEBUG_MODE=False
LOG_LEVEL=INFO
MAX_EMAILS_PER_REPORT=1000
```

---

## Paso 5: Configurar Outlook (Microsoft 365)

### 5a. Generar App Password en Azure Portal

1. **Ve a [Azure Portal](https://portal.azure.com/)**
2. **Inicia sesión** con tu cuenta de Microsoft 365

3. **Navega a Azure Active Directory:**
   - Haz clic en "Menú" (≡) en la esquina superior izquierda
   - Selecciona "Azure Active Directory"

4. **Configura autenticación multifactor (MFA):**
   - En el panel izquierdo, ve a "Usuarios"
   - Selecciona tu usuario
   - Haz clic en "Multi-factor Authentication"
   - Haz clic en "Activar" si no está activo

5. **Genera una contraseña de aplicación:**
   - Ve a [https://myaccount.microsoft.com/security-info](https://myaccount.microsoft.com/security-info)
   - Haz clic en "App password"
   - Selecciona "Outlook" y "Windows (o tu dispositivo)"
   - Se generará una contraseña de 16 caracteres
   - **Cópiala inmediatamente** en tu archivo `.env` como `EMAIL_PASSWORD`

### 5b. Configurar el servidor Exchange

En `.env`, asegúrate de que tienes:
```env
EMAIL_PROVIDER=outlook
OUTLOOK_EXCHANGE_SERVER=outlook.office365.com
OUTLOOK_USE_SSL=True
EMAIL_ADDRESS=tu_email@outlook.com
EMAIL_PASSWORD=tu_app_password_de_16_caracteres
```

### 5c. Probar la conexión

```bash
python -c "from src.email_service import OutlookService; OutlookService().test_connection()"
```

---

## Paso 6: Configurar Gmail (Google)

### 6a. Crear un Proyecto en Google Cloud

1. **Ve a [Google Cloud Console](https://console.cloud.google.com/)**
2. **Crea un nuevo proyecto:**
   - Haz clic en el selector de proyectos en la parte superior
   - Haz clic en "Nuevo Proyecto"
   - Nombre: "Email Report Bot"
   - Haz clic en "Crear"

3. **Habilita la Gmail API:**
   - En el panel izquierdo, ve a "APIs y servicios"
   - Haz clic en "Habilitar API"
   - Busca "Gmail API"
   - Haz clic en el resultado y luego en "Habilitar"

4. **Crea credenciales OAuth 2.0:**
   - Ve a "Credenciales" en el panel izquierdo
   - Haz clic en "Crear credenciales" → "ID de cliente de OAuth"
   - Si se solicita, haz clic en "Configurar pantalla de consentimiento de OAuth"
   - Selecciona "Aplicación de escritorio" y rellena los detalles requeridos
   - En "Crear credenciales", selecciona "ID de cliente de OAuth"
   - Elige "Aplicación de escritorio"
   - Haz clic en "Crear"

5. **Descarga el archivo de credenciales:**
   - Haz clic en el icono de descarga al lado del ID de cliente que acabas de crear
   - Renombra el archivo a `credentials.json`
   - Colócalo en la raíz de tu proyecto

### 6b. Configurar variables de entorno

En `.env`:
```env
EMAIL_PROVIDER=gmail
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.pickle
EMAIL_ADDRESS=tu_email@gmail.com
```

### 6c. Primer inicio de sesión

La primera vez que ejecutes el bot:

```bash
python main.py
```

Se abrirá una ventana del navegador pidiendo permiso. Haz clic en "Permitir" para que el bot acceda a tu Gmail.

El token se guardará automáticamente en `token.pickle` para futuros accesos.

---

## Paso 7: Validar la Instalación

### Test de Configuración Básica

```bash
# Ejecutar el script de validación
python -m src.installer.validate_setup

# O manualmente
python -c "
from src.config import Config
from src.email_service import EmailService

config = Config()
print(f'✓ Configuración cargada: {config.EMAIL_PROVIDER}')

service = EmailService.factory(config)
print(f'✓ Servicio de email inicializado')

service.test_connection()
print('✓ Conexión exitosa al servidor de correo')
"
```

### Test de Lectura de Correos

```bash
python -c "
from src.email_service import EmailService
from src.config import Config

config = Config()
service = EmailService.factory(config)
emails = service.get_recent_emails(limit=5)
print(f'✓ Se leyeron {len(emails)} correos recientemente')
for email in emails[:3]:
    print(f'  - {email.sender}: {email.subject}')
"
```

### Test de Generación de Reportes

```bash
python -c "
from src.report_generator import ReportGenerator
from src.config import Config

config = Config()
generator = ReportGenerator(config)
report_path = generator.generate_report()
print(f'✓ Reporte generado exitosamente en: {report_path}')
"
```

---

## Paso 8: Configuración Adicional (Opcional)

### Ejecutar Bot como Servicio (Windows)

Para que el bot se ejecute automáticamente al iniciar:

1. **Instala el gestor de tareas:**
```bash
pip install python-windows-taskscheduler
```

2. **Programa el bot:**
```bash
python -m src.installer.install_service
```

### Ejecutar Bot como Daemon (Linux/macOS)

1. **Crea un servicio systemd:**
```bash
sudo nano /etc/systemd/system/email-report-bot.service
```

2. **Copia el siguiente contenido:**
```ini
[Unit]
Description=Email Report Bot
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/al/bot
ExecStart=/ruta/al/bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Habilita el servicio:**
```bash
sudo systemctl enable email-report-bot
sudo systemctl start email-report-bot
```

### Configurar Logs

En `.env`, configura el nivel de logging:
```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/email_report_bot.log
```

---

## Troubleshooting de Instalación

### Error: "python: command not found"

**Solución:** Python no está en tu PATH. 
- Reinstala Python y asegúrate de marcar "Add Python to PATH" durante la instalación
- O usa el instalador de Microsoft Store: `winget install Python.Python.3.11`

### Error: "No module named 'requirements'"

**Solución:** Las dependencias no están instaladas
```bash
pip install -r requirements.txt --upgrade
```

### Error: "Permission Denied" (venv activation)

**Solución (Windows PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Error al conectar a Outlook

- Verifica tu app password (no tu contraseña normal)
- Asegúrate de que MFA esté activado en tu cuenta
- Prueba con la contraseña de 16 caracteres sin espacios

### Error al conectar a Gmail

- Verifica que `credentials.json` esté en la raíz del proyecto
- Elimina `token.pickle` y vuelve a ejecutar el bot para re-autenticar
- Asegúrate de que la Gmail API está habilitada en Google Cloud Console

---

## ¿Necesitas Ayuda?

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Soluciones a problemas comunes
- **[Abrir un Issue en GitHub](https://github.com/tuusuario/email-report-bot/issues)** - Reportar bugs
- **[Documentación del Proyecto](README.md)** - Información general

---

## Próximos Pasos

Una vez instalado:

1. **Lee la documentación:** [README.md](README.md)
2. **Configura tus primeros reportes:** Edita `config.yaml`
3. **Ejecuta el bot:** `python main.py`
4. **Contribuye:** Ver [CONTRIBUTING.md](CONTRIBUTING.md)

¡Felicidades! Ahora estás listo para usar el Email Report Bot.
