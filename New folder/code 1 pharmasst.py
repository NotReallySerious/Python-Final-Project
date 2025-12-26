import csv


def add():
    i = int(input("How many Medicines do you want to add?"))
    for t in range(i):
        b = input("Enter the Barcode:")
        n = input("Enter the Name:")
        qy = (input("Enter the Quantity in stock:"))
        p = (input("Enter the Price:"))
        d = input("Enter the Demand Status(Low/Moderate/High):")
        with open("medicine_stock.txt", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([b, n, qy, p, d])
    print("Medicines Added Succesfully")
    print("\n\n")

    
def update():
    b = input("Enter the Barcode:")
    qy =(input("Enter the Quantity in stock:"))
    p = (input("Enter the Price:"))
    d = input("Enter the Demand Status:")
    rows = []
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 6:
                continue
            if row[0] == b:
                row[2] = str(qy)
                row[3] = str(p)
                row[4] = str(d)
            rows.append(row)
    with open("medicine_stock.txt", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("Medicine Updated Succesfully")
    print("\n\n")
    
def remove():
    b = input("Enter the Barcode:")
    rows =[]
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 6:
                continue
            if row[0] == b:
                continue
            else :
                rows.append(row)
    with open("medicine_stock.txt", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("Medicine Removed Succesfully")
    print("\n\n")


def view():
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Price':<10}")
        for row in reader:
            if len(row) < 6:
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
            if len(row) < 6:
                continue
            if row[0] == b :
                print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}")
                w += 1
        if w == 0 :
            print(f'Barcode Not Found in Database')
        print("\n\n")
    

def view_low():
     with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        print(f"{'Barcode':<10}{'Medicine Name':<15}{'Quantity':<10}{'Demand':<10}")
        for row in reader:
            if len(row) < 6:
                continue
            if int(row[2]) < 5 :
                print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[4]:<10}")
        print("\n\n")

def prepare(i):
    global total, prows
    total = 0
    prows = []

    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    for _ in range(i):
        barcode = input("Enter the barcode of the Medicine:")
        qty_needed = int(input("Enter the Quantity of the Medicine:"))

        found = False
        for row in rows:
            if row[0] == barcode:
                found = True
                if len(row) < 1:
                    continue
                if int(row[2]) >= qty_needed:
                    row[2] = str(int(row[2]) - qty_needed)
                    pr = qty_needed * float(row[3])
                    total += pr
                    prows.append((row[0], row[1], qty_needed, pr))
                else:
                    print(f"Not enough stock for {row[1]}")
                break

        if not found:
            print("Barcode not found.")

    with open("medicine_stock.txt", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("\n\n")

        

def prepare_patient_medicine():
    global total, prows
    i = int(input("Enter no. of Medicines Prescribed:"))
    
    p_id = input("Enter Patient ID:")
    prepare(i)

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
            print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}{row[4]:<10}")
        print("\n\n")

def banner():
    with open("medicine_stock.txt", "r") as file:
        reader = csv.reader(file)
        out_of_stock = [row for row in reader if len(row) >= 3 and row[2].isdigit() and int(row[2]) == 0]

        if out_of_stock:
            print("The Following Medicines Are Out Of Stock:")
            for row in out_of_stock:
                print(f"{row[0]:<10}{row[1]:<15}")
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


pharmasist()

        
