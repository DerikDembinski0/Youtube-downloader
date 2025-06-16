# main.py
import os
from yt_dlp import YoutubeDL

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def baixar_video(url, pasta_destino, so_audio, log_callback, progresso_callback, fim_callback):
    if not url.strip() or not pasta_destino.strip():
        log_callback("❌ Link ou pasta inválidos.")
        return

    os.makedirs(pasta_destino, exist_ok=True)

    formato = "bestaudio/best" if so_audio else "bestvideo+bestaudio/best"
    saida = "mp3" if so_audio else "mp4"

    def progresso_hook(d):
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '').strip().replace('%', '')
                progresso = float(percent_str)
                progresso_callback(progresso)
            except:
                progresso_callback(0)
            log_callback(f"📦 Baixando: {d['_percent_str'].strip()}")
        elif d['status'] == 'finished':
            log_callback("✅ Download concluído.")
            progresso_callback(100)
            fim_callback()

    opts = {
        'format': formato,
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
        'merge_output_format': saida,
        'user_agent': UA,
        'quiet': True,
        'progress_hooks': [progresso_hook],
        'no_color': True,

    }

    if so_audio:
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        log_callback(f"❌ Erro: {e}")
        progresso_callback(0)
