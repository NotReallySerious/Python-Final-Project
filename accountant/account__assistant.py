import os
import datetime

def redo_action(prompt):
    while True:
        choice = input(f'{prompt}? (yes/no): ').strip().lower()
        if choice in ('yes','y'):
            return True
        elif choice in ('no','n'):
            return False
        else:
            print("Invalid Value. please enter 'yes', or 'no'.")
        
def get_user_total_details():
    try:
        with open('accountant/receipt_id.txt','r') as re:
            last_id = int(re.read())
    except FileNotFoundError:
        last_id = 0
    
    receipt_id = last_id + 1
    receipt_id_str = str(receipt_id)

    patient_name = input('Enter patient name to be totalled: ').strip()
    receipt_details = []
    found = False
    total = 0.00
    Date_Entry = ""
    with open('accountant/patient_billing_record.txt','r') as user_sum:
        for user in user_sum:
            if not user.strip():
                continue

            line = user.strip().split(';')

            if len(line) < 5:
                continue
            try:
                Date_Entry = line[0].strip().split(',')
                username = line[1].strip()
                item_name = line[2].strip()
                Quantity = int(line[3].strip())
                price = float(line[4].strip())
            except (ValueError, IndexError):
                continue

            if username == patient_name:
                found = True
                item_total = Quantity * price
                total += item_total
                receipt_details.append(f"{item_name} x {Quantity} = {item_total:.2f}")
            
        if not found:
            print(f'no records found for patient: {patient_name}')
            if not redo_action('Create Another receipt'):
                return
            else:
                get_user_total_details()
                return
    
    # Display and store them into a different username billing receipts
    receipt_path = f"accountant/{patient_name.replace(' ','_')}_receipt.txt"
    try:
        with open(receipt_path, 'a') as receipt:
            receipt.write("Asia Pacific Hospital receipt\n")
            receipt.write("================================\n")
            receipt.write(f"Receipt Id: {receipt_id_str}\n")
            receipt.write(f"Name : {patient_name.replace('_',' ')}\n")
            receipt.write(f"Time created: {Date_Entry}\n")
            receipt.write("================================\n")
            for i in receipt_details:
                receipt.write(i + '\n')
            receipt.write(f"Total Amount: {total:.2f}\n")
        
        print(f'receipt created successfully at {receipt_path}')

    except Exception as e:
        print(f"Error creating receipt: {e}")
    
    try:
        with open('accountant/receipt_db.txt','a') as rl:
            rl.write(f"{receipt_id_str}: {patient_name}\n")
        
        with open('receipt_id.txt', 'w') as re:
            re.write(str(receipt_id))
        
        print(f"{patient_name}'s receipt has been created")
        
    except Exception as e: 
        print(f"Error inserting receipt into the list: {e}") 
    
    if not redo_action('Create another receipt'):
        return

def get_receipt_list():
    receipts = {}
    current_id = 1
    with open('accountant/receipt_db.txt','r') as rl:
        lines = rl.readlines()
        for line in lines:

            patient_name = line.split(':')[1].strip()

            receipts[current_id] = patient_name
            print(f'{current_id}. {patient_name}')

            current_id += 1
    
    print('Enter the ID to view the receipt details (00 to exit)')
    while True:
        choice = input('>>> ')

        if choice == '00':
            break

        try:
            choice = int(choice)
        except ValueError:
            print('invalid ID')
            continue
            
        if choice in receipts:
            patient_name = receipts[choice]
            receipt_file = f"accountant/{patient_name.lower().replace(' ','_')}_receipt.txt"
        else:
            print('invalid ID')
            continue

        try:
            with open(receipt_file, 'r') as file:
                print(f" Receipt for {patient_name}")
                print(file.read())
        except FileNotFoundError:
            print(f'Error : receipt for {patient_name} cant be found')

        if not redo_action('see another receipt'):
            return

def delete_receipt():
    receipts = {}
    current_id = 1
    with open('accountant/receipt_db.txt','r') as rl:
        lines = rl.readlines()
        for line in lines:

            patient_name = line.split(':')[1].strip()

            receipts[current_id] = patient_name
            print(f'{current_id}. {patient_name}')

            current_id += 1
    
    print('Enter the receipt ID to Delete (00 to exit)')
    while True:
        choice = input('>>> ')

        if choice == '00':
            break

        if not lines:
            print("No receipts to delete")
            return

        try:
            choice = int(choice)
        except ValueError:
            print('invalid ID')
            continue
            
        if choice in receipts:
            patient_name = receipts[choice]
            receipt_file = f"accountant/{patient_name.lower().replace(' ','_')}_receipt.txt"
        else:
            print('invalid ID')
            continue

        if os.path.exists(receipt_file):
            os.remove(receipt_file)
            print(f"{patient_name}'s receipt has been deleted")
        else: 
            print(f"receipt for {patient_name} not found")

        del lines[choice - 1]

        with open('accountant/receipt_db.txt', 'w') as rl:
            rl.writelines(lines)    
        
        print('Receipt deleted successfully')

        if not redo_action('delete another receipt'):
            return

