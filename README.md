
# API de Controle de Atendimentos com Flask

Esta aplicação é uma API feita em Flask para controle de clientes, atendentes, serviços, atendimentos e ordens de serviço. Os dados são armazenados em arquivos locais usando `pickle`.

---

## 📦 Tecnologias Utilizadas

- Python 3
- Flask
- Pickle (armazenamento local)
- JSON (para comunicação entre cliente e servidor)

---

## 🚀 Como Executar

1. Instale as dependências (Flask):
```bash
pip install flask
```

2. Salve o script como `app.py` e execute com:
```bash
python app.py
```

A aplicação será iniciada no endereço `http://127.0.0.1:5000`.

---

## 📁 Estrutura de Arquivos

- `clientes.pkl`
- `atendentes.pkl`
- `servicos.pkl`
- `atendimentos.pkl`
- `ordens.pkl` (criado dinamicamente se necessário)

---

## 🔗 Rotas Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET    | `/clientes`, `/atendentes`, `/servicos` | Lista itens |
| POST   | `/clientes`, `/atendentes`, `/servicos` | Cadastra novo |
| POST   | `/atendimentos` | Cadastra atendimento com nota |
| GET    | `/atendimentos` | Lista todos os atendimentos |
| GET    | `/media_notas` | Média de notas por atendente |
| POST   | `/ordens` | Cria ordem de atendimento com expiração |
| GET    | `/ordens/<atendente>` | Lista ordens válidas e expiradas |
| POST   | `/avaliar` | Atualiza nota de um atendimento |
| GET    | `/cliente/<nome>/atendimentos` | Lista atendimentos de um cliente |
| POST   | `/clientes/excluir`, `/atendentes/excluir` | Exclui cliente/atendente |
| DELETE | `/servicos` | Exclui serviço |

---

## 💾 Armazenamento Local

Todos os dados são salvos como listas Python em arquivos `.pkl`, utilizando o módulo `pickle`.

---

## ✅ Exemplo de JSON para Cadastro

### Cliente/Atendente/Serviço:
```json
{ "nome": "João" }
```

### Atendimento:
```json
{
  "cliente": "João",
  "atendente": "Maria",
  "servico": "Formatação",
  "nota": 9
}
```

### Ordem:
```json
{
  "atendente": "Carlos",
  "horas": 2,
  "descricao": "Troca de SSD"
}
```

---



## 🌐 Sobre o Protocolo HTTP

A comunicação entre o cliente (interface gráfica, navegador ou software) e o servidor Flask ocorre via **HTTP** (Hypertext Transfer Protocol). 

O protocolo HTTP define **métodos** que representam ações possíveis:

- **GET**: Buscar dados (ex: listar clientes, atendimentos).
- **POST**: Enviar dados para criação ou alteração.
- **DELETE**: Remover um recurso.
- **PUT/PATCH**: Atualizar dados (não usado neste projeto).

Cada rota da API responde a um ou mais desses métodos, interpretando os dados JSON enviados e retornando respostas também em formato JSON.

### Exemplo de Fluxo:

1. O cliente envia uma requisição `POST` com os dados de um novo cliente:
```json
{ "nome": "João" }
```

2. O servidor Flask recebe, processa e responde com:
```json
{ "mensagem": "Cliente cadastrado com sucesso!" }
```

3. Toda a comunicação ocorre usando a biblioteca `requests` no cliente Python.

---

## 🧰 Cliente Python com `customtkinter`

O cliente desktop que consome a API pode usar a biblioteca `customtkinter`, além de `requests` para enviar/receber dados da API Flask.

### Instalação das dependências do cliente:

```bash
pip install customtkinter pillow requests
```

- `customtkinter`: interface gráfica moderna baseada em tkinter.
- `pillow`: para manipulação de imagens.
- `requests`: para fazer requisições HTTP (GET, POST, DELETE).

---
