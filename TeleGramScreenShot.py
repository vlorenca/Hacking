import requests
import time
import socket
import getpass
import psutil
import pyautogui
import os

# 🔐 PUT YOUR TOKEN HERE (regenerate if needed)
TOKEN = "<YOUR TELEGRAM TOKEN>"

# ✅ Your working chat ID (from your test)
CHAT_ID = "-<YOUR TELEGRAM CHAT ID>"

INTERVAL = 600  # seconds (10 minutes)


def get_system_info():
    hostname = socket.gethostname()
    username = getpass.getuser()
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "Unknown"

    return hostname, ip, username, cpu, ram


def send_telegram_update(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        print("Message response:", response.text)
    except Exception as e:
        print("Error sending message:", e)


def send_screenshot(caption):
    try:
        # 📸 Take screenshot
        screenshot = pyautogui.screenshot()
        file_path = "screenshot.png"
        screenshot.save(file_path)

        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        with open(file_path, "rb") as photo:
            response = requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption,
                    "parse_mode": "Markdown"
                },
                files={"photo": photo}
            )

        print("Screenshot response:", response.text)

        # 🧹 Remove file after sending
        os.remove(file_path)

    except Exception as e:
        print("Error sending screenshot:", e)


# 🚀 MAIN LOOP
print("Monitoring started... Press Ctrl+C to stop.")

while True:
    hostname, ip, user, cpu, ram = get_system_info()

    status_msg = (
        f"*System Heartbeat*\n"
        f"---\n"
        f"*User:* {user}\n"
        f"*Host:* {hostname}\n"
        f"*LAN IP:* {ip}\n"
        f"*CPU:* {cpu}%\n"
        f"*RAM:* {ram}%\n"
        f"*Time:* {time.strftime('%H:%M:%S')}"
    )

    # Send message + screenshot
    send_telegram_update(status_msg)
    send_screenshot(status_msg)

    time.sleep(INTERVAL)
