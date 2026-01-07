def load_appointment():
    try:
        with open("appointment.txt", "r") as a:
            a_lines = a.readlines()
            return a_lines
    except FileNotFoundError:
        print("\nNo such file or directory")

def load_patient():
    try:
        with open("patient.txt", "r") as p:
            p_lines = p.readlines()
            return p_lines
    except FileNotFoundError:
        print("\nNo such file or directory")

def view_appointment():
    # This function handles all appointment viewing related features
    while True:
        try: #Error Handling
            #Using with open to close all files automatically after use
            a_lines = load_appointment()
            print("\n---Appointment Viewer---\n"
                  "1. View All Appointment\n"
                  "2. View Appointment by Patient ID\n"
                  "3. View Appointment by Date\n"
                  "4. View Appointment by Doctor ID\n"
                  "5. View Appointment by Status\n"
                  "6. View Appointment by Appointment ID\n"
                  "7. Exit\n"
                  "Format: Appointment ID, Appointment Date, Appointment Time, Status, Patient ID, Doctor ID\n")
            n = int(input("Enter your choice: "))
        except ValueError:  # If they don't insert an intiger
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        if n not in [1, 2, 3, 4, 5, 6, 7]:
            print("Invalid Choice") #If they insert outside the number range
            continue
        elif n == 7: #To Exit
            print("Exiting")
            break #Breaks the while loop
        else:
            if n == 1:
                count = 1
                with open("../cashier/appointment.txt", "r") as f:
                    a_lines = f.readlines()
                for line in a_lines: #Checks all the lines
                    print(count,line.strip()) #Prints all the lines without white space
                    count += 1 #To display line number while printing
            elif n in [2, 3, 4, 6]:
                if n == 2:
                    place = 4
                    menu = "Patient ID"
                elif n == 3:
                    place = 1
                    menu = "Exact Date (day-month-year)"
                elif n == 4:
                    place = 5
                    menu = "Doctor ID"
                elif n == 6:
                    place = 0
                    menu = "Appointment ID"
                else:
                    continue
                while True:
                    count = 1
                    found = False
                    sort_by = input(f"\nEnter {menu} or exit: ")
                    if sort_by.lower() == "exit":
                        print("\nExiting")
                        break
                    else:
                        for line in a_lines:
                            lst = line.strip().split(",")
                            if lst[place].lower() == sort_by.lower():
                                print(count,line.strip())
                                count += 1
                                found = True
                    if found == False:
                        print("No Records Found")
            elif n == 5:
                while True: #To make it so if they put an invalid input, they will still be on the "Status" menu
                    count = 1 #to number all line outputed
                    print("\nSelect Status\n"
                          "1. Pending\n"
                          "2. Done")
                    status = input("Enter Status or Exit: ")
                    found = False
                    if status.lower().strip() == "exit": # Exit if not capitalize properly
                        print("Exiting")
                        break
                    elif status.strip() == "2":
                        status = "Done"
                    elif status.strip() == "1":
                        status = "Pending"
                    else:
                        print("Invalid Choice")
                        continue
                    for line in a_lines:
                        lst = line.strip().split(",")
                        if lst[3].lower() == status.lower():
                            print(count, line.strip())
                            count += 1
                            found = True
                    if found is False :
                        print("No Appointment")



