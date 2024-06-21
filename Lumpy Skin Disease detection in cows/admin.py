import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Create the database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vdoctor"
)

# Create the doctors table if it doesn't exist
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        contact VARCHAR(255),
        area VARCHAR(255)
    )
""")
login_window = tk.Tk()
login_window.geometry("400x300")
login_window.title("Log In")

# Define the log in function
def login():
    if userid_entry.get() == "admin" and password_entry.get() == "1234":
        messagebox.showinfo("Success", "Logged in successfully!")
        login_window.destroy()
        main_window = tk.Tk()
        main_window.geometry("400x300")
        main_window.title("Doctor Database")
        
        # Define the function to display the doctors in a table
        def display_doctors():
            display_window = tk.Toplevel(main_window)
            display_window.geometry("400x300")
            display_window.title("Available Doctors")
            
            # Fetch the doctors from the database and display them in a table
            c.execute("SELECT * FROM doctors")
            doctors = c.fetchall()
            for i, doctor in enumerate(doctors):
                for j in range(4):
                    label = tk.Label(display_window, text=doctor[j])
                    label.grid(row=i+1, column=j, padx=10, pady=5)
        
        # Define the function to add a new doctor to the database
        def add_doctor():
            add_window = tk.Toplevel(main_window)
            add_window.geometry("400x300")
            add_window.title("Add Doctor")
            
            # Define the function to save the new doctor to the database
            def save_doctor():
                name = name_entry.get()
                contact = contact_entry.get()
                area = area_entry.get()
                c.execute("INSERT INTO doctors (name, contact, area) VALUES (%s, %s, %s)", (name, contact, area))
                conn.commit()
                messagebox.showinfo("Success", "Doctor added successfully!")
                name_entry.delete(0, tk.END)
                contact_entry.delete(0, tk.END)
                area_entry.delete(0, tk.END)
            
            # Create the entry boxes and labels for the new doctor's information
            name_label = tk.Label(add_window, text="Doctor Name:")
            name_label.grid(row=0, column=0, padx=10, pady=5)
            name_entry = tk.Entry(add_window)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            contact_label = tk.Label(add_window, text="Contact:")
            contact_label.grid(row=1, column=0, padx=10, pady=5)
            contact_entry = tk.Entry(add_window)
            contact_entry.grid(row=1, column=1, padx=10, pady=5)
            
            area_label = tk.Label(add_window, text="Area:")
            area_label.grid(row=2, column=0, padx=10, pady=5)
            area_entry = tk.Entry(add_window)
            area_entry.grid(row=2, column=1, padx=10, pady=5)
            
            add_button = tk.Button(add_window, text="Add", command=save_doctor)
            add_button.grid(row=4, column=1, padx=10, pady=5)
        
        # Create the buttons to see the doctors and add a doctor
        see_doctors_button = tk.Button(main_window, text="See Doctors", command=display_doctors    )
        add_doctor_button = tk.Button(main_window, text="Add Doctor", command=add_doctor)
        
        # Position the buttons on the main window
        see_doctors_button.grid(row=0, column=0, padx=10, pady=5)
        add_doctor_button.grid(row=1, column=0, padx=10, pady=5)
    else:
        error_label = tk.Label(login_window, text="Incorrect username or password.")
        error_label.grid(row=2, column=0, padx=10, pady=5)
# Create the entry boxes and labels for the username and password
userid_label = tk.Label(login_window, text="Username:")
userid_label.grid(row=0, column=0, padx=10, pady=5)
userid_entry = tk.Entry(login_window)
userid_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Create the login button
login_button = tk.Button(login_window, text="Log In", command=login)
login_button.grid(row=2, column=1, padx=10, pady=5)

login_window.mainloop()
    

