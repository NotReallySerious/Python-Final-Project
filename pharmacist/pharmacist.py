import csv

from datetime import date

def add():
    new_file = "med_new_stock.txt"
    stock_file = "medicine_stock.txt"
    try:
        with open("med_new_stock.txt", mode="r", newline="") as f_new:
            reader = csv.reader(f_new)
            new_meds = list(reader)
        if not new_meds:
            raise ValueError("No medicines found in med_new_stock.txt")

        with open("medicine_stock.txt", mode="r", newline="") as f_stock:
            reader = csv.reader(f_stock)
            existing_meds = list(reader)
        existing_barcodes = {row[0] for row in existing_meds}
        for med in new_meds:
            if med[0] in existing_barcodes:
                raise ValueError("These Medicine's already exists in database.")


        with open("medicine_stock.txt", mode="a", newline="") as f_stock:
            writer = csv.writer(f_stock)
            writer.writerows(new_meds)
        print("Medicines from med_new_stock.txt:")
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
        for row in new_meds:
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
        print("Medicines Added Successfully")
        print("\n\n")
        
    except ValueError as ve:
        print(f"Error: {ve}")


def update():
    try:
        with open("med_update_stock.txt", mode="r", newline="") as f_update:
            reader = csv.reader(f_update)
            update_meds = list(reader)
            
        if not update_meds:
            raise ValueError("No medicines found in med_update_stock.txt")
        
        with open("medicine_stock.txt", mode="r", newline="") as f_stock:
            reader = csv.reader(f_stock)
            stock_meds = list(reader)

        stock_dict = {row[0]: row for row in stock_meds}

        for med in update_meds:
            barcode, name, qty, price, demand = med
            if barcode in stock_dict:
                existing = stock_dict[barcode]
                existing[2] = str(int(existing[2]) + int(qty))
                existing[3] = price
                existing[4] = demand
            else:
                stock_dict[barcode] = med

        with open("medicine_stock.txt", mode="w", newline="") as f_stock:
            writer = csv.writer(f_stock)
            writer.writerows(stock_dict.values())
            
        print("Updated Medicines from med_update_stock.txt:")
        
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
        for row in update_meds:
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")

        print("Medicines Updated Successfully")
        print("\n\n")

    except ValueError as ve:
        print(f"Error: {ve}")

def remove():
    try:
        with open("med_remove.txt", mode="r", newline="") as f_remove:
            reader = csv.reader(f_remove)
            remove_meds = list(reader)
            for row in reader:
                if row:
                   med_id = row[0].strip().strip(",")
                   if med_id:
                       remove_meds.append(med_id)
            
        if not remove_meds:
            raise ValueError("No medicines found in med_remove.txt")
        rows = []
        with open("medicine_stock.txt", "r") as file:
            reader1 = csv.reader(file)
            for row in reader1:
                if len(row) < 3:
                    continue
                if row[0].strip() in remove_meds:
                    continue
                else :
                    rows.append(row)
        with open("medicine_stock.txt", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print("Medicine Removed Succesfully")
        print("\n\n")
        
    except ValueError as ve:
        print(f"Error: {ve}")
        print("\n\n")


def view():
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}")
        for row in reader:
            if len(row) < 3:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
        print("\n\n")

def view_spe():
    b = input("Enter the Barcode:")
    w = 0
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}")
        for row in reader:
            if len(row) < 3:
                continue
            if row[0] == b :
                print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
                w += 1
        if w == 0 :
            print(f'Barcode Not Found in Database')
        print("\n\n")
    
def view_low():
    data = []
    try:
        with open("medicine_stock.txt", "r") as file:
            reader = csv.reader(file)
            print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
            
            for row in reader:

                if len(row) < 3:
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
                with open("med_stock_low.txt", "w", newline="") as lowfile:
                    writer = csv.writer(lowfile)
                    writer.writerows(data)
            except Exception as e:
                print(f"Error writing to med_stock_low.txt: {e}")

        print("\n\n")

    except FileNotFoundError:
        print("Error: medicine_stock.txt not found.")

