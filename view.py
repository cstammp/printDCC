import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class View:
    def __init__(self, root, controller):
        self.root = root
        self.sshcontroller = controller
        self.root.geometry("430x400")
        #self.root.resizable(False, False)
        self.root.iconbitmap("printdcc.ico")
        self.root.title("printDCC")
        self.root.grid_columnconfigure(0, weight=1)
        
        self.show_login_screen()
        self.printer_frame = None
        self.copies_frame = None
        self.buttons_frame = None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        status, message = self.sshcontroller.connect(username, password)
        if status:
            self.login_frame.grid_forget()
            self.show_print_screen()
        else:
            messagebox.showerror("Login Failed", message)

    def logout(self):
        status, message = self.sshcontroller.disconnect()
        if status:
            self.printer_frame.grid_forget()
            self.copies_frame.grid_forget()
            self.buttons_frame.grid_forget()
            self.show_login_screen()
        else:
            messagebox.showerror("Logout Failed", message)

    def print(self, printer_name,file_name,output_name,copies_spinbox,double_sided):

        self.sshcontroller.print_file(printer_name,file_name,output_name,copies_spinbox,double_sided)

        status, message = self.sshcontroller.print_file(printer_name,file_name,output_name,copies_spinbox,double_sided)
        if status:
            messagebox.showinfo("Impresión", message)
        else:
            messagebox.showerror("Print Failed", message)

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

        login_button = tk.Button(self.login_frame, text="Iniciar Sesión", width=15, command=self.login)
        login_button.grid(row=3, column=1, ipady=5)

    def toggle_password(self):
        # Hide and unhide password
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def show_print_screen(self):
        # Printer selection
        self.printer_frame = tk.LabelFrame(self.root, text="Printer", padx=10, pady=10)
        self.printer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(self.printer_frame, text="Lugar:").grid(row=0, column=0, sticky="w", pady=(0,10))
        printer_name = ttk.Combobox(self.printer_frame, values=["Toqui", "Salita"], width=35)
        printer_name.grid(row=0, column=1, sticky="ew", padx=5, pady=(0,10))
        printer_name.set("Toqui")

        tk.Label(self.printer_frame, text="Archivo:").grid(row=1, column=0, sticky="w", pady=(0,10))
        file_name = tk.Entry(self.printer_frame, width=40)
        file_name.grid(row=1, column=1, sticky="ew", padx=5, pady=(0,10))

        file_button = tk.Button(self.printer_frame, text="Seleccionar...", command=lambda: self.upload_file(file_name))
        file_button.grid(row=1, column=2, padx=5, pady=(0,10))

        tk.Label(self.printer_frame, text="Salida:").grid(row=2, column=0, sticky="w", pady=(0,10))
        output_name = tk.Entry(self.printer_frame, width=40)
        output_name.insert(0, "out.ps")
        output_name.grid(row=2, column=1, sticky="ew", padx=5, pady=(0,10))

        # Copies
        self.copies_frame = tk.LabelFrame(self.root, text="Copias", padx=10, pady=10)
        self.copies_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        tk.Label(self.copies_frame, text="Número de copias:").grid(row=0, column=0, sticky="w", pady=(0,10))
        copies_spinbox = tk.Spinbox(self.copies_frame, from_=1, to=99, width=5)
        copies_spinbox.grid(row=0, column=1, sticky="w", padx=10, pady=(0,10))

        double_sided_var = tk.BooleanVar()
        double_sided = tk.Checkbutton(self.copies_frame, text="Doble cara", variable=double_sided_var)
        double_sided.grid(row=1, column=0, sticky="w")

        # Buttons
        self.buttons_frame = tk.Frame(self.root, padx=10, pady=10)
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=5)

        logout_button = tk.Button(self.buttons_frame, text="Cerrar Sesion", width=15, command=self.logout)
        logout_button.grid(row=0, column=0, padx=(5,20), ipady=5)

        print_button = tk.Button(self.buttons_frame, text="Imprimir", width=15, command=lambda: self.print(printer_name.get(),file_name.get(),output_name.get(),copies_spinbox.get(),double_sided_var.get()))
        print_button.grid(row=0, column=1, padx=(20,5), ipady=5)

    def upload_file(self, file_name):
        # Abrir cuadro de diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Todos los archivos", "*.*")])
        if file_path:
            file_name.delete(0, tk.END)  # Limpiar el Entry
            file_name.insert(0, file_path)  # Insertar la ruta del archivo seleccionado