import uuid
import json
import os
from datetime import datetime, timedelta

# Colors ke codes
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

DB_FILE = "database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

def main_menu():
    keys_db = load_data()
    while True:
        print(f"\n{CYAN}====================================")
        print("     TPC PRO ADMIN PANEL v3.0")
        print("====================================" + f"{RESET}")
        print(f"{YELLOW}Total Active Keys: {len(keys_db)}{RESET}")
        print(f"{GREEN}[1] Generate Key (With Expiry)")
        print(f"[2] View All Keys & Status")
        print(f"{RED}[3] Verify a Key")
        print(f"{CYAN}[4] Exit{RESET}")
        
        choice = input(f"\n{YELLOW}Select Option: {RESET}")
        
        if choice == "1":
            print(f"\n{CYAN}--- Select Plan ---{RESET}")
            print("Days: 1, 3, 7, 10, 15, 30")
            try:
                days = int(input(f"{GREEN}Kitne din ki key banani hai?: {RESET}"))
                expiry_date = datetime.now() + timedelta(days=days)
                new_k = "TPC-" + str(uuid.uuid4()).upper()[:8]
                keys_db[new_k] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                save_data(keys_db)
                print(f"\n{GREEN}[✔] Created: {new_k}")
                print(f"[!] Valid until: {keys_db[new_k]}{RESET}")
            except:
                print(f"{RED}[✘] Ghalat input! Sirf number likhein.{RESET}")
            
        elif choice == "2":
            print(f"\n{CYAN}--- ALL KEYS LIST ---{RESET}")
            if not keys_db: print(f"{RED}Koi key nahi mili.{RESET}")
            for k, exp in keys_db.items():
                print(f"{GREEN}Key: {k} {YELLOW}| Expires: {exp}{RESET}")
                
        elif choice == "3":
            check = input(f"{YELLOW}Enter key to verify: {RESET}")
            if check in keys_db:
                exp_time = datetime.strptime(keys_db[check], "%Y-%m-%d %H:%M:%S")
                if datetime.now() < exp_time:
                    print(f"{GREEN}[✔] VALID! Expires on: {keys_db[check]}{RESET}")
                else:
                    print(f"{RED}[✘] EXPIRED! Time's up.{RESET}")
            else:
                print(f"{RED}[✘] INVALID! Not found.{RESET}")
                
        elif choice == "4":
            print(f"{YELLOW}Closing...{RESET}")
            break

if __name__ == "__main__":
    main_menu()
    
