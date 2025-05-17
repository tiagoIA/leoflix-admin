from flask import Flask, request, render_template_string, redirect
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

LINKS_DIR = "links"

# Garante que a pasta exista
os.makedirs(LINKS_DIR, exist_ok=True)

# Configura o Git para permitir commits no ambiente Render
subprocess.run(['git', 'config', '--global', 'user.name', 'LeoFlix Admin Bot'])
subprocess.run(['git', 'config', '--global', 'user.email', 'admin@leoflix.com'])

HTML_FORM = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>LeoFlix Admin</title>
</head>
<body>
    <h1>Adicionar Vídeo</h1>
    <form method="POST">
        <label for="pasta">Nome da Pasta (Categoria):</label><br>
        <input type="text" id="pasta" name="pasta" required><br><br>

        <label for="titulo">Título do Vídeo:</label><br>
        <input type="text" id="titulo" name="titulo" required><br><br>

        <label for="link">Link do Vídeo (YouTube):</label><br>
        <input type="text" id="link" name="link" required><br><br>

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

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        pasta = request.form["pasta"].strip().replace(" ", "_")
        titulo = request.form["titulo"].strip()
        link = request.form["link"].strip()

        if not pasta or not titulo or not link:
            error = "Todos os campos são obrigatórios!"
        else:
            file_path = os.path.join(LINKS_DIR, f"{pasta}.txt")
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{titulo} | {link}\n")

            # Commit automático no Git
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", f"Atualizado via admin web: {datetime.now()}"], check=True)
                subprocess.run(["git", "push"], check=True)
            except subprocess.CalledProcessError as e:
                return f"Erro ao fazer push: {e}"

            return redirect("/")

    pastas = []
    if os.path.exists(LINKS_DIR):
        pastas = [f.replace(".txt", "") for f in os.listdir(LINKS_DIR) if f.endswith(".txt")]

    return render_template_string(HTML_FORM, pastas=pastas, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=10000, host="0.0.0.0")