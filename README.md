# 📧 Email Bot - Report Generator

A Python automation bot that reads emails from Outlook (university notifications) and Gmail (personal emails) and generates Excel reports.

## Features

- ✅ Connect to Outlook for university emails and notifications
- ✅ Connect to Gmail for personal emails (from specific senders)
- ✅ Automatic email categorization (University, Notifications, Personal)
- ✅ Generate formatted Excel (XLSX) reports with email data
- ✅ Summary statistics sheet
- ✅ Easy configuration via `.env` file
- ✅ Scheduled automation support

## Requirements

- Python 3.8+
- Outlook account (university email)
- Gmail account (for personal emails)

## Installation

### 1. Clone/Download the Project

```bash
cd "Bot que lea correos y genere reportes"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Configuration

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

Edit `.env`:
```
OUTLOOK_EMAIL=your_university_email@outlook.com
OUTLOOK_PASSWORD=your_app_password
MOM_EMAIL=mom_email@gmail.com
REPORT_OUTPUT_DIR=./reports
```

#### Outlook Setup
1. Use your university email and password
2. Or generate an "App Password" for more security:
   - Go to https://account.microsoft.com/security
   - Enable two-factor authentication
   - Create an app password for "Other (Windows Device)"

#### Gmail Setup
To enable the bot to read Gmail:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials as JSON and save as `gmail_credentials.json` in the project folder
6. Run the bot once - it will prompt you to authorize
7. OR use a service account with appropriate permissions

**Current Status**: Gmail integration requires additional setup. See `email_clients.py` for implementation notes.

## Usage

### Run the Bot

```bash
python main.py
```

The bot will:
1. Connect to Outlook
2. Fetch your latest emails
3. Connect to Gmail (if configured)
4. Fetch emails from specified sender
5. Categorize all emails
6. Generate an Excel report in `./reports/`

### Output

Reports are saved as `email_report_YYYYMMDD_HHMMSS.xlsx` with:
- **Summary Sheet**: Total counts by category
- **Universidad Sheet**: University-related emails
- **Notificaciones Sheet**: Notification emails
- **Correos Personales Sheet**: Personal emails from family

## Scheduling (Optional)

### Windows Task Scheduler

1. Create a batch file `run_bot.bat`:
```batch
@echo off
cd C:\Users\tu_usuario\path\to\bot
python main.py
pause
```

2. Open Task Scheduler
3. Create Basic Task
4. Set trigger (e.g., daily at 9 AM)
5. Set action: Start program → `run_bot.bat`

### Linux/Mac (Cron)

Add to crontab:
```bash
0 9 * * * cd /path/to/bot && python main.py
```

## Project Structure

```
Bot que lea correos y genere reportes/
├── main.py                 # Main bot script
├── config.py               # Configuration management
├── email_clients.py        # Outlook & Gmail clients
├── report_generator.py     # Excel report generation
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── .env                   # Configuration (not in git)
├── README.md              # This file
└── reports/               # Output folder (created automatically)
    └── email_report_*.xlsx # Generated reports
```

## Troubleshooting

### "Failed to authenticate with Outlook"
- Check your email and password in `.env`
- Use an app password instead of your regular password
- Verify two-factor authentication is enabled

### "Gmail credentials file not found"
- Download OAuth2 credentials from Google Cloud Console
- Save as `gmail_credentials.json` in project folder

### "No emails found"
- Check that your email addresses in `.env` are correct
- Verify you have emails matching the filters
- Check email folder permissions

### "No module named 'O365'"
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Support for other email providers (Thunderbird, ProtonMail, etc.)
- [ ] Advanced email filtering (regex, date ranges)
- [ ] Email attachment extraction
- [ ] PDF and Word report formats
- [ ] Email analytics and charts
- [ ] Automatic email archiving
- [ ] Multi-language support

## License

MIT

## Support

For issues or questions, please check the logs and ensure:
1. All dependencies are installed: `pip install -r requirements.txt`
2. `.env` file is properly configured
3. Email credentials are correct
4. Two-factor authentication is set up for Outlook (if required)
