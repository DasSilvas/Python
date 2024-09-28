import tkinter as tk
from tkinter import messagebox
import csv
import os

# Function to save parameters to CSV
def save_to_csv(parameters, csv_file):
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=parameters.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(parameters)

# Function to handle form submission
def submit_form(entries):
    parameters = {param: entry.get() for param, entry in entries.items()}
    
    if not all(parameters.values()):
        messagebox.showerror("Input Error", "All fields are required")
        return

    save_to_csv(parameters, 'parameters.csv')
    messagebox.showinfo("Success", "Parameters saved to CSV")

# Function to create input fields and labels
def create_input_fields(root, parameters):
    entries = {}
    for i, param in enumerate(parameters):
        tk.Label(root, text=f"{param}:").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[param] = entry
    return entries

# Create the main Tkinter window
root = tk.Tk()
root.title("Parameter Input Form")

# Define the parameters
parameters = ["Name", "Date", "Address"]

# Create input fields
entries = create_input_fields(root, parameters)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=lambda: submit_form(entries))
submit_button.grid(row=len(parameters), columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