def prepare(p_id,t_id):
    global total, prows
    total = 0
    prows = []

    with open("medicine_stock.txt", "r") as f1, \
         open("med_db.txt", "r") as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)
        rows1 = [row for row in reader1]
        rows2 = [row for row in reader2]

    with open("doctor_prescription.txt", "r") as f3:
        reader3 = csv.reader(f3)
        prescriptions = [row for row in reader3]
        
    patient_prescriptions = [row for row in prescriptions if row[0] == p_id and row[1] == t_id]
    if not patient_prescriptions:
        print(f"No prescriptions found for patient {p_id}")
        return
    

    for pres in patient_prescriptions:
        _, _, barcode, qty_needed = pres
        qty_needed = int(qty_needed)

        found = False
        for idx in range(len(rows1)):
            if len(rows1[idx]) < 3:  
                continue
            if rows1[idx][0] == barcode:
                found = True
                stock_row = rows1[idx]
    
                sales_row = next((row for row in rows2 if row[0] == barcode), None)

                if sales_row and int(stock_row[2]) >= qty_needed:
                  
                    stock_row[2] = str(int(stock_row[2]) - qty_needed)
                    sales_row[2] = str(int(sales_row[2]) + qty_needed)

                    pr = qty_needed * float(stock_row[3])
                    total += pr
                    prows.append((stock_row[0], stock_row[1], qty_needed, pr))
                    with open("patient_billing_record.txt", "a", newline="") as f_billing:
                        writer = csv.writer(f_billing)
                        today = datetime.now().strftime("%Y-%m-%d")
                        writer.writerow([today, p_id, barcode, qty_needed, stock_row[3]])  
                else:
                    print(f"Not enough stock for {stock_row[1]}")
                break

        if not found:
            print(f"Barcode {barcode} not found in stock.")
            
    with open("medicine_stock.txt", "w", newline="") as f1, \
         open("med_db.txt", "w", newline="") as f2:
        writer1 = csv.writer(f1)
        writer2 = csv.writer(f2)
        writer1.writerows(rows1)
        writer2.writerows(rows2)

    print("\n\n")


        

def prepare_patient_medicine():
    global total, prows
    t_id = input("Enter Token No.")
    p_id = input("Enter Patient ID:")
    prepare(p_id,t_id)

    print("Medicine slip for Patient", p_id)
    print(f"{'|Barcode|':<10}{'|Medicine Name|':<15}{'|Quantity|':<10}{'|Price|':<10}")
    for row in  prows:
        print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10.2f}")


    
    print("TOTAL:                                   ", f"{total:.2f}")
    print("\n\n") 
    
def report():
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}{'Demand':<10}")
        for row in reader:
            if len(row) < 3:
                continue
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}{row[4]:<10}")
        print("\n\n")

def banner():
    with open("pharmacist/medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        out_of_stock = [row for row in reader if len(row) >= 3 and int(row[2]) == 0]

        if out_of_stock:
            print("The Following Medicines Are Out Of Stock:")
            for row in out_of_stock:
                print(f"{row[0]:<10}{row[1]:<15}")
            with open("med_stock_out.txt", "w", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerows(out_of_stock)
        else:
            print("All medicines are in stock.")

    print("\n\n")
                    

def pharmasist():
    while True:
        banner()
        print("Welcome These are the following operations")
        print(("\n1. Add Medicine\n2. Update Medicine\n3. Remove Medicine\n4. View All Medicine \n5. View Specific Medicine\n6. View Low Stock\n7. Prepare Patient Medicine\n8. Print Report\n9. Exit"))
        try:
            i = str(input("What Operation would you like to Perform: "))
            print("\n\n")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")
            continue  

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
            break
        else:
            print("Invalid choice! Please select a number between 1 and 9.")



        
