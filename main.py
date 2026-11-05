import flet as ft
import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse

def is_proxy_alive(ip, port):
    try:
        with socket.create_connection((ip, int(port)), timeout=1.2):
            return True
    except:
        return False

def main(page: ft.Page):
    page.title = "ZastoParser"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    status_text = ft.Text(value="Нажмите кнопку для поиска ключа", size=16)
    
    def on_connect_click(e):
        btn.disabled = True
        status_text.value = "Загрузка списка и проверка ключей..."
        page.update()

        try:
            response = requests.get("https://shadowsocks.gov.kg", timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a['href'] for a in soup.find_all('a', href=True) 
                     if a['href'].startswith(('tg://proxy', 'https://t.me'))]
            
            working_url = None
            for link in links:
                parsed = urllib.parse.urlparse(link)
                params = urllib.parse.parse_qs(parsed.query)
                server = params.get('server', [None])
                port = params.get('port', [None])

                if server and port and is_proxy_alive(server, port):
                    working_url = link
                    break

            if working_url:
                status_text.value = "Рабочий ключ найден! Открываю в ZaStoGram..."
                page.update()
                page.launch_url(working_url)
            else:
                status_text.value = "Все ключи на сайте сейчас недоступны ❌"
        except:
            status_text.value = "Ошибка сети. Проверьте интернет."
        
        btn.disabled = False
        page.update()

    btn = ft.ElevatedButton(text="НАЙТИ И ПРОВЕРИТЬ КЛЮЧ", on_click=on_connect_click)
    page.add(status_text, ft.Container(height=20), btn)

ft.app(target=main)
