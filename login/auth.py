import base64
import codecs
import hashlib

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
    
    email_domain = ['aphdoctor.com','aphaccount.com','aphreceptionist.com','aphpharmacist.com','aphhadmin.com']
    try:
        domain = user_email.split('@')[1]
        if domain == email_domain[0]:
            role = 'Doctor'
        elif domain == email_domain[1]:
            role = 'account personnel'
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
    
    
    username = input("Enter your username: ").strip()

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
        with open('users.txt', 'a') as f:
            f.write(f'{username},{user_email},{encrypted_pass},{role}')
            print('User registered successfully')
    except FileNotFoundError as e:
        print(f'Error: {e}')            

def login():
    while True:
        email = input('Enter your email: ').strip()
        password = input('Enter your password: ').strip()
        enc_password = encrypt_password(password)
        valid_user  = False
        with open('users.txt','r') as f:
            lines = f.readlines()
            
            for line in lines:
                file_email = line[1]
                file_password = line[2]
                if file_email == email and file_password == enc_password:
                    valid_user = True
                    user_role = line[3]
                    break
            if valid_user == True:
                print(f'Hello, {line[0]}, you are logged in as {user_role}, welcome to APU Hospital')
