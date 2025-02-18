import os
import flet as ft

def baixar_playlist(playlist_url, pasta_destino, status_text):
    if not playlist_url:
        status_text.value = "Por favor, insira um link válido!"
        status_text.update()
        return
    
    if not pasta_destino:
        status_text.value = "Por favor, selecione uma pasta de destino!"
        status_text.update()
        return
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    comando = f'spotdl "{playlist_url}" --output "{pasta_destino}"'
    
    status_text.value = "Baixando... Aguarde!"
    status_text.update()
    
    os.system(comando)
    
    status_text.value = "Download concluído!"
    status_text.update()

def selecionar_pasta(dialog, pasta_destino_text):
    def on_result(e: ft.FilePickerResultEvent):
        if e.path:
            pasta_destino_text.value = e.path
            pasta_destino_text.update()
    dialog.on_result = on_result
    dialog.get_directory_path()

def main(page: ft.Page):
    page.title = "Spotify Playlist Downloader"
    page.window_width = 500
    page.window_height = 300
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    link_input = ft.TextField(label="Cole o link da playlist do Spotify", width=400)
    pasta_destino_text = ft.TextField(label="Pasta de destino", width=400, read_only=True)
    status_text = ft.Text("", color="blue")
    file_picker = ft.FilePicker()
    selecionar_pasta_button = ft.ElevatedButton("Selecionar Pasta", on_click=lambda _: selecionar_pasta(file_picker, pasta_destino_text))
    download_button = ft.ElevatedButton("Baixar Playlist", on_click=lambda _: baixar_playlist(link_input.value, pasta_destino_text.value, status_text))
    
    page.overlay.append(file_picker)
    page.add(
        pasta_destino_text,
        selecionar_pasta_button,
        link_input,
        download_button,
        status_text
    )

ft.app(target=main)
