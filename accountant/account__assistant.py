import os
import datetime


def redo_action(prompt):
    while True:
        choice = input(f'{prompt}? (yes/no): ').strip().lower()
        if choice in ('yes', 'y'):
            return True
        elif choice in ('no', 'n'):
            return False
        else:
            print("Invalid Value. please enter 'yes', or 'no'.")


def load_medicine_database():
    """Load medicine information from med_db.txt"""
    medicines = {}
    try:
        with open('../pharmacist/pharmacist/med_db.txt', 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    barcode = parts[0].strip()
                    name = parts[1].strip()
                    medicines[barcode] = name
    except FileNotFoundError:
        print("Warning: med_db.txt not found")
    return medicines


def load_patient_database():
    """Load patient information from patient.txt"""
    patients = {}
    try:
        with open('../cashier/patient.txt', 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    patient_id = parts[0].strip()
                    patient_name = parts[1].strip()
                    patients[patient_id] = patient_name
    except FileNotFoundError:
        print("Warning: patient.txt not found")
    return patients


def get_user_total_details():
    try:
        with open('../accountant/receipt_id.txt', 'r') as re:
            last_id = int(re.read())
    except FileNotFoundError:
        last_id = 0

    receipt_id = last_id + 1
    receipt_id_str = str(receipt_id)

    # Load databases
    medicines = load_medicine_database()
    patients = load_patient_database()

    # Display available patients in billing records
    print("\n" + "=" * 60)
    print("   PATIENTS WITH BILLING RECORDS")
    print("=" * 60)

    available_patients = set()
    try:
        with open('../pharmacist/pharmacist/patient_billing_record.txt', 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    patient_id = parts[1].strip()
                    available_patients.add(patient_id)

        if available_patients:
            print(f"{'Patient ID':<15} {'Patient Name':<30}")
            print("-" * 60)
            for pid in sorted(available_patients):
                pname = patients.get(pid, "Unknown")
                print(f"{pid:<15} {pname:<30}")
            print("=" * 60 + "\n")
        else:
            print("No billing records found!")
            print("=" * 60 + "\n")
            return
    except FileNotFoundError:
        print("Error: patient_billing_record.txt not found")
        print("=" * 60 + "\n")
        return

    patient_id = input('Enter patient ID to be totalled (e.g., P01): ').strip()

    # Get patient name
    patient_name = patients.get(patient_id, "Unknown Patient")

    receipt_details = []
    found = False
    total = 0.00
    Date_Entry = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('../pharmacist/pharmacist/patient_billing_record.txt', 'r') as user_sum:
        for user in user_sum:
            if not user.strip():
                continue

            line = user.strip().split(',')

            if len(line) < 5:
                continue
            try:
                date = line[0].strip()
                pid = line[1].strip()
                barcode = line[2].strip()
                quantity = int(line[3].strip())
                price = float(line[4].strip())
            except (ValueError, IndexError):
                continue

            if pid == patient_id:
                found = True
                item_total = quantity * price
                total += item_total

                # Get medicine name from barcode
                med_name = medicines.get(barcode, f"Unknown Med (Barcode: {barcode})")
                receipt_details.append(f"{med_name} x {quantity} = RM {item_total:.2f}")

        if not found:
            print(f'No records found for patient: {patient_id} ({patient_name})')
            if not redo_action('Create Another receipt'):
                return
            else:
                get_user_total_details()
                return

    # Display and store them into a different patient billing receipts
    receipt_path = f"../accountant/{patient_name}_{patient_id}_receipt.txt"
    try:
        with open(receipt_path, 'a') as receipt:
            receipt.write("=========================================\n")
            receipt.write("   Asia Pacific Hospital Receipt\n")
            receipt.write("=========================================\n")
            receipt.write(f"Receipt ID: {receipt_id_str}\n")
            receipt.write(f"Patient ID: {patient_id}\n")
            receipt.write(f"Patient Name: {patient_name}\n")
            receipt.write(f"Time Created: {Date_Entry}\n")
            receipt.write("=========================================\n")
            receipt.write("Items Purchased:\n")
            for i in receipt_details:
                receipt.write(f"  {i}\n")
            receipt.write("=========================================\n")
            receipt.write(f"Total Amount: RM {total:.2f}\n")
            receipt.write("=========================================\n\n")

        print(f'\nReceipt created successfully!')
        print(f'Patient: {patient_name} ({patient_id})')
        print(f'Total: RM {total:.2f}')
        print(f'Location: {receipt_path}')

    except Exception as e:
        print(f"Error creating receipt: {e}")

    try:
        with open('../accountant/receipt_db.txt', 'a') as rl:
            rl.write(f"{receipt_id_str}: {patient_id} - {patient_name}\n")

        with open('../accountant/receipt_id.txt', 'w') as re:
            re.write(str(receipt_id))

        print(f"{patient_name}'s receipt has been saved")

    except Exception as e:
        print(f"Error inserting receipt into the list: {e}")

    if not redo_action('Create another receipt'):
        return


def get_receipt_list():
    receipts = {}
    current_id = 1

    try:
        with open('../accountant/receipt_db.txt', 'r') as rl:
            lines = rl.readlines()
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    receipt_info = parts[1].strip()
                    receipts[current_id] = receipt_info
                    print(f'{current_id}. {receipt_info}')
                    current_id += 1
    except FileNotFoundError:
        print("No receipts found")
        return

    if not receipts:
        print("No receipts available")
        return

    print('\nEnter the ID to view the receipt details (00 to exit)')
    while True:
        choice = input('>>> ')

        if choice == '00':
            break

        try:
            choice = int(choice)
        except ValueError:
            print('Invalid ID')
            continue

        if choice in receipts:
            # Extract patient ID from the receipt info
            receipt_info = receipts[choice]
            patient_id = receipt_info.split()[0]  # Gets "P01" from "P01 - Alex Smith"
            receipt_file = f"../accountant/{patient_id}_receipt.txt"
        else:
            print('Invalid ID')
            continue

        try:
            with open(receipt_file, 'r') as file:
                print(f"\n{'=' * 45}")
                print(file.read())
        except FileNotFoundError:
            print(f'Error: receipt file not found')

        if not redo_action('See another receipt'):
            return


def delete_receipt():
    receipts = {}
    current_id = 1

    try:
        with open('../accountant/receipt_db.txt', 'r') as rl:
            lines = rl.readlines()
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    receipt_info = parts[1].strip()
                    receipts[current_id] = receipt_info
                    print(f'{current_id}. {receipt_info}')
                    current_id += 1
    except FileNotFoundError:
        print("No receipts found")
        return

    if not lines:
        print("No receipts to delete")
        return

    print('\nEnter the receipt ID to Delete (00 to exit)')
    while True:
        choice = input('>>> ')

        if choice == '00':
            break

        try:
            choice = int(choice)
        except ValueError:
            print('Invalid ID')
            continue

        if choice in receipts:
            receipt_info = receipts[choice]
            patient_id = receipt_info.split()[0]
            receipt_file = f"../accountant/{patient_id}_receipt.txt"
        else:
            print('Invalid ID')
            continue

        if os.path.exists(receipt_file):
            os.remove(receipt_file)
            print(f"Receipt for {receipt_info} has been deleted")
        else:
            print(f"Receipt file not found")

        del lines[choice - 1]

        with open('../accountant/receipt_db.txt', 'w') as rl:
            rl.writelines(lines)

        print('Receipt deleted successfully from database')

        if not redo_action('Delete another receipt'):
            return


def daily_summary():
    patient_count = 0
    med_sold = {}
    patients = set()
    total = 0
    Date = ""
    VALID_DATE = False

    # Load databases
    medicines = load_medicine_database()
    patient_names = load_patient_database()

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

    with open('../pharmacist/pharmacist/patient_billing_record.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:

            if not line.strip():
                continue
            part = line.strip().split(',')

            if len(part) < 5:
                continue

            try:
                date = part[0].strip()
                patient_id = part[1].strip()
                barcode = part[2].strip()
                quantity = int(part[3].strip())
                price = float(part[4].strip())
            except (ValueError, IndexError):
                continue

            if Date == date:
                patients.add(patient_id)
                # Use medicine name instead of barcode
                med_name = medicines.get(barcode, f"Unknown (Code: {barcode})")
                med_sold[med_name] = med_sold.get(med_name, {'qty': 0, 'total': 0})
                med_sold[med_name]['qty'] += quantity
                med_sold[med_name]['total'] += (quantity * price)
                total += (quantity * price)

        patient_count = len(patients)

    if patient_count == 0:
        print(f'No transaction found for {Date}')
        return

    summary_file_path = f"../accountant/{Date}_daily_summary.txt"

    with open(summary_file_path, 'w') as sum:
        sum.write("=" * 50 + "\n")
        sum.write("  Asia Pacific Hospital Healthplus Sales Summary\n")
        sum.write("=" * 50 + "\n")
        sum.write(f"Date: {Date}\n")
        sum.write(f"Total Patients Served: {patient_count}\n")
        sum.write("=" * 50 + "\n")
        sum.write("Items Sold:\n")
        sum.write("-" * 50 + "\n")
        for med_name, data in sorted(med_sold.items()):
            sum.write(f"{med_name}\n")
            sum.write(f"  Quantity: {data['qty']} units\n")
            sum.write(f"  Subtotal: RM {data['total']:.2f}\n")
            sum.write("-" * 50 + "\n")

        sum.write("=" * 50 + "\n")
        sum.write(f"TOTAL INCOME: RM {total:.2f}\n")
        sum.write("=" * 50 + "\n")

    print(f"\nDaily Summary Generated Successfully!")
    print(f"Date: {Date}")
    print(f"Total Income: RM {total:.2f}")
    print(f"Saved at: {summary_file_path}")

    if not redo_action('Generate another summary'):
        return


def add_new_med_stock():
    try:
        with open('../pharmacist/med_stock_low.txt', 'r') as f:
            info = f.readlines()
            print("\nCurrent Low Stock Medicines:")
            print("=" * 60)
            print(f"{'Barcode':<10} {'Name':<20} {'Stock':<8} {'Price':<10} {'Demand':<10}")
            print("-" * 60)
            for line in info:
                element = line.strip().split(',')
                if len(element) >= 5:
                    code = element[0].strip()
                    Name = element[1].strip()
                    stock = element[2].strip()
                    Price = element[3].strip()
                    Demands = element[4].strip()
                    print(f"{code:<10} {Name:<20} {stock:<8} {Price:<10} {Demands:<10}")
            print("=" * 60 + "\n")
    except FileNotFoundError:
        print("Low stock file not found\n")

    barcode = input("Enter Medicine's Barcode: ").strip()
    med_name = input('Enter medicine name: ').strip().replace(' ', '_')
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter the price: "))
    demand = input("Enter demand [low, medium, high]: ").strip().title()

    if demand not in ['Low', 'Medium', 'High']:
        print('Wrong demand type. Must be Low, Medium, or High.')
    else:
        with open('../pharmacist/med_new_stock.txt', 'w') as p:
            p.write(f"{barcode},{med_name},{quantity},{price},{demand}\n")
        with open('../pharmacist/medicine_stock.txt', 'a') as m:
            m.write(f"{barcode},{med_name},{quantity},{price}\n")

        print(f'\nItem "{med_name}" (Barcode: {barcode}) has been added to the stock')

    if not redo_action("Want to enter another medicine"):
        return


def update_quantity_med():
    existing_meds = {}
    try:
        with open('../pharmacist/pharmacist/med_db.txt', 'r') as p:
            lines = p.readlines()
            print("\nAvailable Medicines:")
            print("=" * 70)
            print(f"{'Barcode':<10} {'Name':<25} {'Quantity':<12} {'Price':<10}")
            print("-" * 70)
            for line in lines:
                if not line.strip():
                    continue
                values = line.strip().split(',')
                if len(values) >= 4:
                    Barcode = values[0].strip()
                    med_name = values[1].strip()
                    quantity = values[2].strip()
                    price = values[3].strip()
                    existing_meds[Barcode] = {
                        'Name': med_name,
                        'Quantity': int(quantity),
                        'Price': price
                    }
                    print(f"{Barcode:<10} {med_name:<25} {quantity:<12} {price:<10}")
            print("=" * 70 + "\n")
    except FileNotFoundError:
        print("Medicine database not found")
        return

    select_item_barcode = input('Enter the medicine barcode: ').strip()

    if select_item_barcode in existing_meds:
        print(f"\nMedicine: {existing_meds[select_item_barcode]['Name']}")
        print(f"Current Quantity: {existing_meds[select_item_barcode]['Quantity']}")
        print(f"Price: RM {existing_meds[select_item_barcode]['Price']}")

        add_quantity = int(input("\nEnter the quantity to be added: "))
        existing_meds[select_item_barcode]['Quantity'] += add_quantity

        print(f"\nNew quantity: {existing_meds[select_item_barcode]['Quantity']}")
        print("Quantity updated successfully!")

        demand = input("Enter demand level [low, medium, high]: ").strip().title()
        if demand not in ['Low', 'Medium', 'High']:
            print('Wrong demand type.')
        else:
            with open('../pharmacist/med_update_stock.txt', 'w') as up:
                up.write(
                    f"{select_item_barcode},{existing_meds[select_item_barcode]['Name']},{existing_meds[select_item_barcode]['Quantity']},{existing_meds[select_item_barcode]['Price']},{demand}\n")
                print("Item quantity updated in system")
    else:
        print(f"\nBarcode {select_item_barcode} not found in database")

    if not redo_action('Update another item quantity'):
        return


def accountant_main():
    while True:
        print('\n' + '=' * 45)
        print('   ACCOUNTANT MANAGEMENT DASHBOARD')
        print('=' * 45)
        print("1. Create Billing Receipt")
        print("2. View All Receipts")
        print("3. Delete Receipt(s)")
        print("4. Daily Summary Generator")
        print("5. Add New Medicine to Stock")
        print("6. Update Existing Medicine Stock")
        print("7. Log Out")
        print('=' * 45)
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
                try:
                    with open('../login/logged_out.txt', 'a') as l:
                        l.write(f'[{datetime.datetime.now()}] accountant logged out\n')
                except:
                    pass
                print('\nLogging out...')
                print('Bye. See you tomorrow. Have a great day!')
                break
            case _:
                print("Invalid choice. Please select 1-7")


if __name__ == "__main__":
    accountant_main()