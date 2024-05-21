import tkinter as tk
from tkinter import simpledialog, ttk
import sqlite3
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from tkinter import Label, LEFT
from datetime import datetime
from tkinter import Frame
from tkinter import BOTH
from tkinter import ttk, Scrollbar, VERTICAL, Y, RIGHT
from tkinter import PhotoImage
import sys
import uuid


# Database setup
try:
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY_PRODUCTS (
                             PRODUCT_ID TEXT PRIMARY KEY,
                             NAME TEXT,
                             FLAVOR TEXT,
                             SIZE INT,
                             PRICE REAL,
                             QUANTITY INT,
                             PRODUCTION_DATE TEXT,
                             EXPIRY_DATE TEXT                  
                         );''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY_RAW (
                             MATERIAL_ID TEXT PRIMARY KEY,
                             NAME TEXT,
                             SUPPLIER TEXT,
                             UNIT_PRICE REAL,
                             STOCK_QTY INT,
                             ORDER_THRESHOLD TEXT,
                             EXPIRY_DATE TEXT,
                             LEAD_TIME TEXT,
                             STORE_LOCATION TEXT
                         );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER_SALES (
                            ORDER_ID TEXT ,
                            CUSTOMER_ID TEXT ,
                            PRODUCT_ID TEXT ,
                            PRODUCT_NAME TEXT ,
                            PAYMENT_METHOD TEXT ,
                            PAYMENT_STATUS TEXT 
                        );''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS RETAILER_SALES (
                            ORDER_ID TEXT ,
                            RETAILER_ID TEXT ,
                            PRODUCT_ID TEXT ,
                            PRODUCT_NAME TEXT ,
                            PAYMENT_METHOD TEXT ,
                            PAYMENT_STATUS TEXT 
                        );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS WAREHOUSE_ITEMS (
                             WAREHOUSE_ID TEXT,
                             LOCATION TEXT,
                             SIZE TEXT,
                             TEMPERATURE_ZONE TEXT,
                             PRODUCT_ID TEXT,
                             PRODUCT_NAME TEXT,
                             QUANTITY INT
                         );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS WAREHOUSE_RAW_MATERIALS (
                             WAREHOUSE_ID TEXT,
                             LOCATION TEXT,
                             SIZE TEXT,
                             TEMPERATURE_ZONE TEXT,
                             MATERIAL_ID TEXT,
                             MATERIAL_NAME TEXT,
                             QUANTITY INT
                         );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS SUPPLIERS (
                             SUPPLIER_ID TEXT PRIMARY KEY,
                             SUPPLIER_NAME TEXT,
                             CONTACT_PERSON TEXT,
                             EMAIL TEXT,
                             PHONE TEXT,
                             ADDRESS TEXT,
                             PRODUCTS_SUPPLIED TEXT,
                             LEAD_TIME TEXT,
                             PAYMENT_TERMS TEXT
                         );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER_ORDERS (
                      ORDER_ID TEXT PRIMARY KEY,
                      CUSTOMER_ID TEXT,
                      DATE TEXT,
                      STATUS TEXT,
                      TOTAL_AMOUNT REAL,
                      PRODUCT_ID TEXT,
                      PRODUCT_NAME TEXT,
                      PRICE REAL,
                      DELIVERY_ADDRESS TEXT         
                         );''')


    

    conn.commit()
except sqlite3.Error as e:
    print("Database error:", e)

class SCM:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Supply Chain Management")
        self.root.config(bg="white")

        # Load and resize the image
        try:
            self.logo_image = Image.open("image/truck.png")
            self.logo_image = self.logo_image.resize((150, 150))
            self.icon_title = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            self.icon_title = None

        title = tk.Label(self.root, text="Supply Chain Management System", image=self.icon_title, compound=tk.LEFT,
                         font=("Bauhaus 93", 40, "bold"), bg="white", fg="#492E87", anchor="w")
        title.pack(fill=tk.X)

        # Clock
        self.lbl_clock = Label(self.root, text="", font=("Ariel", 12), bg="#FFF455", fg="black")
        self.lbl_clock.place(x=0, y=135, relwidth=1, height=20)

        self.update_clock() # Call the function to update clock initially


        # Left Menu
        left_menu = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="White", width=100, height=300)
        left_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Image icon aside dashboard button
        dash_image = PhotoImage(file="image/dash.png")  
        # Resize the image to 100x100 pixels
        dash_image_resized = dash_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_dashboard = tk.Button(left_menu, text="Dashboard", font=("Arial", 15, "bold"), bg="#9E61FF", height=70,
                                   command=self.open_dashboard, compound="top", image=dash_image_resized)
        btn_dashboard.image = dash_image_resized
        btn_dashboard.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside inventory button
        invent_image = PhotoImage(file="image/invent.png")  
        # Resize the image to 100x100 pixels
        invent_image_resized = invent_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_inventory = tk.Button(left_menu, text="Main Inventory", font=("Arial", 15, "bold"), bg="#9E61FF", height=70,
                                   command=self.open_inventory, compound="top", image=invent_image_resized)
        btn_inventory.image = invent_image_resized
        btn_inventory.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside warehouse button
        ware_image = PhotoImage(file="image/ware.png")  
        # Resize the image to 100x100 pixels
        ware_image_resized = ware_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_warehouse = tk.Button(left_menu, text="Warehouse", font=("Arial", 15, "bold"), bg="#9E61FF", height=70, command=self.open_warehouse_management, compound="top", image=ware_image_resized, padx=10)
        btn_warehouse.image = ware_image_resized
        btn_warehouse.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside order button
        order_image = PhotoImage(file="image/order.png")  
        # Resize the image to 100x100 pixels
        order_image_resized = order_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_order = tk.Button(left_menu, text="Order Management", font=("Arial", 15, "bold"), bg="#9E61FF", height=70, command=self.open_order_management, compound="top", image=order_image_resized)
        btn_order.image = order_image_resized
        btn_order.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside supplier button
        sup_image = PhotoImage(file="image/sup.png")  
        # Resize the image to 100x100 pixels
        sup_image_resized = sup_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_supplier = tk.Button(left_menu, text="Suppliers", font=("Arial", 15, "bold"), bg="#9E61FF", height=70, command=self.open_supplier_management, compound="top", image=sup_image_resized)
        btn_supplier.image = sup_image_resized
        btn_supplier.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside sales button
        sale_image = PhotoImage(file="image/sale.png")  
        # Resize the image to 100x100 pixels
        sale_image_resized = sale_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_sales = tk.Button(left_menu, text="Sales", font=("Arial", 15, "bold"), bg="#9E61FF", height=70, command=self.open_sales, compound="top", image=sale_image_resized)
        btn_sales.image = sale_image_resized
        btn_sales.pack(side=tk.TOP, fill=tk.X)

        # Image icon aside exit button
        exit_image = PhotoImage(file="image/exit.png")  
        # Resize the image to 100x100 pixels
        exit_image_resized = exit_image.subsample(20) # Adjust the parameter to resize as per your requirement
        btn_exit = tk.Button(left_menu, text="Exit", font=("Arial", 15, "bold"), bg="#9E61FF", height=70, command=self.close_window, compound="top", image=exit_image_resized)
        btn_exit.image = exit_image_resized
        btn_exit.pack(side=tk.TOP, fill=tk.X)

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        self.dashboard_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.open_dashboard()



        # Schedule the function to run again after 1 minutes
        self.root.after(60000, self.check_inventory_levels) # Check every 1 minutes (60000 milliseconds)


    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S") # Format the current time
        current_date = now.strftime("%d-%m-%Y") # Format the current date
        self.lbl_clock.config(
            text=f"Welcome to Supply Chain Management Application \t\t Date: {current_date} \t\t Time: {current_time}")
        self.root.after(1000, self.update_clock) # Update the clock every second

    def open_dashboard(self):
        # Hide the warehouse frame
        self.dashboard_frame.pack_forget()

        # Clear the warehouse frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        self.update_dashboard_info()



    # Repack the dashboard frame
        self.dashboard_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def update_dashboard_info(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Query the database for counts
        try:
            cursor.execute("SELECT COUNT(*) FROM INVENTORY_PRODUCTS")
            total_products = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM INVENTORY_RAW")
            total_materials = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM CUSTOMER_SALES")
            total_csales = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM RETAILER_SALES")
            total_rsales = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM WAREHOUSE_ITEMS")
            total_pwarehouse = cursor.fetchone()[0]     

            cursor.execute("SELECT COUNT(*) FROM WAREHOUSE_RAW_MATERIALS")
            total_rwarehouse = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM CUSTOMER_ORDERS")
            total_corders = cursor.fetchone()[0]     

            cursor.execute("SELECT COUNT(*) FROM SUPPLIERS")
            total_suppliers = cursor.fetchone()[0]            
            

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

        # Function to create a box with a label
        def create_info_box(frame, text, bg_color="white", fg_color="black"):
            box = tk.Frame(frame, bg=bg_color, bd=2, relief=tk.RIDGE)
            box.pack(side=tk.LEFT, padx=10, pady=10)
            label = tk.Label(box, text=text, font=("Arial", 15), bg=bg_color, fg=fg_color)
            label.pack(padx=10, pady=10)

        # Create a container for the information boxes
        info_container = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        info_container.pack(fill=tk.X)

        info_container2 = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        info_container2.pack(fill=tk.X)


        # Display the counts in boxes on the dashboard
        create_info_box(info_container, f"Total Products:\n {total_products}", bg_color="#FFEBD8")
        create_info_box(info_container, f"Total Raw Materials:\n{total_materials}", bg_color="#F2F597")
        create_info_box(info_container, f"Total Customer Sales:\n {total_csales}", bg_color="#8DDFCB")
        create_info_box(info_container, f"Total Retailer Sales:\n {total_rsales}", bg_color="#EED3D9")
        create_info_box(info_container2, f"Total Product Warehouses:\n {total_pwarehouse}", bg_color="#C68484")
        create_info_box(info_container2, f"Total Raw Material Warehouses:\n {total_rwarehouse}", bg_color="#BFD8AF")
        create_info_box(info_container2, f"Total Customer Orders:\n {total_corders}", bg_color="#FAF3F0")
        create_info_box(info_container2, f"Total Suppliers:\n {total_suppliers}", bg_color="#E2F6CA")
        
        self.load_and_display_image_below_info_boxes()

    def load_and_display_image_below_info_boxes(self):
        try:
            original_image = tk.PhotoImage(file="image/scm.png")
            resized_image = original_image.subsample(2)
            image_label = tk.Label(self.dashboard_frame, image=resized_image, bg="white")
            image_label.pack(pady=20)
            self.image = resized_image # Keep a reference to the image
        except tk.TclError:
            messagebox.showerror("Error", "Failed to load the image. Please check the file path.")


  
        

    def open_inventory(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
            
        title = tk.Label(self.dashboard_frame, text="Inventory Management", font=("Arial", 30, "bold"), bg="white",
                         fg="#9E61FF")
        title.pack(pady=20)

        button = tk.Button(self.dashboard_frame, text="Add Finished Products", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_invent)
        button.pack(side=tk.TOP, padx=20, pady=10)

        button = tk.Button(self.dashboard_frame, text="Add Raw Materials", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_raw_invent)
        button.pack(side=tk.TOP, padx=20, pady=10)

    def open_invent(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        

        # Add Product Section
        add_product_button = tk.Button(self.dashboard_frame, text="Add Product", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_add_product_frame)
        add_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # Remove Product Section
        remove_product_button = tk.Button(self.dashboard_frame, text="Remove Product", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_remove_product_frame)
        remove_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Inventory Section
        view_inventory_button = tk.Button(self.dashboard_frame, text="View Inventory", font=("Arial", 20, "bold"),
                                           bg="#FFF455", bd=3, command=self.open_view_inventory_frame)
        view_inventory_button.pack(side=tk.TOP, padx=20, pady=10)

        # Update Product Section
        update_product_button = tk.Button(self.dashboard_frame, text="Update Product", font=("Arial", 20, "bold"),
                                         bg="#FFF455", bd=3, command=self.open_update_product_frame)
        update_product_button.pack(side=tk.TOP, padx=20, pady=10)


    def open_raw_invent(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Add Product Section
        add_product_button = tk.Button(self.dashboard_frame, text="Add Raw Material", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_add_raw_frame)
        add_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # Remove Product Section
        remove_product_button = tk.Button(self.dashboard_frame, text="Remove Raw Material", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_remove_raw_frame)
        remove_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Inventory Section
        view_inventory_button = tk.Button(self.dashboard_frame, text="View Raw Material Inventory", font=("Arial", 20, "bold"),
                                           bg="#FFF455", bd=3, command=self.open_view_inventory_raw_frame)
        view_inventory_button.pack(side=tk.TOP, padx=20, pady=10)

        # Update Raw Material Section
        update_raw_button = tk.Button(self.dashboard_frame, text="Update Raw Material", font=("Arial", 20, "bold"),
                                      bg="#FFF455", bd=3, command=self.open_update_raw_frame)
        update_raw_button.pack(side=tk.TOP, padx=20, pady=10)


    def open_add_product_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_product_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_product_label = tk.Label(add_product_frame, text="Add Product to Inventory", font=("Arial", 20, "bold"),
                                     bg="white")
        add_product_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["PRODUCT_ID", "NAME", "FLAVOR", "SIZE", "PRICE", "QUANTITY", "PRODUCTION_DATE",
                        "EXPIRY_DATE"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_product_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_product_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the product
        add_button = tk.Button(add_product_frame, text="Add", font=("Arial", 15, "bold"), bg="yellow",
                               command=lambda: self.add_product(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_product_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)

    def open_remove_product_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Remove Product from Inventory", font=("Arial", 30, "bold"),
                         bg="white", fg="purple")
        title.pack(pady=20)

        # Remove Product Section
        remove_product_label = tk.Label(self.dashboard_frame, text="Product Name:", font=("Arial", 20), bg="white")
        remove_product_label.pack(pady=5)

        self.remove_product_entry = tk.Entry(self.dashboard_frame, font=("Arial", 20))
        self.remove_product_entry.pack(pady=5)

        remove_button = tk.Button(self.dashboard_frame, text="Remove", font=("Arial", 20, "bold"), bg="yellow",
                                 command=self.remove_product)
        remove_button.pack(pady=10)

        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.pack(pady=10)

    def open_view_inventory_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Main Inventory", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("ID", 60), ("Name", 170), ("Flavor", 100), ("Size", 60), ("Price", 100), ("Quantity", 60),
                   ("Production Date", 130), ("Expiry Date", 130)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM INVENTORY_PRODUCTS")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.pack(pady=10)


    def open_update_product_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        update_product_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        update_product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        update_product_label = tk.Label(update_product_frame, text="Update Product", font=("Arial", 20, "bold"),
                                        bg="white")
        update_product_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["PRODUCT_ID", "NAME", "FLAVOR", "SIZE", "PRICE", "QUANTITY", "PRODUCTION_DATE", "EXPIRY_DATE"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(update_product_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_product_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to update the product
        update_button = tk.Button(update_product_frame, text="Update", font=("Arial", 15, "bold"), bg="yellow",
                                  command=lambda: self.update_product(entry_fields))
        update_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(update_product_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)


    def update_product(self, entry_fields):
        # Extract values from the entry fields dictionary
        values = [entry_fields[key].get() for key in entry_fields]
        product_id = values[0] # Assuming the first entry is the PRODUCT_ID

        try:
            cursor.execute('''UPDATE INVENTORY_PRODUCTS SET NAME = ?, FLAVOR = ?, SIZE = ?, PRICE = ?, QUANTITY = ?, PRODUCTION_DATE = ?, EXPIRY_DATE = ? 
                              WHERE PRODUCT_ID = ?;''', (values[1], values[2], values[3], values[4], values[5], values[6], values[7], product_id))
            conn.commit() # Commit changes to the database
            print(f"Product with ID {product_id} updated in the database.")
            messagebox.showinfo("Success", f"Product updated successfully.") # Show success message
        except sqlite3.Error as e:
            print("Database error:", e)


    

    def open_add_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_raw_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_raw_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_raw_label = tk.Label(add_raw_frame, text="Add Raw Material to Inventory", font=("Arial", 20, "bold"),
                                     bg="white")
        add_raw_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["MATERIAL_ID", "NAME", "SUPPLIER", "UNIT_PRICE", "STOCK_QTY", "ORDER_THRESHOLD", "EXPIRY_DATE", "LEAD_TIME", "STORE_LOCATION"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_raw_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_raw_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the product
        add_button = tk.Button(add_raw_frame, text="Add", font=("Arial", 15, "bold"), bg="yellow",
                               command=lambda: self.add_raw(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_raw_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)

    def open_remove_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Remove Raw Material from Inventory", font=("Arial", 30, "bold"),
                         bg="white", fg="purple")
        title.pack(pady=20)

        # Remove Product Section
        remove_raw_label = tk.Label(self.dashboard_frame, text="Material Name:", font=("Arial", 20), bg="white")
        remove_raw_label.pack(pady=5)

        self.remove_raw_entry = tk.Entry(self.dashboard_frame, font=("Arial", 20))
        self.remove_raw_entry.pack(pady=5)

        remove_button = tk.Button(self.dashboard_frame, text="Remove", font=("Arial", 20, "bold"), bg="yellow",
                                 command=self.remove_raw)
        remove_button.pack(pady=10)

        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_raw_invent)
        back_button.pack(pady=10)

    def open_view_inventory_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Raw Material Inventory", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("ID", 60), ("Name", 150), ("Supplier", 120), ("Unit Price", 60), ("Stock Quantity", 60), ("Order Threshold", 60),
                   ("Expiry Date", 130), ("Lead Time", 80), ("Storage Location", 130)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM INVENTORY_RAW")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_raw_invent)
        back_button.pack(pady=10)


    def open_update_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        update_raw_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        update_raw_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        update_raw_label = tk.Label(update_raw_frame, text="Update Raw Material", font=("Arial", 20, "bold"),
                                    bg="white")
        update_raw_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["MATERIAL_ID", "NAME", "SUPPLIER", "UNIT_PRICE", "STOCK_QTY", "ORDER_THRESHOLD", "EXPIRY_DATE", "LEAD_TIME", "STORE_LOCATION"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(update_raw_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_raw_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to update the raw material
        update_button = tk.Button(update_raw_frame, text="Update", font=("Arial", 15, "bold"), bg="yellow",
                                  command=lambda: self.update_raw(entry_fields))
        update_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(update_raw_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_inventory)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)


    def add_raw(self, entry_fields):
        # Extract values from the entry fields dictionary
        values = [entry_fields[key].get() for key in entry_fields]

        try:
            cursor.execute('''INSERT INTO INVENTORY_RAW (MATERIAL_ID, NAME, SUPPLIER, UNIT_PRICE, STOCK_QTY, ORDER_THRESHOLD, EXPIRY_DATE, LEAD_TIME, STORE_LOCATION) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', values)
            conn.commit() # Commit changes to the database
            name = entry_fields.get("NAME").get() # Get the name of the product added
            print(f"{name} added to the inventory.")
            messagebox.showinfo("Success", f"{name} added successfully.") # Show success message
        except sqlite3.Error as e:
            print("Database error:", e)

    def remove_raw(self):
        name = self.remove_raw_entry.get()
        try:
            cursor.execute('''DELETE FROM INVENTORY_RAW WHERE NAME = ?;''', (name,))
            conn.commit() # Commit changes to the database
            print(f"{name} removed from the Inventory.")
            messagebox.showinfo("Success", f"{name} removed from the Inventory.")
        except sqlite3.Error as e:
            print("Database error:", e)

    def update_raw(self, entry_fields):
        # Extract values from the entry fields dictionary
        values = [entry_fields[key].get() for key in entry_fields]
        material_id = values[0] # Assuming the first entry is the MATERIAL_ID

        try:
            cursor.execute('''UPDATE INVENTORY_RAW SET NAME = ?, SUPPLIER = ?, UNIT_PRICE = ?, STOCK_QTY = ?, ORDER_THRESHOLD = ?, EXPIRY_DATE = ?, LEAD_TIME = ?, STORE_LOCATION = ? 
                              WHERE MATERIAL_ID = ?;''', (values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], material_id))
            conn.commit() # Commit changes to the database
            print(f"Raw material with ID {material_id} updated in the database.")
            messagebox.showinfo("Success", f"Raw material updated successfully.") # Show success message
        except sqlite3.Error as e:
            print("Database error:", e)


