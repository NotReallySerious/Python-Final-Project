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

    target_username = input('Enter username to be totalled: ')
    receipt_details = []
    Total = 0.00
    with open('../accountant/patient_billing_record.txt','r') as user_sum:
        for user in user_sum:
            line = user.strip().split(',')
            username = line[0].replace("'","")
            item_name = line[1].replace("'","")
            item_quantity = int(line[2])
            price = float(line[3])

            if username == target_username:
                total = Total + (item_quantity * price)
                receipt_details.append(
                    item_name + 'x' + str(item_quantity) + '=' + str(round(total, 2))
                )
            else:
                print('Username not found. Exiting')
                break
            
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
            receipt.write(f"Total Amount: {str(total)}")
    except FileExistsError as e:
        print(f"Error found: {e}")
    
    try:
        with open('receipt_db.txt','a') as rl:
            rl.write(f"{receipt_id_str}. {target_username}"+'\n')
    except:
        print("error inserting receipt into the list")

def get_receipt_list():
    with open('receipt_db.txt','r') as rl:
        lines = rl.readlines()
        for line in lines
    

