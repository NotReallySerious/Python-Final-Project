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
What is your choice? (enter number 1-5)"""))
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
what is your choice? (enter a number 1-3)"""))
                        if chooseusers== "1":
                            ##register()
                        elif chooseusers == "2":
                            UpdateUsers()
                        elif chooseusers == "3":
                            DeleteUsers()
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
                            ##add function here
                        elif choosedocrecs== "2":
                            ##add function
                        elif choosedocrecs== "3":
                            ##add function
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
3. View Income Report
4. Return to ADMIN MENU
*****************************
                        what is your choice? (enter number 1-3)"""))
                        if chooseviewreports == "1":
                            ##function to view
                        elif chooseviewreports == "2":
                            ##function to view
                        elif chooseviewreports == "3":
                            ##function to view
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
                            ##function to view
                        elif choosinggenerate == "2":
                            ##function to view
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

def UpdateUsers():
    user_id = input("Enter the User ID to update: ")
    try:
        # Step 1: Read all records
        with open("user_db.txt", "r") as file:
            lines = file.readlines()

        updated_lines = []
        found = False

        # Step 2: Search for the user
        for line in lines:
            fields = line.strip().split("|")
            existing_id = fields[0]

            if existing_id == user_id:
                found = True
                print("\nCurrent Record:")
                print(line.strip())

                # Step 3: Show update menu
                print("\nWhich fields do you want to update?")
                print("Options: UserID, Name, Username, Password, Phone, Email")
                print("Separate multiple choices with commas (e.g., Name,Phone,Email)")

                choices = input("Enter fields to update: ").replace(" ", "").split(",")

                # Step 4: Apply updates for each chosen field
                for choice in choices:
                    if choice.lower() == "userid":
                        fields[0] = input("Enter new User ID: ")
                    elif choice.lower() == "name":
                        fields[1] = input("Enter new name: ")
                    elif choice.lower() == "username":
                        fields[3] = input("Enter new username: ")
                    elif choice.lower() == "password":
                        fields[4] = input("Enter new password: ")
                    elif choice.lower() == "phone":
                        fields[5] = input("Enter new phone: ")
                    elif choice.lower() == "email":
                        fields[6] = input("Enter new email: ")
                    else:
                        print(f"Invalid choice: {choice}. Skipped.")

                # Step 5: Rebuild updated line
                new_line = "|".join(fields) + "\n"
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)

        # Step 6: Rewrite file
        with open("user_db.txt", "w") as file:
            file.writelines(updated_lines)

        if found:
            print(f"User {user_id} updated successfully.")
        else:
            print(f"Error: User ID {user_id} not found.")

    except FileNotFoundError:
        print("Error: user_db.txt file not found.")
    except Exception as e:
        print("Error while updating user:", str(e))
def DeleteUsers():
    def DeleteUsers():
        user_id = input("Enter the User ID to delete: ")

        try:
            # Step 1: Read all records
            with open("user_db.txt", "r") as file:
                lines = file.readlines()

            updated_lines = []
            found = False

            # Step 2: Search for the user
            for line in lines:
                fields = line.strip().split("|")
                existing_id = fields[0]

                if existing_id == user_id:
                    found = True
                    print("Deleting record:", line.strip())
                    # Skip adding this line to updated_lines (effectively deleting it)
                else:
                    updated_lines.append(line)

            # Step 3: Rewrite file without the deleted record
            with open("user_db.txt", "w") as file:
                file.writelines(updated_lines)

            if found:
                print(f"User {user_id} deleted successfully.")
            else:
                print(f"Error: User ID {user_id} not found.")

        except FileNotFoundError:
            print("Error: user_db.txt file not found.")
        except Exception as e:
            print("Error while deleting user:", str(e))
def med_remove():
    try:
        count = int(input("How many medicine do you want to remove? "))
        for i in range(0,count):
                while True:
                    barcode = int(input(f"Enter medicine barcode (less than 6 digits): "))
                    # Validation: must be digits and length < 6
                    if len(barcode) < 6:
                        with open("med_remove.txt", "w") as file:
                            file.write(barcode + "\n")
                        print(f"Barcode {barcode} recorded (replaced previous).")
                        break
                    else:
                        print("Invalid barcode. Must be numeric and less than 6 digits. Try again.")
        print("Final barcode saved to med_remove.txt.")
    except ValueError:
        print("Error: Please enter a valid number for how many medicines to remove.")
    except Exception as e:
        print("Unexpected error:", str(e))




