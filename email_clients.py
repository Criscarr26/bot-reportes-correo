import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Optional
from datetime import datetime

from config import OUTLOOK_EMAIL, OUTLOOK_PASSWORD, MOM_EMAIL


class EmailMessage:
    """Unified email message format"""
    def __init__(self, sender: str, subject: str, date: datetime, body: str, source: str):
        self.sender = sender
        self.subject = subject
        self.date = date
        self.body = body
        self.source = source  # 'outlook' or 'gmail'

    def to_dict(self) -> Dict:
        return {
            'Remitente': self.sender,
            'Asunto': self.subject,
            'Fecha': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else 'N/A',
            'Cuerpo': self.body[:500],  # First 500 chars
            'Fuente': self.source.upper()
        }


class OutlookClient:
    """Outlook email client using IMAP (standard Python library)"""
    
    def __init__(self, email_addr: str, password: str):
        self.email = email_addr
        self.password = password
        self.imap = None
        
    def connect(self) -> bool:
        """Authenticate and connect to Outlook via IMAP"""
        try:
            # Outlook/Office365 IMAP server
            self.imap = imaplib.IMAP4_SSL('outlook.office365.com', 993)
            self.imap.login(self.email, self.password)
            print(f"✓ Connected to Outlook: {self.email}")
            return True
        except imaplib.IMAP4.error as e:
            print(f"✗ Outlook authentication failed: {e}")
            print(f"  Tip: Use an app password, not your regular password")
            return False
        except Exception as e:
            print(f"✗ Error connecting to Outlook: {e}")
            return False

    def fetch_emails(self, limit: int = 50, subject_filter: str = None) -> List[EmailMessage]:
        """Fetch emails from Outlook"""
        emails = []
        try:
            if not self.imap:
                print("Not connected to Outlook")
                return emails

            # Select inbox
            self.imap.select('INBOX')
            
            # Search for all emails
            status, message_ids = self.imap.search(None, 'ALL')
            if status != 'OK':
                return emails
            
            # Get latest emails (up to limit)
            msg_ids = message_ids[0].split()[-limit:]
            
            for msg_id in msg_ids:
                try:
                    status, msg_data = self.imap.fetch(msg_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract headers
                    sender = msg.get('From', 'Unknown')
                    subject = msg.get('Subject', '(No Subject)')
                    date_str = msg.get('Date', '')
                    
                    # Decode subject if needed
                    if isinstance(subject, str):
                        try:
                            subject_parts = decode_header(subject)
                            subject = ''.join(
                                part.decode(charset or 'utf-8') if isinstance(part, bytes) else part
                                for part, charset in subject_parts
                            )
                        except:
                            pass
                    
                    # Parse date
                    try:
                        date = datetime.strptime(date_str[:16], '%a, %d %b %Y')
                    except:
                        date = None
                    
                    # Get body
                    body = self._get_email_body(msg)
                    
                    # Filter by subject if specified
                    if subject_filter and subject_filter.lower() not in subject.lower():
                        continue
                    
                    email_msg = EmailMessage(
                        sender=sender,
                        subject=subject,
                        date=date,
                        body=body,
                        source='outlook'
                    )
                    emails.append(email_msg)
                except Exception as e:
                    print(f"  Warning: Error parsing email: {e}")
                    continue

            print(f"✓ Fetched {len(emails)} emails from Outlook")
            return emails
        except Exception as e:
            print(f"✗ Error fetching emails from Outlook: {e}")
            return emails
        finally:
            if self.imap:
                try:
                    self.imap.close()
                    self.imap.logout()
                except:
                    pass

    def _get_email_body(self, msg) -> str:
        """Extract email body"""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            return payload.decode('utf-8', errors='ignore')
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='ignore')
        except:
            pass
        return '(No Body)'


class GmailClient:
    """Gmail email client using IMAP (standard Python library)"""
    
    def __init__(self):
        self.imap = None
        
    def connect(self, email_addr: str, app_password: str) -> bool:
        """Authenticate and connect to Gmail via IMAP"""
        try:
            self.imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            self.imap.login(email_addr, app_password)
            print(f"✓ Connected to Gmail: {email_addr}")
            return True
        except imaplib.IMAP4.error as e:
            print(f"✗ Gmail authentication failed: {e}")
            print(f"  Tip: Use an app password from Google Account")
            return False
        except Exception as e:
            print(f"✗ Error connecting to Gmail: {e}")
            return False

    def fetch_emails(self, sender_email: str = None, limit: int = 50) -> List[EmailMessage]:
        """Fetch emails from Gmail"""
        emails = []
        try:
            if not self.imap:
                print("Not connected to Gmail")
                return emails

            # Select inbox
            self.imap.select('INBOX')
            
            # Build search query
            if sender_email:
                query = f'FROM "{sender_email}"'
            else:
                query = 'ALL'
            
            # Search for emails
            status, message_ids = self.imap.search(None, query)
            if status != 'OK':
                return emails
            
            # Get latest emails (up to limit)
            msg_ids = message_ids[0].split()[-limit:]
            
            for msg_id in msg_ids:
                try:
                    status, msg_data = self.imap.fetch(msg_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract headers
                    sender = msg.get('From', 'Unknown')
                    subject = msg.get('Subject', '(No Subject)')
                    date_str = msg.get('Date', '')
                    
                    # Decode subject if needed
                    if isinstance(subject, str):
                        try:
                            subject_parts = decode_header(subject)
                            subject = ''.join(
                                part.decode(charset or 'utf-8') if isinstance(part, bytes) else part
                                for part, charset in subject_parts
                            )
                        except:
                            pass
                    
                    # Parse date
                    try:
                        date = datetime.strptime(date_str[:16], '%a, %d %b %Y')
                    except:
                        date = None
                    
                    # Get body
                    body = self._get_email_body(msg)
                    
                    email_msg = EmailMessage(
                        sender=sender,
                        subject=subject,
                        date=date,
                        body=body,
                        source='gmail'
                    )
                    emails.append(email_msg)
                except Exception as e:
                    print(f"  Warning: Error parsing Gmail: {e}")
                    continue

            print(f"✓ Fetched {len(emails)} emails from Gmail")
            return emails
        except Exception as e:
            print(f"✗ Error fetching emails from Gmail: {e}")
            return emails
        finally:
            if self.imap:
                try:
                    self.imap.close()
                    self.imap.logout()
                except:
                    pass

    def _get_email_body(self, msg) -> str:
        """Extract email body"""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            return payload.decode('utf-8', errors='ignore')
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='ignore')
        except:
            pass
        return '(No Body)'
