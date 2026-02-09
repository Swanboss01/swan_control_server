from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

current_command = "none"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Contrôle SwanOS</title>
</head>
<body>
    <h1>Panneau de contrôle</h1>

    <button onclick="send('hydra')">Hydra +1</button>
    <button onclick="send('popup')">Popup drôle</button>
    <button onclick="send('message')">Message aléatoire</button>
    <button onclick="send('color')">Changer couleur</button>

    <script>
        function send(cmd) {
            fetch('/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: cmd})
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/command", methods=["POST"])
def set_command():
    global current_command
    data = request.get_json()
    current_command = data.get("command", "none")
    return jsonify({"status": "ok"})

@app.route("/get")
def get_command():
    global current_command
    cmd = current_command
    current_command = "none"
    return jsonify({"command": cmd})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
