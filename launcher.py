import webview
import threading
import sys
import os

# Добавляем путь к текущей папке
sys.path.insert(0, os.path.dirname(__file__))

def start_app():
    from mac_app import app
    app.run(debug=False, port=9090, use_reloader=False)

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    thread = threading.Thread(target=start_app, daemon=True)
    thread.start()
    
    # Открываем окно webview
    webview.create_window('Telegraf', 'http://localhost:9090', width=1200, height=800)
    webview.start()
