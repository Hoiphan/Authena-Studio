# 📊 Daily Report Scheduler

This GitHub Action automates the generation and delivery of a daily report using Python. It runs every day at **08:00 AM (Vietnam time)** and can also be triggered manually from the GitHub Actions UI.

## 🔧 How It Works

The workflow performs the following steps:

1. 🔄 Check out the repository
2. 🐍 Set up Python 3.10
3. 📦 Install dependencies from `requirements.txt`
4. 📈 Run `script.py` with necessary environment variables

## 🔐 GitHub Secrets

To run successfully, the workflow uses the following GitHub Secrets:

| Secret Name        | Description                         |
|--------------------|-------------------------------------|
| `MONGO_URI`        | MongoDB connection string           |
| `SENDGRID_API_KEY` | API key for SendGrid                |
| `ADMIN_EMAIL`      | Recipient email address             |
| `FROM_EMAIL`       | Verified sender email address       |

## 🗓️ Schedule

- Runs automatically every day at `01:00 UTC` (08:00 AM Vietnam time)
- Can also be triggered manually via GitHub UI

## 📁 File Structure

- `script.py` – Main script to generate and send the report
- `requirements.txt` – List of Python dependencies
- `.github/workflows/daily-report.yml` – GitHub Actions workflow file

## 🪪 License

This project is licensed under the MIT License.
