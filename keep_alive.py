from flask import Flask, send_from_directory
import os
from gevent.pywsgi import WSGIServer  # Importar gevent

app = Flask(__name__)

# Ruta para servir el favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.getcwd(), 'favicon.ico')

@app.route('/')
def home():
    return 'Bot is running!'

def run():
    # Usar gevent para ejecutar el servidor Flask
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()  # Iniciar el servidor con gevent

def keep_alive():
    # Iniciar el servidor Flask usando gevent
    run()
