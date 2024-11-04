import socket
import paramiko
import uuid

class SSHController:
    def __init__(self, server):
        self.server = server
        self.ssh_client = None

    def connect(self, username, password):
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

    def store_file(self, local_file_path, output_name):
            if not self.ssh_client:
                return False, "No hay conexión SSH activa"

            try:
                # Crear una sesión SFTP
                sftp = self.ssh_client.open_sftp()

                # Crear la carpeta 'printDCC' en el servidor si no existe
                self.ssh_client.exec_command("mkdir -p ~/printDCC")
                print("Directorio 'printDCC' creado en el servidor.")

                upload_output_name = str(uuid.uuid4()) + ".pdf"
                expanded_home_path = sftp.normalize('~')
                if expanded_home_path.endswith('/~'):
                    expanded_home_path = expanded_home_path[:-2]  # Remove the trailing /~ if present

                remote_file_path = f"{expanded_home_path}/printDCC/{upload_output_name}"
                print(expanded_home_path)
                print(remote_file_path)
                sftp.put(local_file_path, remote_file_path)
                print(f"Archivo subido exitosamente como '{upload_output_name}'")

                # Convertir el archivo a PostScript
                ps_file_path = f"~/printDCC/{output_name}"
                _, _, stderr = self.ssh_client.exec_command(f"pdf2ps {remote_file_path} {ps_file_path}")

                error = stderr.read().decode()
                if error:
                    print(f"Error al convertir a PS: {error}")
                    return False, f"Error al convertir a PS: {error}"

                # Eliminar el archivo pdf después de la conversión
                self.ssh_client.exec_command(f"rm {remote_file_path}")
                print(f"Archivo '{upload_output_name}' eliminado del servidor.")

                sftp.close()
                return True, f"Archivo convertido exitosamente a PS: {output_name}"
            except Exception as e:
                return False, f"Error al cargar el archivo: {e}"

    def print_file(self,printer_name,output_name,copies,double_sided):
        if not self.ssh_client:
            return False, "Invalid SSH connection"

        file_path = f"~/printDCC/{output_name}"

        command = ""
        if double_sided == True:
            command += f"duplex -l {file_path}|"
        command += "lpr"
        if printer_name == "Salita":
            command += " -P hp-335"
        if double_sided == False:
            command += f" {file_path}"

        print(command)
        print(type(double_sided))

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