def daily_summary():
    patient_count = 0
    med_sold = {}
    patients = set()
    total = 0
    Date = ""
    VALID_DATE = False

    while not VALID_DATE:
        Date = input('Enter the date to generate summary (YYYY-MM-DD) or press Enter for today: ').strip()

        if not Date:
            Date = datetime.date.today().strftime('%Y-%m-%d')
            print(f"Using today's date: {Date}")
            VALID_DATE = True  
        else:
            try:
                datetime.datetime.strptime(Date, '%Y-%m-%d')
                VALID_DATE = True 
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD (e.g., 2025-12-30)")


    with open('accountant/patient_billing_record.txt','r') as f:
        lines = f.readlines()
        for line in lines:

            if not line.strip():
                continue
            part = line.strip().split(';')
            date = part[0].strip().replace("'","")
            patient_name = part[1].strip().replace("'","")
            item_name = part[2].strip().replace("'","")
            quantity = int(part[3].strip())
            price = float(part[4].strip())

            if Date == date:
                patients.add(patient_name)
                med_sold[item_name] = med_sold.get(item_name, 0) + quantity
                total += (quantity * price)

        patient_count = len(patients)
    
    if patient_count == 0:
        print(f'no transaction found for {Date}')
        return
    
    summary_file_path = f"accountant/{Date}_daily_summary.txt"

    with open(summary_file_path, 'w') as sum: 
        sum.write(f"Asia Pacific Hospital Healthplus Sales Summary\n")
        sum.write("============================\n")
        sum.write(f"Date: {Date}\n")
        sum.write(f"Total Patients: {patient_count}\n")
        sum.write("items sold:\n")
        for item, quantity in sorted(med_sold.items()):
            sum.write(f"{item}: {quantity} x {price} = {quantity * price}\n")
        
        sum.write("=================================\n")
        sum.write(f"Total Income = RM.{total:.2f}\n")
    
    print(f"Daily Summary for today is saved on {summary_file_path}")

    if not redo_action('Generate another summary'):
        return

def add_new_med_stock():
    with open('pharmacist/med_stock_low.txt','r') as f:
        info = f.readlines()
        for line in info:
            element = line.strip().split(',')
            code = element[0]
            Name = element[1]
            stock = int(element[2])
            Price = float(element[3])
            Demands = element[4]
            print("Barcode, Name, Stock, Price, Demand")
            print(f"{code}, {Name}, {stock}, {Price}, {Demands}\n")
    
    barcode = int(input("Enter Medicine's QR code: "))
    med_name = input('Enter medicine name: ').replace(' ', '_')
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter the price: "))
    demand = input("Enter demand [low, medium, high]: ").title()
    if demand not in ['Low', 'Medium', 'High']:
        print('Wrong demand type.')
    else:
        with open('pharmacist/med_new_stock.txt','w') as p:
            p.write(f"{barcode},{med_name},{quantity},{price},{demand}")
        with open('pharmacist/medicine_stock.txt', 'a') as m:
            m.write(f"{barcode},{med_name},{quantity},{price}")

        print('Item has been added to the list')

    if not redo_action("Want to enter another medicine? (yes/no): "):
        return
        
def update_quantity_med():
    existing_meds = {}
    with open('pharmacist/med_db.txt', 'r') as p:
        lines = p.readlines()
        for line in lines:
            values = line.strip().split(',')
            Barcode = values[0]
            med_name = values[1]
            quantity = values[2]
            price = values[3]
            demand = values[4]
            existing_meds[Barcode] = {
                'Name' : med_name,
                'Quantity' : int(quantity),
                'Price' : price,  
                'Demand' : demand
            }
    
    select_item_barcode = str(int(input('Enter the medicine barcode: ')))
    if select_item_barcode in existing_meds:
        print(f"Medicine name: {existing_meds[select_item_barcode]['Name']}")
        print(f"Quantity: {existing_meds[select_item_barcode]['Quantity']}")

        add_quantity = int(input("enter the quantity to be added: "))
        existing_meds[select_item_barcode]['Quantity'] += add_quantity
        
        print(f"New quantity: {existing_meds[select_item_barcode]['Quantity']}")
        print("Quantity updated successfully!")

        demand = input("Enter demand [low, medium, high]: ").title()
        if demand not in ['Low', 'Medium', 'High']:
            print('Wrong demand type.')
        else:
            with open('pharmacist/med_update_stock.txt','w') as up:
                up.write(f"{select_item_barcode},{existing_meds[select_item_barcode]['Name']},{existing_meds[select_item_barcode]['Quantity']},{existing_meds[select_item_barcode]['Price']},{demand}\n")                
                print("Item quantity updated")
    if not redo_action('Add another item quantity? (yes/no) '):
        return

def accountant_main():
    while True:
        print('Accountant management dashboard')
        print("1. Create Billing Receipt")
        print("2. View all receipts")
        print("3. Delete receipt(s)")
        print("4. Daily Summary Generator")
        print("5. Add new medicine to stock")
        print("6. Update existing medicine(s) stock")
        print("7. Log out")    
        choice = input("> ")
        match choice:
            case '1':
                get_user_total_details()
            case '2':
                get_receipt_list()
            case '3':
                delete_receipt()
            case '4':
                daily_summary()
            case '5':
                add_new_med_stock()
            case '6':
                update_quantity_med()
            case '7':
                with open('login/logged_out.txt','a') as l:
                    l.write(f'[{datetime.datetime.now()}] accountant logged out\n')
                print('Bye. See you tomorrow. Have a great day')
                break






    

