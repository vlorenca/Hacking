# TELEGRAM HEALTH REPORT TO MOBILE PHONE
# AUTHOR: Vince Lorenca
# DATE: 4/20/26
# FOR: LORENCA TECHNOLOGY SOLUTIONS

# IMPORTS
import requests
import time
import socket
import getpass
import psutil

# TELEGRAM SPECIFIC LOGIN ITEMS
TOKEN = "<YOUR TELEGRAM TOKEN>"
CHAT_ID = "<YOUR TELEGRAM CHAT ID STARTS WITH A MINUS SIGN ->"
INTERVAL = 600

# DEFINE
def get_system_info():
    hostname = socket.gethostname()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
    except Exception:
        ip_addr = "Unable to retrieve IP"

    username = getpass.getuser()
    return hostname, ip_addr, username


def send_telegram_update(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")


# MAIN LOOP
print("Monitoring started, Press Ctrl+C to stop...")

while True:
    hostname, ip, user = get_system_info()
    cpu = psutil.cpu_percent()

    status_msg = (
        f"*System Heartbeat*\n"
        f"---\n"
        f"*User:* {user}\n"
        f"*Host:* {hostname}\n"
        f"*LAN IP:* {ip}\n"
        f"*CPU Usage:* {cpu}%\n"
        f"*Last Check:* {time.strftime('%H:%M:%S')}"
    )

    send_telegram_update(status_msg)
    time.sleep(INTERVAL)