#checks the inventory levels
    def check_inventory_levels(self):
        try:
            cursor.execute("SELECT NAME, STOCK_QTY FROM INVENTORY_RAW")
            rows = cursor.fetchall()
            for name, stock_qty in rows:
                if stock_qty < 10:
                    messagebox.showwarning("Low Stock Alert", f"{name} has a stock quantity of {stock_qty}. Please reorder.")
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            # Schedule the function to run again after 1 minute (60000 milliseconds)
            self.root.after(60000, self.check_inventory_levels)


    def open_sales(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()


        title = tk.Label(self.dashboard_frame, text="Sales Management", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Customer Sales Section
        customer_sales_button = tk.Button(self.dashboard_frame, text="Customer Sales", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_customer_sales_frame)
        customer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # Retailer Sales Section
        retailer_sales_button = tk.Button(self.dashboard_frame, text="Retailer Sales", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_retailer_sales_frame)
        retailer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

    def open_customer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Customer Sales Management", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Add Customer Sales Section
        add_customer_sales_button = tk.Button(self.dashboard_frame, text="Add Customer Sales", font=("Arial", 20, "bold"),
                                              bg="#FFF455", bd=3, command=self.open_add_customer_sales_frame)
        add_customer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Customer Sales Section
        view_customer_sales_button = tk.Button(self.dashboard_frame, text="View Customer Sales", font=("Arial", 20, "bold"),
                                              bg="#FFF455", bd=3, command=self.open_view_customer_sales_frame)
        view_customer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # Update Customer Sales Section
        update_customer_sales_button = tk.Button(self.dashboard_frame, text="Update Customer Sales", font=("Arial", 20, "bold"),
                                                bg="#FFF455", bd=3, command=self.open_update_customer_sales_frame)
        update_customer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # Back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.pack(pady=10)

    def open_add_customer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_customer_sales_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_customer_sales_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_customer_sales_label = tk.Label(add_customer_sales_frame, text="Add Customer Sales Record", font=("Arial", 20, "bold"),
                                            bg="white")
        add_customer_sales_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["CUSTOMER_ID", "ORDER_ID", "PRODUCT_ID", "PRODUCT_NAME", "PAYMENT_METHOD", "PAYMENT_STATUS"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_customer_sales_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_customer_sales_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the sales record
        add_button = tk.Button(add_customer_sales_frame, text="Add", font=("Arial", 15, "bold"), bg="yellow",
                               command=lambda: self.add_customer_sales(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_customer_sales_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)



    def add_customer_sales(self, entry_fields):
        # Assuming you have a database connection named 'conn' and a cursor named 'cursor'
        try:
            # Prepare the INSERT statement
            query = """INSERT INTO CUSTOMER_SALES (CUSTOMER_ID, ORDER_ID, PRODUCT_ID, PRODUCT_NAME, PAYMENT_METHOD, PAYMENT_STATUS)
                       VALUES (?, ?, ?, ?, ?, ?)"""
            values = (entry_fields["CUSTOMER_ID"].get(), entry_fields["ORDER_ID"].get(), entry_fields["PRODUCT_ID"].get(),
                     entry_fields["PRODUCT_NAME"].get(), entry_fields["PAYMENT_METHOD"].get(), entry_fields["PAYMENT_STATUS"].get())
            
            # Execute the query
            cursor.execute(query, values)
            conn.commit()
            
            # Inform the user
            messagebox.showinfo("Success", "Customer sales record added successfully.")
            
            # Clear the entry fields
            for field in entry_fields.values():
                field.delete(0, tk.END)
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



    def open_view_customer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Customer Sales Records", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("Customer ID", 80), ("Order ID", 80), ("Product ID", 100), ("Product Name", 180), ("Payment Method", 100), ("Payment Status", 100)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM CUSTOMER_SALES")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.pack(pady=10)

    def open_update_customer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        update_customer_sales_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        update_customer_sales_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        update_customer_sales_label = tk.Label(update_customer_sales_frame, text="Update Customer Sales Record", font=("Arial", 20, "bold"),
                                               bg="white")
        update_customer_sales_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["ORDER_ID", "CUSTOMER_ID", "PRODUCT_ID", "PRODUCT_NAME", "PAYMENT_METHOD", "PAYMENT_STATUS"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(update_customer_sales_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_customer_sales_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to update the sales record
        update_button = tk.Button(update_customer_sales_frame, text="Update", font=("Arial", 15, "bold"), bg="yellow",
                                  command=lambda: self.update_customer_sales(entry_fields))
        update_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(update_customer_sales_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)



    def update_customer_sales(self, entry_fields):
        # Assuming you have a database connection named 'conn' and a cursor named 'cursor'
        try:
            # Prepare the UPDATE statement
            query = """UPDATE CUSTOMER_SALES SET CUSTOMER_ID = ?, ORDER_ID = ?, PRODUCT_ID = ?, PRODUCT_NAME = ?,
                                                     PAYMENT_METHOD = ?, PAYMENT_STATUS = ?
                       WHERE ORDER_ID = ?"""
            values = (entry_fields["CUSTOMER_ID"].get(), entry_fields["ORDER_ID"].get(), entry_fields["PRODUCT_ID"].get(),
                     entry_fields["PRODUCT_NAME"].get(), entry_fields["PAYMENT_METHOD"].get(), entry_fields["PAYMENT_STATUS"].get(),
                     entry_fields["ORDER_ID"].get())
            
            # Execute the query
            cursor.execute(query, values)
            conn.commit()
            
            # Inform the user
            messagebox.showinfo("Success", "Customer sales record updated successfully.")
            
            # Clear the entry fields
            for field in entry_fields.values():
                field.delete(0, tk.END)
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        



    def open_retailer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Retailer Sales Management", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Add Retailer Sales Section
        add_retailer_sales_button = tk.Button(self.dashboard_frame, text="Add Retailer Sales", font=("Arial", 20, "bold"),
                                              bg="#FFF455", bd=3, command=self.open_add_retailer_sales_frame)
        add_retailer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Retailer Sales Section
        view_retailer_sales_button = tk.Button(self.dashboard_frame, text="View Retailer Sales", font=("Arial", 20, "bold"),
                                              bg="#FFF455", bd=3, command=self.open_view_retailer_sales_frame)
        view_retailer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # Update Retailer Sales Section
        update_retailer_sales_button = tk.Button(self.dashboard_frame, text="Update Retailer Sales", font=("Arial", 20, "bold"),
                                                bg="#FFF455", bd=3, command=self.open_update_retailer_sales_frame)
        update_retailer_sales_button.pack(side=tk.TOP, padx=20, pady=10)

        # Back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.pack(pady=10)



    def open_add_retailer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_retailer_sales_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_retailer_sales_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_retailer_sales_label = tk.Label(add_retailer_sales_frame, text="Add Retailer Sales Record", font=("Arial", 20, "bold"),
                                            bg="white")
        add_retailer_sales_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["ORDER_ID", "RETAILER_ID", "PRODUCT_ID", "PRODUCT_NAME", "PAYMENT_METHOD", "PAYMENT_STATUS"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_retailer_sales_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_retailer_sales_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the sales record
        add_button = tk.Button(add_retailer_sales_frame, text="Add", font=("Arial", 15, "bold"), bg="yellow",
                               command=lambda: self.add_retailer_sales(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_retailer_sales_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)


    def add_retailer_sales(self, entry_fields):
        # Assuming you have a database connection named 'conn' and a cursor named 'cursor'
        try:
            # Prepare the INSERT statement
            query = """INSERT INTO RETAILER_SALES (ORDER_ID, RETAILER_ID, PRODUCT_ID, PRODUCT_NAME, PAYMENT_METHOD, PAYMENT_STATUS)
                       VALUES (?, ?, ?, ?, ?, ?)"""
            values = (entry_fields["ORDER_ID"].get(), entry_fields["RETAILER_ID"].get(), entry_fields["PRODUCT_ID"].get(),
                     entry_fields["PRODUCT_NAME"].get(), entry_fields["PAYMENT_METHOD"].get(), entry_fields["PAYMENT_STATUS"].get())
            
            # Execute the query
            cursor.execute(query, values)
            conn.commit()
            
            # Inform the user
            messagebox.showinfo("Success", "Retailer sales record added successfully.")
            
            # Clear the entry fields
            for field in entry_fields.values():
                field.delete(0, tk.END)
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



    def open_view_retailer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Retailer Sales Records", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("ID", 60), ("Order ID", 100), ("Product ID", 100), ("Product Name", 150), ("Payment Method", 150), ("Payment Status", 150)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM RETAILER_SALES")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.pack(pady=10)

    def open_update_retailer_sales_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        update_retailer_sales_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        update_retailer_sales_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        update_retailer_sales_label = tk.Label(update_retailer_sales_frame, text="Update Retailer Sales Record", font=("Arial", 20, "bold"),
                                               bg="white")
        update_retailer_sales_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["ORDER_ID", "RETAILER_ID", "PRODUCT_ID", "PRODUCT_NAME", "PAYMENT_METHOD", "PAYMENT_STATUS"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(update_retailer_sales_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_retailer_sales_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to update the sales record
        update_button = tk.Button(update_retailer_sales_frame, text="Update", font=("Arial", 15, "bold"), bg="yellow",
                                  command=lambda: self.update_retailer_sales(entry_fields))
        update_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(update_retailer_sales_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_sales)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)



    def update_retailer_sales(self, entry_fields):
        # Assuming you have a database connection named 'conn' and a cursor named 'cursor'
        try:
            # Prepare the UPDATE statement
            query = """UPDATE RETAILER_SALES SET ORDER_ID = ?, RETAILER_ID = ?, PRODUCT_ID = ?, PRODUCT_NAME = ?,
                                                     PAYMENT_METHOD = ?, PAYMENT_STATUS = ?
                       WHERE ORDER_ID = ?"""
            values = (entry_fields["ORDER_ID"].get(), entry_fields["RETAILER_ID"].get(), entry_fields["PRODUCT_ID"].get(),
                     entry_fields["PRODUCT_NAME"].get(), entry_fields["PAYMENT_METHOD"].get(), entry_fields["PAYMENT_STATUS"].get(),
                     entry_fields["ORDER_ID"].get())
            
            # Execute the query
            cursor.execute(query, values)
            conn.commit()
            
            # Inform the user
            messagebox.showinfo("Success", "Retailer sales record updated successfully.")
            
            # Clear the entry fields
            for field in entry_fields.values():
                field.delete(0, tk.END)
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")















    def open_warehouse_management(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Warehouse Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
        title.pack(pady=20)

        # Add Finished Products to Warehouse
        add_finished_products_button = tk.Button(self.dashboard_frame, text="Add Finished Products Warehouse", font=("Arial", 20, "bold"), bg="#FFF455",
                                                 bd=3, command=self.open_add_finished_products)
        add_finished_products_button.pack(side=tk.TOP, padx=20, pady=10)

        # Add Raw Materials to Warehouse
        add_raw_materials_button = tk.Button(self.dashboard_frame, text="Add Raw Material Warehouse", font=("Arial", 20, "bold"), bg="#FFF455",
                                             bd=3, command=self.open_add_raw_materials)
        add_raw_materials_button.pack(side=tk.TOP, padx=20, pady=10)


    def open_add_finished_products(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Add Product Section
        add_product_button = tk.Button(self.dashboard_frame, text="Add Products Warehouse", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_add_product_frame)
        add_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # Remove Product Section
        remove_product_button = tk.Button(self.dashboard_frame, text="Remove Product Warehouse", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_remove_product_frame)
        remove_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Inventory Section
        view_inventory_button = tk.Button(self.dashboard_frame, text="View Product Warehouse", font=("Arial", 20, "bold"),
                                           bg="#FFF455", bd=3, command=self.open_view_warehouse_frame)
        view_inventory_button.pack(side=tk.TOP, padx=20, pady=10)

    def open_add_raw_materials(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Add Product Section
        add_product_button = tk.Button(self.dashboard_frame, text="Add Raw Material Warehouse", font=("Arial", 20, "bold"),
                                       bg="#FFF455", bd=3, command=self.open_add_raw_frame)
        add_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # Remove Product Section
        remove_product_button = tk.Button(self.dashboard_frame, text="Remove Raw Material Warehouse", font=("Arial", 20, "bold"),
                                          bg="#FFF455", bd=3, command=self.open_remove_raw_frame)
        remove_product_button.pack(side=tk.TOP, padx=20, pady=10)

        # View Inventory Section
        view_inventory_button = tk.Button(self.dashboard_frame, text="View Raw Material Warehouse", font=("Arial", 20, "bold"),
                                           bg="#FFF455", bd=3, command=self.open_view_warehouse_raw_frame)
        view_inventory_button.pack(side=tk.TOP, padx=20, pady=10)

    def open_add_product_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_product_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_product_label = tk.Label(add_product_frame, text="Add Product to Warehouse", font=("Arial", 20, "bold"),
                                     bg="white")
        add_product_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["WAREHOUSE_ID", "LOCATION", "SIZE", "TEMPERATURE_ZONE", "PRODUCT_ID", "PRODUCT_NAME","QUANTITY"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_product_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_product_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the product
        add_button = tk.Button(add_product_frame, text="Add", font=("Arial", 15, "bold"), bg="purple",
                               command=lambda: self.add_product(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_product_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_warehouse_management)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)

    def open_remove_product_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Remove Product from Warehouse", font=("Arial", 30, "bold"),
                         bg="white", fg="purple")
        title.pack(pady=20)

        # Remove Product Section
        remove_product_label = tk.Label(self.dashboard_frame, text="Product Name:", font=("Arial", 20), bg="white")
        remove_product_label.pack(pady=5)

        self.remove_product_entry = tk.Entry(self.dashboard_frame, font=("Arial", 20))
        self.remove_product_entry.pack(pady=5)

        remove_button = tk.Button(self.dashboard_frame, text="Remove", font=("Arial", 20, "bold"), bg="yellow",
                                 command=self.remove_product)
        remove_button.pack(pady=10)

        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_warehouse_management)
        back_button.pack(pady=10)

    def open_view_warehouse_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Main Warehouse", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("Warehouse ID", 100), ("Location", 90), ("Size", 60), ("Temperature zone", 100), ("Product ID", 130), ("Product name", 130), ("Quantity", 60)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM WAREHOUSE_ITEMS")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_warehouse_management)
        back_button.pack(pady=10)

    def open_add_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        add_raw_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        add_raw_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_raw_label = tk.Label(add_raw_frame, text="Add Raw Material to Warehouse", font=("Arial", 20, "bold"),
                                     bg="white")
        add_raw_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create entry fields for each attribute
        entry_fields = {}
        column_names = ["WAREHOUSE_ID", "LOCATION", "SIZE", "TEMPERATURE_ZONE", "MATERIAL_ID", "MATERIAL_NAME","QUANTITY"]
        for idx, column_name in enumerate(column_names, start=1):
            label = tk.Label(add_raw_frame, text=f"{column_name}:", font=("Arial", 15), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(add_raw_frame, font=("Arial", 15))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_fields[column_name] = entry

        # Add button to add the product
        add_button = tk.Button(add_raw_frame, text="Add", font=("Arial", 15, "bold"), bg="yellow",
                               command=lambda: self.add_raw(entry_fields))
        add_button.grid(row=len(column_names) + 1, columnspan=2, pady=10)

        back_button = tk.Button(add_raw_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_warehouse_management)
        back_button.grid(row=len(column_names) + 2, columnspan=2, pady=10)

    def open_remove_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Remove Raw Material from Warehouse", font=("Arial", 30, "bold"),
                         bg="white", fg="purple")
        title.pack(pady=20)

        # Remove Product Section
        remove_raw_label = tk.Label(self.dashboard_frame, text="Material Name:", font=("Arial", 20), bg="white")
        remove_raw_label.pack(pady=5)

        self.remove_raw_entry = tk.Entry(self.dashboard_frame, font=("Arial", 20))
        self.remove_raw_entry.pack(pady=5)

        remove_button = tk.Button(self.dashboard_frame, text="Remove", font=("Arial", 20, "bold"), bg="yellow",
                                 command=self.remove_raw)
        remove_button.pack(pady=10)

        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_add_raw_materials)
        back_button.pack(pady=10)

    def open_view_warehouse_raw_frame(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.dashboard_frame, text="View Raw Material Warehouse", font=("Arial", 30, "bold"), bg="white",
                         fg="purple")
        title.pack(pady=20)

        # Define column names and their corresponding widths
        columns = [("Warehouse ID", 100), ("Location", 90), ("Size", 60), ("Temperature zone", 100), ("Product ID", 130), ("Product name", 130), ("Quantity", 60)]

        tree_frame = Frame(self.dashboard_frame)
        tree_frame.pack(pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, selectmode="extended", columns=[col[0] for col in columns], show="headings")
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define the scrollbar
        tree_scroll = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=tree_scroll.set)

        # Set column headings and widths
        for i, (column_name, width) in enumerate(columns, start=1):
            tree.heading(f'#{i}', text=column_name)
            tree.column(f'#{i}', width=width, anchor="center")

        # Add a theme to the Treeview
        tree_style = ttk.Style()
        tree_style.theme_use("default") # Ensure default theme is used
        tree_style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # stripped row tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        try:
            cursor.execute("SELECT * FROM WAREHOUSE_RAW_MATERIAL")
            rows = cursor.fetchall()

            for count, record in enumerate(rows, start=1):
                if count % 2 == 0:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=count, values=record, tags=('oddrow',))
        except sqlite3.Error as e:
            print("Database error:", e)

        # Add back button
        back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",
                                command=self.open_add_raw_materials)
        back_button.pack(pady=10)


    def add_product(self, entry_fields):
        # Extract values from the entry fields dictionary
        values = [entry_fields[key].get() for key in entry_fields]

        try:
            cursor.execute('''INSERT INTO WAREHOUSE_ITEMS (WAREHOUSE_ID, LOCATION, SIZE, TEMPERATURE_ZONE, PRODUCT_ID, PRODUCT_NAME, QUANTITY) 
                              VALUES (?, ?, ?, ?, ?, ?, ?);''', values)
            conn.commit() # Commit changes to the database
            name = entry_fields.get("PRODUCT_NAME").get() # Get the name of the product added
            print(f"{name} added to the Warehouse.")
            messagebox.showinfo("Success", f"{name} added successfully.") # Show success message
        except sqlite3.Error as e:
            print("Database error:", e)


    def add_raw(self, entry_fields):
        # Extract values from the entry fields dictionary
        values = [entry_fields[key].get() for key in entry_fields]

        try:
            cursor.execute('''INSERT INTO WAREHOUSE_RAW_MATERIALS (WAREHOUSE_ID, LOCATION, SIZE, TEMPERATURE_ZONE, MATERIAL_ID, MATERIAL_NAME, QUANTITY) 
                              VALUES (?, ?, ?, ?, ?, ?, ?);''', values)
            conn.commit() # Commit changes to the database
            name = entry_fields.get("MATERIAL_NAME").get() # Get the name of the product added
            print(f"{name} added to the Warehouse.")
            messagebox.showinfo("Success", f"{name} added successfully.") # Show success message
        except sqlite3.Error as e:
            print("Database error:", e)

    def remove_raw(self):
        name = self.remove_raw_entry.get()
        try:
            cursor.execute('''DELETE FROM WAREHOUSE_RAW_MATERiALS WHERE MATERIAL_NAME = ?;''', (name,))
            conn.commit() # Commit changes to the database
            print(f"{name} removed from the Warehouse.")
            messagebox.showinfo("Success", f"{name} removed from the Warehouse.")
        except sqlite3.Error as e:
            print("Database error:", e)

    def remove_product(self):
        name = self.remove_product_entry.get()
        try:
            cursor.execute('''DELETE FROM WAREHOUSE_ITEMS WHERE PRODUCT_NAME = ?;''', (name,))
            conn.commit() # Commit changes to the database
            print(f"{name} removed from the Warehouse.")
            messagebox.showinfo("Success", f"{name} removed from the Warehouse.")
        except sqlite3.Error as e:
            print("Database error:", e)





    def submit_order(self):
    # Fetch values from Entry widgets
      order_id = self.order_id_entry.get()
      customer_id = self.customer_id_entry.get()
      date = self.date_entry.get()
      status = self.status_entry.get()
      total_amount = self.total_amount_entry.get()
      product_id = self.product_id_entry.get()
      product_name = self.product_name_entry.get()
      price = self.price_entry.get()
      delivery_address = self.delivery_address_entry.get()

    # Call insert_order_details method with fetched values
      self.insert_order_details(order_id, customer_id, date, status, total_amount, product_id, product_name, price, delivery_address)


    def insert_order_details(self, order_id, customer_id, date, status, total_amount, product_id, product_name, price, delivery_address):
     try:
        cursor.execute('''
        INSERT INTO ORDERS (ORDER_ID, CUSTOMER_ID, DATE, STATUS, TOTAL_AMOUNT, PRODUCT_ID, PRODUCT_NAME, PRICE, DELIVERY_ADDRESS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (order_id, customer_id, date, status, total_amount, product_id, product_name, price, delivery_address))
        conn.commit()
        print("Order details inserted successfully.")
        messagebox.showinfo("Success", f"{product_name} added successfully.") # Show success message

     except sqlite3.Error as e:
        print("Database error:", e)

    def open_order_management_customer(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Order Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.pack(pady=20)

    # Generate a unique order ID
      order_id = str(uuid.uuid4())[:8]  # Generate a UUID and truncate it to 8 characters

    # Order Details Section
      order_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
      order_frame.pack(side=tk.LEFT)

      order_label = tk.Label(order_frame, text="Order Details", font=("Arial", 20, "bold"), bg="white")
      order_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

      order_id_label = tk.Label(order_frame, text="Order ID:", font=("Arial", 15), bg="white")
      order_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
      self.order_id_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.order_id_entry.insert(0, order_id)  # Insert the generated order ID
      self.order_id_entry.config(state="readonly")  # Make the entry read-only
      self.order_id_entry.grid(row=1, column=1, padx=10, pady=5)

      customer_id_label = tk.Label(order_frame, text="Customer ID:", font=("Arial", 15), bg="white")
      customer_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
      self.customer_id_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.customer_id_entry.grid(row=2, column=1, padx=10, pady=5)

      date_label = tk.Label(order_frame, text="Date:", font=("Arial", 15), bg="white")
      date_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
      self.date_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.date_entry.grid(row=3, column=1, padx=10, pady=5)

      status_label = tk.Label(order_frame, text="Status:", font=("Arial", 15), bg="white")
      status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
      self.status_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.status_entry.grid(row=4, column=1, padx=10, pady=5)

      total_amount_label = tk.Label(order_frame, text="Total Amount:", font=("Arial", 15), bg="white")
      total_amount_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
      self.total_amount_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.total_amount_entry.grid(row=5, column=1, padx=10, pady=5)

      product_id_label = tk.Label(order_frame, text="Product ID:", font=("Arial", 15), bg="white")
      product_id_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
      self.product_id_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.product_id_entry.grid(row=6, column=1, padx=10, pady=5)

      product_name_label = tk.Label(order_frame, text="Product Name:", font=("Arial", 15), bg="white")
      product_name_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
      self.product_name_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.product_name_entry.grid(row=7, column=1, padx=10, pady=5)

      price_label = tk.Label(order_frame, text="Price:", font=("Arial", 15), bg="white")
      price_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
      self.price_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.price_entry.grid(row=8, column=1, padx=10, pady=5)

      delivery_address_label = tk.Label(order_frame, text="Delivery Address:", font=("Arial", 15), bg="white")
      delivery_address_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
      self.delivery_address_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.delivery_address_entry.grid(row=9, column=1, padx=10, pady=5)

      submit_button = tk.Button(order_frame, text="Submit",command=self.submit_order, font=("Arial", 15, "bold"), bg="yellow")
      submit_button.grid(row=10, columnspan=2, pady=10)

      back_button = tk.Button(order_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white")
      back_button.grid(row=11, columnspan=2, pady=10)


    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.lbl_title = tk.Label(self.root, text="Customer Orders")
        self.lbl_title.pack()

        self.btn_view_orders = tk.Button(self.root, text="View Orders", command=self.view_customer_order)
        self.btn_view_orders.pack()

    def view_customer_order(self):

    # Fetch data from the CUSTOMER_ORDERS table
      for widget in self.root.winfo_children():
            if widget != self.lbl_title:
                widget.destroy()
      cursor.execute("SELECT * FROM CUSTOMER_ORDERS")
      orders = cursor.fetchall()
    # Create labels for column names
      columns = ["ORDER_ID", "CUSTOMER_ID"]
      for col_index, col_name in enumerate(columns):
        label = tk.Label(self.root, text=col_name)
        label.grid(row=0, column=col_index)

    # Display data using grid layout
      for row_index, order in enumerate(orders, start=1):
        for col_index, value in enumerate(order):
            label = tk.Label(self.root, text=value)
            label.grid(row=row_index, column=col_index)


    def cancel_customer_order(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Order Cancellation", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.pack(pady=20)

    # Entry widget for entering the order ID
      order_id_label = tk.Label(self.dashboard_frame, text="Enter Order ID:", font=("Arial", 15), bg="white")
      order_id_label.pack(pady=10)
      self.order_id_entry = tk.Entry(self.dashboard_frame, font=("Arial", 15))
      self.order_id_entry.pack(pady=5)

    # Confirm button to trigger the cancellation
      confirm_button = tk.Button(self.dashboard_frame, text="Confirm", command=self.confirm_cancel, font=("Arial", 15, "bold"), bg="red", fg="white")
      confirm_button.pack(pady=10)

      back_button = tk.Button(self.dashboard_frame, text="Back", font=("Arial", 15, "bold"), bg="blue", fg="white", command=self.go_back)
      back_button.pack(pady=10)

    def order_exists(self, order_id):
        # Check if the order ID exists in the orders table
        self.cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        order = self.cursor.fetchone()
        if order:
           return True
        else:
            return False

    # def delete_order(self, order_id):
    #     # Delete the order with the given order ID from the database
    #     self.cursor.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
    #     self.connection.commit()
    def add_retailer_order(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Order Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.pack(pady=20)

    # Generate a unique order ID
      order_id = str(uuid.uuid4())[:8]  # Generate a UUID and truncate it to 8 characters

    # Order Details Section
      order_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
      order_frame.pack(side=tk.LEFT)

      order_label = tk.Label(order_frame, text="Order Details", font=("Arial", 20, "bold"), bg="white")
      order_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

      order_id_label = tk.Label(order_frame, text="Order ID:", font=("Arial", 15), bg="white")
      order_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
      self.order_id_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.order_id_entry.insert(0, order_id)  # Insert the generated order ID
      self.order_id_entry.config(state="readonly")  # Make the entry read-only
      self.order_id_entry.grid(row=1, column=1, padx=10, pady=5)

      retailer_id_label = tk.Label(order_frame, text="Retailer ID:", font=("Arial", 15), bg="white")
      retailer_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
      self.retailer_id_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.retailer_id_entry.grid(row=2, column=1, padx=10, pady=5)

      date_label = tk.Label(order_frame, text="Date:", font=("Arial", 15), bg="white")
      date_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
      self.date_entry = tk.Entry(order_frame, font=("Arial", 15))
      self.date_entry.grid(row=3, column=1, padx=10, pady=5)

      status_label = tk.Label(order_frame, text="Status:", font=("Arial", 15), bg="white")
      status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
      self.status_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.status_entry.grid(row=4, column=1, padx=10, pady=5)

      total_amount_label = tk.Label(order_frame, text="Total Amount:", font=("Arial", 15), bg="white")
      total_amount_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
      self.total_amount_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.total_amount_entry.grid(row=5, column=1, padx=10, pady=5)

      product_id_label = tk.Label(order_frame, text="Product ID:", font=("Arial", 15), bg="white")
      product_id_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
      self.product_id_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.product_id_entry.grid(row=6, column=1, padx=10, pady=5)

      product_name_label = tk.Label(order_frame, text="Product Name:", font=("Arial", 15), bg="white")
      product_name_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
      self.product_name_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.product_name_entry.grid(row=7, column=1, padx=10, pady=5)

      price_label = tk.Label(order_frame, text="Price:", font=("Arial", 15), bg="white")
      price_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
      self.price_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.price_entry.grid(row=8, column=1, padx=10, pady=5)

      delivery_address_label = tk.Label(order_frame, text="Delivery Address:", font=("Arial", 15), bg="white")
      delivery_address_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
      self.delivery_address_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
      self.delivery_address_entry.grid(row=9, column=1, padx=10, pady=5)

      submit_button = tk.Button(order_frame, text="Submit",command=self.submit_order_retailer, font=("Arial", 15, "bold"), bg="yellow")
      submit_button.grid(row=10, columnspan=2, pady=10)

      back_button = tk.Button(order_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white", command=self.go_back)
      back_button.grid(row=11, columnspan=2, pady=10)

    def order_exists_retailer(self, order_id):
    # Check if the order ID exists in the orders table
      self.cursor.execute("SELECT * FROM retailer_orders WHERE order_id=?", (order_id,))
      order = self.cursor.fetchone()
      if order:
          return True
      else:
          return False

    def confirm_cancel_retailer(self):
    # Get the order ID from the entry widget
      order_id = self.order_id_entry.get()

    # Perform actions to cancel the order
    # Example:
      if(self.order_exists_retailer(order_id)):
          self.cursor.execute("DELETE FROM retailer_orders WHERE order_id=?", (order_id,))
          messagebox.showinfo("Order cancelled successfully!")
          self.connection.commit()
      else:
          messagebox.showinfo("Invalid Order ID Please Enter valid one!")

    # After cancellation, you might want to go back to the main dashboard or perform other actions
      self.open_dashboard()  


    def confirm_cancel(self):
    # Get the order ID from the entry widget
      order_id = self.order_id_entry.get()

    # Perform actions to cancel the order
    # Example:
      if(self.order_exists(order_id)):
          self.cursor.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
        #   confirmation = tk.Label(self.dashboard_frame, text="Order Cancelled Successfully", font=("Arial", 30, "bold"), bg="white", fg="purple") 
        #   confirmation.pack(pady=20)
          messagebox.showinfo("Order cancelled successfully!")
          self.connection.commit()
      else:
          messagebox.showinfo("Invalid Order ID Please Enter valid one!")
    # After cancellation, you might want to go back to the main dashboard or perform other actions
      self.open_dashboard()

 
    def go_back(self):
        # Implement going back to the previous state, for instance, the main dashboard
        self.open_dashboard()  
      
    def add_customer_order(self):
    # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
          widget.destroy()

        title = tk.Label(self.dashboard_frame, text="Order Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
        title.pack(pady=20)

    # Generate a unique order ID
        order_id = str(uuid.uuid4())[:8]  # Generate a UUID and truncate it to 8 characters

    # Order Details Section
        order_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
        order_frame.pack(side=tk.LEFT)

        order_label = tk.Label(order_frame, text="Order Details", font=("Arial", 20, "bold"), bg="white")
        order_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        order_id_label = tk.Label(order_frame, text="Order ID:", font=("Arial", 15), bg="white")
        order_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.order_id_entry = tk.Entry(order_frame, font=("Arial", 15))
        self.order_id_entry.insert(0, order_id)  # Insert the generated order ID
        self.order_id_entry.config(state="readonly")  # Make the entry read-only
        self.order_id_entry.grid(row=1, column=1, padx=10, pady=5)

        customer_id_label = tk.Label(order_frame, text="Customer ID:", font=("Arial", 15), bg="white")
        customer_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.customer_id_entry = tk.Entry(order_frame, font=("Arial", 15))
        self.customer_id_entry.grid(row=2, column=1, padx=10, pady=5)

        date_label = tk.Label(order_frame, text="Date:", font=("Arial", 15), bg="white")
        date_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = tk.Entry(order_frame, font=("Arial", 15))
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        status_label = tk.Label(order_frame, text="Status:", font=("Arial", 15), bg="white")
        status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.status_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.status_entry.grid(row=4, column=1, padx=10, pady=5)

        total_amount_label = tk.Label(order_frame, text="Total Amount:", font=("Arial", 15), bg="white")
        total_amount_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.total_amount_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.total_amount_entry.grid(row=5, column=1, padx=10, pady=5)

        product_id_label = tk.Label(order_frame, text="Product ID:", font=("Arial", 15), bg="white")
        product_id_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.product_id_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.product_id_entry.grid(row=6, column=1, padx=10, pady=5)

        product_name_label = tk.Label(order_frame, text="Product Name:", font=("Arial", 15), bg="white")
        product_name_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.product_name_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.product_name_entry.grid(row=7, column=1, padx=10, pady=5)

        price_label = tk.Label(order_frame, text="Price:", font=("Arial", 15), bg="white")
        price_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.price_entry.grid(row=8, column=1, padx=10, pady=5)

        delivery_address_label = tk.Label(order_frame, text="Delivery Address:", font=("Arial", 15), bg="white")
        delivery_address_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.delivery_address_entry = tk.Entry(order_frame, font=("Arial", 15))  # Assign to instance variable
        self.delivery_address_entry.grid(row=9, column=1, padx=10, pady=5)

        submit_button = tk.Button(order_frame, text="Submit",command=self.submit_order, font=("Arial", 15, "bold"), bg="yellow")
        submit_button.grid(row=10, columnspan=2, pady=10)

        back_button = tk.Button(order_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white", command=self.go_back)
        back_button.grid(row=11, columnspan=2, pady=10)

    def insert_supplier_details(self, supplier_id, supplier_name, contact_person, email, phone, address, products_supplied, lead_time, payment_terms):
      try:
          cursor.execute('''
          INSERT INTO SUPPLIERS (SUPPLIER_ID, SUPPLIER_NAME, CONTACT_PERSON, EMAIL, PHONE, ADDRESS, PRODUCTS_SUPPLIED, LEAD_TIME, PAYMENT_TERMS)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
          ''', (supplier_id, supplier_name, contact_person, email, phone, address, products_supplied, lead_time, payment_terms))
          conn.commit()
          print("Supplier details inserted successfully.")
          self.display_message("Supplier details inserted successfully!")
          messagebox.showinfo("Success", f"{supplier_name} added successfully.") # Show success message

      except sqlite3.Error as e:
          print("Database error:", e)

    def submit_supplier(self):
    # Fetch values from Entry widgets
      supplier_id = self.supplier_id_entry.get()
      supplier_name = self.supplier_name_entry.get()
      contact_person = self.contact_person_entry.get()
      email = self.email_entry.get()
      phone = self.phone_entry.get()
      address = self.address_entry.get()
      products_supplied = self.products_supplied_entry.get()
      lead_time = self.lead_time_entry.get()
      payment_terms = self.payment_terms_entry.get()

    # Call insert_supplier_details method with fetched values
      self.insert_supplier_details(supplier_id, supplier_name, contact_person, email, phone, address, products_supplied, lead_time, payment_terms)

    def open_supplier_management(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Supplier Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.pack(pady=20)

    # Generate a unique supplier ID
      supplier_id = str(uuid.uuid4())[:8]  # Generate a UUID and truncate it to 8 characters

    # Supplier Details Section
      supplier_frame = tk.Frame(self.dashboard_frame, bg="white", bd=2, relief=tk.RIDGE)
      supplier_frame.pack(side=tk.LEFT)

      supplier_label = tk.Label(supplier_frame, text="Supplier Details", font=("Arial", 20, "bold"), bg="white")
      supplier_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

      supplier_id_label = tk.Label(supplier_frame, text="Supplier ID:", font=("Arial", 15), bg="white")
      supplier_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
      self.supplier_id_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.supplier_id_entry.insert(0, supplier_id)  # Insert the generated supplier ID
      self.supplier_id_entry.config(state="readonly")  # Make the entry read-only
      self.supplier_id_entry.grid(row=1, column=1, padx=10, pady=5)

      supplier_name_label = tk.Label(supplier_frame, text="Supplier Name:", font=("Arial", 15), bg="white")
      supplier_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
      self.supplier_name_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.supplier_name_entry.grid(row=2, column=1, padx=10, pady=5)

      contact_person_label = tk.Label(supplier_frame, text="Contact Person:", font=("Arial", 15), bg="white")
      contact_person_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
      self.contact_person_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.contact_person_entry.grid(row=3, column=1, padx=10, pady=5)

      email_label = tk.Label(supplier_frame, text="Email:", font=("Arial", 15), bg="white")
      email_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
      self.email_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.email_entry.grid(row=4, column=1, padx=10, pady=5)

      phone_label = tk.Label(supplier_frame, text="Phone:", font=("Arial", 15), bg="white")
      phone_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
      self.phone_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.phone_entry.grid(row=5, column=1, padx=10, pady=5)

      address_label = tk.Label(supplier_frame, text="Address:", font=("Arial", 15), bg="white")
      address_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
      self.address_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.address_entry.grid(row=6, column=1, padx=10, pady=5)

      products_supplied_label = tk.Label(supplier_frame, text="Products Supplied:", font=("Arial", 15), bg="white")
      products_supplied_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
      self.products_supplied_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.products_supplied_entry.grid(row=7, column=1, padx=10, pady=5)

      lead_time_label = tk.Label(supplier_frame, text="Lead Time:", font=("Arial", 15), bg="white")
      lead_time_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
      self.lead_time_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.lead_time_entry.grid(row=8, column=1, padx=10, pady=5)

      payment_terms_label = tk.Label(supplier_frame, text="Payment Terms:", font=("Arial", 15), bg="white")
      payment_terms_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
      self.payment_terms_entry = tk.Entry(supplier_frame, font=("Arial", 15))
      self.payment_terms_entry.grid(row=9, column=1, padx=10, pady=5)

      submit_button = tk.Button(supplier_frame, text="Submit", command=self.submit_supplier, font=("Arial", 15, "bold"), bg="yellow")
      submit_button.grid(row=10, columnspan=2, pady=10)

      back_button = tk.Button(supplier_frame, text="Back", font=("Arial", 15, "bold"), bg="red", fg="white",  command=self.open_dashboard)
      back_button.grid(row=11, columnspan=2, pady=10)
      
    def retailer_options(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Retailer Options", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.grid(row=0, column=0, pady=20)

    # Add Product Section
      add_product_button = tk.Button(self.dashboard_frame, text="Add Product", font=("Arial", 20, "bold"),
                                   bg="green", bd=3, command=self.add_retailer_product)
      add_product_button.grid(row=1, column=0, padx=20, pady=10)

    # Manage Inventory Section
      manage_inventory_button = tk.Button(self.dashboard_frame, text="Manage Inventory", font=("Arial", 20, "bold"),
                                        bg="green", bd=3, command=self.manage_inventory)
      manage_inventory_button.grid(row=2, column=0, padx=20, pady=10)

    # View Sales Section
      view_sales_button = tk.Button(self.dashboard_frame, text="View Sales", font=("Arial", 20, "bold"),
                                  bg="green", bd=3, command=self.view_sales)
      view_sales_button.grid(row=3, column=0, padx=20, pady=10)

    def customer_options(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Customer Options", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.grid(row=0, column=0, pady=20)

    # Add Order Section
      add_order_button = tk.Button(self.dashboard_frame, text="Add Order", font=("Arial", 20, "bold"),
                                  bg="green", bd=3, command=self.add_customer_order)
      add_order_button.grid(row=1, column=0, padx=20, pady=10)

    # Cancel Order Section
      cancel_order_button = tk.Button(self.dashboard_frame, text="Cancel Order", font=("Arial", 20, "bold"),
                                     bg="green", bd=3, command=self.cancel_customer_order)
      cancel_order_button.grid(row=2, column=0, padx=20, pady=10)

    # View Order Section
      view_order_button = tk.Button(self.dashboard_frame, text="View Order", font=("Arial", 20, "bold"),
                                   bg="green", bd=3, command=self.create_widgets)
      view_order_button.grid(row=3, column=0, padx=20, pady=10)


# Assuming you have corresponding methods add_order(), cancel_order(), and view_order() defined within your class.

    def open_order_management(self):
    # Clear the dashboard frame
      for widget in self.dashboard_frame.winfo_children():
        widget.destroy()

      title = tk.Label(self.dashboard_frame, text="Order Management", font=("Arial", 30, "bold"), bg="white", fg="purple")
      title.grid(row=0, column=0, pady=20)

    # Add Customer Order Section
      add_customer_order_button = tk.Button(self.dashboard_frame, text="Customer Order", font=("Arial", 20, "bold"),
                                           bg="green", bd=3, command=self.customer_options)
      add_customer_order_button.grid(row=1, column=0, padx=20, pady=10)

    # Add Retailer Order Section
      add_retailer_order_button = tk.Button(self.dashboard_frame, text="Retailer Order", font=("Arial", 20, "bold"),
                                           bg="green", bd=3, command=self.retailer_options)
      add_retailer_order_button.grid(row=2, column=0, padx=20, pady=10)







    def close_window(event=None):
      root.destroy()
      sys.exit()





if __name__ == "__main__":
    root = tk.Tk()
    scm = SCM(root)
    root.mainloop()

                         
