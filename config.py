import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# Outlook Configuration
OUTLOOK_EMAIL = os.getenv('OUTLOOK_EMAIL', '')
OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD', '')

# Gmail Configuration
GMAIL_CREDENTIALS_FILE = os.getenv('GMAIL_CREDENTIALS_FILE', 'gmail_credentials.json')
GMAIL_CREDENTIALS_PATH = BASE_DIR / GMAIL_CREDENTIALS_FILE

# Bot Configuration
REPORT_OUTPUT_DIR = Path(os.getenv('REPORT_OUTPUT_DIR', BASE_DIR / 'reports'))
REPORT_OUTPUT_DIR.mkdir(exist_ok=True)

INCLUDE_NOTIFICATIONS = os.getenv('INCLUDE_NOTIFICATIONS', 'true').lower() == 'true'
MOM_EMAIL = os.getenv('MOM_EMAIL', '')

# Email filtering keywords
UNIVERSITY_KEYWORDS = ['universidad', 'university', 'campus', 'clase', 'tarea', 'examen']
NOTIFICATION_KEYWORDS = ['notificación', 'notification', 'alert', 'alerta', 'update']
