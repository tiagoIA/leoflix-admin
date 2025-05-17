from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

LINKS_DIR = 'static/links'
VIDEOS_JSON_PATH = os.path.join('static', 'videos.json')  # agora está DENTRO de /static

# Garante que a pasta exista
os.makedirs(LINKS_DIR, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    pastas = sorted([f.replace('.txt', '') for f in os.listdir(LINKS_DIR) if f.endswith('.txt')])
    html = '''
    <h1>Adicionar Vídeo</h1>
    <form method="post">
        Nome da Pasta (Categoria):<br>
        <input type="text" name="pasta"><br><br>
        Link do Vídeo (YouTube):<br>
        <input type="text" name="link"><br><br>
        <input type="submit" value="Adicionar">
    </form>
    <hr>
    <h2>Pastas Existentes</h2>
    <ul>
    '''
    for pasta in pastas:
        html += f'<li>{pasta}</li>'
    html += '</ul>'
    return html

@app.route('/', methods=['POST'])
def adicionar():
    pasta = request.form['pasta'].strip()
    link = request.form['link'].strip()

    if not pasta or not link:
        return redirect(url_for('index'))

    caminho = os.path.join(LINKS_DIR, f'{pasta}.txt')
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

    gerar_json()
    return redirect(url_for('index'))

@app.route('/videos.json', methods=['GET'])
def servir_json():
    if not os.path.exists(VIDEOS_JSON_PATH):
        gerar_json()
    with open(VIDEOS_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

def gerar_json():
    videos = {}
    for arquivo in os.listdir(LINKS_DIR):
        if arquivo.endswith('.txt'):
            categoria = arquivo.replace('.txt', '')
            with open(os.path.join(LINKS_DIR, arquivo), 'r', encoding='utf-8') as f:
                links = [linha.strip() for linha in f.readlines() if linha.strip()]
                videos[categoria] = links
    with open(VIDEOS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
