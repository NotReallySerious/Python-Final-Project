import accountant
from accountant.account__assistant import redo_action

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
    patients = {}
    with open('cashier/patient.txt', 'r') as p:
        lines = p.readlines()
        for line in lines:
            value = line.strip().split(',')
            patient_id = value[0]
            Name = value[1]
            patients[patient_id] = {
                'Name' : Name
            }

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
                    print(f"Patient ID: {details[patient_id]}")
                    print(f"Patient Name: {patients.get(patient_id,{}).get('Name','unknown')}")
            else:
                print(f"No appointments for Doctor. {get_doctor_name(doctor_id)}")
    return records

def record_consultation(doctor_id):
    patient_details = {}
    with open('cashier/patient.txt','r') as patient:
        patients = patient.readlines()
        for person in patients:
            values = person.strip().split(',')
            Patient_Id = values[0]
            Patient_Name = values[1].replace(' ', '_')
            DOB = values[2]
            Address = values[3].replace('','_')
            Contact_num = values[4]
            emergency_num = values[5]

            patient_details[Patient_Id] = {
                'Name' : Patient_Name,
                'DOB' : DOB,
                'Address' : Address,
                'Contact number' : Contact_num,
                'emergency contact number' : emergency_num
            }
    
    appointment_details = {}
    with open('cashier/appointment.txt', 'r') as app:
        lines = app.readlines()
        for line in lines:
            values = line.strip().split(',')
            app_id = values[0]
            date = values[1]
            hour = values[2]
            status = values[3]
            patient_id = values[4]
            doctor_id_in_file = values[5]
            
            if doctor_id == doctor_id_in_file:
                appointment_details[app_id] = {
                    'Date' : date,
                    'Hour' : hour,
                    'Status' : status,
                    'Patient_ID' : patient_id,
                }

    index = 1
    appointment_list = {}
    for app_id in appointment_details:
        patient_id = appointment_details[app_id]['Patient ID']
        patient_name = patient_details.get(patient_id, {}).get('Name','unknown')

        appointment_list[index] = {
            'appointment_id': app_id,
            'appointment_data': appointment_details[app_id],
            'patient_name': patient_name
        }
        print(f"{index}. {patient_id}, {patient_name}")
        index += 1
    
    while True:
        patient_selection = int(input("Enter the index number: "))

        try:
            if patient_selection < 1 or patient_selection > index:
                print('Invalid selection')
                continue
        except ValueError:
            print('invalid value')

        selected_patient = appointment_list[patient_selection]
        patient_id = selected_patient['patient_id']
        patient_name = selected_patient['patient_name'].replace('_', ' ')
        
        print(f"\nRecording consultation for: {patient_name} ({patient_id})")
        print("-" * 50)

        age = int(input("Enter the patient's age: "))
        diagnosis = input('Diagnosis: ')
        
def Doctor_Menu(doctor_id):

    print(f"Hello Dr. get_doctor_name(doctor_id)")
    while True:
        print("~~Doctor Menu~~")
        print("1.View appointments")
        print("2.Record diagnosis and Consultation notes")
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


        
            
            