def view_patient():
# This function handles all patient viewing related features
    while True:
        try:
            p_lines = load_patient()
            print("\n---Patient Data Viewer---\n"
                  "1. View All Patients\n"
                  "2. View Patient by Name\n"
                  "3. View Patient by Sex\n"
                  "4. View Patient by Birth Year\n"
                  "5. View Patient by Address\n"
                  "6. View Patient by PatientID\n"
                  "7. Exit\n"
                  "Format: PatientID, Name, Sex, DOB, Address, Contact Number, Emergency Contact Number\n")

            n = int(input("Enter your choice: "))
        except ValueError:  # If they don't insert an intiger
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        if n not in [1, 2, 3, 4, 5, 6, 7]:
            print("Invalid Choice")  # If they insert outside the number range
            continue
        elif n == 7:
            print("\nExiting")
            break
        elif n == 1:
            count = 1 #to number all line outputed
            for line in p_lines:
                print(count,line.strip())
                count += 1
        elif n in [2, 5, 6]:
            if n == 2:
                place = 1
                menu = "Patient Name"
            elif n == 5:
                place = 4
                menu = "Address"
            elif n == 6:
                place = 0
                menu = "Patient ID"
            else:
                continue
            while True:
                count = 1
                found = False
                sort_by = input(f"\nEnter {menu} or exit: ")
                if sort_by.lower() == "exit":
                    print("\nExiting")
                    break
                else:
                    for line in p_lines:
                        lst = line.strip().split(",")
                        if lst[place].lower() == sort_by.lower():
                            print(count, line.strip())
                            count += 1
                            found = True
                    if found == False:
                        print("No Records Found")
        elif n == 3:
            while True:  # To make it so if they put an invalid input, they will still be on the "Status" menu
                count = 1  # to number all line outputed
                print("\nSelect Sex\n"
                      "1. Male\n"
                      "2. Female")
                sex = input("Enter Sex or Exit: ")
                found = False
                if sex.lower() == "exit":  # Exit if not capitalize properly
                    print("\nExiting")
                    break
                elif sex.strip() == "2":
                    sex = "F"
                elif sex.strip() == "1":
                    sex = "M"
                else:
                    print("\nInvalid Choice")
                    continue

                for line in p_lines:
                    lst = line.strip().split(",")
                    if lst[2].lower() == sex.lower():
                        print(count, line.strip())
                        count += 1
                        found = True
                if found is False:
                    print("\nNo Records Found")
        elif n == 4:
            while True:
                try:
                    found = False
                    count = 1
                    year = int(input("\nEnter Patient Birth Year or insert 0 to Exit: "))
                    if year == 0:
                        print("Exiting")
                        break
                    else:
                        year = str(year)
                        for line in p_lines:
                            lst = line.strip().split(",")
                            if year in lst[3]:
                                print(count,line.strip())
                                found = True
                                count += 1  # To display line number while printing
                    if found is False:
                        print("\nNo patient record found")
                except ValueError: #If they dont insert an valid year
                    print("\nInvalid Year")

def alter_patient():
# This function handles all patient-related operations via menu options
    while True:
        try:
            p_lines = load_patient()
            print("\n---Patient Data Alterator---\n"
                  "1. View All Patients\n"
                  "2. Add Patient\n"
                  "3. Alter Patient Details\n"
                  "4. Exit\n"
                  "Format: PatientID, Name, Sex, DOB, Address, Contact Number, Emergency Contact Number\n")
            n = int(input("Enter your choice: "))
        except ValueError:
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        if n not in [1, 2, 3, 4]: #To handle if they put outside of range
            print("\nInvalid Choice")
            continue
        elif n == 4:
            print("\nExiting")
            break
        elif n == 1:
            count = 1
            for line in p_lines:
                print(count,line.strip())
                count += 1
        elif n == 2:
            add_patient()
        elif n == 3:
            alter_patient_details()


def alter_patient_details():
    while True:
        p_lines = load_patient()  # to put the new data inserted into the list
        found = False
        # -------- ALTER PATIENTS DETAILS --------
        print("\n1. Alter Name\n"
              "2. Alter Contact Number\n"
              "3. Alter Emergency Contact Number\n"
              "4. Alter Address\n"
              "5. Exit\n")
        choice = input("\nEnter your choice: ")
        if choice.strip() not in ["1", "2", "3", "4", "5"]:
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        elif choice.strip() == "5":
            print("\nExiting")
            break
        # The "place" represents the respective indexes of the data in the file
        elif choice.strip() == "1":
            place = 1
            menu = "Patient Name"
        elif choice.strip() == "2":
            place = 5
            menu = "Contact Number"
        elif choice.strip() == "3":
            place = 6
            menu = "Emergency Contact Number"
        elif choice.strip() == "4":
            place = 4
            menu = "Address"
        else:
            continue
        p_id = input("\nEnter Patient ID: ")
        new_value = input(f"\nEnter new {menu}: ")
        if choice.strip() in ["2", "3"] and not new_value.isdigit():
            print("\nPlease Insert a Contact Number.")
            continue
        with open("patient.txt", "w") as w:
            for line in p_lines:
                lst = line.strip().split(",")
                if lst[0].lower() != p_id.lower():
                    w.write(line)
                elif lst[0].lower() == p_id.lower():
                    if choice.strip() in ["2", "3"]:
                        lst[place] = new_value  # Does not title numbers
                    else:
                        lst[place] = new_value.title()
                    w.write(f"{lst[0]},{lst[1]},{lst[2]},{lst[3]},{lst[4]},{lst[5]},{lst[6]}\n")
                    found = True
        if found == False:
            print("\nNo Records Found")
        elif found == True:
            print("\nPatient Record Updated")

