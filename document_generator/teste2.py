import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import TkinterDnD for drag-and-drop functionality
from docxtpl import DocxTemplate


# Function to fill the DOCX template
def fill_template(template_path, context, output_docx_path):
    # Step 1: Load the DOCX template
    template = DocxTemplate(template_path)

    # Step 2: Render the template with the context
    template.render(context)

    # Step 3: Save the filled document as DOCX
    template.save(output_docx_path)


# Function to load data from the specified file path
def load_data_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Clear the fields
        clear_fields()

        # Populate the fields with the loaded data
        entry_requerente.insert(0, data.get("requerente", ""))
        entry_titulo.insert(0, data.get("titulo", ""))
        entry_morada.insert(0, data.get("morada", ""))
        entry_freguesia.insert(0, data.get("freguesia", ""))
        entry_concelho.insert(0, data.get("concelho", ""))
        entry_morada_cliente.insert(0, data.get("morada_cliente", ""))
        entry_codigo_cliente.insert(0, data.get("codigo_cliente", ""))
        entry_freguesia_cliente.insert(0, data.get("freguesia_cliente", ""))
        entry_concelho_cliente.insert(0, data.get("concelho_cliente", ""))

        messagebox.showinfo("Info", "Data loaded successfully!")
    else:
        messagebox.showwarning("Warning", "The selected file does not exist.")


# Function to save data to a user-specified JSON file
def save_data():
    data = {
        "requerente": entry_requerente.get(),
        "titulo": entry_titulo.get(),
        "morada": entry_morada.get(),
        "freguesia": entry_freguesia.get(),
        "concelho": entry_concelho.get(),
        "morada_cliente": entry_morada_cliente.get(),
        "codigo_cliente": entry_codigo_cliente.get(),
        "freguesia_cliente": entry_freguesia_cliente.get(),
        "concelho_cliente": entry_concelho_cliente.get(),
    }

    # Open a file dialog for saving the file
    file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

    # Save the data if a path is selected
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(data, f)

        messagebox.showinfo("Info", "Data saved successfully!")
    else:
        messagebox.showwarning("Warning", "Save operation was cancelled.")


# Function to load data from a user-specified JSON file
def load_data():
    # Open a file dialog for selecting the file to load
    file_path = filedialog.askopenfilename(defaultextension=".json",
                                           filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

    # Load the data if a file is selected
    if file_path:
        load_data_from_file(file_path)
    else:
        messagebox.showwarning("Warning", "No file was selected.")


# Function to clear the input fields
def clear_fields():
    entry_requerente.delete(0, tk.END)
    entry_titulo.delete(0, tk.END)
    entry_morada.delete(0, tk.END)
    entry_freguesia.delete(0, tk.END)
    entry_concelho.delete(0, tk.END)
    entry_morada_cliente.delete(0, tk.END)
    entry_codigo_cliente.delete(0, tk.END)
    entry_freguesia_cliente.delete(0, tk.END)
    entry_concelho_cliente.delete(0, tk.END)


# Function to handle drag-and-drop files
def drop(event):
    file_path = event.data
    # Remove curly braces around path if they exist
    file_path = file_path.strip("{}")
    load_data_from_file(file_path)


# Function to open the form window with variable checkboxes
def open_form_window():
    # Create a new window
    form_window = tk.Toplevel(root)
    form_window.title("MD Estabilidade Form")

    # List of checkboxes and their corresponding file paths
    templates_info = [
        {
            "label": "MD Acustica",
            "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ACUSTICO.docx"
        },
        {
            "label": "MD Abastecimento de água",
            "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ABASTECIMENTO AGUA.docx"
        },
        {
            "label": "MD Esgotos domésticos",
            "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESGOTOS DOMESTICOS.docx"
        },
        {
            "label": "MD Esgotos pluviais",
            "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESGOTOS PLUVIAIS.docx"
        },
        {
            "label": "MD Estabilidade",
            "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESTABILIDADE.docx"
        }
    ]

    # Dictionary to store the IntVar for each checkbox
    checkbox_vars = {}

    # Create checkboxes dynamically
    for idx, info in enumerate(templates_info):
        checkbox_vars[info['label']] = tk.IntVar()  # Create a new IntVar for each checkbox
        checkbox = tk.Checkbutton(form_window, text=info['label'], variable=checkbox_vars[info['label']])
        checkbox.grid(row=idx, column=0, padx=10, pady=5, sticky="w")  # Display each checkbox on a new row

    # Run button in the new form window
    def run_form():
        # Collect information from the main window (the first window with the user inputs)
        context = {
            "requerente": entry_requerente.get(),
            "titulo": entry_titulo.get(),
            "morada": entry_morada.get(),
            "freguesia": entry_freguesia.get(),
            "concelho": entry_concelho.get(),
            "morada_cliente": entry_morada_cliente.get(),
            "codigo_cliente": entry_codigo_cliente.get(),
            "freguesia_cliente": entry_freguesia_cliente.get(),
            "concelho_cliente": entry_concelho_cliente.get(),
        }

        # Loop through each checkbox and check if it's selected
        for info in templates_info:
            if checkbox_vars[info['label']].get() == 1:
                # Open file dialog to choose the output path for each selected template
                output_docx_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                                filetypes=[("DOCX files", "*.docx")],
                                                                title=f"Save {info['label']} As")

                if output_docx_path:  # If the user didn't cancel the file dialog
                    # Fill the template and save it to the selected path, using the context from the first window
                    fill_template(info['template_path'], context, output_docx_path)
                    messagebox.showinfo("Success", f"{info['label']} document generated successfully at:\n{output_docx_path}")
                else:
                    messagebox.showwarning("Warning", f"Saving {info['label']} was cancelled.")

    # Add Run button at the bottom of the form
    btn_run = tk.Button(form_window, text="Run", command=run_form)
    btn_run.grid(row=len(templates_info), column=0, padx=10, pady=10)


