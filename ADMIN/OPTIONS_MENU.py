def menu():
    while True:
        print('*' * 30)
        print("Welcome to ADMIN MENU")
        print('*' * 30)
        print("Manage Clinic Users")
        print('1. Add Clinic Users')
        print('2. Update Clinic Users')
        print('3. Delete Clinic Users')
        print("")
        print("Manage Doctor Records")
        print('4. Add Doctor Records')
        print('5. Update Doctor Records')
        print('6. Delete Doctor Records')
        print("")
        print("Reports")
        print('7. Update Medicine Deletion Records')
        print('8. Change Password')
        print('9. Update Profile')
        print("")
        print('10. Exit')
        print('*' * 30)
        choice = int(input("What is your choice?"))
        match choice:
            case 1:
                Add_Users()
            case 2:
                UpdateUsers()
            case 3:
                DeleteUsers()
            case 4:
                RegisterRecords()
            case 5:
                UpdateRecords()
            case 6:
                DeleteRecords()
            case 7:
                MedicineDeletion()
            case 8:
                Password()
            case 9:
                Profile()
            case 10:
                print("End.")
                break
            case _: ## Input validation example
                print("Invalid choice.")
                return
def Add_Users():
    try:
        num = int(input("Enter how many clinic user(s) to add"))
        for i in range(num, num+1):
            name = input(f"Enter the full name of user no.{i}")
            role = input(f"Enter the clinic role (Admin/Receptionist/Doctor/Pharmacist/Accounts) of user no.{i}")
            username = input(f"Enter the username of user no.{i}")
            password = input(f"Enter password of user no.{i}")
            phone = input(f"Enter the phone of user no.{i}")
            email = input(f"Enter the email of user no.{i}")
            userID = input(f"Enter the id of user no.{i}")
            with open("users.txt", "a") as f:
                f.write(f"{userID},{name},{username},{password},{phone},{email}\n")
                print("User(s) added successfully.")
    except ValueError:
        print("Please enter a number.")
        return
def UpdateUsers():
    user_id = input("Enter the User ID to update: ")

    try:
        # Step 1: Read all records
        with open("users.txt", "r") as file:
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
        with open("users.txt", "w") as file:
            file.writelines(updated_lines)

        if found:
            print(f"User {user_id} updated successfully.")
        else:
            print(f"Error: User ID {user_id} not found.")

    except FileNotFoundError:
        print("Error: users.txt file not found.")
    except Exception as e:
        print("Error while updating user:", str(e))
def DeleteUsers():
    def DeleteUsers():
        user_id = input("Enter the User ID to delete: ")

        try:
            # Step 1: Read all records
            with open("users.txt", "r") as file:
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
            with open("users.txt", "w") as file:
                file.writelines(updated_lines)

            if found:
                print(f"User {user_id} deleted successfully.")
            else:
                print(f"Error: User ID {user_id} not found.")

        except FileNotFoundError:
            print("Error: users.txt file not found.")
        except Exception as e:
            print("Error while deleting user:", str(e))





