import webview
import threading
import time
import sys
import os

# Добавляем путь к текущей папке
sys.path.insert(0, os.path.dirname(__file__))

def start_flask():
    """Запускаем Flask-приложение"""
    from app import app
    app.run(debug=False, host='127.0.0.1', port=9090, use_reloader=False)

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Ждём, пока сервер запустится
    time.sleep(3)
    
    # Создаём окно приложения
    webview.create_window(
        title='Telegraf',
        url='http://localhost:9090',
        width=1280,
        height=800,
        min_size=(800, 600),
        resizable=True
    )
    webview.start()
