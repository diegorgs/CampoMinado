import tkinter as tk


class SplashScreen:
    def __init__(self, root):
        self.root = root

        self.root.overrideredirect(True)
        self.root.geometry("300x200")

        frame = tk.Frame(root, bg="#F0F0FD")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Campo Minado", font=("Arial", 16, "bold"),
                 bg="#F0F0FD").pack(pady=40)

        tk.Label(frame, text="Carregando...",
                 bg="#F0F0FD").pack()