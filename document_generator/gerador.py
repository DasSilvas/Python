import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from docxtpl import DocxTemplate
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys


def obter_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # .exe
    else:
        return os.path.dirname(os.path.abspath(__file__))  # .py

# ---------- utilitário para centrar janelas ----------
def centrar_janela(janela):
    janela.update_idletasks()
    w, h = janela.winfo_width(), janela.winfo_height()
    sw, sh = janela.winfo_screenwidth(), janela.winfo_screenheight()
    janela.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


# ---------- carregar parâmetros ----------
def carregar_parametros(excel_path):
    df = pd.read_excel(excel_path, header=None, skiprows=1, usecols=[0, 1])
    return {str(k).strip(): v for k, v in df.itertuples(index=False)
            if pd.notna(v) and str(v).strip()}


# ---------- renderizar templates ----------
def processar_templates(templates, parametros, pasta_output):
    os.makedirs(pasta_output, exist_ok=True)
    base_dir = obter_base_dir()
    templates_dir = os.path.join(base_dir, "templates")

    for tpl_name in templates:
        doc = DocxTemplate(os.path.join(templates_dir, tpl_name))
        doc.render(parametros)
        doc.save(os.path.join(pasta_output, tpl_name))

    messagebox.showinfo("Concluído",
                        f"{len(templates)} ficheiro(s) criado(s) em «{pasta_output}».")
    

# ---------- interface ----------
def gui_principal():
    root = TkinterDnD.Tk()
    root.title("Gerador de Documentos")
    frame = ttk.Frame(root, padding=20); frame.pack()

    ttk.Label(frame, text="Selecione os templates Word:").pack(anchor="w")

    # --- garantir que a pasta templates existe ---
    base_dir = obter_base_dir()
    templates_dir = os.path.join(base_dir, "templates")
    os.makedirs(templates_dir, exist_ok=True)

    ficheiros = [f for f in os.listdir(templates_dir) if f.lower().endswith(".docx")]
    if not ficheiros:
        messagebox.showinfo("Informação",
                            f"A pasta «{templates_dir}» está vazia.\nColoque lá ficheiros .docx.")
    vars_cks  = []
    last_idx  = {'idx': None}

    def on_click(event, idx):
        if event.state & 0x0001 and last_idx['idx'] is not None:
            novo_estado = not vars_cks[idx].get()
            i1, i2 = sorted((last_idx['idx'], idx))
            for j in range(i1, i2 + 1):
                vars_cks[j].set(novo_estado)
        last_idx['idx'] = idx

    for i, ficheiro in enumerate(ficheiros):
        var = tk.BooleanVar()
        vars_cks.append(var)
        cb = tk.Checkbutton(frame, text=ficheiro, variable=var, anchor='w')
        cb.pack(fill='x', anchor='w')
        cb.bind('<Button-1>', lambda e, j=i: on_click(e, j))

    # --- botões Selecionar / Desselecionar tudo ---
    def selecionar_tudo():     [v.set(True)  for v in vars_cks]
    def desselecionar_tudo():  [v.set(False) for v in vars_cks]

    bf = ttk.Frame(frame); bf.pack(pady=5)
    ttk.Button(bf, text="Selecionar tudo",   command=selecionar_tudo).pack(side="left", padx=5)
    ttk.Button(bf, text="Desselecionar tudo", command=desselecionar_tudo).pack(side="left", padx=5)

    # --- escolher ficheiro Excel ---
    ttk.Label(frame, text="Ficheiro Excel com parâmetros:").pack(anchor="w", pady=(10,0))
    ef = ttk.Frame(frame); ef.pack(fill='x', pady=(0,10))
    excel_var = tk.StringVar(value="parametros.xlsx")  # valor por defeito

    entry_excel = ttk.Entry(ef, textvariable=excel_var, width=45)
    entry_excel.pack(side='left', fill='x', expand=True)

    def escolher_excel():
        ficheiro = filedialog.askopenfilename(filetypes=[("Ficheiros Excel", "*.xlsx")])
        if ficheiro:
            excel_var.set(ficheiro)

    def drop_excel(event):
        caminho = event.data.strip()

        if caminho.startswith("{") and caminho.endswith("}"):
            caminho = caminho[1:-1]

        if caminho.lower().endswith(".xlsx"):
            excel_var.set(caminho)
        else:
            messagebox.showwarning("Aviso", "Por favor arraste um ficheiro .xlsx válido.")

    entry_excel.drop_target_register(DND_FILES)
    entry_excel.dnd_bind('<<Drop>>', drop_excel)

    ttk.Button(ef, text="Procurar...", command=escolher_excel).pack(side='left', padx=5)

    # --- pasta de saída ---
    ttk.Label(frame, text="Pasta para guardar ficheiros gerados:").pack(anchor="w", pady=(10,0))
    pf = ttk.Frame(frame); pf.pack(fill='x', pady=(0,10))
    pasta_var = tk.StringVar()
    ttk.Entry(pf, textvariable=pasta_var, width=45).pack(side='left', fill='x', expand=True)

    def escolher_pasta():
        pasta = filedialog.askdirectory()
        if pasta: pasta_var.set(pasta)
    ttk.Button(pf, text="Procurar...", command=escolher_pasta).pack(side='left', padx=5)

    # --- gerar documentos ---
    def ao_confirmar():
        selecionados = [f for f, v in zip(ficheiros, vars_cks) if v.get()]
        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhum ficheiro selecionado."); return
        pasta_out = pasta_var.get().strip()
        if not pasta_out:
            messagebox.showwarning("Aviso", "Indique a pasta de destino.");  return
        excel_path = excel_var.get().strip()
        if not os.path.isfile(excel_path):
            messagebox.showwarning("Aviso", f"O ficheiro Excel não existe:\n{excel_path}"); return
        try:
            parametros = carregar_parametros(excel_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Problema ao ler o Excel:\n{e}");   return
        if not parametros:
            messagebox.showwarning("Aviso", "Não encontrei parâmetros válidos no Excel."); return
        processar_templates(selecionados, parametros, pasta_out)
        root.destroy()

    ttk.Button(frame, text="Gerar documentos", command=ao_confirmar).pack(pady=10)

    centrar_janela(root)
    root.mainloop()


# ---------- correr ----------
if __name__ == "__main__":
    gui_principal()
