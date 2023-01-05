import tkinter as tk
import tkinter.messagebox
import shutil
import os
import time
import subprocess
import re

# Name of the template folder
template_folder = "C:\\Users\\hp\\Desktop\\WORK\\00-Templates\\tema"

# Path where the new folder will be created
folder_path = "C:\\Users\\hp\\Dropbox\\01-Idea!lab"

# Create the GUI window
window = tk.Tk()
window.title("Nova Pasta")

# Set the icon and the size of the window
window.wm_iconbitmap("icone.ico")
window.geometry("+500+500")

# Center the window on the screen
window_width = 300
window_height = 100
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
next_number = max(numbers) + 1

# Generate a suggested folder name using the next available number and the current year
timestamp = time.strftime("%Y")
suggested_folder_name = f"{next_number}_{timestamp}-"

# Create a label and an entry field for the folder name
tk.Label(window, text="Nome da pasta:").pack(padx=5, pady=5)

# Create an entry field for the folder name and insert the suggested folder name
folder_name_entry = tk.Entry(window)
folder_name_entry.insert(0, suggested_folder_name)
folder_name_entry.pack(padx=5, pady=5)

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
    
    # Create the new folder
    os.makedirs(os.path.join(folder_path, folder_name))

# Copy the contents of the template folder and all its subfolders into the new folder
    for root, dirs, files in os.walk(template_folder):
        for dir in dirs:
            shutil.copytree(os.path.join(root, dir), os.path.join(folder_path, folder_name, dir))
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(folder_path, folder_name))

    # Open the newly created folder
        os.startfile(os.path.join(folder_path, folder_name))

    # Close the GUI window
    window.destroy()

# Create a "Create" button
create = tk.Button(window, text="Create", command=create_folder)
create.pack(padx=5, pady=5)

window.bind('<Return>', lambda event: create.invoke())

# Bind the Esc key to the window
window.bind('<Escape>', lambda event: window.destroy())

# Run the GUI loop
window.mainloop()
