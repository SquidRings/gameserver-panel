from flask import Flask, render_template, request
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    # Get a list of active Docker containers
    containers = client.containers.list()

    container_info = []
    for container in containers:
        container_id = container.id
        container_ip = container.attrs['NetworkSettings']['IPAddress']
        container_ports = container.attrs['NetworkSettings']['Ports']
        ports = []
        for port in container_ports:
            if container_ports[port] is not None:
                container_port = port.split('/')[0]
                host_port = container_ports[port][0]['HostPort']
                ports.append({'container_port': container_port, 'host_port': host_port})

        container_info.append({'id': container_id, 'ip_address': container_ip, 'ports': ports})

    return render_template('index.html', container_info=container_info)

@app.route('/start_server', methods=['POST'])
def start_server():
    # Retrieve form information
    game = request.form.get('game')
    port = request.form.get('port')
    ram = request.form.get('ram')
    image_size = request.form.get('image_size')

    if game == 'minecraft':
        # Create a new container for the Minecraft server
        container = client.containers.run('itzg/minecraft-server', ports={'25565/tcp': int(port)}, environment={'EULA': 'TRUE', 'IMAGE_SIZE': image_size}, detach=True, tty=True, mem_limit=ram)

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

    return 'Game server deleted successfully !'

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
