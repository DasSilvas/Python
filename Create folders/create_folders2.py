import tkinter as tk
import tkinter.messagebox
import shutil
import os
import time
import re

# Name of the template folder
template_folder = "C:\\Users\\hp\\Desktop\\WORK\\00-Templates\\tema"
template_folder_NAS = "C:\\Users\\hp\\Desktop\\WORK\\00-Templates\\tema"

# Path where the new folder will be created
folder_path = "C:\\Users\\hp\\Dropbox\\01-Idea!lab"

# Alternate path where the new folder will be created
folder_path_NAS = "C:\\Users\\hp\\Dropbox\\01 - SER-RA"

# Create the GUI window
window = tk.Tk()
window.title("Nova pasta")

# Set the icon and the size of the window
window.wm_iconbitmap("icone.ico")
window.geometry("+500+500")

# Center the window on the screen
window_width = 300
window_height = 140
window.geometry(f"{window_width}x{window_height}+{int((window.winfo_screenwidth() - window_width) / 2)}+{int((window.winfo_screenheight() - window_height) / 2)}")

# Get a list of the existing folders in the folder path
existing_folders = os.listdir(folder_path)

# Extract the numbers from the names of the existing folders
numbers = []
for folder in existing_folders:
    match = re.search(r'(\d+)_(\d+)', folder)
    if match:
        numbers.append(int(match.group(1)))

# Find the next available number
next_number = max(numbers) + 1 if numbers else 1

# Generate a suggested folder name using the next available number and the current year
timestamp = time.strftime("%Y")
suggested_folder_name = f"{next_number}_{timestamp}-"

# Create a label and an entry field for the folder name
folder_name_label = tk.Label(window, text="Nome da pasta:")
folder_name_label.pack(padx=5, pady=5)

# Create an entry field for the folder name and insert the suggested folder name
folder_name_entry = tk.Entry(window)
folder_name_entry.insert(0, suggested_folder_name)
folder_name_entry.pack(padx=5, pady=5)

# Create a checkbox for the option to create a copy of the folder in the additional path
alternate_folder_var = tk.IntVar()
alternate_folder_checkbox = tk.Checkbutton(window, text="Criar na NAS", variable=alternate_folder_var)
alternate_folder_checkbox.pack(padx=5, pady=5)

# Define a function to be called when the "Create" button is clicked
def create_folder():
    # Get the folder name from the entry field
    folder_name = folder_name_entry.get()
    
    # Check if the folder already exists
    while os.path.exists(os.path.join(folder_path, folder_name)):
        # Display a prompt to ask the user to enter a new folder name
        messagebox = tkinter.messagebox.askretrycancel("Error", "O nome da pasta já existe. Dá outro nome")
        if messagebox:
            # Get the new folder name from the entry field
            folder_name = folder_name_entry.get()
        else:
            return
    
    # create the destination path 
    destination = os.path.join(folder_path, folder_name)

    shutil.copytree(template_folder, destination)
    # Copy the template folder to the new folder path
# Copy the template folder to the desired path
    if alternate_folder_var.get() == 1:
        destination_NAS = os.path.join(folder_path_NAS, folder_name)
        shutil.copytree(template_folder_NAS, destination_NAS)

    # Open the newly created folder
    os.startfile(destination)

    # Close the GUI window
    window.destroy()

# Create a "Create" button
create = tk.Button(window, text="Criar pasta", command=create_folder)
create.pack(padx=5, pady=5)

window.bind('<Return>', lambda event: create.invoke())

# Bind the Esc key to the window
window.bind('<Escape>', lambda event: window.destroy())

# Run the GUI loop
window.mainloop()
