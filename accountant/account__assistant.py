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
        with open('receipt_id.txt','r') as re:
            last_id = int(re.read())
    except FileNotFoundError:
        last_id = 0
    
    receipt_id = last_id + 1
    receipt_id_str = str(receipt_id)

    target_username = input('Enter username to be totalled: ').strip()
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
                Date_Entry = line[0].strip().replace("'","")
                username = line[1].strip().replace("'", "")
                item_name = line[2].strip().replace("'", "")
                Quantity = int(line[3].strip())
                price = float(line[4].strip())
            except (ValueError, IndexError):
                continue

            if username == target_username:
                found = True
                item_total = Quantity * price
                total += item_total
                receipt_details.append(f"{item_name} x {Quantity} = {item_total:.2f}")
            
        if not found:
            print(f'no records found for patient: {target_username}')
            if not redo_action('Create Another receipt'):
                return
            else:
                get_user_total_details()
                return
    
    # Display and store them into a different username billing receipts
    receipt_path = f"accountant/{target_username.replace(" ","_")}_receipt.txt"
    try:
        with open(receipt_path, 'a') as receipt:
            receipt.write("Asia Pacific Hospital receipt\n")
            receipt.write("================================\n")
            receipt.write(f"Receipt Id: {receipt_id_str}\n")
            receipt.write(f"Name : {target_username.replace('_',' ')}\n")
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
            rl.write(f"{receipt_id_str}: {target_username}\n")
        
        with open('receipt_id.txt', 'w') as re:
            re.write(str(receipt_id))
        
        print(f"{target_username}'s receipt has been created")
        
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

            customer_name = line.split(':')[1].strip()

            receipts[current_id] = customer_name
            print(f'{current_id}. {customer_name}')

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
            customer_name = receipts[choice]
            receipt_file = f"accountant/{customer_name.lower().replace(' ','_')}_receipt.txt"
        else:
            print('invalid ID')
            continue

        try:
            with open(receipt_file, 'r') as file:
                print(f" Receipt for {customer_name}")
                print(file.read())
        except FileNotFoundError:
            print(f'Error : receipt for {customer_name} cant be found')

        if not redo_action('see another receipt'):
            return

def delete_receipt():
    receipts = {}
    current_id = 1
    with open('accountant/receipt_db.txt','r') as rl:
        lines = rl.readlines()
        for line in lines:

            customer_name = line.split(':')[1].strip()

            receipts[current_id] = customer_name
            print(f'{current_id}. {customer_name}')

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
            customer_name = receipts[choice]
            receipt_file = f"accountant/{customer_name.lower().replace(' ','_')}_receipt.txt"
        else:
            print('invalid ID')
            continue

        if os.path.exists(receipt_file):
            os.remove(receipt_file)
            print(f"{customer_name}'s receipt has been deleted")
        else: 
            print(f"receipt for {customer_name} not found")

        del lines[choice - 1]

        with open('accountant/receipt_db.txt', 'w') as rl:
            rl.writelines(lines)    
        
        print('Receipt deleted successfully')

        if not redo_action('delete another receipt'):
            return

def daily_summary():
    patient_count = 0
    med_sold = {}
    total = 0
    Date = datetime.date.today().strftime('%Y-%m-%d')

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
                patient_count += 1
                med_sold[item_name] = med_sold.get(item_name, 0) + quantity
                total += (quantity * price)
    
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
            sum.write(f"{item}: {quantity} x {price}\n")
        
        sum.write("=================================\n")
        sum.write(f"Total Income = RM. {total:.2f}\n")
    
    print(f"Daily Summary for today is saved on {summary_file_path}")

    if not redo_action('Generate another summary'):
        return

def accountant_main():
    while True:
        print('Accountant management dashboard')
        print("1. Create Billing Receipt")
        print("2. View all receipts")
        print("3. Delete receipt(s)")
        print("4. Daily Summary Generator")
        print("5. Log out")    
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
                with open('login/logged_out.txt','a') as l:
                    l.write(f'[{datetime.datetime.now()}] accountant logged out\n')
                print('Bye. See you tomorrow. Have a great day')
                break

accountant_main()





    

