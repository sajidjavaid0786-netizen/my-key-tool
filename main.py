import uuid
import json
import os
import requests
import base64
from datetime import datetime, timedelta

# ================== SETTINGS ==================
# 1. Yahan apna NAYA token paste karein
TOKEN = "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" 

# 2. Check karein ke repo ka naam bilkul yehi hai
REPO = "sajidjavaid0786-netizen/my-key-tool"
FILE_PATH = "database.json"
DB_FILE = "database.json"
# ==============================================

# Colors
G = "\033[92m" # Green
R = "\033[91m" # Red
Y = "\033[93m" # Yellow
C = "\033[96m" # Cyan
W = "\033[0m"  # White/Reset

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def push_to_github():
    """Is function se keys automatic Cloud par chali jayengi"""
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Get current file SHA
    r = requests.get(url, headers=headers)
    
    if r.status_code == 401:
        print(f"{R}[✘] Error 401: Token Invalid hai! Naya banayein.{W}")
        return
    elif r.status_code == 404:
        sha = None # File pehle se nahi hai toh naya banayega
    else:
        sha = r.json().get('sha', None)

    # 2. Encode database to Base64
    with open(DB_FILE, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    data = {
        "message": "Update Keys: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": content
    }
    if sha:
        data["sha"] = sha

    # 3. Upload to GitHub
    res = requests.put(url, headers=headers, json=data)
    
    if res.status_code in [200, 201]:
        print(f"{G}[✔] Cloud Sync Done! Keys are now LIVE on GitHub.{W}")
    else:
        print(f"{R}[✘] Sync Failed! Code: {res.status_code}{W}")
        print(f"{Y}Tip: Token banate waqt 'repo' par tick lagaya tha?{W}")

def main_menu():
    keys_db = load_data()
    while True:
        print(f"\n{C}====================================")
        print("     TPC PRO ADMIN PANEL v3.5")
        print("====================================" + f"{W}")
        print(f"{Y}Cloud Storage: {REPO}{W}")
        print(f"{G}[1] Generate New License Key")
        print(f"[2] View Active Keys List")
        print(f"{R}[3] Exit{W}")
        
        choice = input(f"\n{Y}Select Option: {W}")
        
        if choice == "1":
            try:
                days = int(input(f"{G}Enter Validity (Days): {W}"))
                expiry_date = datetime.now() + timedelta(days=days)
                new_k = "TPC-" + str(uuid.uuid4()).upper()[:8]
                
                keys_db[new_k] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                save_data(keys_db)
                
                print(f"\n{G}[✔] Key Generated: {new_k}{W}")
                print(f"{Y}[*] Syncing to Cloud... Please wait.{W}")
                push_to_github()
            except ValueError:
                print(f"{R}[!] Error: Sirf number likhein (e.g. 7){W}")
            except Exception as e:
                print(f"{R}[!] Error: {e}{W}")
            
        elif choice == "2":
            print(f"\n{C}--- CURRENT KEYS IN DATABASE ---{W}")
            if not keys_db: print(f"{R}No keys found.{W}")
            for k, exp in keys_db.items():
                print(f"{G}Key: {k} {W}| {Y}Exp: {exp}{W}")
                
        elif choice == "3":
            print(f"{C}Closing Admin Panel...{W}")
            break

if __name__ == "__main__":
    main_menu()
    
