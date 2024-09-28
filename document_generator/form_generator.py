import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from tkinterdnd2 import TkinterDnD, DND_FILES
from docxtpl import DocxTemplate

# Function to fill the DOCX template
def fill_template(template_path, context, output_docx_path):
    # Step 1: Load the DOCX template
    try:
        template = DocxTemplate(template_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load template: {e}")
        return
    
    # Step 2: Render the template with the context
    try:
        template.render(context)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to render template: {e}")
        return
    
    # Step 3: Save the filled document as DOCX
    try:
        template.save(output_docx_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save document: {e}")

# Load data from a JSON file
def load_data_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            clear_fields()
            for key, entry in zip(data.keys(), entries.values()):
                entry.insert(0, data.get(key, ""))
        messagebox.showinfo("Info", "Data loaded successfully!")
    else:
        messagebox.showwarning("Warning", "The selected file does not exist.")

# Save data to a user-specified JSON file
def save_data():
    data = {key: entry.get() for key, entry in entries.items()}
    file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                             filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(data, f)
        messagebox.showinfo("Info", "Data saved successfully!")

# Load data from a user-specified JSON file
def load_data():
    file_path = filedialog.askopenfilename(defaultextension=".json", 
                                           filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        load_data_from_file(file_path)
    else:
        messagebox.showwarning("Warning", "No file was selected.")

# Clear the input fields
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)

# Handle drag-and-drop files
def drop(event):
    load_data_from_file(event.data.strip("{}"))

# Open the form window for template selection
def open_form_window():
    form_window = tk.Toplevel(root)
    form_window.title("MD Estabilidade Form")

    templates_info = [
        {"label": "MD Acustica", "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ACUSTICO.docx"},
        {"label": "MD Abastecimento de água", "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ABASTECIMENTO AGUA.docx"},
        {"label": "MD Esgotos domésticos", "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESGOTOS DOMESTICOS.docx"},
        {"label": "MD Esgotos pluviais", "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESGOTOS PLUVIAIS.docx"},
        {"label": "MD Estabilidade", "template_path": "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\00-TEMPLATES\\md_template\\MD-ESTABILIDADE.docx"}
    ]

    checkbox_vars = {info['label']: tk.IntVar() for info in templates_info}
    for idx, info in enumerate(templates_info):
        tk.Checkbutton(form_window, text=info['label'], variable=checkbox_vars[info['label']]).grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    # Run button in the form window
    tk.Button(form_window, text="Run", command=lambda: run_form(checkbox_vars, templates_info)).grid(row=len(templates_info), column=0, padx=10, pady=10)

# Run the selected templates
def run_form(checkbox_vars, templates_info):
    context = {key: entry.get() for key, entry in entries.items()}
    for info in templates_info:
        if checkbox_vars[info['label']].get() == 1:
            output_docx_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("DOCX files", "*.docx")], title=f"Save {info['label']} As")
            if output_docx_path:
                fill_template(info['template_path'], context, output_docx_path)
                messagebox.showinfo("Success", f"{info['label']} document generated successfully at:\n{output_docx_path}")
            else:
                messagebox.showwarning("Warning", f"Saving {info['label']} was cancelled.")

# Create the menu bar
def create_menu():
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save", command=save_data)
    file_menu.add_command(label="Load", command=load_data)
    file_menu.add_separator()
    file_menu.add_command(label="Clear", command=clear_fields)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

# Create the main window
root = TkinterDnD.Tk()
root.title("Form Application")

# Create Labels and Entry widgets
labels = ["Requerente", "Título", "Morada", "Freguesia", "Concelho", "Morada Cliente", "Código Postal Cliente", "Freguesia Cliente", "Concelho Cliente"]
entries = {label.lower().replace(" ", "_"): tk.Entry(root) for label in labels}

for idx, label in enumerate(labels):
    tk.Label(root, text=label + ":").grid(row=idx, column=0, padx=10, pady=10)
    entries[label.lower().replace(" ", "_")].grid(row=idx, column=1, padx=10, pady=10)

# Button to open the form window for template selection
tk.Button(root, text="Select Templates", command=open_form_window).grid(row=len(labels), columnspan=2, pady=20)

# Create the menu bar
create_menu()

# Bind the drop event for file drag-and-drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Start the main event loop
root.mainloop()