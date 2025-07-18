import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import requests

URL_BASE = "http://127.0.0.1:5000"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
'''
O método __init__ será executado automaticamente.
Pode colocar parâmetros dentro do __init__ para passar dados na criação
self é uma convenção de nome para o primeiro parâmetro de qualquer método de instância em uma classe.
Dentro do método __init__(self), o self permite que
acesse e defina atributos da instância, como self.nome = "João", que fica guardado dentro do objeto.
Diferencie variáveis do objeto (atributos) das variáveis locais do método.
'''
class App(ctk.CTk):
    def __init__(self):
        super().__init__() # Inicializa a janela principal da aplicação CustomTkinter,chama o construtor da classe pai (CTk) para iniciar a janela do CustomTkinter.

        self.title("Sistema de Atendimento")
        self.geometry("600x600")
        self.resizable(False, False)
        self.atendente_logado = None

        self.frame_login = None
        self.frame_principal = None

        self.servicos = []
        self.clientes = []

        self.criar_frame_login()

    def criar_frame_login(self):
        if self.frame_principal:
            self.frame_principal.destroy()
        if self.frame_login:
            self.frame_login.destroy()

        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(self.frame_login, text="Login do Atendente", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        self.entry_login = ctk.CTkEntry(self.frame_login, placeholder_text="Digite o nome do atendente")
        self.entry_login.pack(pady=10)

        btn_login = ctk.CTkButton(self.frame_login, text="Entrar", command=self.tentar_login)
        btn_login.pack(pady=10)

    def tentar_login(self):
        nome = self.entry_login.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do atendente.")
            return
        
        try:
            resp = requests.get(f"{URL_BASE}/atendentes")
            if resp.status_code == 200:
                atendentes = resp.json()
                if nome in atendentes:
                    self.atendente_logado = nome
                    self.criar_frame_principal()
                else:
                    messagebox.showerror("Erro", "Atendente não encontrado.")
            else:
                messagebox.showerror("Erro", "Erro ao acessar o servidor.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão com o servidor.")

    def criar_frame_principal(self):
        self.frame_login.destroy()

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        topo = ctk.CTkFrame(self.frame_principal)
        topo.pack(fill="x", pady=(0, 10))

        label_user = ctk.CTkLabel(topo, text=f"Atendente: {self.atendente_logado}", font=ctk.CTkFont(size=14, weight="bold"))
        label_user.pack(side="left", padx=10)

        btn_sair = ctk.CTkButton(topo, text="Sair", width=60, command=self.sair)
        btn_sair.pack(side="right", padx=10)

        atendimento_frame = ctk.CTkFrame(self.frame_principal)
        atendimento_frame.pack(fill="both", expand=True)

        # Cliente
        label_cliente = ctk.CTkLabel(atendimento_frame, text="Cliente:")
        label_cliente.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.entry_cliente = ctk.CTkEntry(atendimento_frame)
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_cliente.bind("<KeyRelease>", self.atualizar_sugestoes_clientes)

        self.lista_sugestoes = tk.Listbox(atendimento_frame, height=5)
        self.lista_sugestoes.grid(row=1, column=1, sticky="ew", padx=5)
        self.lista_sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao_cliente)
        self.lista_sugestoes.grid_remove()

        btn_add_cliente = ctk.CTkButton(atendimento_frame, text="Adicionar Cliente", width=130, command=self.abrir_popup_add_cliente)
        btn_add_cliente.grid(row=0, column=2, padx=10, pady=5)

        # Serviço com autocomplete
        label_servico = ctk.CTkLabel(atendimento_frame, text="Serviço:")
        label_servico.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.entry_servico = ctk.CTkEntry(atendimento_frame)
        self.entry_servico.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.entry_servico.bind("<KeyRelease>", self.atualizar_sugestoes_servicos)

        self.lista_sugestoes_servicos = tk.Listbox(atendimento_frame, height=5)
        self.lista_sugestoes_servicos.grid(row=3, column=1, sticky="ew", padx=5)
        self.lista_sugestoes_servicos.bind("<<ListboxSelect>>", self.selecionar_sugestao_servico)
        self.lista_sugestoes_servicos.grid_remove()

        # Nota
        label_nota = ctk.CTkLabel(atendimento_frame, text="Nota (0-10):")
        label_nota.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.entry_nota = ctk.CTkEntry(atendimento_frame)
        self.entry_nota.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        btn_cadastrar = ctk.CTkButton(atendimento_frame, text="Registrar Atendimento", command=self.cadastrar_atendimento)
        btn_cadastrar.grid(row=5, column=0, columnspan=3, pady=10)

        label_lista = ctk.CTkLabel(self.frame_principal, text="Atendimentos realizados:")
        label_lista.pack(anchor="w", padx=10)

        self.texto_atendimentos = ctk.CTkTextbox(self.frame_principal, width=580, height=250)
        self.texto_atendimentos.pack(padx=10, pady=5)

        atendimento_frame.grid_columnconfigure(1, weight=1)

        self.carregar_servicos()
        self.carregar_clientes()
        self.atualizar_lista_atendimentos()

    def abrir_popup_add_cliente(self):
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Adicionar Cliente")
        self.popup.geometry("300x150")
        self.popup.resizable(False, False)

        label = ctk.CTkLabel(self.popup, text="Nome do Cliente:")
        label.pack(pady=(20, 5))

        self.entry_novo_cliente = ctk.CTkEntry(self.popup)
        self.entry_novo_cliente.pack(pady=5)

        btn_salvar = ctk.CTkButton(self.popup, text="Salvar", command=self.adicionar_cliente)
        btn_salvar.pack(pady=10)

    def adicionar_cliente(self):
        nome = self.entry_novo_cliente.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Informe o nome do cliente.")
            return

        try:
            resp = requests.post(f"{URL_BASE}/clientes", json={"nome": nome})
            if resp.status_code == 200:
                messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
                self.popup.destroy()
                self.carregar_clientes()
            else:
                messagebox.showerror("Erro", "Falha ao adicionar cliente.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão ao adicionar cliente.")

    def sair(self):
        self.atendente_logado = None
        self.frame_principal.destroy()
        self.criar_frame_login()

    def carregar_servicos(self):
        try:
            resp = requests.get(f"{URL_BASE}/servicos")
            if resp.status_code == 200:
                self.servicos = resp.json()
            else:
                messagebox.showerror("Erro", "Falha ao carregar serviços.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão ao carregar serviços.")

    def carregar_clientes(self):
        try:
            resp = requests.get(f"{URL_BASE}/clientes")
            if resp.status_code == 200:
                self.clientes = resp.json()
            else:
                messagebox.showerror("Erro", "Falha ao carregar clientes.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão ao carregar clientes.")

    def atualizar_sugestoes_clientes(self, event=None):
        texto = self.entry_cliente.get().lower()
        self.lista_sugestoes.delete(0, tk.END)
        if texto == "":
            self.lista_sugestoes.grid_remove()
            return
        sugestoes = [c for c in self.clientes if texto in c.lower()]
        if sugestoes:
            for s in sugestoes:
                self.lista_sugestoes.insert(tk.END, s)
            self.lista_sugestoes.grid()
        else:
            self.lista_sugestoes.grid_remove()

    def selecionar_sugestao_cliente(self, event):
        if not self.lista_sugestoes.curselection():
            return
        index = self.lista_sugestoes.curselection()[0]
        valor = self.lista_sugestoes.get(index)
        self.entry_cliente.delete(0, tk.END)
        self.entry_cliente.insert(0, valor)
        self.lista_sugestoes.grid_remove()

    def atualizar_sugestoes_servicos(self, event=None):
        texto = self.entry_servico.get().lower()
        self.lista_sugestoes_servicos.delete(0, tk.END)
        if texto == "":
            self.lista_sugestoes_servicos.grid_remove()
            return
        sugestoes = [s for s in self.servicos if texto in s.lower()]
        if sugestoes:
            for s in sugestoes:
                self.lista_sugestoes_servicos.insert(tk.END, s)
            self.lista_sugestoes_servicos.grid()
        else:
            self.lista_sugestoes_servicos.grid_remove()

    def selecionar_sugestao_servico(self, event):
        if not self.lista_sugestoes_servicos.curselection():
            return
        index = self.lista_sugestoes_servicos.curselection()[0]
        valor = self.lista_sugestoes_servicos.get(index)
        self.entry_servico.delete(0, tk.END)
        self.entry_servico.insert(0, valor)
        self.lista_sugestoes_servicos.grid_remove()

    def cadastrar_atendimento(self):
        cliente = self.entry_cliente.get().strip()
        servico = self.entry_servico.get().strip()
        nota_str = self.entry_nota.get().strip()

        if not cliente or not servico or not nota_str:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            nota = int(nota_str)
            if nota < 0 or nota > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número entre 0 e 10.")
            return

        dados = {
            "cliente": cliente,
            "atendente": self.atendente_logado,
            "servico": servico,
            "nota": nota
        }

        try:
            resp = requests.post(f"{URL_BASE}/atendimentos", json=dados)
            if resp.status_code == 200:
                messagebox.showinfo("Sucesso", "Atendimento registrado com sucesso!")
                self.entry_cliente.delete(0, tk.END)
                self.entry_servico.delete(0, tk.END)
                self.entry_nota.delete(0, tk.END)
                self.atualizar_lista_atendimentos()
            else:
                messagebox.showerror("Erro", "Erro ao registrar atendimento.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão ao registrar atendimento.")

    def atualizar_lista_atendimentos(self):
        try:
            resp = requests.get(f"{URL_BASE}/atendimentos")
            if resp.status_code == 200:
                atendimentos = resp.json()
                self.texto_atendimentos.configure(state="normal")
                self.texto_atendimentos.delete("1.0", tk.END)
                for at in atendimentos:
                    if at.get("atendente") == self.atendente_logado:
                        self.texto_atendimentos.insert(tk.END,
                            f"Cliente: {at.get('cliente')}\n"
                            f"Serviço: {at.get('servico')}\n"
                            f"Nota: {at.get('nota')}\n\n"
                        )
                self.texto_atendimentos.configure(state="disabled")
            else:
                messagebox.showerror("Erro", "Erro ao carregar atendimentos.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Erro de conexão ao carregar atendimentos.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
