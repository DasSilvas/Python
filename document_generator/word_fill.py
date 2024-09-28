from docxtpl import DocxTemplate
import pdfkit

# Function to fill the template
def fill_template(template_path, context, output_docx_path):
    # Step 1: Load the DOCX template
    template = DocxTemplate(template_path)

    # Step 2: Render the template with the context
    template.render(context)

    # Step 3: Save the filled document as DOCX
    template.save(output_docx_path)

# Define the context for rendering the template
context = {
    'requerente': 'ana vbanana',
    'titulo': 'Legalização de habitação',
    'morada': 'Rua das ruas',
    'freguesia':'Lo4543545ira',
    'concelho': 'Al123434565656a',
    'morada_cliente':'Rua ddas ruas',
    'codigo_postal_cliente': '22222',
    'freguesia_cliente': 'L2234ira',
    'concelho_cliente': '123234r'
}

# Define file paths
template_path = "C:\\Users\\joao_\\Desktop\\Python\\document_generator\\pai\\templates\\MD-ACUSTICO.docx"
output_docx_path = "C:\\Users\\joao_\\Dropbox\\02-Eng.Civil\\pai\\003-Louriceira\\02-Shared\\202409XX-Especialidades_Louriceira\\acustica\\MD-ACUSTICO.docx"

# Fill the template and generate the document
fill_template(template_path, context, output_docx_path)