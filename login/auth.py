import base64
import codecs
import hashlib
import datetime as dt
from pharmacist.pharmacist import pharmasist
from accountant.account__assistant import accountant_main, delete_receipt, get_user_total_details, get_receipt_list

def encrypt_password(password):
    #change password into bytes before encoding
    password_bytes = password.encode('utf-8')

    base64_encoded = base64.b64encode(password_bytes)
    base64_string = base64_encoded.decode('utf-8')

    # changed into rot-13 
    ROT_13_encode = codecs.encode(base64_string, 'rot_13')
    
    # change to SHA256
    hash_bytes = ROT_13_encode.encode('utf-8')
    sha256_string = hashlib.sha256(hash_bytes)
    final_hex_representation = sha256_string.hexdigest()
    return final_hex_representation

def register():
    while True:
        user_email = input("Enter your valid email: ").strip()
        # Email checking
        if '@' not in user_email:
            print("Invalid email")
        else:
            break
    
    email_domain = ['aphdoctor.aph.com','aphaccountant.aph.com','aphreceptionist.aph.com','aphpharmacist.aph.com','aphhadmin.aph.com']
    try:
        domain = user_email.split('@')[1]
        if domain == email_domain[0]:
            role = 'Doctor'
        elif domain == email_domain[1]:
            role = 'accountant'
        elif domain == email_domain[2]:
            role = 'receptionist'
        elif domain == email_domain[3]:
            role = 'pharmacist'
        elif domain == email_domain[4]:
            role = 'administrator'
        else:
            role = 'patient'
    except IndexError:
        print('invalid email format.')
    
    
    username = input("Enter your username: ").strip().replace(' ','_')

    while True: 
        password = input("Enter your password: ").strip()
        
        # Password checking
        password_length = len(password)
        uppercase_count = 0
        lowercase_count = 0
        num_count = 0
        special_characters = ['[','!','@','#','$','%','^','&','*','(',')','.','?','"',':','{','}','|','<','>',']']
        special_count = 0
        all_valid = True
        if password_length < 12:
            print(f"your password length is {len(password)}. you password must have at least 12 characters")
            all_valid = False
        
        for letter in password:
            if letter.isupper():
                uppercase_count += 1
            elif letter.islower():
                lowercase_count += 1
            if letter.isnumeric():
                num_count += 1

        if uppercase_count < 1:
            print("Your password must have at least 1 uppercase letter.")
            all_valid = False

        if lowercase_count < 1:
            print("Your password must have at least 1 lowercase letter")
            all_valid = False
        
        for letter in password:
            if letter in special_characters:
                special_count += 1
        if special_count < 1:
            print("Your password must have at least 1 special characters")
            all_valid = False
        
        if num_count < 1:
            print('Your password must have at least 1 digit number')
            all_valid = False
        
        if all_valid:
            print("Password all match")
            encrypted_pass = encrypt_password(password)
            break

    print(f'username: {username}, email: {user_email}, Password: {encrypted_pass} Role: {role}')

    try:
        with open('login/user_db.txt', 'a') as f:
            f.write(f'{username};{user_email};{password};{role}\n')
            print('User registered successfully')
    except FileNotFoundError as e:
        print(f'Error: {e}')   
    try:
        with open('login/user_db_encrypted.txt','a') as fe:
            fe.write(f'{username};{user_email};{encrypt_password(password)};{role}\n')   
    except FileNotFoundError as e:
        print(f'Error: {e}')  

def login():
    wrong_attempt_count = 3

    while wrong_attempt_count != 0:
        email = input('Enter your email: ').strip()
        password = input('Enter your password: ').strip()
        enc_password = encrypt_password(password)
        valid_user  = False

        with open('login/user_db_encrypted.txt','r') as f:
            lines = f.readlines()
            
            for line in lines:
                fields = line.strip().split(';')
                username = fields[0].strip('"')
                file_email = fields[1].strip('"')
                file_password = fields[2].strip('"')
                user_role = fields[3].strip('"')
                if file_email == email and file_password == enc_password:
                    valid_user = True
                    break

            if valid_user == True:
                with open('login/clocked_in.txt','a') as cl:
                    cl.write(f"{dt.datetime.now()}: {user_role}, {username}\n")
                print(f'Hello {user_role}, {username}\n')

                if user_role == 'Doctor':
                    print(f'Hello Doctor {username}')
                    return

                elif user_role == 'accountant':
                    print(f'Hello accountant {username}, ready to count some money?')
                    accountant_main()
                    return

                elif user_role == 'pharmacist':
                    print(f'Hello pharmacist {username}')
                    pharmasist()
                    return
            
                elif user_role == 'receptionist':
                    print(f"Catchingg... Hello {username}")
                    return
                
                elif user_role == 'administrator':
                    print(f"Hello Admin. lets go manage some stuffs today")
                    return
                
                else:
                    print('No role for you. do you even work here?')
                    break
                
            else:
                wrong_attempt_count -= 1
                print(f'credentials invalid. you have {wrong_attempt_count} attempt(S) left')
                
    print('Hacker detected, go away')
            
def main():
    while True:
        print('Asia Pacific Hospital HealthPlus patient management')
        print('1. Register')
        print('2. Login')
        print('3. Exit')
        choice = int(input('Enter your option: '))
        match choice:
            case 1:
                register()
            case 2:
                login()

main()
