from flaskwebgui import FlaskUI
from app import app

if __name__ == '__main__':
    ui = FlaskUI(app, port=9090, width=1200, height=800)
    ui.run()
