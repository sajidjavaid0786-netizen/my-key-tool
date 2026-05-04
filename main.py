import uuid
import json
import os
import requests
import base64
from datetime import datetime, timedelta

# --- SETTINGS (Token Added) ---
TOKEN = "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" 
REPO = "sajidjavaid0786-netizen/my-key-tool"
FILE_PATH = "database.json"
DB_FILE = "database.json"

# Colors
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def push_to_github():
    """Is function se keys automatic GitHub par upload ho jayengi"""
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Get file SHA
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha', '')

    with open(DB_FILE, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    data = {
        "message": "Auto-sync keys from Termux",
        "content": content,
        "sha": sha
    }
    
    res = requests.put(url, headers=headers, json=data)
    if res.status_code in [200, 201]:
        print(f"{G}[✔] Cloud Sync Successful! Keys are now LIVE.{W}")
    else:
        print(f"{R}[✘] Sync Failed! Error Code: {res.status_code}{W}")

def main_menu():
    keys_db = load_data()
    while True:
        print(f"\n{C}====================================")
        print("     TPC PRO ADMIN PANEL v3.0")
        print("====================================" + f"{W}")
        print(f"{Y}Status: Connected to GitHub Cloud{W}")
        print(f"{G}[1] Generate New Key")
        print(f"[2] View All Keys")
        print(f"{R}[3] Exit{W}")
        
        choice = input(f"\n{Y}Select Option: {W}")
        
        if choice == "1":
            try:
                days = int(input(f"{G}Enter validity (days): {W}"))
                expiry_date = datetime.now() + timedelta(days=days)
                new_k = "TPC-" + str(uuid.uuid4()).upper()[:8]
                
                keys_db[new_k] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                save_data(keys_db)
                
                print(f"\n{G}[✔] Local Key Created: {new_k}{W}")
                print(f"{Y}[*] Syncing to GitHub...{W}")
                push_to_github()
            except Exception as e:
                print(f"{R}[!] Error: {e}{W}")
            
        elif choice == "2":
            print(f"\n{C}--- CURRENT DATABASE ---{W}")
            for k, exp in keys_db.items():
                print(f"{G}Key: {k} | Exp: {exp}{W}")
                
        elif choice == "3":
            break

if __name__ == "__main__":
    main_menu()
    
