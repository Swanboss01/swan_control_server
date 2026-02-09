from flask import Flask, request, jsonify, render_template_string
from time import time

app = Flask(__name__)

current_command = "none"
last_ping = 0  # Dernier ping du client

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Contrôle SwanOS</title>
</head>
<body>
    <h1>Panneau de contrôle</h1>

    <p id="status">Statut : en attente...</p>

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

        async function updateStatus() {
            try {
                const res = await fetch('/status');
                const data = await res.json();

                if (data.running) {
                    document.getElementById("status").textContent = "🟢 Programme lancé";
                } else {
                    document.getElementById("status").textContent = "🔴 Programme non lancé";
                }
            } catch {
                document.getElementById("status").textContent = "🔴 Hors ligne";
            }
        }

        setInterval(updateStatus, 1000);
        updateStatus();
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

@app.route("/ping")
def ping():
    global last_ping
    last_ping = time()
    return jsonify({"status": "ok"})

@app.route("/status")
def status():
    global last_ping
    if time() - last_ping < 10:
        return jsonify({"running": True})
    else:
        return jsonify({"running": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
