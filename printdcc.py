import paramiko
import tkinter as tk
from tkinter import filedialog, messagebox, font


class SSHPrinter:
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
        # Envía el comando de impresión al servidor SSH
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
    server = "servidor_universidad.com"
    username = "usuario"
    password = "contraseña"
    filepath = "/ruta/al/archivo.ps"

    # Usar la clase con un bloque 'with' para asegurar cierre automático
    with SSHPrinter(server, username, password) as printer:
        printer.print_file(filepath)
'''

# -- TKINTER --

root = tk.Tk()
root.geometry("400x400")
root.iconbitmap("printdcc.ico")
root.title("printDCC")

def upload_file():
    # Abrir cuadro de diálogo para seleccionar archivo
    file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Todos los archivos", "*.*")])
    
    if file_path:
        file_text.config(state="normal")  # Habilitar escritura temporalmente
        file_text.delete("1.0", tk.END)  # Limpiar el contenido
        max_length = 52  # Máximo número de caracteres antes de agregar "..."
        display_text = file_path if len(file_path) <= max_length else file_path[:max_length - 3] + "..."
        file_text.insert(tk.END, display_text)
        file_text.config(state="disabled")  # Deshabilitar escritura para que sea de solo lectura

# Botón para cargar archivo
upload_button = tk.Button(root, text="Cargar Archivo", command=upload_file)
upload_button.pack(pady=20)

# Text para mostrar la ruta del archivo en modo de solo lectura
arial_font = font.Font(family="Arial", size=10)
file_text = tk.Text(root, width=50, height=2, wrap="word", bg=root["bg"], bd=0, font=arial_font)
file_text.pack(pady=10)
file_text.insert(tk.END, "No se ha seleccionado ningún archivo".center(65))  # Texto inicial centrado
file_text.config(state="disabled")  # Establecer en solo lectura


root.mainloop()