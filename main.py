import customtkinter as ctk
import os
from PIL import Image
from tkinter import messagebox
import requests

URL_BASE = "http://127.0.0.1:5000"

main = ctk.CTk()
main.title("SISTEMA")
main.geometry("600x600")
main.resizable(False, False)
main.iconbitmap(os.path.abspath("vicon.ico"))

# Função para exibir mensagens no monitor (textbox)
def exibir_no_monitor(mensagem):
    monitor.insert("end", mensagem + "\n")
    monitor.yview_moveto(1)

# Função para cadastrar cliente
def cadastrar_cliente(nome_cliente_entry):
    nome_cliente = nome_cliente_entry.get()
    if nome_cliente:
        dados = {"nome": nome_cliente}
        try:
            response = requests.post(f"{URL_BASE}/clientes", json=dados)
            exibir_no_monitor(response.json().get("mensagem", "Erro ao cadastrar cliente"))
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
    else:
        exibir_no_monitor("Por favor, insira o nome do cliente.")

# Função para criar uma janela Toplevel de cadastro de cliente
def criar_janela_cliente():
    janela_cliente = ctk.CTkToplevel(main)
    janela_cliente.title("Cadastrar Cliente")
    janela_cliente.geometry("300x150")
    
    nome_cliente_entry = ctk.CTkEntry(janela_cliente, placeholder_text="Nome do Cliente")
    nome_cliente_entry.pack(pady=10)
    
    cadastrar_cliente_button = ctk.CTkButton(janela_cliente, text="Cadastrar Cliente", command=lambda: cadastrar_cliente(nome_cliente_entry))
    cadastrar_cliente_button.pack(pady=10)

# Função para cadastrar atendente
def cadastrar_atendente(nome_atendente_entry):
    nome_atendente = nome_atendente_entry.get()
    if nome_atendente:
        dados = {"nome": nome_atendente}
        try:
            response = requests.post(f"{URL_BASE}/atendentes", json=dados)
            exibir_no_monitor(response.json().get("mensagem", "Erro ao cadastrar atendente"))
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
    else:
        exibir_no_monitor("Por favor, insira o nome do atendente.")

# Função para criar uma janela Toplevel de cadastro de atendente
def criar_janela_atendente():
    janela_atendente = ctk.CTkToplevel(main)
    janela_atendente.title("Cadastrar Atendente")
    janela_atendente.geometry("300x150")
    
    nome_atendente_entry = ctk.CTkEntry(janela_atendente, placeholder_text="Nome do Atendente")
    nome_atendente_entry.pack(pady=10)
    
    cadastrar_atendente_button = ctk.CTkButton(janela_atendente, text="Cadastrar Atendente", command=lambda: cadastrar_atendente(nome_atendente_entry))
    cadastrar_atendente_button.pack(pady=10)

# Função para cadastrar serviço
def cadastrar_servico(nome_servico_entry):
    nome_servico = nome_servico_entry.get()
    if nome_servico:
        dados = {"nome": nome_servico}
        try:
            response = requests.post(f"{URL_BASE}/servicos", json=dados)
            exibir_no_monitor(response.json().get("mensagem", "Erro ao cadastrar serviço"))
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
    else:
        exibir_no_monitor("Por favor, insira o nome do serviço.")

# Função para criar uma janela Toplevel de cadastro de serviço
def criar_janela_servico():
    janela_servico = ctk.CTkToplevel(main)
    janela_servico.title("Cadastrar Serviço")
    janela_servico.geometry("300x150")
    
    nome_servico_entry = ctk.CTkEntry(janela_servico, placeholder_text="Nome do Serviço")
    nome_servico_entry.pack(pady=10)
    
    cadastrar_servico_button = ctk.CTkButton(janela_servico, text="Cadastrar Serviço", command=lambda: cadastrar_servico(nome_servico_entry))
    cadastrar_servico_button.pack(pady=10)

# Função para registrar atendimento
def registrar_atendimento(cliente_entry, atendente_entry, servico_entry, nota_entry):
    cliente = cliente_entry.get()
    atendente = atendente_entry.get()
    servico = servico_entry.get()
    nota = nota_entry.get()
    
    if cliente and atendente and servico and nota:
        dados = {"cliente": cliente, "atendente": atendente, "servico": servico, "nota": int(nota)}
        try:
            response = requests.post(f"{URL_BASE}/atendimentos", json=dados)
            exibir_no_monitor(response.json().get("mensagem", "Erro ao registrar atendimento"))
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
    else:
        exibir_no_monitor("Por favor, preencha todos os campos.")

