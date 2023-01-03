import tkinter as tk
import tkinter.messagebox
import shutil
import os

# Name of the template folder
template_folder = "C:\\Users\\hp\\Desktop\\WORK\\00-Templates\\tema"

# Path where the new folder will be created
folder_path = "C:\\Users\\hp\\Desktop"

# Create the GUI window
window = tk.Tk()
window.title("Create New Folder")

# Create a label and an entry field for the folder name
tk.Label(window, text="Folder Name:").pack(padx=5, pady=5)
folder_name_entry = tk.Entry(window)
folder_name_entry.pack(padx=5, pady=5)

# Define a function to be called when the "Create" button is clicked
def create_folder():
    # Get the folder name from the entry field
    folder_name = folder_name_entry.get()
    
    # Check if the folder already exists
    if os.path.exists(os.path.join(folder_path, folder_name)):
        # Display a prompt to ask the user to enter a new folder name
        tk.messagebox.showinfo("Error", "O nome da pasta já existe. Dá outro nome")
    else:
        # Create the new folder
        os.makedirs(os.path.join(folder_path, folder_name))

# Copy the contents of the template folder and all its subfolders into the new folder
    for root, dirs, files in os.walk(template_folder):
        for dir in dirs:
            shutil.copytree(os.path.join(root, dir), os.path.join(folder_path, folder_name, dir))
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(folder_path, folder_name))

    # Close the GUI window
    window.destroy()

# Create a "Create" button
tk.Button(window, text="Create", command=create_folder).pack(padx=5, pady=5)

# Run the GUI loop
window.mainloop()