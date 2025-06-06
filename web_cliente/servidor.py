from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Conectar a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect("clientes.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/buscar', methods=['GET'])
def buscar_cliente():
    codigo = request.args.get('codigo', '').strip()

    if not codigo:
        return jsonify({"error": "Código vacío"}), 400

    conn = get_db_connection()
    cliente = conn.execute(
        "SELECT nombre_cliente, valor FROM clientes WHERE codigo = ?",
        (codigo,)
    ).fetchone()
    conn.close()

    if cliente:
        return jsonify(dict(cliente))
    else:
        return jsonify({"error": "Cliente no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)