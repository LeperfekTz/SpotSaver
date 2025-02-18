import os

def baixar_playlist(playlist_url):
    # Obtém o caminho da pasta Downloads do usuário
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # Garante que a pasta exista
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

    # Monta o comando para baixar as músicas na pasta Downloads
    comando = f'spotdl "{playlist_url}" --output "{downloads_path}\\musicas_spotify"'
    
    os.system(comando)

if __name__ == "__main__":
    link = input("Cole o link da playlist do Spotify: ").strip()
    baixar_playlist(link)
