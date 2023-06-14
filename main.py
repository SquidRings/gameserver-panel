from flask import Flask, render_template, request
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    # Get a list of active Docker containers
    containers = client.containers.list()
    return render_template('index.html', containers=containers)

@app.route('/start_server', methods=['POST'])
def start_server():
    # Retrieve form information
    game = request.form.get('game')
    port = request.form.get('port')

    if game == 'minecraft':
        # Create a new container for the Minecraft server
        container = client.containers.run('itzg/minecraft-server', ports={'25565/tcp': int(port)}, detach=True)

    elif game == 'ark':
        # Create a new container for the ARK: Survival Evolved server
        container = client.containers.run('troydo42/ark-docker', ports={'27015/tcp': int(port)}, detach=True)

    elif game == 'rust':
        # Create a new container for the Rust server
        container = client.containers.run('didstopia/rust-server', ports={'28015/tcp': int(port), '28016/tcp': int(port)}, detach=True)

    else:
        return 'Unsupported game'

    return 'Game server successfully started !'

@app.route('/stop_server', methods=['POST'])
def stop_server():
    # Retrieve the ID of the container to stop
    container_id = request.form.get('container_id')

    # Stop and delete the Docker container
    container = client.containers.get(container_id)
    container.stop()
    container.remove()

    return 'Game server shut down successfully !'

# add a button to control all container with terminal ftp control and always show all containers run or not running
@app.route('/container_control', methods=['POST'])
def container_control():
    # Get a list of active Docker containers
    containers = client.containers.list()
    return render_template('container_control.html', containers=containers)

    # Retrieve button action
    action = request.form.get('action')

    container = client.containers.get(container_id)
    if action == 'start':
        container.start()
    elif action == 'stop':
        container.stop()

    return 'Action successfully completed !'

if __name__ == '__main__':
    app.run(debug=True)
