'''n = input("Enter name: ")
p = input("Enter pass: ")'''


'''f = open("login.txt","r")
a = open("login.txt","a")'''



'''for line in f:
    if n in line:
        lst = line.strip().split(",")
        if lst[0] == n and lst[1] == p:
            print("Login Successful")
        else:
            print("Login Failed")'''


def view_schedule():
    failsafe = "exit" #Assign a variable so they can exit easily even with random lower/uppercase letters
    while True:
        try: #Error Handling
            #Using with open to close all files automatically after use
            print("\n---Schedule Viewer---\n"
                  "1. View All Schedule\n"
                  "2. View Schedule by Patient Name\n"
                  "3. View Schedule by date\n"
                  "4. View Schedule by Doctor\n"
                  "5. View Schedule by Status\n"
                  "6. View Schedule by ID\n"
                  "7. Exit\n"
                  "Format: ScheduleID, Patient Name, Appointment Date, Doctor Name, Status")
            n = int(input("Enter your choice: "))

            if n not in [1, 2, 3, 4, 5, 6, 7]:
                print("Invalid Choice") #If they insert outside the number range
                continue
            elif n == 7: #To Exit
                print("Exiting")
                break #Breaks the while loop
            else:
                if n == 1:
                    count = 1
                    with open("cashier/schedule.txt", "r") as r:
                        for line in r: #Checks all the lines
                            print(count,line.strip()) #Prints all the lines without white space
                            count += 1 #To display line number while printing
                elif n == 2:
                    while True:
                        count = 1
                        with open("schedule.txt", "r") as r:
                            name = input("\nEnter Patient Name or Exit: ") #Insert Patient Name
                            found = False
                            if name.lower() == failsafe.lower(): # Exit if not capitalize properly
                                print("Exiting")
                                break
                            else:
                                for line in r: #Checks all the lines
                                    lst = line.strip().split(",") #Print line without white space and split the lines into lst[0] = name and lst [1] = date
                                    if name.lower().strip() == lst[1].lower().strip(): #Search for an exact match for the patient name while avoiding case sensitivity
                                        print(count,line.strip()) #Prints the lines that matches without white space
                                        found = True
                                        count += 1 #To display line number while printing
                                if found is False: #Only runs if none of the lines contain the name
                                    print("No Schedule")
                elif n == 3:
                    while True:
                        count = 1
                        with open("schedule.txt", "r") as r:
                            date = input("\nEnter Exact Date or Exit: ") #Insert date
                            found = False
                            if date.lower() == failsafe.lower():  # Exit if not capitalize properly
                                print("Exiting")
                                break
                            else:
                                for line in r:
                                    lst = line.strip().split(",")
                                    if lst[2] == date: #To make sure only the specific date is shown
                                        print(count,line.strip())
                                        found = True
                                        count += 1
                                        continue
                                if found is False:
                                    print("No Schedule")
                elif n == 4:
                    while True:
                        with open("schedule.txt", "r") as r:
                            count = 1
                            doctor = input("\nEnter Doctor Name or Exit: ")
                            found = False
                            if doctor.lower() == failsafe.lower(): # Exit if not capitalize properly
                                print("Exiting")
                                break
                            else:
                                for line in r:
                                    lst = line.strip().split(",")
                                    if lst[3].lower() == doctor.lower():
                                        print(count,line.strip())
                                        found = True
                                        count += 1
                                        continue
                                if found is False:
                                    print("No Schedule")
                elif n == 5:

                    while True: #To make it so if they put an invalid input, they will still be on the "Status" menu
                        count = 1
                        print("\nSelect Status\n"
                              "1. Pending\n"
                              "2. Done")
                        status = input("Enter Status or Exit: ")
                        found = False
                        if status.lower() == failsafe.lower(): # Exit if not capitalize properly
                            print("Exiting")
                            break
                        elif status == "2":
                            status = "Done"
                        elif status == "1":
                            status = "Pending"
                        else:
                            print("Invalid Choice")
                            continue

                        with open("schedule.txt", "r") as r:
                            for line in r:
                                lst = line.strip().split(",")
                                if lst[4].lower() == status.lower():
                                    print(count, line.strip())
                                    count += 1
                                    found = True
                        if found is False :
                            print("No Schedule")

                elif n == 6:
                    while True:
                        count = 1
                        with open("schedule.txt", "r") as r:
                            name = input("\nEnter ScheduleID or Exit: ")  # Insert Patient Name
                            found = False
                            if name.lower() == failsafe.lower():  # Exit if not capitalize properly
                                print("Exiting")
                                break
                            else:
                                for line in r:  # Checks all the lines
                                    lst = line.strip().split(
                                        ",")  # Print line without white space and split the lines into lst[0] = name and lst [1] = date
                                    if name.lower().strip() == lst[
                                        0].lower().strip():  # Search for an exact match for the patient name while avoiding case sensitivity
                                        print(count, line.strip())  # Prints the lines that matches without white space
                                        found = True
                                        count += 1  # To display line number while printing
                                if found is False:  # Only runs if none of the lines contain the name
                                    print("No Schedule")


        except ValueError: #If they don't insert an intiger
            print("\nInvalid Choice")
        except FileNotFoundError:
            print("\nNo such file or directory")
        except KeyboardInterrupt:
            print("\nExiting")
            break

view_schedule()
def view_patient():
        failsafe = "exit" #To make sure people can exit menus
        while True:
            try:
                print("---Patient Data Viewer---\n"
                      "1. View All Patients\n"
                      "2. View Patient by Name\n"
                      "3. View Patient by Age\n"
                      "4. View Patient by Address\n"
                      "5. View Patient by PatientID\n"
                      "6. Exit\n"
                      "Format: PatientID, Name, Age, Address\n")

                n = int(input("Enter your choice: "))
                if n == 1:
                    with open("cashier/patient.txt", "r") as r:
                        for line in r:
                            print(line.strip())
            except ValueError:
                print("\nInvalid Choice")

        #Make a patient ID
        #Dont forget to capitalize
        #def delete()
            #Make a pending schedule file and a done schedule file
            #Copy both in seperate files
            #Delete after X amount of years
            #make it so u can change status, name, etc
            #Put output in a file so they can edit based on output

view_patient()