# Função para criar uma janela Toplevel de registro de atendimento
def criar_janela_atendimento():
    janela_atendimento = ctk.CTkToplevel(main)
    janela_atendimento.title("Registrar Atendimento")
    janela_atendimento.geometry("300x250")
    
    cliente_entry = ctk.CTkEntry(janela_atendimento, placeholder_text="Nome do Cliente")
    cliente_entry.pack(pady=5)
    
    atendente_entry = ctk.CTkEntry(janela_atendimento, placeholder_text="Nome do Atendente")
    atendente_entry.pack(pady=5)
    
    servico_entry = ctk.CTkEntry(janela_atendimento, placeholder_text="Nome do Serviço")
    servico_entry.pack(pady=5)
    
    nota_entry = ctk.CTkEntry(janela_atendimento, placeholder_text="Nota (0-10)")
    nota_entry.pack(pady=5)
    
    registrar_atendimento_button = ctk.CTkButton(janela_atendimento, text="Registrar Atendimento", command=lambda: registrar_atendimento(cliente_entry, atendente_entry, servico_entry, nota_entry))
    registrar_atendimento_button.pack(pady=10)

# Função para calcular a média das notas
def calcular_media_notas():
    try:
        response = requests.get(f"{URL_BASE}/media_notas")
        medias = response.json()  # A resposta é um dicionário com as médias dos atendentes
        if medias:
            # Exibe as médias de todos os atendentes
            for atendente, media in medias.items():
                exibir_no_monitor(f"Média de {atendente}: {media}")
        else:
            exibir_no_monitor("Não foi possível calcular a média.")
    except requests.exceptions.RequestException as e:
        exibir_no_monitor(str(e))


# Função para listar todos os atendentes
def listar_atendentes():
    try:
        response = requests.get(f"{URL_BASE}/atendentes")
        atendentes = response.json()
        exibir_no_monitor("Atendentes:\n" + "\n".join(atendentes))
    except requests.exceptions.RequestException as e:
        exibir_no_monitor(str(e))

# Função para listar todos os serviços
def listar_servicos():
    try:
        response = requests.get(f"{URL_BASE}/servicos")
        servicos = response.json()
        exibir_no_monitor("Serviços:\n" + "\n".join(servicos))
    except requests.exceptions.RequestException as e:
        exibir_no_monitor(str(e))

# Função para excluir serviço
def excluir_servico(nome_servico_entry):
    nome_servico = nome_servico_entry.get()
    if nome_servico:
        dados = {"nome": nome_servico}
        try:
            response = requests.delete(f"{URL_BASE}/servicos", json=dados)
            exibir_no_monitor(response.json().get("mensagem", "Erro ao excluir serviço"))
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
    else:
        exibir_no_monitor("Por favor, insira o nome do serviço.")

# Função para criar uma janela Toplevel para excluir serviço
def criar_janela_excluir_servico():
    janela_excluir_servico = ctk.CTkToplevel(main)
    janela_excluir_servico.title("Excluir Serviço")
    janela_excluir_servico.geometry("300x150")
    
    nome_servico_entry = ctk.CTkEntry(janela_excluir_servico, placeholder_text="Nome do Serviço")
    nome_servico_entry.pack(pady=10)
    
    excluir_servico_button = ctk.CTkButton(janela_excluir_servico, text="Excluir Serviço", command=lambda: excluir_servico(nome_servico_entry))
    excluir_servico_button.pack(pady=10)

def listar_clientes():
    try:
        response = requests.get(f"{URL_BASE}/clientes")
        if response.status_code == 200:
            clientes = response.json()
            exibir_no_monitor(f"Clientes: {clientes}")
            # Aqui você pode exibir os clientes na interface ou fazer o que for necessário
        else:
            exibir_no_monitor("Falha ao listar clientes!")
            messagebox.showerror("Erro", "Falha ao listar clientes!")
    except requests.exceptions.RequestException as e:
        exibir_no_monitor(str(e))
        messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")

