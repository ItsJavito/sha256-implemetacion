import sha256 as sha
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    hash_value = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Leer el archivo y generar el hash
            content = file.read()
            hash_value = sha.generate_hash(content).hex()
    return render_template('index.html', hash_value=hash_value)

@app.route('/check-integrity', methods=['POST'])
def check_integrity():
    file = request.files['file']
    hash_value = request.form['hash']
    if file:
        content = file.read()
        calculated_hash =  sha.generate_hash(content).hex()
        if calculated_hash == hash_value:
            return jsonify({'message': 'El archivo es íntegro.'})
        else:
            return jsonify({'message': 'El archivo ha sido modificado.'})
    return jsonify({'message': 'No se ha proporcionado un archivo.'})
@app.route('/generate-collision', methods=['POST'])
def generate_collision():
    start_time = time.time()
    mensaje = find_collision(start_time)
    return jsonify({'message': mensaje})

def find_collision(start_time):
    file = request.files['file']
    if file:
        content = file.read()
        hash1 = sha.generate_hash(content).hex()
    else:
        return jsonify({'message': 'no se ha proporcionado un archivo.'})
    message2 = b'Alianza Lima'
    hash2 =  sha.generate_hash(message2).hex()
    while hash1 != hash2:
        message2 = bytes([((x + 1) % 256) for x in message2]) # Cambiar el mensaje ligeramente
        hash2 =  sha.generate_hash(message2).hex()
        #hasta un minuto buscando una colisión
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            return "Colisión no encontrada."
    return "Colisión encontrada."

if __name__ == '__main__':
    app.run(debug=True)