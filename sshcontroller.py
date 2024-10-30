import paramiko
import tkinter as tk
from tkinter import messagebox
import socket

class SSHController:
    def __init__(self, server):
        self.server = server
        self.username = None
        self.password = None
        self.ssh_client = None

    def connect(self, username, password):
        self.username = username
        self.password = password
        # Establece una conexión SSH mediante paramiko
        if not self.ssh_client:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Intenta establecer la conexión SSH con un tiempo de espera de 10 segundos
            self.ssh_client.connect(self.server, username=username, password=password, timeout=10)
            print(f"Conectado a {self.server}")
            return True, "Conexión exitosa"
        except paramiko.AuthenticationException:
            return False, "Credenciales SSH inválidas"
        except paramiko.SSHException as e:
            return False, f"Error de SSH: {str(e)}"
        except socket.timeout:
            return False, "Tiempo de conexión agotado"
        except Exception as e:
            return False, f"Error al conectar: {str(e)}"

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