import os
import datetime


'''This section is for record patient billing and payment method'''
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
    receipt_path = f"{target_username.replace(" ","_")}_receipt.txt"
    try:
        with open(receipt_path, 'a') as receipt:
            receipt.write(f"Asia Pacific Hospital receipt")
            receipt.write("================================")
            receipt.write(f"Receipt Id: {receipt_id_str}")
            receipt.write(f"Name : {target_username}")
            receipt.write(f"Time created: {datetime.datetime.now()}")
            receipt.write("================================")
            for i in receipt_details:
                receipt.write(i + '\n')
            receipt.write(f"Total Amount: {total:.2f}\n")

    except FileExistsError as e:
        print(f"Error found: {e}")
    
    try:
        with open('receipt_db.txt','a') as rl:
            rl.write(f"{receipt_id_str}: {target_username}"+'\n')
    except:
        print("error inserting receipt into the list")

def get_receipt_list():
    receipts = {}
    with open('receipt_db.txt','r') as rl:
        lines = rl.readlines()
        for line in lines:

            param = line.split(':')
            receipt_id = int(param[0])
            customer_name = param[1]

            receipts[receipt_id] = customer_name
            print(f'{receipt_id}. {customer_name}')
    
    print('Enter the ID to view the receipt details (00 to exit)')
    while True:
        choice = input('>>> ')

        if choice == 00:
            break
            
        if choice in receipts:
            customer_name = receipts[choice]
            receipt_file = f"{customer_name.replace(' ','_')}_receipt.txt"
        else:
            print('invalid ID')
            continue

        try:
            with open(receipt_file, 'r') as file:
                print(f" Receipt for {customer_name}")
                print(file.read())
        except FileNotFoundError:
            print(f'Error : receipt for {customer_name} cant be found')
        
def accountant():
    while True:
        print('Accountant management dashboard')
        print("1. Create Billing Receipt")
        print("2. View all receipts")
        print("3. Log out")    
        choice = input("> ")
        match choice:
            case '1':
                user_total_details()
            case '2':
                get_receipt_list()
            case '3':
                break

accountant()





    

