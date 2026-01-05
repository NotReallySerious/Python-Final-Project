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






