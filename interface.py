import customtkinter as ctk
import requests
import csv
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

API_URL = "http://127.0.0.1:5000/clientes"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📋 Sistema de Clientes")
        self.geometry("800x700")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self.cliente_em_edicao = None

        self.titulo = ctk.CTkLabel(self, text="SISTEMA DE CADASTRO DE CLIENTES", font=("Arial Bold", 22))
        self.titulo.pack(pady=10)

        self.nome = ctk.CTkEntry(self, placeholder_text="Nome")
        self.nome.pack(pady=5, fill="x")

        self.idade = ctk.CTkEntry(self, placeholder_text="Idade")
        self.idade.pack(pady=5, fill="x")

        self.cpf = ctk.CTkEntry(self, placeholder_text="CPF")
        self.cpf.pack(pady=5, fill="x")
        self.cpf.bind("<KeyRelease>", self.formatar_cpf)

        self.cidade = ctk.CTkEntry(self, placeholder_text="Cidade")
        self.cidade.pack(pady=5, fill="x")

        self.botao_cadastrar = ctk.CTkButton(self, text="➕ Cadastrar", command=self.cadastrar_ou_atualizar)
        self.botao_cadastrar.pack(pady=10)

        self.botao_planilha = ctk.CTkButton(self, text="📁 Gerar Planilha", command=self.gerar_planilha)
        self.botao_planilha.pack(pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=750, height=400)
        self.scroll_frame.pack(pady=10)

        self.listar_clientes()

    def formatar_cpf(self, event=None):
        texto = self.cpf.get()
        texto = ''.join(filter(str.isdigit, texto))[:11]  # Apenas números

        formatado = ""
        if len(texto) > 0:
            formatado += texto[:3]
        if len(texto) >= 4:
            formatado += '.' + texto[3:6]
        if len(texto) >= 7:
            formatado += '.' + texto[6:9]
        if len(texto) >= 10:
            formatado += '-' + texto[9:11]

        self.cpf.delete(0, "end")
        self.cpf.insert(0, formatado)

    def limpar_campos(self):
        self.nome.delete(0, "end")
        self.idade.delete(0, "end")
        self.cpf.delete(0, "end")
        self.cidade.delete(0, "end")
        self.cliente_em_edicao = None
        self.botao_cadastrar.configure(text="➕ Cadastrar")

    def cadastrar_ou_atualizar(self):
        dados = {
            "nome": self.nome.get(),
            "idade": int(self.idade.get()),
            "cpf": self.cpf.get(),
            "cidade": self.cidade.get()
        }

        if self.cliente_em_edicao:
            id_cliente = self.cliente_em_edicao
            r = requests.put(f"{API_URL}/{id_cliente}", json=dados)
        else:
            r = requests.post(API_URL, json=dados)

        if r.ok:
            self.limpar_campos()
            self.listar_clientes()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o cliente.")

    def listar_clientes(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        r = requests.get(API_URL)
        if r.ok:
            clientes = r.json()
            for cliente in clientes:
                self.criar_card_cliente(cliente)

    def criar_card_cliente(self, cliente):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.pack(padx=5, pady=5, fill="x")

        texto = f"🆔 {cliente['id']} | {cliente['nome']} | CPF: {cliente['cpf']} | {cliente['cidade']}"
        label = ctk.CTkLabel(frame, text=texto, anchor="w")
        label.pack(side="left", padx=10)

        btn_editar = ctk.CTkButton(frame, text="✏ Editar", width=80, command=lambda: self.preencher_para_editar(cliente))
        btn_editar.pack(side="right", padx=5)

        btn_excluir = ctk.CTkButton(frame, text="🗑 Excluir", width=80, fg_color="red", hover_color="#880000",
                                    command=lambda: self.excluir_cliente(cliente['id']))
        btn_excluir.pack(side="right", padx=5)

    def preencher_para_editar(self, cliente):
        self.nome.delete(0, "end")
        self.nome.insert(0, cliente["nome"])

        self.idade.delete(0, "end")
        self.idade.insert(0, cliente["idade"])

        self.cpf.delete(0, "end")
        self.cpf.insert(0, cliente["cpf"])

        self.cidade.delete(0, "end")
        self.cidade.insert(0, cliente["cidade"])

        self.cliente_em_edicao = cliente["id"]
        self.botao_cadastrar.configure(text="✏ Atualizar")

    def excluir_cliente(self, id_cliente):
        r = requests.delete(f"{API_URL}/{id_cliente}")
        if r.ok:
            self.listar_clientes()
        else:
            messagebox.showerror("Erro", "Erro ao excluir cliente.")

    def gerar_planilha(self):
        r = requests.get(API_URL)
        if r.ok:
            clientes = r.json()
            caminho = "clientes.csv"
            with open(caminho, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nome", "Idade", "CPF", "Cidade"])
                for cliente in clientes:
                    writer.writerow([
                        cliente["id"],
                        cliente["nome"],
                        cliente["idade"],
                        cliente["cpf"],
                        cliente["cidade"]
                    ])
            messagebox.showinfo("Planilha Gerada", f"Arquivo '{caminho}' criado/atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível gerar a planilha.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
