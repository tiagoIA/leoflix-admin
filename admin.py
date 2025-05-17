from flask import Flask, request, render_template_string
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

LINKS_DIR = "static/links"
VIDEOS_JSON_PATH = "static/videos.json"

# Garante que a pasta de links existe
os.makedirs(LINKS_DIR, exist_ok=True)

# HTML simples para o painel admin
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LeoFlix Admin</title>
</head>
<body>
    <h1>Adicionar Vídeo</h1>
    <form method="post">
        <label>Nome da Pasta (Categoria):</label><br>
        <input type="text" name="folder" required><br><br>
        <label>Link do Vídeo (YouTube):</label><br>
        <input type="text" name="link" required><br><br>
        <button type="submit">Adicionar</button>
    </form>
    <hr>
    <h2>Pastas Existentes</h2>
    <ul>
    {% for pasta in pastas %}
        <li>{{ pasta }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

def gerar_videos_json():
    resultado = {}

    for arquivo in os.listdir(LINKS_DIR):
        if arquivo.endswith(".txt"):
            nome_pasta = os.path.splitext(arquivo)[0]
            caminho = os.path.join(LINKS_DIR, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                links = [linha.strip() for linha in f if linha.strip()]
                resultado[nome_pasta] = links

    with open(VIDEOS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        folder = request.form["folder"].strip()
        link = request.form["link"].strip()

        if not folder or not link:
            return "Erro: todos os campos são obrigatórios", 400

        # Salva o link no arquivo da pasta
        arquivo_path = os.path.join(LINKS_DIR, f"{folder}.txt")
        with open(arquivo_path, "a", encoding="utf-8") as f:
            f.write(link + "\n")

        gerar_videos_json()

    # Exibe as pastas existentes
    pastas = [os.path.splitext(p)[0] for p in os.listdir(LINKS_DIR) if p.endswith(".txt")]
    return render_template_string(HTML_TEMPLATE, pastas=pastas)

@app.route("/videos.json")
def videos():
    with open(VIDEOS_JSON_PATH, "r", encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
