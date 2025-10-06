from lib.py3270 import Emulator
import time

retardo_emulador=0.5


#función para comprobar el mensaje del emulador despues del login
def verificar_inicio():
    line=terminal.string_get(7,2,24)
    if line=="Userid is not authorized":
        return 1
    line=terminal.string_get(7,2,18)
    if line=="Password incorrect":
        return 1
    line=terminal.string_get(1,1,16)
    if line.rstrip()=="Userid is in use":
        return 2
    return 0

#Función para capturar la pantalla del emulador en un archivo de texto
def pantalla(filename="pantalla.txt"):
    time.sleep(retardo_emulador)
    screen_content = ''
    for row in range(1, 43 + 1):
        line = terminal.string_get(row, 1, 79)
        screen_content += line + '\n'
    archivo = open(filename, "w")
    archivo.write(screen_content)
    archivo.close()

#Función para leer una línea específica de un archivo de texto
def leer_linea(line, file="pantalla.txt"):
    with open(file, "r") as archivo:
        lineas = archivo.readlines()  

        if 0 <= line < len(lineas):
            linea_deseada = lineas[line]
            return linea_deseada.strip()  
        else:
            return 0

#Función para obtener las tareas generales de la pantalla del emulador linea a linea        
def obtener_generales(file="pantalla.txt"):
    resultado = []
    for num_line in range(0, 43 + 1):
        line=leer_linea(num_line,file)
        if line!=0:
            if line.find("TOTAL TASK")!=-1:
                return resultado
            else:
                partes = line.split(" ")
                if partes[0]=="TASK":
                    temp = {"fecha":partes[3],"descripcion":partes[5].strip('"')}
                    resultado.append(temp)
    print("Obtenemos estas generales: ", resultado)
    return resultado

#Función para obtener las tareas específicas de la pantalla del emulador linea a linea
def obtener_especificas(file="pantalla.txt"):
    resultado = []
    for num_line in range(0, 43 + 1):
        line=leer_linea(num_line,file)
        if line!=0:
            if line.find("TOTAL TASK")!=-1:
                return resultado
            else:
                partes = line.split(" ")
                if partes[0]=="TASK":
                    temp = {"fecha":partes[3],"nombre":partes[4].strip('"'),"descripcion":partes[5].strip('"')}
                    resultado.append(temp)
    print("Obtenemos estas específicas: ", resultado)
    return resultado


def emulador(usuario, contrasena):
    global terminal, active_window
    print ("Iniciando emulador..." )

    terminal = Emulator(visible=True)
    terminal.connect('155.210.152.51:3270')
    print ("Conectado a host" )
    time.sleep(retardo_emulador)

    print("Llegamos a la pantalla inicial")
    terminal.send_enter()

    time.sleep(retardo_emulador)
    print("Llegamos al login")

    # Usuario
    for attempt in range(5):
        try:
            terminal.wait_for_field()
            terminal.send_string(usuario)
            terminal.send_enter()
            print("Enviado usuario " + usuario)
            break
        except Exception as ex:
            print(f"Intento {attempt+1} de enviar usuario fallido: {ex}")
            time.sleep(1)
    else:
        print("No se pudo enviar el usuario")

    # Contraseña
    for attempt in range(5):
        try:
            terminal.wait_for_field()
            terminal.send_string(contrasena)
            terminal.send_enter()
            time.sleep(retardo_emulador)
            print("Enviada contraseña")
            break
        except Exception as ex:
            print(f"Intento {attempt+1} de enviar contraseña fallido: {ex}")
            time.sleep(1)
    else:
        print("No se pudo enviar la contraseña")

    inicio = verificar_inicio()

    match inicio:
        case 0:
            print("Login correcto")
            time.sleep(retardo_emulador)
            terminal.wait_for_field()
            terminal.send_enter()
            # Pantalla del terminal del emulador
            time.sleep(retardo_emulador)
            terminal.wait_for_field()
            terminal.send_string('tasks.c')
            terminal.send_enter()
            return 0
        case 1:     # Usuario o contraseña incorrectos
            terminal.terminate()
            return 1
        case 2:     # Usuario ya en uso
            terminal.terminate()
            return 2

# Función para crear tareas
def crear_tarea(tipo:str, fecha:str, desc:str, nombre:str):
    desc = '"' + desc.replace(" ", " ") + '"'
    nombre = '"' + nombre.replace(" ", " ") + '"'
    print("Pasamos a crear una tarea.")
    terminal.send_string("1")
    terminal.send_enter()
    terminal.delete_field()

    print ("Creando tarea con tipo:", tipo, "fecha:", fecha, "desc:", desc, "nombre:", nombre)
    if tipo=="General":
        terminal.send_string("1")
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string(fecha)
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string(desc)
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string("a")
        terminal.send_enter()

    elif tipo=="Especifica":
        terminal.send_string("2")
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string(fecha)
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string(nombre)
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_string(desc)
        terminal.send_enter()
        terminal.delete_field()
        terminal.send_enter() 
        terminal.send_string("a")
        terminal.send_enter()
        terminal.send_enter()
    
    print("Volvemos menu inicial.")
    terminal.send_string("0")
    terminal.send_enter()
    terminal.delete_field()

# Función para ver tareas
def ver_tareas():
    print("Pasamos a mostrar las tareas.")
    resultado=[]
    terminal.send_string("2")
    print("Enviando 2")
    terminal.send_enter()
    terminal.delete_field()
    terminal.send_clear()
    terminal.send_string("1")
    terminal.send_enter()
    terminal.delete_field()
    pantalla()
    general = obtener_generales()
    terminal.send_clear()
    terminal.send_string("a")
    terminal.send_enter()
    terminal.send_string("2")
    terminal.send_enter()
    terminal.delete_field()
    pantalla()
    terminal.send_string("a")
    terminal.send_enter()
    specific = obtener_especificas()
    terminal.send_string("0")
    terminal.send_enter()
    terminal.delete_field()
    terminal.send_string("0")
    terminal.send_enter()
    resultado =  specific + general
    return resultado

# función para salir del emulador
def salir_emulador():
    global terminal
    terminal.send_string("3")
    terminal.send_enter()
    terminal.delete_field()
    terminal.send_string("off")
    terminal.send_enter()
    terminal.delete_field()
    time.sleep(0.5)
    terminal.terminate()