import tkinter as tk
from view import View
from sshcontroller import SSHController

if __name__ == "__main__":
    root = tk.Tk()
    server = "anakena.dcc.uchile.cl"
    controller = SSHController(server)
    view = View(root, controller)
    root.mainloop()