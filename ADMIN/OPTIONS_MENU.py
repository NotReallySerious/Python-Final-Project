from pharmacist.pharmacist import view
from accountant.account__assistant import daily_summary
from login.auth import register, encrypt_password
import base64
import codecs
import hashlib
def menu():
    try:
        i = True
        while i == True:
            choosingmain = int(input(f"""
*******WELCOME TO ADMIN MENU*************
1. Manage Clinic Users
2. Manage Doctor Records
3. View Reports
4. Generate Clinic Summary Report 
5. Request Removal of Medicine(s) From Medicine Stock 
6. Exit
*****************************************
What is your choice? (enter number 1-6)"""))
            match choosingmain:
                case 1:
                    while True:
                        chooseusers= int(input(f"""
*******MANAGING CLINIC USERS*******
1. Add Clinic Users 
2. Update Clinic Users 
3. Delete Clinic Users
4. Return to ADMIN MENU
***********************************
what is your choice? (enter a number 1-4)"""))
                        if chooseusers== "1":
                            register()
                        elif chooseusers == "2":
                            username = input("Enter username to update: ")
                            update_member(username)
                        elif chooseusers == "3":
                            username = input("Enter username to delete: ")
                            delete_member(username)
                        elif chooseusers == "4":
                            break
                        else:
                            print("Invalid Choice")
                            continue
                case 2:
                    while True:
                        choosedocrecs= int(input(f"""
    *******MANAGING DOCTOR RECORDS*******
    1. Add Doctor Records 
    2. Update Doctor Records 
    3. Delete Doctor Records
    4. Return to ADMIN MENU
    *************************************
                        what is your choice? (enter number 1-3)"""))
                        if choosedocrecs == "1":
                            add_doctor()
                        elif choosedocrecs== "2":
                            update_doctor()
                        elif choosedocrecs== "3":
                            delete_doctor()
                        elif choosedocrecs== "4":
                            break
                        else:
                            print("Invalid Choice")
                            continue
                case 3:
                    while True:
                        chooseviewreports= int(input(f"""
*******VIEWING REPORTS*******
1. View Total Patients Report
2. View Appointments Report
3. View Daily Income Report
4. Return to ADMIN MENU
*****************************
                        what is your choice? (enter number 1-3)"""))
                        if chooseviewreports == "1":
                            totalpatients()
                        elif chooseviewreports == "2":
                            totalappointments()
                        elif chooseviewreports == "3":
                            daily_summary()
                        elif chooseviewreports == "4":
                            break
                        else:
                            print("Invalid Choice")
                            continue
                case 4:
                    while True:
                        choosinggenerate = int(input(f"""
*******GENERATE CLINIC SUMMARY REPORT*******
1. Generate Staff Summary Report
2. Generate Medicine Summary Report
3. Return to ADMIN MENU
********************************************
what is your choice? (enter number 1-2)"""))
                        if choosinggenerate == "1":
                            read_staff()
                        elif choosinggenerate == "2":
                            view() ##view function from pharmacist
                        elif choosinggenerate == "3":
                            break
                        else:
                            print("Invalid Choice")
                            continue
                case 5:
                    while True:
                        med_remove()
                case 6:
                    print("End.")
                    i = False
                    break
                case _: ## Input validation example
                    print("Invalid choice.")
                    continue
    except ValueError:
        print("Please enter a number.")

def update_member(username):
    with open("login/user_db.txt", "r") as file:
        lines = file.readlines()

    updated = False
    with open("login/user_db.txt", "w") as file, open("login/user_db_encrypted.txt", "w") as enc_file:
        for line in lines:
            stored_username, stored_email, stored_password, stored_role = line.strip().split(",")

            if stored_username == username:
                print("\nWhat would you like to update?")
                print("1. Email")
                print("2. Password")
                print("3. Role")
                choice = input("Enter choice (1-3): ")

                if choice == "1":
                    new_email = input("Enter new email: ")
                    # EMAIL CHECKING
                    if "@" not in new_email or "." not in new_email.split("@")[-1]:
                        print("Invalid email format. Update failed.")
                        file.write(line)
                        enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")
                    else:
                        file.write(f"{stored_username},{new_email},{stored_password},{stored_role}\n")
                        enc_file.write(f"{stored_username},{new_email},{encrypt_password(stored_password)},{stored_role}\n")
                        print("Email updated successfully.")

                elif choice == "2":
                    new_password = input("Enter new password: ")
                    # PASSWORD CHECKING
                    if len(new_password) < 8 or not any(char.isdigit() for char in new_password):
                        print("Password must be at least 8 characters and contain a number. Update failed.")
                        file.write(line)
                        enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")
                    else:
                        file.write(f"{stored_username},{stored_email},{new_password},{stored_role}\n")
                        enc_file.write(f"{stored_username},{stored_email},{encrypt_password(new_password)},{stored_role}\n")
                        print("Password updated successfully.")

                elif choice == "3":
                    new_role = input("Enter new role: ")
                    # DOMAIN ROLE CHECKING
                    allowed_roles = ["admin", "user", "staff"]
                    if new_role.lower() not in allowed_roles:
                        print("Invalid role. Must be one of: admin, user, staff. Update failed.")
                        file.write(line)
                        enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")
                    else:
                        file.write(f"{stored_username},{stored_email},{stored_password},{new_role}\n")
                        enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{new_role}\n")
                        print("Role updated successfully.")

                else:
                    print("Invalid choice. No changes made.")
                    file.write(line)
                    enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")

                updated = True
            else:
                file.write(line)
                enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")
    if not updated:
        print("Username not found. No updates made.")
