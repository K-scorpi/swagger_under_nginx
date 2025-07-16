import subprocess

def get_status():
    result = subprocess.run(['systemctl', 'is-active', 'nginx'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()

def start_service():
    subprocess.run(['systemctl', 'start', 'nginx'], check=True)

def stop_service():
    subprocess.run(['systemctl', 'stop', 'nginx'], check=True)

def restart_service():
    subprocess.run(['systemctl', 'restart', 'nginx'], check=True)
