import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import heapq

class ShipmentManager:
    def __init__(self):
        self.shipments = {}

    def add_shipment(self, shipment_id, customer_id, location, destination):
        if shipment_id in self.shipments:
            return False
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.shipments[shipment_id] = {
            "customer_id": customer_id,
            "date": current_date,
            "status": "New",
            "location": location,
            "destination": destination
        }
        return True

    def get_shipment_by_customer(self, customer_id):
        return [
            {"id": sid, **details} for sid, details in self.shipments.items() if details["customer_id"] == customer_id
        ]

    def update_status(self, shipment_id, new_status):
        if shipment_id in self.shipments:
            self.shipments[shipment_id]["status"] = new_status
            print(f"Shipment {shipment_id} updated to status: {new_status}")  # Güncelleme kontrolü
        else:
            print(f"Shipment {shipment_id} not found.")

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, shipment_id, priority):
        heapq.heappush(self.heap, (priority, shipment_id))

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def get_all(self):
        return sorted(self.heap)

shipment_manager = ShipmentManager()
priority_queue = PriorityQueue()

class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer_id, name):
        if any(c["customer_id"] == customer_id for c in self.customers):
            return False
        self.customers.append({"customer_id": customer_id, "name": name})
        return True

    def get_customers(self):
        return self.customers

customer_manager = CustomerManager()

