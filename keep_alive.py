from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    app_status = "Bot Tài Xỉu đang hoạt động 24/7!"
    return app_status

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
