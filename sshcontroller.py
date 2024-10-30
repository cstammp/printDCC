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

    def print_file(self,printer_name,file_name,output_name,copies,double_sided):
        if not self.ssh_client:
            return False, "Invalid SSH connection"

        command = f"pdf2ps {file_name} {output_name} && "
        if double_sided == True:
            command += "duplex -l out.ps|"
        command += "lpr"
        if printer_name == "Salita":
            command += " -P hp-335"
        if double_sided == False:
            command += f" {output_name}"

        print(command)

        for i in range(int(copies)):
            try:
                _, _, stderr = self.ssh_client.exec_command(command)
                error = stderr.read().decode()

                if error:
                    return False, f"Error en el servidor remoto: {error}"
                return True, "El documento ha sido enviado a la impresora"

            except paramiko.SSHException as ssh_error:
                return False, f"Error de SSH: {ssh_error}"

            except RuntimeError as runtime_error:
                return False, f"Error de ejecución: {runtime_error}"

            except Exception as e:
                return False, f"Error inesperado: {e}"

    def disconnect(self):
        # Cierra la conexión SSH
        if self.ssh_client and self.ssh_client.get_transport() and self.ssh_client.get_transport().is_active():
            self.ssh_client.close()
            self.ssh_client = None
            print("Conexión SSH cerrada.")
            return True, "Conexión SSH cerrada exitosamente"
        else:
            return False, "No hay una conexión SSH activa"