def main_gui():
    root = tk.Tk()
    root.title("Logistics Management System")
    root.geometry("1920x1080")

    tab_control = ttk.Notebook(root)

    # Customer Management Tab
    customer_tab = ttk.Frame(tab_control)
    tab_control.add(customer_tab, text="Customer Management")

    tk.Label(customer_tab, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(customer_tab, text="Name:").grid(row=1, column=0, padx=5, pady=5)

    customer_id_entry_1 = tk.Entry(customer_tab)
    customer_id_entry_1.grid(row=0, column=1, padx=5, pady=5)

    name_entry = tk.Entry(customer_tab)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
   
    def update_customer_list_and_dropdown():
        update_customer_list()
        update_customer_dropdown()
   
    def add_customer():
        customer_id = customer_id_entry_1.get()
        name = name_entry.get()

        if not customer_id or not name:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not customer_id.isdigit():
            messagebox.showerror("Error", "Customer ID must be a number.")
            return

        if customer_manager.add_customer(int(customer_id), name):
            messagebox.showinfo("Success", "Customer added successfully.")
            update_customer_list_and_dropdown()
        else:
            messagebox.showerror("Error", "Customer ID already exists.")

    def update_customer_list():
        for row in customer_tree.get_children():
            customer_tree.delete(row)

        for customer in customer_manager.get_customers():
            customer_tree.insert("", "end", values=(customer["customer_id"], customer["name"]))

    add_button = tk.Button(customer_tab, text="Add Customer", command=add_customer)
    add_button.grid(row=2, column=0, columnspan=2, pady=10)

    customer_tree = ttk.Treeview(customer_tab, columns=("Customer ID", "Name"), show="headings")
    customer_tree.heading("Customer ID", text="Customer ID")
    customer_tree.heading("Name", text="Name")
    customer_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    update_customer_list()

    # Shipment History Tab
    shipment_tab = ttk.Frame(tab_control)
    tab_control.add(shipment_tab, text="Shipment History")
    
    customer_dropdown = ttk.Combobox(shipment_tab, state="readonly")
    customer_dropdown.grid(row=0, column=1, padx=5, pady=5)
    def update_customer_dropdown():
        customer_dropdown['values'] = [f'{c["customer_id"]}: {c["name"]}' for c in customer_manager.get_customers()]
        if customer_dropdown['values']:
            customer_dropdown.current(0)  # İlk öğeyi seçili yap
    
    update_customer_dropdown()
    

    tk.Label(shipment_tab, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(shipment_tab, text="Shipment ID:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(shipment_tab, text="Location:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(shipment_tab, text="Destination:").grid(row=3, column=0, padx=5, pady=5)

    customer_id_entry = tk.Entry(shipment_tab)
    customer_id_entry.grid(row=0, column=1, padx=5, pady=5)

    shipment_id_entry = tk.Entry(shipment_tab)
    shipment_id_entry.grid(row=1, column=1, padx=5, pady=5)

    location_entry = ttk.Combobox(shipment_tab, values=["CityA", "CityB", "CityC", "CityD", "CityE", "CityF"])
    location_entry.grid(row=2, column=1, padx=5, pady=5)

    destination_entry = ttk.Combobox(shipment_tab, values=["CityA", "CityB", "CityC", "CityD", "CityE", "CityF"])
    destination_entry.grid(row=3, column=1, padx=5, pady=5)

    # Shipment Treeview
    shipment_tree = ttk.Treeview(shipment_tab, columns=("ID", "Date", "Status", "Location", "Destination"), show="headings")
    shipment_tree.heading("ID", text="Shipment ID")
    shipment_tree.heading("Date", text="Date")
    shipment_tree.heading("Status", text="Status")
    shipment_tree.heading("Location", text="Location")
    shipment_tree.heading("Destination", text="Destination")
    shipment_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def add_shipment():
        if not shipment_id_entry.get() or not customer_dropdown.get() or not location_entry.get() or not destination_entry.get():
            messagebox.showerror("Error", "All fields are required.")
            return

        customer_id = customer_dropdown.get().split(":")[0]  # ID kısmını ayır
        shipment_id = shipment_id_entry.get()
        location = location_entry.get()
        destination = destination_entry.get()

        if shipment_manager.add_shipment(shipment_id, customer_id, location, destination):
            priority_queue.push(shipment_id, 1)  # Example priority
            messagebox.showinfo("Success", "Shipment added successfully.")
            update_treeview()
        else:
            messagebox.showerror("Error", "Shipment ID already exists.")

    add_shipment_button = tk.Button(shipment_tab, text="Add Shipment", command=add_shipment)
    add_shipment_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_treeview():
        cost_matrix = {
            "CityA": {"CityA": 0, "CityB": 1, "CityC": 2, "CityD": 3, "CityE": 4, "CityF": 5},
            "CityB": {"CityA": 1, "CityB": 0, "CityC": 1, "CityD": 2, "CityE": 3, "CityF": 4},
            "CityC": {"CityA": 2, "CityB": 1, "CityC": 0, "CityD": 1, "CityE": 2, "CityF": 3},
            "CityD": {"CityA": 3, "CityB": 2, "CityC": 1, "CityD": 0, "CityE": 1, "CityF": 2},
            "CityE": {"CityA": 4, "CityB": 3, "CityC": 2, "CityD": 1, "CityE": 0, "CityF": 1},
            "CityF": {"CityA": 5, "CityB": 4, "CityC": 3, "CityD": 2, "CityE": 1, "CityF": 0},
        }

        # Eski veriyi temizle
        shipment_tree.delete(*shipment_tree.get_children())

        # Gönderileri sıralamak için bir liste oluştur
        sorted_shipments = []
        for shipment_id, data in shipment_manager.shipments.items():
            location = data["location"]
            destination = data["destination"]
            priority = cost_matrix[location][destination]  # Maliyet matrisinden öncelik al
            sorted_shipments.append((priority, shipment_id, data))

        # Önceliğe göre sırala
        sorted_shipments.sort(key=lambda x: x[0])  # Maliyete göre sıralama

        # Treeview'a sıralanmış gönderileri ekle
        for _, shipment_id, data in sorted_shipments:
            shipment_tree.insert("", "end", values=(
                shipment_id, data["date"], data["status"], data["location"], data["destination"]
            ))

    def view_shipment_history():
        def show_popup():
            customer_id = popup_entry.get()
            if not customer_id:
                messagebox.showerror("Error", "Customer ID is required.")
                return

            popup = tk.Toplevel(root)
            popup.title("Shipment History")

            popup_tree = ttk.Treeview(popup, columns=("ID", "Date", "Status", "Location", "Destination"), show="headings")
            popup_tree.heading("ID", text="Shipment ID")
            popup_tree.heading("Date", text="Date")
            popup_tree.heading("Status", text="Status")
            popup_tree.heading("Location", text="Location")
            popup_tree.heading("Destination", text="Destination")
            popup_tree.pack(fill="both", expand=True)

            shipments = shipment_manager.get_shipment_by_customer(customer_id)
            for shipment in shipments:
                popup_tree.insert("", "end", values=(shipment["id"], shipment["date"], shipment["status"], shipment["location"], shipment["destination"]))

        popup = tk.Toplevel(root)
        popup.title("Enter Customer ID")
        tk.Label(popup, text="Customer ID:").pack(pady=5)
        popup_entry = tk.Entry(popup)
        popup_entry.pack(pady=5)
        tk.Button(popup, text="View History", command=show_popup).pack(pady=10)

    def change_status(event):
        selected_item = shipment_tree.selection()
        if not selected_item:
            return

        shipment_id = shipment_tree.item(selected_item[0])['values'][0]  # Seçilen kargonun ID'sini al

        def update_status(shipment_id, new_status):
            shipment_id = str(shipment_id)  # ID'yi string yap
            if shipment_id in shipment_manager.shipments:
                shipment_manager.shipments[shipment_id]["status"] = new_status
                print(f"Shipment {shipment_id} updated to status: {new_status}")
                update_treeview()  # Treeview'i güncelle
            else:
                print(f"Shipment {shipment_id} not found.")  # Hata mesajı
        # Yeni bir popup penceresi oluştur
        status_popup = tk.Toplevel(root)
        status_popup.title("Update Status")
        tk.Label(status_popup, text="Select new status:").pack(pady=5)

        # Olası durumlar için butonlar
        for status in ["Processing", "In Transit", "Delivered"]:
           tk.Button(
                status_popup,
                text=status,
                command=lambda s=status: update_status(shipment_id, s)
            ).pack(pady=5)

    shipment_tree.bind("<Double-1>", change_status)

    add_shipment_button = tk.Button(shipment_tab, text="Add Shipment", command=add_shipment)
    add_shipment_button.grid(row=4, column=0, columnspan=2, pady=10)

    view_history_button = tk.Button(shipment_tab, text="View Shipment History", command=view_shipment_history)
    view_history_button.grid(row=5, column=0, columnspan=2, pady=10)

    tab_control.pack(expand=1, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main_gui()
