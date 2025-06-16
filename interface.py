import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from main import baixar_video

def criar_interface():
    def iniciar_download():
        url = entrada_url.get()
        pasta = entrada_pasta.get()
        so_audio = var_audio.get()

        if not url.strip() or not pasta.strip():
            log("❌ Preencha todos os campos.")
            return

        botao.config(state="disabled")
        log("⏳ Iniciando download...")
        progresso_bar["value"] = 0

        threading.Thread(
            target=baixar_video,
            args=(url, pasta, so_audio, log, atualizar_progresso, fim_do_download),
            daemon=True
        ).start()

    def escolher_pasta():
        path = filedialog.askdirectory()
        if path:
            entrada_pasta.delete(0, tk.END)
            entrada_pasta.insert(0, path)

    def log(mensagem):
        log_area.configure(state="normal")
        log_area.insert(tk.END, mensagem + "\n")
        log_area.configure(state="disabled")
        log_area.see(tk.END)

    def atualizar_progresso(valor):
        progresso_bar["value"] = valor
        root.update_idletasks()

    def fim_do_download():
        botao.config(state="normal")
        messagebox.showinfo("Download finalizado", "✅ O vídeo foi baixado com sucesso!")

    # === CORES MIDNIGHT DARK ===
    preto = "#0D0D0D"
    escuro = "#151515"
    texto = "#F5F5F5"
    roxo = "#9C7FFF"
    azul = "#00CFFF"

    # === JANELA ===
    root = tk.Tk()
    root.title("YouTube Downloader - Midnight 🌙")
    root.geometry("1000x500")
    root.configure(bg=preto)
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar", troughcolor=escuro, background=azul, thickness=20, bordercolor=preto)

    # === FRAME ESQUERDO ===
    frame_esquerdo = tk.Frame(root, bg=escuro, width=499, height=500)
    frame_esquerdo.pack(side="left", fill="both")
    frame_esquerdo.pack_propagate(False)

    # === LINHA DIVISÓRIA ===
    separator = tk.Frame(root, bg=roxo, width=1)
    separator.pack(side="left", fill="y")

    # === FRAME DIREITO ===
    frame_direito = tk.Frame(root, bg=escuro, width=500, height=500)
    frame_direito.pack(side="left", fill="both")
    frame_direito.pack_propagate(False)

    # === CONTEÚDO ESQUERDO ===
    tk.Label(frame_esquerdo, text="INSIRA O LINK:", bg=escuro, fg=texto).pack(pady=(20, 2))
    entrada_url = tk.Entry(frame_esquerdo, width=60, bg=preto, fg=texto, insertbackground=texto, relief="flat")
    entrada_url.pack(pady=(0, 8))

    tk.Label(frame_esquerdo, text="PASTA DE DESTINO:", bg=escuro, fg=texto).pack()
    frame_pasta = tk.Frame(frame_esquerdo, bg=escuro)
    frame_pasta.pack(pady=(0, 10))
    entrada_pasta = tk.Entry(frame_pasta, width=47, bg=preto, fg=texto, insertbackground=texto, relief="flat")
    entrada_pasta.pack(side="left", padx=(0, 5))
    tk.Button(frame_pasta, text="📂", command=escolher_pasta, bg=roxo, fg=preto, relief="flat").pack(side="left")

    var_audio = tk.BooleanVar()
    chk_audio = tk.Checkbutton(frame_esquerdo, text="BAIXAR SOMENTE O ÁUDIO", variable=var_audio,
                               bg=escuro, fg=texto, selectcolor=preto, activebackground=escuro)
    chk_audio.pack()

    botao = tk.Button(frame_esquerdo, text="DOWNLOAD", command=iniciar_download,
                      bg=roxo, fg=preto, relief="flat", width=20)
    botao.pack(pady=10)

    tk.Label(frame_esquerdo, text="PROGRESSO:", bg=escuro, fg=texto).pack(pady=(10, 0))
    progresso_bar = ttk.Progressbar(frame_esquerdo, orient="horizontal", length=400, mode="determinate")
    progresso_bar.pack(pady=(0, 20))

    tk.Label(frame_esquerdo, text="Desenvolvido por Midnight 🌙", bg=escuro, fg=roxo,
             font=("Arial", 8)).pack(side="bottom", pady=10)

    # === CONTEÚDO DIREITO ===
    tk.Label(frame_direito, text="LOG TERMINAL", bg=escuro, fg=roxo).pack(pady=(20, 5))
    log_area = tk.Text(frame_direito, height=22, width=58, bg=preto, fg=texto, insertbackground=texto,
                       relief="flat", borderwidth=5)
    log_area.pack(pady=(0, 10))
    log_area.configure(state="disabled")

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
