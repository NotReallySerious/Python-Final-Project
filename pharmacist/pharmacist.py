import csv
import datetime
from datetime import date


# Function to add new medicines from 'med_new_stock.txt' into the main stock file.
# Ensures no duplicate barcodes are added and prints the newly added medicines.
def add():
    try:
        with open("pharmacist/med_new_stock.txt", mode="r", newline="") as f_new:
            reader = csv.reader(f_new)
            new_meds = list(reader)

        if not new_meds:
            raise ValueError("No medicines found in med_new_stock.txt")

        with open("pharmacist/medicine_stock.txt", mode="r", newline="") as f_stock:
            reader = csv.reader(f_stock)
            existing_meds = list(reader)

        existing_barcodes = {row[0] for row in existing_meds if row}

        for med in new_meds:
            if len(med) < 4:
                continue
            if med[0] in existing_barcodes:
                raise ValueError("One or more medicines already exist in database.")

        with open("pharmacist/medicine_stock.txt", mode="a", newline="") as f_stock:
            writer = csv.writer(f_stock)
            writer.writerows(new_meds)

        print("Medicines from med_new_stock.txt:")
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
        for row in new_meds:
            if len(row) < 4:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
        print("Medicines Added Successfully")
        print("\n\n")

    except ValueError as ve:
        print(f"Error: {ve}")


# Function to update existing medicine stock using 'med_update_stock.txt'.
# Increases quantities, updates price and demand, or adds new medicines if not already present.
def update():
    try:
        with open("pharmacist/med_update_stock.txt", mode="r", newline="") as f_update:
            reader = csv.reader(f_update)
            update_meds = list(reader)

        if not update_meds:
            raise ValueError("No medicines found in med_update_stock.txt")

        with open("pharmacist/medicine_stock.txt", mode="r", newline="") as f_stock:
            reader = csv.reader(f_stock)
            stock_meds = list(reader)

        stock_dict = {row[0]: row for row in stock_meds if row}

        for med in update_meds:
            if len(med) != 5:
                continue
            barcode, name, qty, price, demand = med
            if barcode in stock_dict:
                existing = stock_dict[barcode]
                existing[2] = str(int(existing[2]) + int(qty))
                existing[3] = price
                existing[4] = demand
            else:
                stock_dict[barcode] = med

        with open("pharmacist/medicine_stock.txt", mode="w", newline="") as f_stock:
            writer = csv.writer(f_stock)
            writer.writerows(stock_dict.values())

        print("Updated Medicines from med_update_stock.txt:")
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
        for row in update_meds:
            if len(row) < 4:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
        print("Medicines Updated Successfully")
        print("\n\n")

    except ValueError as ve:
        print(f"Error: {ve}")


# Function to remove medicines listed in 'med_remove.txt' from the main stock file.
# Reads barcodes to be removed and rewrites the stock file without them.
def remove():
    try:
        remove_ids = []

        with open("pharmacist/med_remove.txt", mode="r", newline="") as f_remove:
            reader = csv.reader(f_remove)
            for row in reader:
                if row and row[0].strip():
                    med_id = row[0].strip().strip(",")
                    remove_ids.append(med_id)

        if not remove_ids:
            raise ValueError("No medicines found in med_remove.txt")

        rows = []
        removed_count = 0
        with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
            reader1 = csv.reader(file)
            for row in reader1:
                if not row or len(row) < 3:
                    continue
                if row[0].strip() in remove_ids:
                    removed_count += 1
                    continue
                rows.append(row)

        with open("pharmacist/medicine_stock.txt", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"{removed_count} medicines removed successfully\n\n")

    except ValueError as ve:
        print(f"Error: {ve}\n\n")


# Function to view all medicines currently in stock.
# Displays barcode, name, quantity, and price for each medicine.
def view():
    with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}")
        for row in reader:
            if len(row) < 4:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
        print("\n\n")


# Function to view a specific medicine by barcode.
# Prompts user for barcode and displays details if found.
def view_spe():
    b = input("Enter the Barcode:")
    w = 0
    with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}")
        for row in reader:
            if len(row) < 4:
                continue
            if row[0] == b:
                print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
                w += 1
        if w == 0:
            print("Barcode Not Found in Database")
        print("\n\n")


# Function to check for medicines with low stock (quantity < 5).
# Prints them and saves the list into 'med_stock_low.txt'.
def view_low():
    data = []
    try:
        with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
            reader = csv.reader(file)
            print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")

            for row in reader:
                if len(row) < 4:
                    continue

                try:
                    quantity = int(row[2])
                except ValueError:
                    continue

                if quantity < 5:
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
                    data.append(row)

        if data:
            try:
                with open("pharmacist/med_stock_low.txt", "w", newline="") as lowfile:
                    writer = csv.writer(lowfile)
                    writer.writerows(data)
            except Exception as e:
                print(f"Error writing to med_stock_low.txt: {e}")

        print("\n\n")

    except FileNotFoundError:
        print("Error: medicine_stock.txt not found.")


