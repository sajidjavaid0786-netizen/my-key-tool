import uuid
import json
import os
from datetime import datetime, timedelta

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
        print("\n" + "="*35)
        print("   TPC PRO ADMIN PANEL v3.0")
        print("="*35)
        print("1. Generate Key (With Expiry)")
        print("2. View All Keys & Status")
        print("3. Verify a Key")
        print("4. Exit")
        
        choice = input("\nSelect Option: ")
        
        if choice == "1":
            print("\nSelect Plan:")
            print("Days: 1, 3, 7, 10, 15, 20, 25, 30")
            days = int(input("Kitne din ki key banani hai? "))
            
            # Key ki expiry date calculate karna
            expiry_date = datetime.now() + timedelta(days=days)
            new_k = "TPC-" + str(uuid.uuid4()).upper()[:8]
            
            # Database mein save karna
            keys_db[new_k] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
            save_data(keys_db)
            print(f"\n[✔] Created: {new_k}")
            print(f"[!] Valid until: {keys_db[new_k]}")
            
        elif choice == "2":
            print("\n--- ALL KEYS & EXPIRY ---")
            for k, exp in keys_db.items():
                print(f"Key: {k} | Expires: {exp}")
                
        elif choice == "3":
            check = input("Enter key to verify: ")
            if check in keys_db:
                # Check karein ke waqt guzar toh nahi gaya?
                exp_time = datetime.strptime(keys_db[check], "%Y-%m-%d %H:%M:%S")
                if datetime.now() < exp_time:
                    print(f"[✔] VALID! Expires on: {keys_db[check]}")
                else:
                    print("[✘] EXPIRED! Yeh key ab kaam nahi karegi.")
            else:
                print("[✘] INVALID! Key database mein nahi hai.")
                
        elif choice == "4": break

if __name__ == "__main__":
    main_menu()
        