def add_patient():
    while True:
        p_lines = load_patient()  # to put the new data inserted into the list
        try:
            i = int(input("\nHow Many Patients do you want to add or 0 to exit: "))
        except ValueError:
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        if i == 0:
            print("\nExiting")
            break
        elif i > 0:
            for i in range(int(i)):
                # -------- INSERTING ALL THE NESCESARRY DATA --------
                while True:
                    p_id = input("\nEnter Patient ID: ")
                    exist = False
                    for line in p_lines:
                        lst = line.strip().split(",")
                        if p_id.lower() == lst[0].lower():  # Check if there is already a patient with said ID
                            print("Patient ID already exists")
                            exist = True
                    if exist is False:
                        break
                name = input("\nEnter Patient Name: ")
                while True:
                    sex = input("\nEnter Patient Sex (M or F): ")
                    if sex.upper().strip() not in ["M", "F"]:
                        print("\nInvalid Choice")
                    else:
                        break
                DOB = input("\nEnter Patient DOB (day-month-year): ")
                address = input("\nEnter Patient Address: ")
                while True:  # To ensure that if they put the wrong data, they will be prompted the same contact number prompt
                    try:
                        C_No = int(input("\nEnter Patient Contact Number: "))
                        break
                    except ValueError:
                        print("\nPlease Enter a Valid Contact Number")

                while True:  # To ensure that if they put the wrong data, they will be prompted the same contact number prompt
                    try:
                        E_No = int(input("\nEnter Patient Emergency Contact Number: "))
                        break
                    except ValueError:
                        print("\nPlease Enter a Valid Contact Number")
                with open("patient.txt", "a") as a:
                    a.write(f"{p_id.title()},{name.title()},{sex},{DOB},{address.title()},{C_No},{E_No}\n")

def alter_appointment():
# This function handles all appointment-related operations via menu options
    while True:
        try:
            a_lines = load_appointment()
            print("\n---Appointment Alterator---\n"
                  "1. View All Appointments\n"
                  "2. Add Appointments\n"
                  "3. Delete Appointments\n"
                  "4. Alter Appointment Details\n"
                  "5. Exit\n"
                  "Format: Appointment ID, Appointment Date, Appointment Time, Status, Patient ID, Doctor ID\n")
            n = int(input("Enter your choice: "))
        except ValueError:
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        if n not in [1, 2, 3, 4, 5]: #To handle if they put outside of range
            print("\nInvalid Choice")
            continue
        elif n == 5:
            print("\nExiting")
            break
        elif n == 1:
            count = 1
            for line in a_lines:
                print(count,line.strip())
                count += 1
        elif n == 2:
            add_appointment()
        elif n == 3:
            delete_appointment()
        elif n == 4:
            alter_appointment_details()



def add_appointment():
    try:
        while True:
            a_lines = load_appointment() #to put the new data inserted into the list
            try:
                i = int(input("\nHow Many Appointments do you want to add or 0 to exit: "))
            except ValueError:
                print("\nInvalid Choice, Enter a Valid Number")
                continue
            if i == 0:
                print("\nExiting")
                break
            elif i > 0:
                # -------- INSERTING ALL THE NESCESARRY DATA --------
                for i in range(int(i)):
                    while True:
                        a_id = input("\nEnter Appointment ID: ")
                        exist = False
                        for line in a_lines:
                            lst = line.strip().split(",")
                            if a_id.lower() == lst[0].lower():  # Check if there is already an appointment with said ID
                                print("Appointment ID already exists, Please enter a new ID")
                                exist = True
                        if exist == False:
                            break
                    while True:
                        p_id = input("\nEnter Patient ID: ")
                        exist = False
                        with open("patient.txt", "r") as p_r:
                            for line in p_r:
                                lst = line.strip().split(",")
                                if p_id.lower() == lst[0].lower():  # Check if the Patient ID exist
                                    exist = True
                            if exist == True:
                                break
                            else:
                                print("Patient ID not found. Please enter a valid Patient ID.")
                    date = input("\nEnter Appointment Date (day-month-year): ")
                    time = input("\nEnter Time (24 hour format): ")
                    while True:
                        d_id = input("\nEnter Doctor ID: ")
                        exist = False
                        with open("../doctor/doctor.txt", "r") as d_r:
                            for line in d_r:
                                lst = line.strip().split(",")
                                if d_id.lower() == lst[0].lower():  # Check if the Doctor ID exist
                                    exist = True
                        if exist == True:
                            break
                        else:
                            print("Doctor ID not found. Please enter a valid Doctor ID.")
                    with open("appointment.txt", "a") as a:
                        a.write(f"{a_id.title()},{date},{time},Pending,{p_id.title()},{d_id.title()}\n")
    except FileNotFoundError:
        print("\nNo Files Found")

