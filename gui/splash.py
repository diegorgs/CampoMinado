class SplashScreen:
    def __init__(self, root):
        self.root = root

        self.root.overrideredirect(True)  # remove borda
        self.root.geometry("300x200")

        # Centralizar janela
        largura = 300
        altura = 200
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

        frame = tk.Frame(root, bg="#F0F0FD")
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Campo Minado", font=("Arial", 16, "bold"), bg="#F0F0FD")
        label.pack(pady=40)

        sub = tk.Label(frame, text="Carregando...", font=("Arial", 10), bg="#F0F0FD")
        sub.pack()

    def fechar(self):
        self.root.destroy()