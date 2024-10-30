import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class PrintDCCApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("435x400")
        self.root.iconbitmap("printdcc.ico")
        self.root.title("printDCC")
        self.root.grid_columnconfigure(0, weight=1)
        
        self.show_login_screen()

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "1234":
            self.login_frame.grid_forget()  # Oculta la pantalla de login
            self.show_print_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_login_screen(self):
        self.login_frame = tk.LabelFrame(self.root, text="Conectarse a SSH Anakena", padx=10, pady=10)
        self.login_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, padx=(0,10), pady=(10,10))
        self.username_entry = tk.Entry(self.login_frame, width=40)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=(10,10))

        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, padx=(0,10), pady=(0,10))
        self.password_entry = tk.Entry(self.login_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0,10))

        show_password_var = tk.BooleanVar()
        show_password = tk.Checkbutton(self.login_frame, text="Ver Contraseña", variable=show_password_var, command=self.toggle_password)
        show_password.grid(row=2, column=1, sticky="w", pady=(0,20))

        login_button = tk.Button(self.login_frame, text="Iniciar Sesión", width=15, command=self.validate_login)
        login_button.grid(row=3, column=1, ipady=5)

    def toggle_password(self):
        # Alterna la visibilidad de la contraseña
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def show_print_screen(self):
        # Printer selection
        printer_frame = tk.LabelFrame(self.root, text="Printer", padx=10, pady=10)
        printer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(printer_frame, text="Lugar:").grid(row=0, column=0, sticky="w", pady=(0,10))
        printer_name = ttk.Combobox(printer_frame, values=["Toqui", "Salita"], width=35)
        printer_name.grid(row=0, column=1, sticky="ew", padx=5, pady=(0,10))
        printer_name.set("Toqui")

        tk.Label(printer_frame, text="Archivo:").grid(row=1, column=0, sticky="w", pady=(0,10))
        file_name = tk.Entry(printer_frame, width=40)
        file_name.grid(row=1, column=1, sticky="ew", padx=5, pady=(0,10))

        file_button = tk.Button(printer_frame, text="Seleccionar...", command=self.upload_file)
        file_button.grid(row=1, column=2, padx=5, pady=(0,10))

        tk.Label(printer_frame, text="Salida:").grid(row=2, column=0, sticky="w", pady=(0,10))
        output_name = tk.Entry(printer_frame, width=40)
        output_name.insert(0, "out.ps")
        output_name.grid(row=2, column=1, sticky="ew", padx=5, pady=(0,10))

        # Copies
        copies_frame = tk.LabelFrame(self.root, text="Copias", padx=10, pady=10)
        copies_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        tk.Label(copies_frame, text="Número de copias:").grid(row=0, column=0, sticky="w", pady=(0,10))
        copies_spinbox = tk.Spinbox(copies_frame, from_=1, to=99, width=5)
        copies_spinbox.grid(row=0, column=1, sticky="w", padx=10, pady=(0,10))

        double_sided = tk.Checkbutton(copies_frame, text="Doble cara")
        double_sided.grid(row=1, column=0, sticky="w")

        # Buttons
        buttons_frame = tk.Frame(self.root, padx=10, pady=10)
        buttons_frame.grid(row=2, column=0, padx=10, pady=5)

        logout_button = tk.Button(buttons_frame, text="Cerrar Sesion", width=15, command=self.show_login_screen)
        logout_button.grid(row=0, column=0, padx=(5,20), ipady=5)

        print_button = tk.Button(buttons_frame, text="Imprimir", width=15)
        print_button.grid(row=0, column=1, padx=(20,5), ipady=5)

    def upload_file(self):
        # Abrir cuadro de diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Todos los archivos", "*.*")])
        if file_path:
            file_name.delete(0, tk.END)  # Limpiar el Entry
            file_name.insert(0, file_path)  # Insertar la ruta del archivo seleccionado

if __name__ == "__main__":
    root = tk.Tk()
    app = PrintDCCApp(root)
    root.mainloop()