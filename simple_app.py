from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Telegraf</title>
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a, #1a1a1a);
                color: #00e5ff;
                font-family: 'Courier New', monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 40px;
                border: 2px solid #00e5ff;
                border-radius: 20px;
                box-shadow: 0 0 50px rgba(0,229,255,0.3);
                background: rgba(0,0,0,0.8);
            }
            h1 {
                font-size: 48px;
                text-shadow: 0 0 20px #00e5ff;
                letter-spacing: 5px;
            }
            p {
                font-size: 18px;
                margin: 20px 0;
            }
            .glow {
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 0.6; text-shadow: 0 0 5px #00e5ff; }
                50% { opacity: 1; text-shadow: 0 0 20px #00e5ff; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="glow">⚡ TELEGRAF</h1>
            <p>Приложение успешно запущено!</p>
            <p>Стиль: Трон: Наследие</p>
            <p>Версия: 1.0</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=9090)
