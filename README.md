📊 Daily Report Scheduler
This GitHub Action automates the generation and distribution of a daily report using Python. It runs every day at 08:00 AM (Vietnam time) and can also be triggered manually via the GitHub UI.

🧩 Features
⏰ Scheduled to run daily using cron (01:00 UTC)

🐍 Runs a custom Python script to fetch data, generate reports, and send email notifications

🔒 Uses GitHub Secrets to securely handle credentials (MongoDB, SendGrid, etc.)

💌 Sends reports via email using SendGrid

🚀 How It Works
Checkout the repository

Set up Python (version 3.10)

Install dependencies from requirements.txt

Run the main script (script.py) with environment variables

🛠️ Configuration
To use this workflow, make sure to set the following GitHub Secrets:

Secret Name	Description
MONGO_URI	MongoDB connection string
SENDGRID_API_KEY	API key for sending emails
ADMIN_EMAIL	Recipient email address
FROM_EMAIL	Sender email address (verified)

📅 Schedule
This workflow is triggered automatically every day at:

01:00 UTC

08:00 AM (Vietnam Time)

Or you can trigger it manually from the GitHub Actions UI.

📄 License
This project is licensed under the MIT License.

