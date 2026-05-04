import uuid
import time

# Keys ka data yahan save hoga
keys_database = {}

def main_menu():
    while True:
        print("\n" + "="*30)
        print("   TPC KEY ADMIN PANEL")
        print("="*30)
        print("1. Generate New Keys")
        print("2. View All Keys")
        print("3. Check Key Status")
        print("4. Exit")
        
        choice = input("\nSelect Option: ")
        
        if choice == "1":
            qty = int(input("Kitni keys banani hain? "))
            print("\nGenerating...")
            time.sleep(1)
            for _ in range(qty):
                # Unique random key banana
                k = "TPC-" + str(uuid.uuid4()).upper()[:8]
                keys_database[k] = "Active"
                print(f"[✔] Created: {k}")
            
        elif choice == "2":
            print("\n--- ALL ACTIVE KEYS ---")
            if not keys_database:
                print("Abhi koi key nahi bani.")
            for k in keys_database:
                print(f"Key: {k} | Status: Active")
                
        elif choice == "3":
            check = input("Verify karne ke liye key likhein: ")
            if check in keys_database:
                print(f"Result: [✔] {check} is VALID.")
            else:
                print("Result: [✘] Invalid or Expired Key!")
                
        elif choice == "4":
            print("Dashboard band ho raha hai...")
            break
        else:
            print("Ghalat button! Dobara koshish karein.")

if __name__ == "__main__":
    main_menu()
  