# Function to prepare medicines for a patient based on doctor prescriptions.
# Updates stock, sales database, and billing records while calculating total cost.
def prepare(p_id, t_id):
    global total, prows
    total = 0
    prows = []

    with open("pharmacist/medicine_stock.txt", "r", newline="") as f1, \
         open("pharmacist/med_db.txt", "r", newline="") as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)
        rows1 = [row for row in reader1]
        rows2 = [row for row in reader2]

    with open("pharmacist/doctor_prescription.txt", "r", newline="") as f3:
        reader3 = csv.reader(f3)
        prescriptions = [row for row in reader3]

    patient_prescriptions = [
        row for row in prescriptions if row and row[0] == p_id and row[1] == t_id
    ]
    if not patient_prescriptions:
        print(f"No prescriptions found for patient {p_id}")
        return

    for pres in patient_prescriptions:
        if len(pres) < 4:
            continue
        _, _, barcode, qty_needed = pres
        qty_needed = int(qty_needed)

        found = False
        for idx in range(len(rows1)):
            if len(rows1[idx]) < 4:
                continue
            if rows1[idx][0] == barcode:
                found = True
                stock_row = rows1[idx]

                sales_row = next((row for row in rows2 if row and row[0] == barcode), None)

                if sales_row and int(stock_row[2]) >= qty_needed:
                    stock_row[2] = str(int(stock_row[2]) - qty_needed)
                    sales_row[2] = str(int(sales_row[2]) + qty_needed)

                    pr = qty_needed * float(stock_row[3])
                    total += pr
                    prows.append((stock_row[0], stock_row[1], qty_needed, pr))

                    with open("pharmacist/patient_billing_record.txt", "a", newline="") as f_billing:
                        writer = csv.writer(f_billing)
                        today = date.today().strftime("%Y-%m-%d")
                        writer.writerow([today, p_id, barcode, qty_needed, stock_row[3]])
                else:
                    print(f"Not enough stock for {stock_row[1]}")
                break

        if not found:
            print(f"Barcode {barcode} not found in stock.")

    with open("pharmacist/medicine_stock.txt", "w", newline="") as f1, \
         open("pharmacist/med_db.txt", "w", newline="") as f2:
        writer1 = csv.writer(f1)
        writer2 = csv.writer(f2)
        writer1.writerows(rows1)
        writer2.writerows(rows2)

    print("\n\n")


# Function to generate a medicine slip for a patient.
# Calls 'prepare' and then prints a formatted bill with total cost.
def prepare_patient_medicine():
    global total, prows
    
    t_id = input("Enter Token No:")
    p_id = input("Enter Patient ID:")
    prepare(p_id, t_id)

    print("Medicine slip for Patient", p_id)
    print(f"{'|Barcode|':<10}{'|Medicine Name|':<15}{'|Quantity|':<10}{'|Price|':<10}")
    for row in prows:
        print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10.2f}")

    print("TOTAL:                                   ", f"{total:.2f}")
    print("\n\n")


# Function to print a detailed report of all medicines in stock.
# Displays barcode, name, quantity, price, and demand.
def report():
    with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}{'Demand':<10}")
        for row in reader:
            if len(row) < 5:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}{row[4]:<10}")
        print("\n\n")


# Function to check for medicines that are out of stock.
# Prints them and saves the list into 'med_stock_out.txt'.
def banner():
    with open("pharmacist/medicine_stock.txt", "r", newline="") as file:
        reader = csv.reader(file)
        out_of_stock = [row for row in reader if row and len(row) >= 3 and row[2].isdigit() and int(row[2]) == 0]

        if out_of_stock:
            print("The Following Medicines Are Out Of Stock:")
            for row in out_of_stock:
                print(f"{row[0]:<10}{row[1]:<15}")
            with open("pharmacist/med_stock_out.txt", "w", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerows(out_of_stock)
        else:
            print("All medicines are in stock.")

    print("\n\n")


# Main pharmacist menu function.
# Continuously displays options for managing medicine stock until user exits.
def pharmacist():
    while True:
        banner()
        print("Welcome These are the following operations")
        print(
            "\n1. Add Medicine"
            "\n2. Update Medicine"
            "\n3. Remove Medicine"
            "\n4. View All Medicine"
            "\n5. View Specific Medicine"
            "\n6. View Low Stock"
            "\n7. Prepare Patient Medicine"
            "\n8. Print Report"
            "\n9. Exit"
        )
        i = input("What Operation would you like to Perform: ")
        print("\n\n")

        if i == "1":
            add()
        elif i == "2":
            update()
        elif i == "3":
            remove()
        elif i == "4":
            view()
        elif i == "5":
            view_spe()
        elif i == "6":
            view_low()
        elif i == "7":
            prepare_patient_medicine()
        elif i == "8":
            report()
        elif i == "9":
            with open('../login/logged_out.txt','a') as l:
                l.write(f'[{datetime.datetime.now()}] Doctor logged out\n')
            print('Bye. See you tomorrow. Have a great day')
            break
        else:
            print("Invalid choice! Please select a number between 1 and 9.")


if __name__ == "__main__":
    pharmacist()
