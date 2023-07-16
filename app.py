from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    hash_value = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Leer el archivo y generar el hash
            content = file.read()
            hash_value = hashlib.sha256(content).hexdigest()
    return render_template('index.html', hash_value=hash_value)

@app.route('/check-integrity', methods=['POST'])
def check_integrity():
    file = request.files['file']
    hash_value = request.form['hash']
    if file:
        content = file.read()
        calculated_hash = hashlib.sha256(content).hexdigest()
        if calculated_hash == hash_value:
            return jsonify({'message': 'El archivo es íntegro.'})
        else:
            return jsonify({'message': 'El archivo ha sido modificado.'})
    return jsonify({'message': 'No se ha proporcionado un archivo.'})

if __name__ == '__main__':
    app.run(debug=True)