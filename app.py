from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def buscar_cliente(cedula_ruc):
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    cliente = conn.execute(
        "SELECT nombre_cliente, valor FROM clientes WHERE cedula_ruc = ?",
        (cedula_ruc,)
    ).fetchone()
    conn.close()
    return cliente

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        cedula_ruc = request.form['cedula_ruc'].strip()
        if cedula_ruc:
            cliente = buscar_cliente(cedula_ruc)
            if cliente:
                resultado = f"Cliente: {cliente['nombre_cliente']} - Valor: ${cliente['valor']:.2f}"
            else:
                resultado = "Cliente no encontrado."
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
