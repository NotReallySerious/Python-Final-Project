
def Doctor_Menu(doctor_id):
    while True:
        print("~~Doctor Menu~~")
        print("1. View appointments")
        print("2.Record diasgnosis and Consultation notes")
        print("3.View Consultation Reports")
        print("4.Back to Menu")

        choice = input("Which one do you want to pick")
        if choice == "1":
           view_appointments(doctor_id) 
        elif choice == "2":
            record_consultation(doctor_id)
        elif choice == "3":
            view_consultation_reports(doctor_id)
        elif choice == "4":
            print("Going back to menu....")
            break
        else:
            print("Invalid choice. Please choose the number above")
def view_appointments(doctor_id):
    print("~~ My Appointments ~~")
    found = False

    try:
        file = open("appointments.txt", "r")
        for line in file:
            data = line.strip().split("|")
            if data[2] == doctor_id:
                print(
                    "Appointment ID:", data[0],
                    "| Patient ID:", data[1]
                )
                found = True
        file.close()
        if not found:
            print("No appointments found.")
    except:
        print("Error: Unable to read appointments file.")\

                
 
        
            
            