# Function to create the dropdown menu
def create_menu():
    menubar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save", command=save_data)
    file_menu.add_command(label="Load", command=load_data)
    file_menu.add_separator()  # Adds a separator line
    file_menu.add_command(label="Clear", command=clear_fields)

    menubar.add_cascade(label="File", menu=file_menu)

    # Add the menubar to the root window
    root.config(menu=menubar)


# Create the main window with drag-and-drop support
root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop functionality
root.title("Form Application")

# Create Labels and Entry widgets
label_requerente = tk.Label(root, text="Requerente:")
label_requerente.grid(row=0, column=0, padx=10, pady=10)

entry_requerente = tk.Entry(root)
entry_requerente.grid(row=0, column=1, padx=10, pady=10)

label_titulo = tk.Label(root, text="Título:")
label_titulo.grid(row=1, column=0, padx=10, pady=10)

entry_titulo = tk.Entry(root)
entry_titulo.grid(row=1, column=1, padx=10, pady=10)

label_morada = tk.Label(root, text="Morada:")
label_morada.grid(row=2, column=0, padx=10, pady=10)

entry_morada = tk.Entry(root)
entry_morada.grid(row=2, column=1, padx=10, pady=10)

label_freguesia = tk.Label(root, text="Freguesia:")
label_freguesia.grid(row=3, column=0, padx=10, pady=10)

entry_freguesia = tk.Entry(root)
entry_freguesia.grid(row=3, column=1, padx=10, pady=10)

label_concelho = tk.Label(root, text="Concelho:")
label_concelho.grid(row=4, column=0, padx=10, pady=10)

entry_concelho = tk.Entry(root)
entry_concelho.grid(row=4, column=1, padx=10, pady=10)

label_morada_cliente = tk.Label(root, text="Morada Cliente:")
label_morada_cliente.grid(row=5, column=0, padx=10, pady=10)

entry_morada_cliente = tk.Entry(root)
entry_morada_cliente.grid(row=5, column=1, padx=10, pady=10)

label_codigo_cliente = tk.Label(root, text="Código Cliente:")
label_codigo_cliente.grid(row=6, column=0, padx=10, pady=10)

entry_codigo_cliente = tk.Entry(root)
entry_codigo_cliente.grid(row=6, column=1, padx=10, pady=10)

label_freguesia_cliente = tk.Label(root, text="Freguesia Cliente:")
label_freguesia_cliente.grid(row=7, column=0, padx=10, pady=10)

entry_freguesia_cliente = tk.Entry(root)
entry_freguesia_cliente.grid(row=7, column=1, padx=10, pady=10)

label_concelho_cliente = tk.Label(root, text="Concelho Cliente:")
label_concelho_cliente.grid(row=8, column=0, padx=10, pady=10)

entry_concelho_cliente = tk.Entry(root)
entry_concelho_cliente.grid(row=8, column=1, padx=10, pady=10)

# Button to open the form window for template selection
btn_open_form = tk.Button(root, text="Select Templates", command=open_form_window)
btn_open_form.grid(row=9, columnspan=2, pady=20)

# Create the menu bar
create_menu()

# Bind the drop event to the root window for file drag-and-drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Start the main event loop
root.mainloop()




