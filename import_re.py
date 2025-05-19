import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import re
# import csv
import os
from pathlib import Path


# Funções principais
def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto


def extrair_linhas_adicionais(texto):
    return [f"V09{linha}" for linha in re.findall(r"(0\w+\*[^\n\r]*)", texto)]


def salvar_arquivos(linhas, nome_base):
    pasta_downloads = str(Path.home() / "Downloads")
    caminho_csv = os.path.join(pasta_downloads, f"{nome_base}.csv")
    caminho_txt = os.path.join(pasta_downloads, f"{nome_base}.txt")

    # Salvar CSV
    # with open(caminho_csv, 'w', newline='', encoding='utf-8') as f_csv:
    #    writer = csv.writer(f_csv)
    #    writer.writerow(["Informações Adicionais"])
    #    for linha in linhas:
    #        writer.writerow([linha])

    # Salvar TXT
    with open(caminho_txt, 'w', encoding='utf-8') as f_txt:
        for linha in linhas:
            f_txt.write(f"{linha}\n")

    return caminho_csv, caminho_txt


# Função acionada no botão
def processar_pdf():
    caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not caminho_pdf:
        return

    texto = extrair_texto_pdf(caminho_pdf)
    linhas = extrair_linhas_adicionais(texto)

    if not linhas:
        messagebox.showinfo("Resultado", "Nenhuma informação encontrada!")
        return

    nome_base = Path(caminho_pdf).stem + "_informacoes"
    caminho_csv, caminho_txt = salvar_arquivos(linhas, nome_base)

    messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{caminho_txt}")


# Interface com customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Extrator de serial Vertco")

# Defina tamanho da janela
largura_janela = 500
altura_janela = 300

# Obtenha largura e altura da tela do usuário
largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()

# Calcule a posição para centralizar
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)

# Aplique a geometria centralizada
app.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Widgets
label = ctk.CTkLabel(app, text="Selecione o arquivo PDF para extrair o serial.", font=ctk.CTkFont(size=20))
label.pack(pady=30)

botao = ctk.CTkButton(app, fg_color=("orangered"), text="Selecionar PDF", command=processar_pdf)
botao.pack(pady=10)

app.mainloop()
