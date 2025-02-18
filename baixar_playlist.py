import os
import flet as ft
import subprocess

def baixar_playlist(playlist_url, pasta_destino, log_container, page):
    if not playlist_url:
        log_container.controls.append(ft.Text("Por favor, insira um link válido!", color="red"))
        page.update()
        return
    
    if not pasta_destino:
        log_container.controls.append(ft.Text("Por favor, selecione uma pasta de destino!", color="red"))
        page.update()
        return
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Comando para baixar a playlist
    comando = ["spotdl", playlist_url, "--output", pasta_destino, "--log-level", "INFO"]
    
    log_container.controls.append(ft.Text("Baixando... Aguarde!", color="blue"))
    page.update()
    
    try:
        # Executa o comando
        process = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Buffer de linha por linha
            universal_newlines=True
        )
        
        # Lê a saída do comando em tempo real
        for line in process.stdout:
            log_container.controls.append(ft.Text(line.strip(), color="white"))
            page.update()  # Atualiza a interface
        
        process.wait()  # Aguarda o término do processo
        log_container.controls.append(ft.Text("Download concluído!", color="green"))
        page.update()
    except Exception as e:
        log_container.controls.append(ft.Text(f"Erro durante o download: {e}", color="red"))
        page.update()

def selecionar_pasta(dialog, pasta_destino_text, page):
    def on_result(e: ft.FilePickerResultEvent):
        if e.path:
            pasta_destino_text.value = e.path
            page.update()
    dialog.on_result = on_result
    dialog.get_directory_path()

def main(page: ft.Page):
    page.title = "SpotSaver App"
    page.window.width = 600
    page.window.height = 600
    page.window.resizable = False
    page.window.maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    link_input = ft.TextField(label="Cole o link da playlist do Spotify", width=400)
    pasta_destino_text = ft.TextField(label="Pasta de destino", width=400, read_only=True)
    
    # ListView para exibir o log
    log_container = ft.ListView(
        width=400,
        height=150,
        spacing=5,
        auto_scroll=True  # Rola automaticamente para o final
    )
    
    file_picker = ft.FilePicker()
    selecionar_pasta_button = ft.ElevatedButton("Selecionar Pasta", on_click=lambda _: selecionar_pasta(file_picker, pasta_destino_text, page))
    download_button = ft.ElevatedButton("Baixar Playlist", on_click=lambda _: baixar_playlist(link_input.value, pasta_destino_text.value, log_container, page))
    
    page.overlay.append(file_picker)
    page.add(
        pasta_destino_text,
        selecionar_pasta_button,
        link_input,
        download_button,
        log_container  # Usa o ListView para exibir o log
    )

ft.app(target=main)
