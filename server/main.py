from flask import Flask, request, jsonify
import pickle
import os
import datetime
from datetime import datetime, timedelta
app = Flask(__name__)

# Arquivos para armazenar os dados
DB_FILES = {
    "clientes": "clientes.pkl",
    "atendentes": "atendentes.pkl",
    "servicos": "servicos.pkl",
    "atendimentos": "atendimentos.pkl"
}

# Funções auxiliares para carregar e salvar dados
def carregar_dados(arquivo):
    if os.path.exists(arquivo) and os.path.getsize(arquivo) > 0:
        with open(arquivo, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return []
    return []


def salvar_dados(arquivo, dados):
    with open(arquivo, "wb") as f:
        pickle.dump(dados, f)

# Inicializa os bancos de dados se não existirem
for key, file in DB_FILES.items():
    if not os.path.exists(file):
        salvar_dados(file, [])

# Rota: Listar todos os atendentes
@app.route("/atendentes", methods=["GET"])
def listar_atendentes():
    atendentes = carregar_dados(DB_FILES["atendentes"])
    return jsonify(atendentes)

# Rota: Listar todos os serviços
@app.route("/servicos", methods=["GET"])
def listar_servicos():
    servicos = carregar_dados(DB_FILES["servicos"])
    return jsonify(servicos)

# Rota: Excluir um serviço
@app.route("/servicos", methods=["DELETE"])
def excluir_servico():
    data = request.json
    nome_servico = data.get("nome")
    
    if not nome_servico:
        return jsonify({"erro": "Nome do serviço é necessário para exclusão!"}), 400
    
    servicos = carregar_dados(DB_FILES["servicos"])
    
    # Tenta remover o serviço
    if nome_servico in servicos:
        servicos.remove(nome_servico)
        salvar_dados(DB_FILES["servicos"], servicos)
        return jsonify({"mensagem": f"Serviço '{nome_servico}' excluído com sucesso!"})
    else:
        return jsonify({"erro": "Serviço não encontrado!"}), 404

# Rota: Cadastrar Cliente
@app.route("/clientes", methods=["POST"])
def cadastrar_cliente():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Nome do cliente é obrigatório!"}), 400

    clientes = carregar_dados(DB_FILES["clientes"])

    if nome in clientes:
        return jsonify({"erro": "Cliente já cadastrado!"}), 400

    clientes.append(nome)
    salvar_dados(DB_FILES["clientes"], clientes)
    return jsonify({"mensagem": "Cliente cadastrado com sucesso!"})


# Rota: Cadastrar Atendente
@app.route("/atendentes", methods=["POST"])
def cadastrar_atendente():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Nome do atendente é obrigatório!"}), 400

    atendentes = carregar_dados(DB_FILES["atendentes"])

    if nome in atendentes:
        return jsonify({"erro": "Atendente já cadastrado!"}), 400

    atendentes.append(nome)
    salvar_dados(DB_FILES["atendentes"], atendentes)
    return jsonify({"mensagem": "Atendente cadastrado com sucesso!"})

# Rota: Cadastrar Serviço
@app.route("/servicos", methods=["POST"])
def cadastrar_servico():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Nome do serviço é obrigatório!"}), 400

    servicos = carregar_dados(DB_FILES["servicos"])

    if nome in servicos:
        return jsonify({"erro": "Serviço já cadastrado!"}), 400

    servicos.append(nome)
    salvar_dados(DB_FILES["servicos"], servicos)
    return jsonify({"mensagem": "Serviço cadastrado com sucesso!"})


# Rota: Cadastrar Atendimento com Nota
@app.route("/atendimentos", methods=["POST"])
def cadastrar_atendimento():
    data = request.json
    clientes = carregar_dados(DB_FILES["clientes"])
    atendentes = carregar_dados(DB_FILES["atendentes"])
    servicos = carregar_dados(DB_FILES["servicos"])
    atendimentos = carregar_dados(DB_FILES["atendimentos"])

    if (data["cliente"] not in clientes or 
        data["atendente"] not in atendentes or 
        data["servico"] not in servicos or 
        not isinstance(data["nota"], int) or 
        not (0 <= data["nota"] <= 10)):
        return jsonify({"erro": "Dados inválidos!"}), 400

    atendimentos.append(data)
    salvar_dados(DB_FILES["atendimentos"], atendimentos)
    return jsonify({"mensagem": "Atendimento registrado com sucesso!"})

# Rota: Listar Serviços Realizados
@app.route("/atendimentos", methods=["GET"])
def listar_servicos_realizados():
    atendimentos = carregar_dados(DB_FILES["atendimentos"])
    return jsonify(atendimentos)


@app.route("/media_notas", methods=["GET"])
def media_notas():
    atendimentos = carregar_dados(DB_FILES["atendimentos"])
    
    # Verifica se há atendimentos registrados
    if not atendimentos:
        return jsonify({"erro": "Nenhuma nota registrada!"}), 404

    # Log de depuração: Imprimir os atendimentos carregados
    print("Atendimentos carregados:", atendimentos)

    # Criação de um dicionário para armazenar a soma das notas e a quantidade de atendimentos por atendente
    medias = {}
    
    for atendimento in atendimentos:
        atendente = atendimento.get("atendente")
        nota = atendimento.get("nota")
        
        # Verifica se o atendimento possui dados necessários
        if not atendente or nota is None:
            print(f"Atendimento ignorado (incompleto): {atendimento}")
            continue  # Ignora atendimentos incompletos ou com dados faltando
        
        if atendente not in medias:
            medias[atendente] = {"total_notas": 0, "quantidade_atendimentos": 0}
        
        medias[atendente]["total_notas"] += nota
        medias[atendente]["quantidade_atendimentos"] += 1

    # Log para checar as médias após o cálculo
    print("Médias calculadas:", medias)
    
    # Verifica se as médias foram calculadas para algum atendente
    if not medias:
        return jsonify({"erro": "Nenhum atendimento válido para calcular a média!"}), 404

    # Calculando a média das notas para cada atendente
    resultados = {}
    for atendente, dados in medias.items():
        media_atendente = dados["total_notas"] / dados["quantidade_atendimentos"]
        resultados[atendente] = media_atendente
    
    # Log de resultados
    print("Resultados finais:", resultados)

    return jsonify(resultados)

@app.route("/ordens", methods=["POST"])
def adicionar_ordem():
    data = request.json
    atendentes = carregar_dados(DB_FILES["atendentes"])

    if data["atendente"] not in atendentes:
        return jsonify({"erro": "Atendente não encontrado!"}), 404

    try:
        horas = int(data["horas"])
    except ValueError:
        return jsonify({"erro": "A quantidade de horas deve ser um número válido!"}), 400

    if horas <= 0:
        return jsonify({"erro": "A quantidade de horas deve ser maior que zero!"}), 400

    ordens = carregar_dados(DB_FILES["ordens"])

    # Calculando o horário de expiração
    hora_atual = datetime.now()
    hora_expiracao = hora_atual + timedelta(hours=horas)

    ordem = {
        "atendente": data["atendente"],
        "horas": horas,
        "hora_criacao": hora_atual.strftime("%Y-%m-%d %H:%M:%S"),
        "hora_expiracao": hora_expiracao.strftime("%Y-%m-%d %H:%M:%S"),
        "descricao": data["descricao"]
    }

    ordens.append(ordem)
    salvar_dados(DB_FILES["ordens"], ordens)
    return jsonify({"mensagem": "Ordem registrada com sucesso!"})

# Rota: Listar Ordens de um Atendente
@app.route("/ordens/<string:atendente>", methods=["GET"])
def listar_ordens_atendente(atendente):
    ordens = carregar_dados(DB_FILES["ordens"])
    ordens_atendente = [ordem for ordem in ordens if ordem["atendente"] == atendente]

    # Verificando se algum prazo expirou
    hora_atual = datetime.now()
    ordens_expiradas = []
    ordens_validas = []

    for ordem in ordens_atendente:
        hora_expiracao = datetime.strptime(ordem["hora_expiracao"], "%Y-%m-%d %H:%M:%S")
        if hora_atual > hora_expiracao:
            ordens_expiradas.append(ordem)
        else:
            ordens_validas.append(ordem)

    # Remover ordens expiradas
    ordens = [ordem for ordem in ordens if ordem not in ordens_expiradas]
    salvar_dados(DB_FILES["ordens"], ordens)

    return jsonify({
        "ordens_validas": ordens_validas,
        "ordens_expiradas": ordens_expiradas
    })

# Rota: Listar todos os clientes
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    clientes = carregar_dados(DB_FILES["clientes"])
    return jsonify(clientes)

# Rota: Excluir um cliente usando POST
@app.route("/clientes/excluir", methods=["POST"])
def excluir_cliente():
    data = request.json
    nome_cliente = data.get("nome")
    
    if not nome_cliente:
        return jsonify({"erro": "Nome do cliente é necessário para exclusão!"}), 400
    
    clientes = carregar_dados(DB_FILES["clientes"])
    
    # Tenta remover o cliente
    if nome_cliente in clientes:
        clientes.remove(nome_cliente)
        salvar_dados(DB_FILES["clientes"], clientes)
        return jsonify({"mensagem": f"Cliente '{nome_cliente}' excluído com sucesso!"})
    else:
        return jsonify({"erro": "Cliente não encontrado!"}), 404

# Rota: Excluir um atendente usando POST
@app.route("/atendentes/excluir", methods=["POST"])
def excluir_atendente():
    data = request.json
    nome_atendente = data.get("nome")
    
    if not nome_atendente:
        return jsonify({"erro": "Nome do atendente é necessário para exclusão!"}), 400
    
    atendentes = carregar_dados(DB_FILES["atendentes"])
    
    # Tenta remover o atendente
    if nome_atendente in atendentes:
        atendentes.remove(nome_atendente)
        salvar_dados(DB_FILES["atendentes"], atendentes)
        return jsonify({"mensagem": f"Atendente '{nome_atendente}' excluído com sucesso!"})
    else:
        return jsonify({"erro": "Atendente não encontrado!"}), 404
@app.route('/avaliar', methods=['POST'])
def avaliar():
    dados = request.get_json()
    cliente = dados.get("cliente")
    servico = dados.get("servico")
    nota = dados.get("nota")

    atendimentos = carregar_dados(DB_FILES["atendimentos"])

    for atendimento in atendimentos:
        if atendimento["cliente"] == cliente and atendimento["servico"] == servico:
            atendimento["nota"] = nota
            salvar_dados(DB_FILES["atendimentos"], atendimentos)
            return jsonify({"mensagem": "Nota registrada com sucesso!"}), 200

    return jsonify({"mensagem": "Atendimento não encontrado."}), 404
@app.route("/cliente/<nome>/atendimentos", methods=["GET"])
def atendimentos_por_cliente(nome):
    atendimentos = carregar_dados(DB_FILES["atendimentos"])
    resultados = [a for a in atendimentos if a["cliente"].lower() == nome.lower()]
    return jsonify(resultados), 200




if __name__ == "__main__":
    app.run(debug=True)
