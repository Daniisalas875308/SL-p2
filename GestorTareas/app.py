from flask import Flask, render_template, request
from lib.emulator import emulador
import os
import webview
import atexit

app = Flask(__name__, template_folder='templates')
window = webview.create_window('Gestor de tareas (wc3270)', app, width=1920, height=1080)


@app.route('/')
def index():
    return render_template('index_inicio.html')

@app.route('/ini', methods=['POST'])
def ini():
    last_user = request.form['usuario']
    last_passwd = request.form['contrasena'] 
    e = emulador(last_user,last_passwd)
    if e==0:
        return render_template('tareas.html')  
    elif e==1:
        return render_template('index_inicio_error.html')
    elif e==2:
        return render_template('index_inicio_ocupado.html')


if __name__ == '__main__':
    webview.start()