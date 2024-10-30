import paramiko
import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk


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

# -- INTERFACE --

def show_print_screen():

    def upload_file():
    # Abrir cuadro de diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Todos los archivos", "*.*")])
        if file_path:
            file_name.delete(0, tk.END)  # Limpiar el Entry
            file_name.insert(0, file_path)  # Insertar la ruta del archivo seleccionado

    # Printer selection
    printer_frame = tk.LabelFrame(root, text="Printer", padx=10, pady=10)
    printer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(printer_frame, text="Lugar:").grid(row=0, column=0, sticky="w", pady=(0,10))
    printer_name = ttk.Combobox(printer_frame, values=["Toqui", "Salita"], width=35)
    printer_name.grid(row=0, column=1, sticky="ew", padx=5, pady=(0,10))
    printer_name.set("Toqui")

    tk.Label(printer_frame, text="Archivo:").grid(row=1, column=0, sticky="w", pady=(0,10))
    file_name = tk.Entry(printer_frame, width=40)
    file_name.grid(row=1, column=1, sticky="ew", padx=5, pady=(0,10))

    file_button = tk.Button(printer_frame, text="Seleccionar...",  command=upload_file)
    file_button.grid(row=1, column=2, padx=5, pady=(0,10))

    tk.Label(printer_frame, text="Salida:").grid(row=2, column=0, sticky="w", pady=(0,10))
    output_name = tk.Entry(printer_frame, width=40)
    output_name.insert(0, "out.ps")
    output_name.grid(row=2, column=1, sticky="ew", padx=5, pady=(0,10))

    # Copies
    copies_frame = tk.LabelFrame(root, text="Copias", padx=10, pady=10)
    copies_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    tk.Label(copies_frame, text="Número de copias:").grid(row=0, column=0, sticky="w", pady=(0,10))
    copies_spinbox = tk.Spinbox(copies_frame, from_=1, to=99, width=5)
    copies_spinbox.grid(row=0, column=1, sticky="w", padx=10, pady=(0,10))

    double_sided = tk.Checkbutton(copies_frame, text="Doble cara")
    double_sided.grid(row=1, column=0, sticky="w")

# Main
root = tk.Tk()
root.geometry("435x400")
root.iconbitmap("printdcc.ico")
root.title("printDCC")
root.grid_columnconfigure(0, weight=1)
#root.resizable(False, False)
show_print_screen()

root.mainloop()