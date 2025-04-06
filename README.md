
# 🧾 Sistema de Cadastro de Clientes (API + Interface Python)

Este projeto é um sistema completo de cadastro de clientes, desenvolvido com **Python**, **Flask** e **CustomTkinter**. Permite o registro, edição, exclusão, listagem e exportação de clientes para um arquivo CSV, tudo integrado a uma API REST.

---

## 🚀 Tecnologias utilizadas

- **Python 3.11+**
- **Flask** — para criação da API REST
- **SQLite** — banco de dados local
- **CustomTkinter** — interface moderna em modo escuro
- **Requests** — consumo da API na interface

---

## 📦 Funcionalidades

✅ Cadastro de novos clientes  
✅ Edição de clientes existentes  
✅ Exclusão de clientes  
✅ Listagem automática de todos os clientes  
✅ Exportação dos dados para planilha CSV  
✅ Campo de CPF com formatação automática (`000.000.000-00`)  
✅ Interface 100% em modo escuro e responsiva

---

## 🗂 Estrutura do Projeto

```
📁 projeto/
├── db.py              # Criação da tabela e conexão SQLite
├── conexao.py         # Conecta ao banco de dados
├── app.py             # API Flask com rotas REST
├── interface.py       # Interface feita com CustomTkinter
├── clientes.csv       # Planilha gerada automaticamente
├── README.md
```

---

## 🔧 Como executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-clientes.git
cd sistema-clientes
```

2. Instale as dependências:

```bash
pip install flask customtkinter requests
```

3. Rode a API:

```bash
python app.py
```

4. Em outro terminal, rode a interface:

```bash
python interface.py
```

---

## 🧪 Teste com o Postman

Você pode usar o [Postman](https://www.postman.com/) para testar os endpoints:

- `GET /clientes` → listar todos
- `POST /clientes` → cadastrar
- `GET /clientes/<id>` → buscar específico
- `PUT /clientes/<id>` → atualizar
- `DELETE /clientes/<id>` → excluir

---

## 📷 Interface em funcionamento

![interface](https://via.placeholder.com/800x400?text=Coloque+um+print+aqui+da+sua+interface)

---

## 💡 Possíveis melhorias futuras

- Validação de CPF real
- Exportar para Excel `.xlsx`
- Barra de pesquisa
- Filtros por cidade ou idade
- Deploy da API com render/vercel

---

## 🧑‍💻 Autor

**Gilberto Portilho**  
