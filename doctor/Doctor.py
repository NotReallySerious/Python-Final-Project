from accountant.account__assistant import redo_action
import datetime

def get_doctor_name(doctor_id):
    with open('../doctor/Doctor.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split(',')
            doctor_id_in_file = values[0]
            Name = values[1].replace('_',' ')

            if doctor_id == doctor_id_in_file:
                return Name  
        
        return "Unknown"  # Return a default value instead of printing error

def view_appointments(doctor_id):
    patients = {}
    with open('cashier/patient.txt', 'r') as p:
        lines = p.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            value = line.split(',')
            if len(value) >= 2:
                patient_id = value[0].strip()
                Name = value[1].strip()
                patients[patient_id] = {
                    'Name': Name
                }

    records = {}
    with open('cashier/appointment.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            values = line.split(',')
            if len(values) >= 6:
                app_id = values[0].strip()
                date = values[1].strip()
                hour = values[2].strip()
                status = values[3].strip()
                patient_id = values[4].strip()
                doctor_id_in_file = values[5].strip()
            
                if doctor_id_in_file == doctor_id:
                    records[app_id] = {
                        'date': date,
                        'hour': hour,
                        'status': status,
                        'patient_id': patient_id,
                        'doctor_id': doctor_id_in_file
                    }
    
    if records:
        print("-" * 30)
        print(f"Appointments for Dr. {get_doctor_name(doctor_id)}")
        print("-" * 30)
        for app_id, details in records.items():
            print(f"Appointment ID: {app_id}")
            print(f"Date: {details['date']}")
            print(f"Hour: {details['hour']}")
            print(f"Patient ID: {details['patient_id']}")
            patient_name = patients.get(details['patient_id'], {}).get('Name', 'Unknown')
            print(f"Patient Name: {patient_name}")
            print("-" * 30)
    else:
        print(f"No appointments for Dr. {get_doctor_name(doctor_id)}")
    
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
        patient_id = appointment_details[app_id]['Patient_ID']
        patient_name = patient_details.get(patient_id, {}).get('Name','unknown')

        appointment_list[index] = {
            'appointment_id': app_id,
            'appointment_data': appointment_details[app_id],
            'patient_name': patient_name,
            'patient_id' : patient_id
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
                diagnosis = input('Diagnosis: ').strip()
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

        record = f"'{doctor_id}','{patient_id}','{patient_name}',{age},'{diagnosis}','{meds}','{qty}','{advice}'\n"

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
        token_number = 1

        # First, check if prescription file exists to determine next token number
        try:
            with open('pharmacist/doctor_prescription.txt', 'r') as existing:
                existing_lines = existing.readlines()
                if existing_lines:
                    # Get the last token number and increment
                    last_line = existing_lines[-1].strip()
                    if last_line:
                        last_token = int(last_line.split(',')[1])
                        token_number = last_token + 1
        except FileNotFoundError:
            token_number = 1  # File doesn't exist, start at 1

        # Get medicine stock with barcodes
        medicine_stock = {}
        try:
            with open('pharmacist/medicine_stock.txt', 'r') as stock:
                stock_lines = stock.readlines()
                for line in stock_lines:
                    line = line.strip()
                    if not line:
                        continue
                    stock_values = line.split(',')
                    if len(stock_values) >= 2:
                        med_name = stock_values[1].strip().lower()
                        barcode = stock_values[0].strip()
                        medicine_stock[med_name] = barcode
        except FileNotFoundError:
            print("Warning: medicine_stock.txt not found. Prescriptions will be created without barcodes.")

        # Parse medicines and quantities from the current patient
        meds_list = [m.strip() for m in meds.split(';')]
        qty_list = [q.strip() for q in qty.split(';')]

        # Write prescription to pharmacist file
        try:
            with open('pharmacist/doctor_prescription.txt', 'a') as pres_file:
                for i, medicine in enumerate(meds_list):
                    quantity = qty_list[i] if i < len(qty_list) else '1'  # Default to 1 if quantity missing
                    
                    # Look up barcode (case-insensitive)
                    barcode = medicine_stock.get(medicine.lower(), 'UNKNOWN')
                    
                    # Format: patient_id,token_no,medicine_name,barcode,quantity
                    prescription_line = f"{patient_id},{token_number},{medicine},{barcode},{quantity}\n"
                    pres_file.write(prescription_line)
                
                print(f"Prescription sent to pharmacist with token number: {token_number}")
        except Exception as e:
            print(f"Error writing prescription: {e}")        
        if not redo_action('Do you want to record another consultation? '):
            break

def view_consultation_reports(doctor_id):
    print("\n VIEW CONSULTATION REPORTS ")
    found = False
    
    try:
        with open('doctor/patient_record_db.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                values = line.strip().split(',')
                D_id = values[0].replace("'", "").strip()  
                patient_id = values[1].replace("'", "").strip()
                patient_name = values[2].replace("'", "").replace("_", " ").strip()
                age = values[3].strip()
                diagnosis = values[4].replace("'", "").strip()
                meds = values[5].replace("'", "").replace(';', ', ').strip()
                qty = values[6].replace("'", "").strip() 
                advice = values[7].replace("'", "").replace(';', ', ').strip() 

                if D_id == doctor_id:
                    print("-" * 30 + '\n')
                    print(f"Patient: {patient_name} ({patient_id})")
                    print(f"Age: {age}")
                    print(f"Diagnosis: {diagnosis}")
                    print(f"Medications: {meds}")
                    print(f"Quantity: {qty}")
                    print(f"Advice: {advice}\n")
                    print("-" * 30 + '\n')
                    found = True
                
        if not found:
            print("No record found.")

    except FileNotFoundError:
        print("No record found")
    
def Doctor_Menu(doctor_id):

    print(f"Hello Dr. {get_doctor_name(doctor_id)}")
    while True:
        print("~~Doctor Menu~~")
        print("1.View appointments")
        print("2.Record diagnosis and Consultation notes")
        print("3.View Consultation Reports")
        print("4.Back to Menu")

        choice = input("Which one do you want to pick: ")
        if choice == "1":
            view_appointments(doctor_id) 
        elif choice == "2":
            record_consultation(doctor_id)
        elif choice == "3":
            view_consultation_reports(doctor_id)
        elif choice == "4":
            with open('login/logged_out.txt','a') as l:
                l.write(f'[{datetime.datetime.now()}] Doctor logged out\n')
            print('Bye. See you tomorrow. Have a great day')
            break
        else:
            print("Invalid choice. Please choose the number above")   

Doctor_Menu('D01')