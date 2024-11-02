import tkinter as tk
from view import View
from sshcontroller import SSHController

# DPI Awareness for Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, ImportError):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    server = "anakena.dcc.uchile.cl"
    controller = SSHController(server)
    view = View(root, controller)
    root.mainloop()