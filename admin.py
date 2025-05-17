from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
import subprocess

app = Flask(__name__)

# Garante que a pasta 'links' existe
if not os.path.exists('links'):
    os.makedirs('links')

# Garante que a pasta 'static' existe
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    pastas = os.listdir('links')
    return render_template('index.html', pastas=pastas)

@app.route('/', methods=['POST'])
def adicionar():
    pasta = request.form['pasta']
    titulo = request.form['titulo']
    link = request.form['link']

    if not pasta or not link:
        return redirect(url_for('index'))

    if not os.path.exists('links'):
        os.makedirs('links')

    caminho = os.path.join('links', f'{pasta}.txt')
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

    gerar_json()

    try:
        subprocess.run(['git', 'config', '--global', 'user.email', 'seuemail@exemplo.com'])
        subprocess.run(['git', 'config', '--global', 'user.name', 'tiagoIA'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Atualização automática de links'])
        subprocess.run(['git', 'push'])
    except Exception as e:
        print("Erro ao fazer push:", e)

    return redirect(url_for('index'))

def gerar_json():
    videos = {}
    for arquivo in os.listdir('links'):
        if arquivo.endswith('.txt'):
            nome = arquivo.replace('.txt', '')
            with open(os.path.join('links', arquivo), 'r', encoding='utf-8') as f:
                links = [linha.strip() for linha in f.readlines() if linha.strip()]
                videos[nome] = links

    with open('static/videos.json', 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

# Rota para servir arquivos da pasta static (como videos.json)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)
