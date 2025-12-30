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
        
def user_total_details():
    try:
        with open('receipt_id.txt','r') as re:
            last_id = int(re.read())
    except FileNotFoundError:
        last_id = 0
    
    receipt_id = last_id + 1
    receipt_id_str = str(receipt_id)

    target_username = input('Enter username to be totalled: ').strip().lower()
    receipt_details = []
    total = 0.00
    with open('accountant/patient_billing_record.txt','r') as user_sum:
        for user in user_sum:
            line = user.strip().split(',')
            username = line[0].strip().replace("'", "").lower()
            item_name = line[1].strip().replace("'", "")
            Quantity = int(line[2])
            price = float(line[3])

            if username == target_username:
                found = True
                item_total = Quantity * price
                total += item_total
                receipt_details.append(f"{item_name} x {Quantity} = {item_total:.2f}")
    
    # Display and store them into a different username billing receipts
    receipt_path = f"accountant/{target_username.replace(" ","_")}_receipt.txt"
    try:
        with open(receipt_path, 'a') as receipt:
            receipt.write("Asia Pacific Hospital receipt\n")
            receipt.write("================================\n")
            receipt.write(f"Receipt Id: {receipt_id_str}\n")
            receipt.write(f"Name : {target_username.replace('_',' ')}\n")
            receipt.write(f"Time created: {datetime.datetime.now()}\n")
            receipt.write("================================\n")
            for i in receipt_details:
                receipt.write(i + '\n')
            receipt.write(f"Total Amount: {total:.2f}\n")

    except FileExistsError as e:
        print(f"Error found: {e}")
    
    try:
        with open('accountant/receipt_db.txt','a') as rl:
            rl.write(f"{receipt_id_str}: {target_username}"+'\n')
            print(f"{target_username}'s receipt has been created")
    except:
        print("error inserting receipt into the list")
    
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

def accountant_main():
    while True:
        print('Accountant management dashboard')
        print("1. Create Billing Receipt")
        print("2. View all receipts")
        print("3. Delete receipt(s)")
        print("4. Log out")    
        choice = input("> ")
        match choice:
            case '1':
                user_total_details()
            case '2':
                get_receipt_list()
            case '3':
                delete_receipt()
            case '4':
                with open('login/logged_out.txt','a') as l:
                    l.write(f'[{datetime.datetime.now()}] accountant logged out')
                print('Bye. See you tomorrow. Have a great day')
                break






    

