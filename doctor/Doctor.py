from accountant import account__assistant


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
    all_app = []
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
            
            all_app.append({
                'app_id': app_id,
                'date': date,
                'hour': hour,
                'status': status,
                'patient_id': patient_id,
                'doctor_id': doctor_id_in_file
            })

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
        selected_app_id = selected_patient['appointment_id']
        print(f"\nRecording consultation for: {patient_name} ({patient_id})")
        print("-" * 50)
        
        while True:
            try:
                age = int(input("Enter patient's age: "))
                if age < 0:
                    print("Age cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for age!")
        
        while True:
                diagnosis = input('Diagnosis: ').strip
                if not diagnosis:
                    print("Diagnosis Can't be empty.")
                    continue
                break
        
        while True:
            print("Enter medications for your patient (separate with ; for multiple medicines)\n")
            meds = input("Enter medicine(s): ").strip()
            if not meds:
                print("Medications can't be empty.")
                continue
            break

        while True:
            print("Enter the quantity of the medicine(s),(separate with ; for multiple medicines)\n")
            qty = input("Enter quantity: ")
            if not qty:
                print("Quantity can't be empty or negative. Please enter at least 1")
                continue
            break
    
        while True:
            print("Give advice(s) to your patient (separate by ; for multiple advices)\n")
            advice = input("Enter the advices: ").strip()
            if not advice:
                print("Seriously, no advice? give your patient some advice.")
                continue
            break
        while True:
            med_count = len(meds.split(';'))
            qty_count = len(qty.split(';'))
            
            if med_count != qty_count:
                print(f"Warning: You entered {med_count} medication(s) but {qty_count} quantity(ies).")
                confirm = input("Do you want to continue anyway? (yes/no): ").lower()
                if confirm == 'yes' or confirm == 'y':
                    break
                else:
                    continue
            break

        record = f"'{patient_id}','{patient_name}',{age},'{diagnosis}','{meds}','{qty}','{advice}'"

        try:
            with open('doctor/patient_record_db.txt', 'a') as rec:
                rec.write(record)
                print("File saved successfully")
        except Exception:
            print(f"Error writing the file: {Exception}")

        try:
            for appointment in all_app:
                if appointment['app_id'] == selected_app_id:
                    appointment['status'] = 'Completed'
            
            # Write all appointments back to file
            with open('cashier/appointment.txt', 'w') as app_file:
                for appointment in all_app:
                    line = f"{appointment['app_id']},{appointment['date']},{appointment['hour']},{appointment['status']},{appointment['patient_id']},{appointment['doctor_id']}\n"
                    app_file.write(line)
            
            print("Appointment status updated to 'Completed'!")
        except Exception as e:
            print(f"Error updating appointment status: {e}")
        
        # Sending the medicine prescription to the pharmacist in form of patient_id,token_no,barcode,qty of med
        token = 1
        med = {}
        with open('pharmacist/medicine_stock.txt', 'r') as pres:
            medicines = pres.readlines()

def view_consultation_reports(doctor_id):
    print("\n VIEW CONSULTATION REPORTS ")
    found = False
    
    try:
        with open('patient_record_db.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                values = line.strip().split(',')
                
                patient_id = values[0].replace("'", "")
                patient_name = values[1].replace("'", "").replace("_", " ")
                age = values[2]
                diagnosis = values[3].replace("'", "")
                meds = values[4].replace("'", "")
                advice = values[6].replace("'", "")

                print("-" * 30)
                print(f"Patient: {patient_name} ({patient_id})")
                print(f"Age: {age}")
                print(f"Diagnosis: {diagnosis}")
                print(f"Medications: {meds}")
                print(f"Advice: {advice}")
                found = True
                
        if not found:
            print("No record found.")

    except FileNotFoundError:
        print("No record found")
    
    
        
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


        
            
            
