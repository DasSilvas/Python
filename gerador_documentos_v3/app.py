# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import pandas as pd
from docxtpl import DocxTemplate
from tkinterdnd2 import DND_FILES, TkinterDnD


# ---------- caminhos da aplicação ----------
def obter_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def centrar_janela(janela):
    janela.update_idletasks()
    w, h = janela.winfo_width(), janela.winfo_height()
    sw, sh = janela.winfo_screenwidth(), janela.winfo_screenheight()
    janela.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


# ---------- motor de geração: mantém a lógica original ----------
def carregar_parametros(excel_path):
    df = pd.read_excel(excel_path, header=None, skiprows=1, usecols=[0, 1])
    return {
        str(k).strip(): v
        for k, v in df.itertuples(index=False)
        if pd.notna(k) and pd.notna(v)
        and str(k).strip() and str(v).strip()
    }


def processar_templates(templates, parametros, pasta_output):
    """
    templates contém caminhos relativos à pasta templates,
    por exemplo 'Estabilidade/Termo_Responsabilidade.docx'.
    """
    os.makedirs(pasta_output, exist_ok=True)
    templates_dir = os.path.join(obter_base_dir(), "templates")
    gerados = []

    for tpl_relativo in templates:
        template_path = os.path.join(templates_dir, tpl_relativo)
        if not os.path.isfile(template_path):
            raise FileNotFoundError(
                f"Não foi encontrado o modelo Word:\n{template_path}"
            )

        doc = DocxTemplate(template_path)
        doc.render(parametros)

        # Preserva a subpasta na identificação do ficheiro de saída para evitar
        # colisões se duas especialidades tiverem modelos com o mesmo nome.
        especialidade = os.path.basename(os.path.dirname(tpl_relativo))
        nome_template = os.path.basename(tpl_relativo)
        nome_saida = f"{especialidade}_{nome_template}"
        output_path = os.path.join(pasta_output, nome_saida)

        doc.save(output_path)
        gerados.append(output_path)

    return gerados


# ---------- descoberta automática de especialidades ----------
def descobrir_especialidades():
    """
    Cada subpasta imediata de templates é uma especialidade.
    Cada .docx nessa subpasta é um documento selecionável.
    Os caminhos guardados são relativos à pasta templates.
    """
    templates_dir = os.path.join(obter_base_dir(), "templates")
    os.makedirs(templates_dir, exist_ok=True)
    resultado = []

    for nome_pasta in sorted(os.listdir(templates_dir), key=str.casefold):
        caminho_pasta = os.path.join(templates_dir, nome_pasta)
        if not os.path.isdir(caminho_pasta):
            continue

        documentos = []
        for nome_ficheiro in sorted(os.listdir(caminho_pasta), key=str.casefold):
            caminho_ficheiro = os.path.join(caminho_pasta, nome_ficheiro)
            if os.path.isfile(caminho_ficheiro) and nome_ficheiro.lower().endswith(".docx"):
                caminho_relativo = os.path.join(nome_pasta, nome_ficheiro)
                documentos.append({
                    "nome": nome_ficheiro,
                    "caminho": caminho_relativo
                })

        # Ignora subpastas vazias ou que ainda não têm modelos Word.
        if documentos:
            resultado.append({
                "nome": nome_pasta.replace("_", " "),
                "pasta": nome_pasta,
                "documentos": documentos
            })

    return resultado