# Função para excluir um cliente usando POST
def excluir_cliente():
    def confirmar_exclusao():
        nome_cliente = entry_cliente.get()

        if not nome_cliente:
            messagebox.showerror("Erro", "Digite o nome do cliente para excluir.")
            return

        try:
            response = requests.post(f"{URL_BASE}/clientes/excluir", json={"nome": nome_cliente})
            if response.status_code == 200:
                exibir_no_monitor(f"Cliente '{nome_cliente}' excluído com sucesso!")
                messagebox.showinfo("Sucesso", f"Cliente '{nome_cliente}' excluído com sucesso!")
                top_level.destroy()  # Fecha a janela TopLevel após sucesso
            else:
                exibir_no_monitor(f"Falha ao excluir cliente '{nome_cliente}'!")
                messagebox.showerror("Erro", f"Falha ao excluir cliente '{nome_cliente}'!")
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")

    top_level = ctk.CTkToplevel()  # Cria um novo TopLevel
    top_level.title("Excluir Cliente")
    
    label_cliente = ctk.CTkLabel(top_level, text="Digite o nome do cliente para excluir:")
    label_cliente.pack(pady=10)
    
    entry_cliente = ctk.CTkEntry(top_level)
    entry_cliente.pack(pady=10)
    
    botao_excluir = ctk.CTkButton(top_level, text="Excluir Cliente", command=confirmar_exclusao)
    botao_excluir.pack(pady=10)

# Função para excluir atendente com TopLevel
def excluir_atendente():
    def confirmar_exclusao():
        nome_atendente = entry_atendente.get()

        if not nome_atendente:
            messagebox.showerror("Erro", "Digite o nome do atendente para excluir.")
            return

        try:
            response = requests.post(f"{URL_BASE}/atendentes/excluir", json={"nome": nome_atendente})
            if response.status_code == 200:
                exibir_no_monitor(f"Atendente '{nome_atendente}' excluído com sucesso!")
                messagebox.showinfo("Sucesso", f"Atendente '{nome_atendente}' excluído com sucesso!")
                top_level.destroy()  # Fecha a janela TopLevel após sucesso
            else:
                exibir_no_monitor(f"Falha ao excluir atendente '{nome_atendente}'!")
                messagebox.showerror("Erro", f"Falha ao excluir atendente '{nome_atendente}'!")
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")

    top_level = ctk.CTkToplevel()  # Cria um novo TopLevel
    top_level.title("Excluir Atendente")
    
    label_atendente = ctk.CTkLabel(top_level, text="Digite o nome do atendente para excluir:")
    label_atendente.pack(pady=10)
    
    entry_atendente = ctk.CTkEntry(top_level)
    entry_atendente.pack(pady=10)
    
    botao_excluir = ctk.CTkButton(top_level, text="Excluir Atendente", command=confirmar_exclusao)
    botao_excluir.pack(pady=10)
def Gerenciador_e_atendimentos():

    # Função para exibir informações no monitor (por exemplo, na tela ou no terminal)
    def exibir_no_monitor(mensagem):
        print(mensagem)  # Pode ser adaptado para exibir na interface gráfica

    # Função para cadastrar um atendimento
    def cadastrar_atendimento():
        cliente = entry_cliente.get()
        atendente = entry_atendente.get()
        servico = entry_servico.get()
        try:
            nota = int(entry_nota.get())
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser um número válido entre 0 e 10.")
            return

        # Verificar se a nota está entre 0 e 10
        if nota < 0 or nota > 10:
            messagebox.showerror("Erro", "A nota deve ser entre 0 e 10.")
            return

        # Enviar os dados do atendimento para o servidor
        atendimento_data = {
            "cliente": cliente,
            "atendente": atendente,
            "servico": servico,
            "nota": nota
        }

        try:
            response = requests.post(f"{URL_BASE}/atendimentos", json=atendimento_data)
            if response.status_code == 200:
                exibir_no_monitor("Atendimento registrado com sucesso!")
                messagebox.showinfo("Sucesso", "Atendimento registrado com sucesso!")
                atualizar_lista_atendimentos()  # Atualiza a lista de atendimentos
            else:
                exibir_no_monitor("Falha ao registrar atendimento!")
                messagebox.showerror("Erro", "Falha ao registrar atendimento!")
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")

    # Função para buscar atendimentos e atualizar a caixa de texto
    def atualizar_lista_atendimentos():
        try:
            response = requests.get(f"{URL_BASE}/atendimentos")
            if response.status_code == 200:
                atendimentos = response.json()
                lista_atendimentos.delete(1.0, ctk.END)  # Limpar a caixa de texto antes de atualizar
                for atendimento in atendimentos:
                    cliente = atendimento.get("cliente", "Desconhecido")
                    atendente = atendimento.get("atendente", "Desconhecido")
                    servico = atendimento.get("servico", "Desconhecido")
                    nota = atendimento.get("nota", "Não atribuída")
                    lista_atendimentos.insert(ctk.END, f"Cliente: {cliente}\nAtendente: {atendente}\nServiço: {servico}\nNota: {nota}\n\n")
                exibir_no_monitor("Atendimentos carregados com sucesso!")
            else:
                exibir_no_monitor("Falha ao buscar atendimentos!")
                messagebox.showerror("Erro", "Falha ao buscar atendimentos!")
        except requests.exceptions.RequestException as e:
            exibir_no_monitor(str(e))
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")

    # Criar a interface gráfica (CTK)
    app = ctk.CTkToplevel()

    app.title("Cadastro de Atendimento")
    app.geometry("600x600")

    # Campos de entrada para o atendimento
    label_cliente = ctk.CTkLabel(app, text="Cliente:")
    label_cliente.pack(pady=5)
    entry_cliente = ctk.CTkEntry(app)
    entry_cliente.pack(pady=5)

    label_atendente = ctk.CTkLabel(app, text="Atendente:")
    label_atendente.pack(pady=5)
    entry_atendente = ctk.CTkEntry(app)
    entry_atendente.pack(pady=5)

    label_servico = ctk.CTkLabel(app, text="Serviço:")
    label_servico.pack(pady=5)
    entry_servico = ctk.CTkEntry(app)
    entry_servico.pack(pady=5)

    label_nota = ctk.CTkLabel(app, text="Nota (0-10):")
    label_nota.pack(pady=5)
    entry_nota = ctk.CTkEntry(app)
    entry_nota.pack(pady=5)

    # Botões para interagir
    botao_cadastrar = ctk.CTkButton(app, text="Cadastrar Atendimento", command=cadastrar_atendimento)
    botao_cadastrar.pack(pady=10)

    # Caixa de texto para exibir os atendimentos
    lista_atendimentos = ctk.CTkTextbox(app, width=400, height=200, state='normal')
    lista_atendimentos.pack(pady=10)

    # Atualiza a lista de atendimentos ao abrir a aplicação
    atualizar_lista_atendimentos()

    # Rodar a aplicação
    app.mainloop()
        
