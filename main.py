from flask import Flask, render_template, request
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    # Obtenir la liste des conteneurs Docker actifs
    containers = client.containers.list()
    return render_template('index.html', containers=containers)

@app.route('/start_server', methods=['POST'])
def start_server():
    # Récupérer les informations du formulaire
    game = request.form.get('game')
    port = request.form.get('port')

    if game == 'minecraft':
        # Créer un nouveau conteneur pour le serveur Minecraft
        container = client.containers.run('itzg/minecraft-server', ports={'25565/tcp': int(port)}, detach=True)

    elif game == 'ark':
        # Créer un nouveau conteneur pour le serveur ARK: Survival Evolved
        container = client.containers.run('troydo42/ark-docker', ports={'27015/tcp': int(port)}, detach=True)

    elif game == 'rust':
        # Créer un nouveau conteneur pour le serveur Rust
        container = client.containers.run('didstopia/rust-server', ports={'28015/tcp': int(port), '28016/tcp': int(port)}, detach=True)

    else:
        return 'Jeu non pris en charge'

    return 'Serveur de jeu démarré avec succès !'

@app.route('/stop_server', methods=['POST'])
def stop_server():
    # Récupérer l'ID du conteneur à arrêter
    container_id = request.form.get('container_id')

    # Arrêter et supprimer le conteneur Docker
    container = client.containers.get(container_id)
    container.stop()
    container.remove()

    return 'Serveur de jeu arrêté avec succès !'


@app.route('/container_control', methods=['POST'])
def container_control():
    # Obtenir la liste des conteneurs Docker actifs
    containers = client.containers.list()
    return render_template('container_control.html', containers=containers)

    # Récupérer l'action du bouton
    action = request.form.get('action')

    container = client.containers.get(container_id)
    if action == 'start':
        container.start()
    elif action == 'stop':
        container.stop()

    return 'Action effectuée avec succès !'

if __name__ == '__main__':
    app.run(debug=True)
