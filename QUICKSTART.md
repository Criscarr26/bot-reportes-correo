# 🚀 Quick Start Guide

## Demo - Get Started Instantly ✨

Test the bot without email credentials:

```bash
python demo.py
```

This creates a sample report with demo emails in `reports/email_report_*.xlsx`

## Setup with Real Email Accounts

### Step 1: Configure Your Credentials

Copy the template:
```bash
copy .env.example .env
```

Edit `.env` with your credentials:

#### For Outlook (University Email)

```
OUTLOOK_EMAIL=your_university_email@outlook.com
OUTLOOK_PASSWORD=your_app_password
```

**How to get an Outlook app password:**
1. Go to https://account.microsoft.com/security
2. Enable two-factor authentication (if not already enabled)
3. Create an "App password" for "Other (Windows Device)"
4. Copy the password to `.env`

#### For Gmail (Personal Emails)

```
GMAIL_EMAIL=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password
MOM_EMAIL=mom_email@gmail.com
```

**How to get a Gmail app password:**
1. Go to https://myaccount.google.com/security
2. Enable two-factor authentication
3. Create an App password for "Mail" on "Windows Computer"
4. Copy the password to `.env`

### Step 2: Run the Bot

```bash
python main.py
```

The bot will:
- ✅ Connect to Outlook and fetch university emails
- ✅ Connect to Gmail and fetch emails from your mom
- ✅ Categorize all emails
- ✅ Generate an Excel report in `reports/`

### Step 3: Schedule It (Optional)

#### Windows Task Scheduler

1. Create file `run_bot.bat`:
```batch
@echo off
cd %~dp0
python main.py
```

2. Press `Win+R`, type `taskschd.msc` and press Enter
3. Create Basic Task
4. Trigger: Daily at 9:00 AM
5. Action: Run `run_bot.bat`

#### Linux/Mac

Add to crontab:
```bash
crontab -e
# Add this line for daily runs at 9 AM:
0 9 * * * cd /path/to/bot && python main.py
```

## Project Structure

```
Bot que lea correos y genere reportes/
├── main.py                  ← Main bot script
├── demo.py                  ← Demo (test without email)
├── config.py                ← Configuration
├── email_clients.py         ← Email connection logic
├── report_generator.py      ← Excel report creation
├── requirements.txt         ← Dependencies
├── .env.example            ← Config template
├── .env                    ← Your config (do NOT commit!)
├── README.md               ← Full documentation
├── QUICKSTART.md           ← This file
└── reports/                ← Generated reports (auto-created)
    └── email_report_*.xlsx
```

## Troubleshooting

### "Authentication Failed"
- Check credentials in `.env`
- Use app passwords, not regular passwords
- Ensure two-factor authentication is enabled

### "No emails found"
- Check that email addresses are correct in `.env`
- Verify you have emails matching the filters
- Try the demo first: `python demo.py`

### "Module not found" error
- Install dependencies: `pip install -r requirements.txt` (or use trusted hosts if SSL issues)
- Or: `pip install --trusted-host pypi.org python-dotenv openpyxl`

## Report Format

Each report contains:

- **Summary Sheet** — Total counts by category
- **Universidad Sheet** — University-related emails
- **Notificaciones Sheet** — System notifications
- **Correos Personales Sheet** — Personal emails from family

## Support

All files are properly structured and tested:
- ✅ Syntax checked
- ✅ Demo works
- ✅ All dependencies installed
- ✅ Ready to use!

Just add your email credentials to `.env` and run!
