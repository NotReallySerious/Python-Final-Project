def get_doctor_name(doctor_id):
    with open('doctor/Doctor.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split(',')
            doctor_id_in_file = values[0]
            Name = values[1].replace('_',' ')

            if doctor_id == doctor_id_in_file:
                print(Name)
            else:
                print('Doctor ID unidentifyable')

def view_appointments(doctor_id):
    records = {}
    with open('cashier/appointment.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.strip().split(',')
            app_id = values[0]
            date = values[1]
            hour = values[2]
            status = values[3]
            patient_id = values[4]
            doctor_id_in_file = values[5]
        
            if doctor_id_in_file == doctor_id:
                records[app_id] = {
                    'date': date,
                    'hour': hour,
                    'status': status,
                    'patient_id': patient_id,
                    'doctor_id': doctor_id_in_file
                }
                
            if records:
                print(f"Appointments for Dr. {get_doctor_name(doctor_id)}")
                for app_id, details in records.items():
                    print(f"Appointment ID: {app_id}")
                    print(f"Date: {details[date]}")
                    print(f"")
                

        
def Doctor_Menu(doctor_id):
    print(f"Hello Dr. get_doctor_name(doctor_id)")
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


        
            
            
