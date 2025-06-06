from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def buscar_cliente(codigo):
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    cliente = conn.execute(
        "SELECT nombre_cliente, valor FROM clientes WHERE codigo = ?",
        (codigo,)
    ).fetchone()
    conn.close()
    return cliente

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        codigo = request.form['codigo'].strip()
        if codigo:
            cliente = buscar_cliente(codigo)
            if cliente:
                resultado = f"Cliente: {cliente['nombre_cliente']} - Valor: ${cliente['valor']:.2f}"
            else:
                resultado = "Cliente no encontrado."
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)