def delete_member(username):
    try:
        with open("login/user_db.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: login/user_db.txt not found.")
        return

    deleted = False
    try:
        with open("login/user_db.txt", "w") as file, open("login/user_db_encrypted.txt", "w") as enc_file:
            for line in lines:
                stored_username, stored_email, stored_password, stored_role = line.strip().split(",")

                if stored_username == username:
                    # Skip writing this line → deletion
                    print(f"User '{stored_username}' deleted successfully.")
                    deleted = True
                else:
                    # Keep other users intact
                    file.write(line)
                    enc_file.write(f"{stored_username},{stored_email},{encrypt_password(stored_password)},{stored_role}\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    if not deleted:
        print("Username not found. No deletion performed.")
def med_remove():
    try:
        count = int(input("How many medicine do you want to remove? "))
        for i in range(0,count):
                while True:
                    barcode = int(input(f"Enter medicine barcode (5 digits): "))
                    # Validation: must be digits and length < 6
                    if len(barcode) == 5:
                        with open("med_remove.txt", "w") as file:
                            file.write(barcode , "\n")
                        print(f"Barcode {barcode} recorded.")
                        break
                    else:
                        print("Invalid barcode. Must be numeric and 5 digits. Try again.")
        print("Final barcode saved to med_remove.txt.")
    except ValueError:
        print("Error: Please enter a valid number for how many medicines to remove.")
    except Exception as e:
        print("Unexpected error:", str(e))
def totalpatients():
    try:
        with open("cashier/patient.txt", "r") as r:
            for line in r:
                print(line.strip())
    except FileNotFoundError:
        print("Error: cashier/patient.txt file not found.")
def totalappointments():
    try:
        with open("cashier/appointments.txt", "r") as r:
            for line in r:
                print(line.strip())
    except FileNotFoundError:
        print("Error: cashier/appointments.txt file not found.")
def read_staff():
    try:
        with open("staff.txt", "r") as file:
            lines = file.readlines()

        total_records = len(lines)
        print(f"Total number of records: {total_records}\n")

        print("--- Staff Records ---")
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 4:
                username, email, password, role = parts
                print(f"Username: {username}, Email: {email}, Password: {password}, Role: {role}")
            else:
                print(f"Invalid record format: {line.strip()}")

    except FileNotFoundError:
        print("Error: hospital_staff.txt file not found.")
def add_doctor():
    doctor_id = input("Enter doctor ID: ").strip()
    doctor_name = input("Enter doctor name: ").strip()

    try:
        with open("doctor/doctor.txt", "a") as file:
            file.write(f"{doctor_id},{doctor_name}\n")
        print("Doctor added successfully.")
    except FileNotFoundError:
        print("Error: doctor.txt file not found.")
def update_doctor():
    doctor_id = input("Enter doctor ID to update: ").strip()
    new_name = input("Enter new doctor name: ").strip()

    try:
        with open("doctor/doctor.txt", "r") as file:
            lines = file.readlines()

        updated = False
        with open("doctor/doctor.txt", "w") as file:
            for line in lines:
                stored_id, stored_name = line.strip().split(",")
                if stored_id == doctor_id:
                    file.write(f"{stored_id},{new_name}\n")
                    updated = True
                    print("Doctor updated successfully.")
                else:
                    file.write(line)

        if not updated:
            print("Doctor ID not found. No updates made.")

    except FileNotFoundError:
        print("Error: doctor.txt file not found.")
def delete_doctor():
    doctor_id = input("Enter doctor ID to delete: ").strip()

    try:
        with open("doctor/doctor.txt", "r") as file:
            lines = file.readlines()

        deleted = False
        with open("doctor/doctor.txt", "w") as file:
            for line in lines:
                stored_id, stored_name = line.strip().split(",")
                if stored_id == doctor_id:
                    deleted = True
                    print(f"Doctor {stored_name} (ID: {stored_id}) deleted successfully.")
                else:
                    file.write(line)

        if not deleted:
            print("Doctor ID not found. No deletion performed.")

    except FileNotFoundError:
        print("Error: doctor.txt file not found.")

menu()