def delete_appointment():
    while True:
        a_lines = load_appointment()  # to put the new data inserted into the list
        # -------- DELETE APPOINTMENT --------
        print("\n1. Delete by Line\n"
              "2. Delete by Patient ID\n"
              "3. Delete by Doctor ID\n"
              "4. Delete by Appointment ID\n"
              "5. Delete by Status\n"
              "6. Delete All Lines\n"
              "7. Exit\n")
        choice = input("\nEnter your choice: ")
        if choice.strip() not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("\nInvalid Choice")
        elif choice.strip() == "7":
            print("\nExiting")
            break
        elif choice.strip() == "1":
            delete_appointment_by_line()
        elif choice.strip() == "4":
           delete_appointment_by_A_ID()
        # The "place" represents the respective indexes of the data in the file
        elif choice.strip() in ["2", "3", "5"]:
            if choice.strip() == "2":
                menu = "Patient ID"
                place = 4
            elif choice.strip() == "3":
                menu = "Doctor ID"
                place = 5
            elif choice.strip() == "5":
                menu = "Status (Done or Pending)"
                place = 3
            else:
                continue
            delete_appointment_by_field(place, menu)

        elif choice.strip() == "6":
            delete_all_appointments()

def delete_all_appointments():
    while True:
        confirm = input("\nAre you sure you want to delete all lines? (y/n): ")
        if confirm.lower() != "y":
            break
        elif confirm.lower() == "y":
            with open("appointment.txt", "w") as w:
                w.writelines("")
                print("\nDeleted successfully")


def delete_appointment_by_line():
    while True:
        a_lines = load_appointment()  # to put the new data inserted into the list
        count = 1
        for line in a_lines:
            print(count, line.strip())
            count += 1
        try:
            done = False
            to_delete = int(input("\nEnter line number to delete or enter 0 to exit: "))
            if to_delete == 0:
                break
            elif to_delete > len(a_lines) or to_delete <= 0:
                print("\nPlease enter a valid line number")
            else:
                confirmation = input("Are you sure you want to delete this line? (y/n): ")
                if confirmation.lower() != "y":
                    print("\nOperation cancelled")
                    break
                elif confirmation.lower() == "y":
                    print("\nDeleted successfully")
                    with open("appointment.txt", "w") as w:
                        for line in a_lines:
                            if line != a_lines[to_delete - 1]:
                                w.write(line)
                                done = True
            if done == True:
                break
        except ValueError:
            print("\nInvalid Data Type")

def delete_appointment_by_A_ID():
    while True:
        a_lines = load_appointment()  # to put the new data inserted into the list
        found = False
        count = 1
        id = input("\nEnter Appointment ID or exit: ")
        if id.lower() == "exit":
            print("\nExiting")
            break
        else:
            for line in a_lines:
                lst = line.strip().split(",")
                if id.lower() == lst[0].lower():
                    print(count, line.strip())
                    count += 1
                    found = True
            if found is True:
                confirm = input("\nDo you want to delete this line? (y/n): ")
                if confirm.lower().strip() != "y":
                    print("\nOperation cancelled")
                    break
                elif confirm.lower().strip() == "y":
                    print("\nDeleted successfully")
                    with open("appointment.txt", "w") as w:
                        for line in a_lines:
                            lst = line.strip().split(",")
                            if id.lower() != lst[0].lower():
                                w.write(line)
            if found is False:
                print("\nNo Records Found")

