from flask import Flask, render_template, request
import webview
import atexit
import os
from lib.emulator import emulador, crear_tarea, ver_tareas, salir_emulador


app = Flask(__name__, template_folder='templates')
window = webview.create_window('Gestor de tareas (wc3270)', app, width=1920, height=1080)

#Funcion para cuando se cierra la aplicación forzosa
def on_application_exit():
    salir_emulador() 
    if os.path.exists("pantalla.txt"):
        os.remove("pantalla.txt")

atexit.register(on_application_exit)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_rellenado = request.form['usuario']
    contrasena_rellenado = request.form['contrasena'] 
    terminal = emulador(usuario_rellenado,contrasena_rellenado)
    print("Valor de terminal en app.py:", terminal) 
    match terminal:
        case 0:
            data = ver_tareas()
            return render_template('home.html', data=data)
        case 1:
            return render_template('login_error.html')
        case 2:
            return render_template('usuario_ocupado.html')

@app.route('/crearGeneral', methods=['POST'])
def crearGeneral():
    tipo = "General"
    fecha = request.form['fechaGeneral']
    desc = request.form['descripcionGeneral']
    nombre = ""

    print(f'TIPO: {tipo}, FECHA: {fecha}, DESCRIPCION: {desc}, NOMBRE: {nombre}')
    crear_tarea(tipo, fecha, desc, nombre)
    data = ver_tareas()
    return render_template('home.html', data=data)

@app.route('/creaEspecifica', methods=['POST'])
def creaEspecifica():
    tipo = "Especifica"
    fecha = request.form['fechaEspecifica']
    desc = request.form['descripcionEspecifica']
    nombre = request.form['nombreEspecifica']

    print(f'TIPO: {tipo}, FECHA: {fecha}, DESCRIPCION: {desc}, NOMBRE: {nombre}')
    crear_tarea(tipo, fecha, desc, nombre)
    data = ver_tareas()
    return render_template('home.html', data=data)

@app.route('/exit', methods=['POST'])
def exit():
    salir_emulador()
    if os.path.exists("pantalla.txt"):
        os.remove("pantalla.txt")
    return render_template('login.html')

if __name__ == '__main__':
    webview.start()