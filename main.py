#!/usr/bin/env python3
"""
Email Bot - Reads emails and generates reports
Supports Outlook (university notifications) and Gmail (personal emails)
"""

import sys
import os
from pathlib import Path
from typing import Dict, List

from config import (
    OUTLOOK_EMAIL, OUTLOOK_PASSWORD, MOM_EMAIL,
    INCLUDE_NOTIFICATIONS, REPORT_OUTPUT_DIR,
    UNIVERSITY_KEYWORDS, NOTIFICATION_KEYWORDS
)
from email_clients import OutlookClient, GmailClient, EmailMessage
from report_generator import ReportGenerator


def filter_emails_by_category(emails: List[EmailMessage]) -> Dict[str, List[EmailMessage]]:
    """Categorize emails"""
    categories = {
        'Universidad': [],
        'Notificaciones': [],
        'Correos Personales': []
    }
    
    for email in emails:
        subject_lower = email.subject.lower()
        sender_lower = email.sender.lower()
        
        # Check for university emails
        if any(kw in subject_lower for kw in UNIVERSITY_KEYWORDS):
            categories['Universidad'].append(email)
        # Check for notifications
        elif any(kw in subject_lower for kw in NOTIFICATION_KEYWORDS):
            categories['Notificaciones'].append(email)
        # Personal emails (from mom)
        elif email.source == 'gmail':
            categories['Correos Personales'].append(email)
        else:
            categories['Notificaciones'].append(email)
    
    return categories


def main():
    """Main bot function"""
    print("\n" + "="*60)
    print("📧 EMAIL BOT - Report Generator")
    print("="*60 + "\n")
    
    all_emails = []
    
    # ===== OUTLOOK =====
    print("📨 Connecting to Outlook...")
    outlook_client = OutlookClient(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
    
    if outlook_client.connect():
        print("  Fetching university emails...")
        outlook_emails = outlook_client.fetch_emails(limit=50)
        all_emails.extend(outlook_emails)
    else:
        print("⚠ Skipping Outlook")
    
    # ===== GMAIL =====
    print("\n📨 Connecting to Gmail...")
    gmail_client = GmailClient()
    
    # Get Gmail credentials from environment
    gmail_email = os.getenv('GMAIL_EMAIL', '')
    gmail_password = os.getenv('GMAIL_APP_PASSWORD', '')
    
    if gmail_email and gmail_password:
        if gmail_client.connect(gmail_email, gmail_password):
            if MOM_EMAIL:
                print(f"  Fetching emails from {MOM_EMAIL}...")
                gmail_emails = gmail_client.fetch_emails(sender_email=MOM_EMAIL, limit=50)
                all_emails.extend(gmail_emails)
            else:
                print("⚠ Gmail setup required - set MOM_EMAIL in .env")
        else:
            print("⚠ Failed to connect to Gmail")
    else:
        print("⚠ Gmail credentials not set - skipping")
    
    # ===== GENERATE REPORT =====
    if all_emails:
        print(f"\n📊 Processing {len(all_emails)} emails...")
        
        # Categorize emails
        categorized = filter_emails_by_category(all_emails)
        
        # Show summary
        print("\n📋 Email Summary:")
        for category, emails in categorized.items():
            if emails:
                print(f"  • {category}: {len(emails)} emails")
        
        # Generate report
        print("\n📄 Generating Excel report...")
        generator = ReportGenerator(REPORT_OUTPUT_DIR)
        report_path = generator.generate_report(categorized)
        
        print(f"\n✓ Report saved to: {report_path}")
        print("="*60 + "\n")
        return 0
    else:
        print("\n✗ No emails found or connection failed")
        print("="*60 + "\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
