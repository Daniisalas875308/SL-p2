from lib.py3270 import Emulator
import time

delayScreen=0.5


def emulador(mylogin, mypass):
    global e, active_window
    print ("Iniciando emulador..." )
    # Main
    host = "155.210.152.51"
    port = "3270"

    e = Emulator(visible=True)
    e.connect(host + ':' + port)
    print ("Conectado a host" )
    time.sleep(delayScreen)

    for row in range(1, 25):  # Filas 1 a 24
        try:
            line = e.string_get(row, 1, 80)
            print(row, line)
        except Exception as ex:
            print(f"Error leyendo fila {row}: {ex}")

    # Pantalla inicio
    time.sleep(delayScreen)
    print("Llegamos a la pantalla inicial")
    e.send_enter()
    time.sleep(1)  # espera a que el host procese
    print("Intentando desbloquear pantalla inicial...")

    #for attempt in range(5):
     #   try:
      #      e.wait_for_field()  
       #     print("Pantalla inicial desbloqueada")
        #    break
        #except Exception as ex:
         #   print(f"Intento {attempt+1} fallido: {ex}")
          #  time.sleep(0.5)
    #else:
     #   print("No se pudo desbloquear la pantalla inicial")
      #  return 2  # indicamos fallo

    # Pantalla Login
    time.sleep(delayScreen)
    print("Llegamos al login")

    # Usuario
    for attempt in range(5):
        try:
            #e.wait_for_field()
            e.send_string(mylogin)
            e.send_enter()
            print("Enviado usuario " + mylogin)
            break
        except Exception as ex:
            print(f"Intento {attempt+1} de enviar usuario fallido: {ex}")
            time.sleep(1)
    else:
        print("No se pudo enviar el usuario")

    # Contraseña
    for attempt in range(5):
        try:
            e.wait_for_field()
            time.sleep(0.5)
            e.send_string(mypass)
            e.send_enter()
            print("Enviada contraseña")
            break
        except Exception as ex:
            print(f"Intento {attempt+1} de enviar contraseña fallido: {ex}")
            time.sleep(1)
    else:
        print("No se pudo enviar la contraseña")

