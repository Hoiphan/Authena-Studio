import os
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import pandas as pd
import matplotlib.dates as mdates


from dotenv import load_dotenv
load_dotenv()

# Kết nối MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["task_logger"]
collection = db["task_logs"]

# Lấy dữ liệu ngày hôm qua
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

logs = list(collection.find({
    "timestamp": {
        "$gte": datetime(yesterday.year, yesterday.month, yesterday.day),
        "$lt": datetime(today.year, today.month, today.day)
    }
}))



# Giả sử df chứa dữ liệu từ MongoDB
df = pd.DataFrame(logs)

# Xác nhận có cột timestamp
if "timestamp" not in df.columns:
    print("❌ Lỗi: không tìm thấy cột 'timestamp' trong dữ liệu MongoDB.")
    print("Các cột hiện có:", df.columns)
    exit(1)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour



# 1. Tính toán
success = df[df["status"] == "success"].shape[0]
failed = df[df["status"] == "failed"].shape[0]
hourly_count = df.groupby("hour").size()
format_count = df["output_format"].value_counts()

# Nếu có thời gian thực thi từng task:
df["duration_sec"] = (df["completed_at"] - df["timestamp"]).dt.total_seconds()

# 2. Plot
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# --- Pie Chart: Success vs Failed ---
labels = ["Success", "Failed"]
sizes = [success, failed]
colors = ["#4CAF50", "#F44336"]
wedges, _, autotexts = axs[0, 0].pie(
    sizes, colors=colors, autopct="%1.1f%%", startangle=140, textprops=dict(color="white")
)
axs[0, 0].axis("equal")
axs[0, 0].set_title("Success vs Failed Rate")
axs[0, 0].legend(wedges, labels, title="Status", loc="center left", bbox_to_anchor=(1, 0.5))

# --- Bar Chart: Task per Hour ---
axs[0, 1].bar(hourly_count.index, hourly_count.values, color="#3498db")
axs[0, 1].set_xticks(range(24))
axs[0, 1].set_xlabel("Hour of Day")
axs[0, 1].set_ylabel("Number of Tasks")
axs[0, 1].set_title("Task Distribution by Hour")

# --- Pie Chart: Output Formats ---
format_labels = format_count.index.tolist()
format_sizes = format_count.values
format_colors = plt.cm.Set3(range(len(format_labels)))

wedges2, _, _ = axs[1, 0].pie(
    format_sizes, labels=None, colors=format_colors, autopct="%1.1f%%", startangle=90, textprops=dict(color="black")
)
axs[1, 0].axis("equal")
axs[1, 0].set_title("Output Format Distribution")
axs[1, 0].legend(wedges2, format_labels, title="Formats", loc="center left", bbox_to_anchor=(1, 0.5))

# --- Boxplot: Task Execution Duration ---
if "duration_sec" in df:
    axs[1, 1].boxplot(df["duration_sec"].dropna(), vert=False)
    axs[1, 1].set_title("Task Execution Time Distribution")
    axs[1, 1].set_xlabel("Seconds")
else:
  axs[1, 1].text(0.5, 0.5, "No duration data available", ha="center", va="center", fontsize=12)
  axs[1, 1].axis("off")

plt.tight_layout()
plt.savefig("report.png")



# Gửi email với SendGrid
with open("report.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()


now = (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")

message = Mail(
    from_email=os.getenv('FROM_EMAIL'),
    to_emails=os.getenv('ADMIN_EMAIL'),
    subject="📊 Daily System Report",
    html_content=f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ccc; border-radius: 10px;">
        <h2 style="color: #2c3e50;">📅 Automated Report - {now}</h2>
        <p style="font-size: 16px;">Hello Admin,</p>

        <p style="font-size: 16px;">Here is the summary of the system tasks for the day:</p>

        <table style="border-collapse: collapse; width: 100%; font-size: 16px;">
            <tr>
                <th style="text-align: left; padding: 8px; background-color: #2ecc71; color: white;">✅ Success</th>
                <th style="text-align: left; padding: 8px; background-color: #e74c3c; color: white;">❌ Failed</th>
            </tr>
            <tr>
                <td style="padding: 8px; background-color: #ecf0f1;">{success}</td>
                <td style="padding: 8px; background-color: #ecf0f1;">{failed}</td>
            </tr>
        </table>

        <p style="margin-top: 20px;">📈 The summary chart is attached to this email.</p>

        <p style="margin-top: 30px; font-size: 14px; color: #888;">
            Regards,<br>
            🤖 Automated Monitoring System
        </p>
    </div>
    """,
)

attachment = Attachment(
    FileContent(encoded),
    FileName("report.png"),
    FileType("image/png"),
    Disposition("attachment"),
)
message.attachment = attachment

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
sg.send(message)