# Botões rápidos ao lado esquerdo
listar_atendentes_button = ctk.CTkButton(main, text="Listar Atendentes", command=listar_atendentes)
listar_atendentes_button.place(x=0, y=250)

listar_servicos_button = ctk.CTkButton(main, text="Listar Serviços", command=listar_servicos)
listar_servicos_button.place(x=0, y=300)

excluir_servico_button = ctk.CTkButton(main, text="Excluir Serviço", command=criar_janela_excluir_servico)
excluir_servico_button.place(x=0, y=350)


excluir_cliente_button = ctk.CTkButton(main, text="Excluir Cliente", command=excluir_cliente)
excluir_cliente_button.place(x=0, y=400)

excluir_atendente_button = ctk.CTkButton(main, text="Excluir Atendente", command=excluir_atendente)
excluir_atendente_button.place(x=0, y=450)

excluir_atendente_button = ctk.CTkButton(main, text="Listar clientes", command=listar_clientes)
excluir_atendente_button.place(x=0, y=500)

Atendimentos_gerenciador_button = ctk.CTkButton(main, text="Cadastrar atendimento", command=Gerenciador_e_atendimentos)
Atendimentos_gerenciador_button.place(x=0, y=550)
# Botões principais
add_cliente_img = ctk.CTkImage(light_image=Image.open(os.path.abspath("humano.png")), size=(30, 30))
add_cliente = ctk.CTkButton(main, text="+ cliente", image=add_cliente_img, command=criar_janela_cliente)
add_cliente.place(x=0, y=10)

add_atendente_img = ctk.CTkImage(light_image=Image.open(os.path.abspath("atendente.png")), size=(30, 30))
add_atendente = ctk.CTkButton(main, text="+ atendente", image=add_atendente_img, command=criar_janela_atendente)
add_atendente.place(x=0, y=60)

add_servico_img = ctk.CTkImage(light_image=Image.open(os.path.abspath("ordem.png")), size=(60, 60))
add_servico = ctk.CTkButton(main, text="+ serviço", image=add_servico_img, command=criar_janela_servico)
add_servico.place(x=0, y=110)

media_img = ctk.CTkImage(light_image=Image.open(os.path.abspath("media.png")), size=(30, 30))
media = ctk.CTkButton(main, text="media dos\natendentes", image=media_img, command=calcular_media_notas)
media.place(x=0, y=190)



monitor = ctk.CTkTextbox(main, width=300, height=390)
monitor.place(x=280, y=10)

main.mainloop()
