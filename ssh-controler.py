import paramiko

class SSHController:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.ssh_client = None

    def connect(self):
        #Establece una conexión SSH
        if not self.ssh_client:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.server, username=self.username, password=self.password)
            print(f"Conectado a {self.server}")

    def print_file(self, filepath):
        if not self.ssh_client:
            raise ConnectionError("Invalid SSH connection")
        
        command = f"lpr {filepath}"
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        print("Salida:", stdout.read().decode())
        print("Errores:", stderr.read().decode())

    def disconnect(self):
        #Cierra la conexión SSH
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            print("Conexión SSH cerrada.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

'''
# Ejemplo de uso
if __name__ == "__main__":
    server = "anakena.dcc.uchile.cl"
    username = "usuario"
    password = "contraseña"
    filepath = "/ruta/al/archivo.ps"

    with SSHPrinter(server, username, password) as printer:
        printer.print_file(filepath)
'''