def delete_appointment_by_field(place, menu):
    while True:
        a_lines = load_appointment()  # to put the new data inserted into the list
        count = 1  # to number all line outputed
        found = False
        temp_list = []
        actual_list = []
        new_value = input(f"\nEnter {menu} or Exit: ")
        if new_value.lower() == "exit":  # to make it easier to exit the menu
            print("\nExiting")
            break
        else:
            for line in a_lines:
                lst = line.strip().split(",")
                if new_value.lower() == lst[
                    place].lower():  # find only exact match + to make capitalisation not matter for accesability
                    print(count, line.strip())
                    found = True
                    count += 1  # To display line number while printing
                    temp_list.append(f"{line}")  # append each record to an empty list for easy access

            if found == True:
                print("\n1. Delete by Line\n"
                      "2. Delete All\n"
                      "3. Exit\n")
                mode = input("\nChoose what mode to use: ")
                if mode.strip() not in ["1", "2", "3"]:
                    print("\nInvalid Choice")
                elif mode.strip() == "3":
                    print("\nExiting")
                    break
                elif mode.strip() == "2":
                    confirm = input("\nAre you sure you want to delete this line(s)? (y/n): ")
                    if confirm.lower() != "y":
                        print("\nOperation cancelled")
                    elif confirm.lower() == "y":
                        print("\nLine(s) Deleted successfully")
                        for line in a_lines:
                            if line not in temp_list:
                                actual_list.append(line)  # To write down all the wanted records in a list
                    with open("appointment.txt", "w") as w:
                        w.writelines(
                            actual_list)  # write the list containing the wanted lines to the actual file
                elif mode.strip() == "1":
                    try:
                        delete = int(input("\nwhat line to delete or insert 0 to Exit: "))  # to prompt user what line to delete base on the output given
                    except ValueError:
                        print("\nInvalid Data Type")
                        continue
                    if delete == 0:
                        print("\nExiting")
                        break
                    elif delete <= len(temp_list) and delete >= 1:  # to ensure they can only input number not larger than the available lines
                        confirmation = input("\nAre you sure you want to delete this line? (y/n): ")
                        if confirmation.lower() == "y":
                            for line in a_lines:
                                if line != temp_list[delete - 1]:
                                    actual_list.append(line)  # Write the lines that don't want to be deleted into a list
                            with open("appointment.txt", "w") as w:
                                w.writelines(
                                    actual_list)  # write the list containing the wanted lines to the actual file
                                print("\nDeleted successfully")
                        elif confirmation.lower() != "y":
                            print("\nOperation cancelled")
                    elif delete not in range(
                            len(temp_list) + 1):  # If they insert a number bigger than the available line number
                        print("\nPlease enter a valid line number")
            if found is False:
                print("No record found")

def alter_appointment_details():
    while True:
        a_lines = load_appointment()  # to put the new data inserted into the list
        found = False
        # -------- ALTER APPOINTMENT DETAILS --------
        print("\n1. Alter Doctor ID\n"  # No alter Patient ID because if is the patient change, its technically a new appointment
            "2. Alter Time\n"
            "3. Alter Date\n"
            "4. Alter Status\n"
            "5. Exit\n")
        choice = input("\nEnter your choice: ")
        if choice.strip() not in ["1", "2", "3", "4", "5"]:
            print("\nInvalid Choice, Enter a Valid Number")
            continue
        elif choice.strip() == "5":
            print("\nExiting")
            break
        # The "place" represents the respective indexes of the data in the file
        elif choice.strip() == "2":
            place = 2
            menu = "Time"
        elif choice.strip() == "3":
            place = 1
            menu = "Date"
        elif choice.strip() == "4":
            place = 3
            menu = "Status"
        elif choice.strip() == "1":
            place = 5
            menu = "Doctor ID"
        else:
            continue
        a_id = input("\nEnter Appointment ID: ")
        new_value = input(f"\nEnter new {menu}: ")
        with open("appointment.txt", "w") as w:
            for line in a_lines:
                lst = line.strip().split(",")
                if lst[0].lower() != a_id.lower():
                    w.write(line)
                elif lst[0].lower() == a_id.lower():
                    lst[place] = new_value.title()
                    w.write(f"{lst[0]},{lst[1]},{lst[2]},{lst[3]},{lst[4]},{lst[5]}\n")
                    found = True
        if found == False:
            print("\nNo Records Found")
        elif found == True:
            print("\nAppointment Updated")


def receptionist_main():
    while True:
        try:
            print("\n---Welcome to Receptionist---\n"
                  "1. View Patient Records\n"
                  "2. View Appointment Records\n"
                  "3. Alter Patient Records\n"
                  "4. Alter Appointment Records\n"
                  "5. Exit\n")
            mode = int(input("\nChoose what mode to use: "))
            if mode not in [1, 2, 3, 4, 5]:
                print("\nInvalid Choice, Enter a Mode")
            elif mode == 5:
                print("\nExiting")
                break
            elif mode == 4:
                alter_appointment()
            elif mode == 3:
                alter_patient()
            elif mode == 2:
                view_appointment()
            elif mode == 1:
                view_patient()
        except ValueError:
            print("\nInvalid Choice, Enter a Valid Number")
        except KeyboardInterrupt:
            print("\nExiting")

