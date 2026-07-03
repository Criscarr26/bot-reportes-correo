#!/usr/bin/env python3
"""
Demo script - generates sample email report without email credentials
Perfect for testing report generation functionality
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from email_clients import EmailMessage
from report_generator import ReportGenerator


def create_sample_emails() -> List[EmailMessage]:
    """Create sample emails for demonstration"""
    now = datetime.now()
    
    samples = [
        EmailMessage(
            sender="registrar@itla.edu.do",
            subject="Notificación: Periodo de inscripción abierto",
            date=now - timedelta(days=1),
            body="El periodo de inscripción para el próximo semestre está abierto. Por favor, regístrese antes del 15 de junio.",
            source="outlook"
        ),
        EmailMessage(
            sender="profesor@itla.edu.do",
            subject="Universidad - Cambio de horario de clase",
            date=now - timedelta(days=2),
            body="Se comunica que la clase de Programación ha sido cambiada al martes a las 2 PM en el aula 301.",
            source="outlook"
        ),
        EmailMessage(
            sender="admision@itla.edu.do",
            subject="ALERTA: Documentos faltantes en tu expediente",
            date=now - timedelta(days=3),
            body="Requiere fotocopia de cédula y comprobante de domicilio. Envíe antes del 10 de junio.",
            source="outlook"
        ),
        EmailMessage(
            sender="notification@outlook.com",
            subject="Notificación de seguridad: Acceso nuevo a tu cuenta",
            date=now - timedelta(days=4),
            body="Se detectó acceso a tu cuenta desde Windows 10. Si no fuiste tú, cambia tu contraseña.",
            source="outlook"
        ),
        EmailMessage(
            sender="mom@gmail.com",
            subject="¡Hola cariño! ¿Cómo estás?",
            date=now - timedelta(days=1),
            body="Solo quería saber cómo te va en la universidad. Recuerda comer bien y dormir lo suficiente. Te quiero mucho.",
            source="gmail"
        ),
        EmailMessage(
            sender="mom@gmail.com",
            subject="Mamá - Recuerda traer ropa limpia",
            date=now - timedelta(days=5),
            body="Cuando vengas a casa trae la ropa sucia para lavar. También compra leche en el camino.",
            source="gmail"
        ),
    ]
    
    return samples


def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("📧 EMAIL BOT - Demo Report Generator")
    print("="*60 + "\n")
    
    print("📝 Generating sample emails for demonstration...")
    sample_emails = create_sample_emails()
    
    # Categorize emails
    categories = {
        'Universidad': [],
        'Notificaciones': [],
        'Correos Personales': []
    }
    
    for email in sample_emails:
        subject_lower = email.subject.lower()
        
        if any(kw in subject_lower for kw in ['universidad', 'university', 'clase', 'tarea', 'examen']):
            categories['Universidad'].append(email)
        elif any(kw in subject_lower for kw in ['notificación', 'notification', 'alert', 'alerta']):
            categories['Notificaciones'].append(email)
        else:
            categories['Correos Personales'].append(email)
    
    # Show summary
    print("📋 Sample Email Summary:")
    for category, emails in categories.items():
        if emails:
            print(f"  • {category}: {len(emails)} emails")
    
    # Generate report
    print("\n📄 Generating Excel report...")
    generator = ReportGenerator(Path('./reports'))
    report_path = generator.generate_report(categories)
    
    print(f"\n✓ Demo report saved to: {report_path}")
    print("="*60)
    print("\n📖 NEXT STEPS:")
    print("  1. Copy .env.example to .env")
    print("  2. Fill in your email credentials:")
    print("     - OUTLOOK_EMAIL: your_university_email@outlook.com")
    print("     - OUTLOOK_PASSWORD: your_app_password")
    print("     - GMAIL_EMAIL: your_gmail@gmail.com")
    print("     - GMAIL_APP_PASSWORD: your_gmail_app_password")
    print("  3. Run: python main.py")
    print("="*60 + "\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
