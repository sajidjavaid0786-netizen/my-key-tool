import uuid
import json
import os
import requests
import base64
from datetime import datetime, timedelta

# --- SETTINGS ---
TOKEN = "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"
REPO = "sajidjavaid0786-netizen/my-key-tool"
FILE_PATH = "database.json"
# ----------------

DB_FILE = "database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def push_to_github():
    """GitHub par database.json ko automatic upload karne ka function"""
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Pehle purani file ka 'sha' (ID) lena parta hai update ke liye
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha', '')

    with open(DB_FILE, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    data = {
        "message": "Auto update database",
        "content": content,
        "sha": sha
    }
    
    res = requests.put(url, headers=headers, json=data)
    if res.status_code == 200 or res.status_code == 201:
        print("\033[92m[✔] GitHub Database Updated Automatically! \033[0m")
    else:
        print("\033[91m[✘] GitHub Update Failed! Error:", res.status_code, "\033[0m")

def main_menu():
    keys_db = load_data()
    while True:
        # ... (Upar wala menu aur logic wahi rahega) ...
        # Bas Option 1 mein end par ye line add karni hai:
        
        if choice == "1":
            # ... key banane ka code ...
            save_data(keys_db)
            push_to_github() # Yeh line automatic upload karegi