# ---------- lista expansível com scroll ----------
class ListaComScroll(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.conteudo = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window(
            (0, 0), window=self.conteudo, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.conteudo.bind("<Configure>", self._atualizar_scroll)
        self.canvas.bind("<Configure>", self._ajustar_largura)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", self._ativar_scroll)
        self.canvas.bind("<Leave>", self._desativar_scroll)

    def _atualizar_scroll(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _ajustar_largura(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _ativar_scroll(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._scroll_roda)
        self.canvas.bind_all("<Button-4>", self._scroll_linux)
        self.canvas.bind_all("<Button-5>", self._scroll_linux)

    def _desativar_scroll(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _scroll_roda(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _scroll_linux(self, event):
        self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")


class CartaoEspecialidade:
    def __init__(self, parent, dados, ao_alterar):
        self.dados = dados
        self.ao_alterar = ao_alterar
        self.expandido = False
        self.vars_documentos = []

        self.frame = ttk.Frame(parent, padding=(10, 8), relief="solid", borderwidth=1)
        self.frame.pack(fill="x", padx=4, pady=4)

        self.cabecalho = ttk.Frame(self.frame)
        self.cabecalho.pack(fill="x")

        self.botao_expandir = ttk.Button(
            self.cabecalho, text="▸", width=3, command=self.alternar
        )
        self.botao_expandir.pack(side="left")

        self.nome_label = ttk.Label(
            self.cabecalho, text=dados["nome"], font=("Segoe UI", 10, "bold")
        )
        self.nome_label.pack(side="left", padx=(7, 8))

        self.contagem_label = ttk.Label(self.cabecalho, text="")
        self.contagem_label.pack(side="right")

        self.corpo = ttk.Frame(self.frame, padding=(34, 8, 8, 4))
        for documento in dados["documentos"]:
            var = tk.BooleanVar(value=False)  # Seleção só existe nesta sessão.
            self.vars_documentos.append((documento, var))
            ttk.Checkbutton(
                self.corpo,
                text=documento["nome"],
                variable=var,
                command=self._alterado
            ).pack(anchor="w", pady=3)

        self.nome_label.bind("<Button-1>", lambda _e: self.alternar())
        self.cabecalho.bind("<Button-1>", lambda _e: self.alternar())
        self.atualizar_contagem()

    def alternar(self):
        self.expandido = not self.expandido
        if self.expandido:
            self.corpo.pack(fill="x")
            self.botao_expandir.configure(text="▾")
        else:
            self.corpo.pack_forget()
            self.botao_expandir.configure(text="▸")

    def _alterado(self):
        self.atualizar_contagem()
        self.ao_alterar()

    def atualizar_contagem(self):
        selecionados = sum(1 for _, var in self.vars_documentos if var.get())
        total = len(self.vars_documentos)
        self.contagem_label.configure(text=f"{selecionados}/{total} selecionado(s)")

    def selecionar_todos(self, estado):
        for _, var in self.vars_documentos:
            var.set(estado)
        self.atualizar_contagem()

    def documentos_selecionados(self):
        return [
            documento["caminho"]
            for documento, var in self.vars_documentos
            if var.get()
        ]


# ---------- interface ----------
def gui_principal():
    root = TkinterDnD.Tk()
    root.title("Gerador de Documentos")
    root.geometry("790x760")
    root.minsize(650, 580)

    try:
        ttk.Style(root).theme_use("vista" if os.name == "nt" else "clam")
    except tk.TclError:
        pass

    base_dir = obter_base_dir()
    templates_dir = os.path.join(base_dir, "templates")
    os.makedirs(templates_dir, exist_ok=True)
    especialidades = descobrir_especialidades()

    principal = ttk.Frame(root, padding=16)
    principal.pack(fill="both", expand=True)

    ttk.Label(
        principal, text="Gerador de Documentação Técnica",
        font=("Segoe UI", 16, "bold")
    ).pack(anchor="w")
    ttk.Label(
        principal,
        text="Selecione o Excel e os documentos que pretende gerar por especialidade."
    ).pack(anchor="w", pady=(3, 14))

    ficheiros_frame = ttk.LabelFrame(principal, text="Dados e destino", padding=10)
    ficheiros_frame.pack(fill="x", pady=(0, 12))

    ttk.Label(ficheiros_frame, text="Ficheiro Excel com parâmetros").grid(
        row=0, column=0, sticky="w"
    )
    excel_var = tk.StringVar(value=os.path.join(base_dir, "parametros.xlsx"))
    excel_entry = ttk.Entry(ficheiros_frame, textvariable=excel_var)
    excel_entry.grid(row=1, column=0, sticky="ew", pady=(4, 9), padx=(0, 8))

    def escolher_excel():
        caminho = filedialog.askopenfilename(
            parent=root,
            title="Selecionar ficheiro Excel",
            filetypes=[("Ficheiros Excel", "*.xlsx"), ("Todos os ficheiros", "*.*")]
        )
        if caminho:
            excel_var.set(caminho)

    def largar_excel(event):
        try:
            caminhos = root.tk.splitlist(event.data)
            caminho = caminhos[0] if caminhos else ""
            if caminho.lower().endswith(".xlsx"):
                excel_var.set(caminho)
            else:
                messagebox.showwarning(
                    "Formato inválido", "Arraste um ficheiro Excel .xlsx.", parent=root
                )
        except Exception:
            messagebox.showwarning(
                "Aviso", "Não foi possível ler o ficheiro largado.", parent=root
            )

    excel_entry.drop_target_register(DND_FILES)
    excel_entry.dnd_bind("<<Drop>>", largar_excel)
    ttk.Button(ficheiros_frame, text="Procurar…", command=escolher_excel).grid(
        row=1, column=1, sticky="ew", pady=(4, 9)
    )

    ttk.Label(ficheiros_frame, text="Pasta para guardar os documentos").grid(
        row=2, column=0, sticky="w"
    )
    pasta_var = tk.StringVar(value=os.path.join(base_dir, "output"))
    ttk.Entry(ficheiros_frame, textvariable=pasta_var).grid(
        row=3, column=0, sticky="ew", pady=(4, 0), padx=(0, 8)
    )

    def escolher_pasta():
        caminho = filedialog.askdirectory(parent=root, title="Selecionar pasta de destino")
        if caminho:
            pasta_var.set(caminho)

    ttk.Button(ficheiros_frame, text="Procurar…", command=escolher_pasta).grid(
        row=3, column=1, sticky="ew", pady=(4, 0)
    )
    ficheiros_frame.columnconfigure(0, weight=1)

    topo = ttk.Frame(principal)
    topo.pack(fill="x", pady=(0, 5))
    ttk.Label(topo, text="Especialidades", font=("Segoe UI", 11, "bold")).pack(side="left")

    lista = ListaComScroll(principal)
    lista.pack(fill="both", expand=True)

    cartoes = []

    def atualizar_resumo():
        total = sum(len(c.documentos_selecionados()) for c in cartoes)
        resumo_var.set(f"{total} documento(s) selecionado(s)")
        botao_gerar.configure(state="normal" if total else "disabled")

    def selecionar_tudo():
        for cartao in cartoes:
            cartao.selecionar_todos(True)
        atualizar_resumo()

    def desselecionar_tudo():
        for cartao in cartoes:
            cartao.selecionar_todos(False)
        atualizar_resumo()

    ttk.Button(topo, text="Selecionar tudo", command=selecionar_tudo).pack(
        side="right", padx=(5, 0)
    )
    ttk.Button(topo, text="Desselecionar tudo", command=desselecionar_tudo).pack(
        side="right"
    )

    for especialidade in especialidades:
        cartoes.append(CartaoEspecialidade(lista.conteudo, especialidade, atualizar_resumo))

    if not especialidades:
        ttk.Label(
            lista.conteudo,
            text=(
                "Ainda não existem modelos Word.\n\n"
                "Crie uma subpasta dentro de 'templates' para cada especialidade "
                "e coloque lá os ficheiros .docx."
            ),
            justify="left"
        ).pack(anchor="w", padx=12, pady=12)

    rodape = ttk.Frame(principal)
    rodape.pack(fill="x", pady=(12, 0))
    resumo_var = tk.StringVar(value="0 documentos selecionados")
    ttk.Label(rodape, textvariable=resumo_var).pack(side="left", fill="x", expand=True)

    def gerar():
        selecionados = []
        for cartao in cartoes:
            selecionados.extend(cartao.documentos_selecionados())

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhum documento selecionado.", parent=root)
            return

        excel_path = excel_var.get().strip()
        if not os.path.isfile(excel_path):
            messagebox.showwarning(
                "Aviso", f"O ficheiro Excel não existe:\n{excel_path}", parent=root
            )
            return

        pasta_output = pasta_var.get().strip()
        if not pasta_output:
            messagebox.showwarning("Aviso", "Indique a pasta de destino.", parent=root)
            return

        try:
            parametros = carregar_parametros(excel_path)
            if not parametros:
                messagebox.showwarning(
                    "Aviso", "Não encontrei parâmetros válidos no Excel.", parent=root
                )
                return
            gerados = processar_templates(selecionados, parametros, pasta_output)
        except Exception as erro:
            messagebox.showerror("Erro ao gerar documentos", str(erro), parent=root)
            return

        messagebox.showinfo(
            "Concluído",
            f"{len(gerados)} ficheiro(s) criado(s) em:\n{pasta_output}",
            parent=root
        )
        # A janela permanece aberta. Ao reabrir, as seleções começam desmarcadas.

    botao_gerar = ttk.Button(
        rodape, text="Gerar documentos selecionados",
        command=gerar, state="disabled"
    )
    botao_gerar.pack(side="right")

    centrar_janela(root)
    root.mainloop()


if __name__ == "__main__":
    gui_principal()
