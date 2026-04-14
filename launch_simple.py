import webview
import threading
import webbrowser
import time

def start_flask():
    from simple_app import app
    app.run(debug=False, port=9090, use_reloader=False)

if __name__ == '__main__':
    # Запускаем Flask
    thread = threading.Thread(target=start_flask, daemon=True)
    thread.start()
    
    # Ждём запуска сервера
    time.sleep(2)
    
    # Открываем окно
    webview.create_window('Telegraf', 'http://localhost:9090', width=1200, height=800)
    webview.start()
