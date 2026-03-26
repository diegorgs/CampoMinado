if __name__ == "__main__":
    root = tk.Tk()

    splash = SplashScreen(root)

    def iniciar_jogo():
        root.destroy()

        main = tk.Tk()
        main.title("Campo Minado")

        jogo = CampoMinadoGUI(main)
        main.mainloop()

    # tempo da splash (2000 ms = 2s)
    root.after(2000, iniciar_jogo)

    root.mainloop()