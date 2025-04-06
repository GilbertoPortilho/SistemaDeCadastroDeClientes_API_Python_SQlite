from flask import Flask, request, jsonify
from conexao import conectar
from banco import criar_tabela

app = Flask(__name__)
criar_tabela()

# Adicionar cliente
@app.route('/clientes', methods=['POST'])
def adicionar_cliente():
    dados = request.get_json()
    nome = dados.get('nome')
    idade = dados.get('idade')
    cpf = dados.get('cpf')
    cidade = dados.get('cidade')

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clientes (nome, idade, cpf, cidade)
            VALUES (?, ?, ?, ?)
        ''', (nome, idade, cpf, cidade))
        conn.commit()
        return jsonify({'mensagem': 'Cliente adicionado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    finally:
        conn.close()

# Listar todos os clientes
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()

    resultado = []
    for c in clientes:
        resultado.append({
            'id': c[0],
            'nome': c[1],
            'idade': c[2],
            'cpf': c[3],
            'cidade': c[4]
        })

    return jsonify(resultado), 200

# Buscar cliente por ID
@app.route('/clientes/<int:id>', methods=['GET'])
def buscar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        return jsonify({
            'id': cliente[0],
            'nome': cliente[1],
            'idade': cliente[2],
            'cpf': cliente[3],
            'cidade': cliente[4]
        }), 200
    else:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

# Atualizar cliente por ID
@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    dados = request.get_json()
    nome = dados.get('nome')
    idade = dados.get('idade')
    cpf = dados.get('cpf')
    cidade = dados.get('cidade')

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    if not cursor.fetchone():
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    try:
        cursor.execute('''
            UPDATE clientes SET nome = ?, idade = ?, cpf = ?, cidade = ?
            WHERE id = ?
        ''', (nome, idade, cpf, cidade, id))
        conn.commit()
        return jsonify({'mensagem': 'Cliente atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    finally:
        conn.close()

# Excluir cliente por ID
@app.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    if not cursor.fetchone():
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Cliente excluído com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
