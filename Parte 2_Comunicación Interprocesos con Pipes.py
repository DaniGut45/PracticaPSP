import os


def modificar_mensaje(leer, escribir):
    #Función para convertir el mensaje que escribir el padre en mayusculas
    mensaje = os.read(leer, 1024).decode('utf-8')  #El hijo lee el mensaje del padre
    mensaje_modificado = mensaje.upper()  #Convierte el mensaje a mayusculas
    os.write(escribir, mensaje_modificado.encode('utf-8'))  #Envia el mensaje modificado al padre

def contar_lineas_y_palabras(mensaje_padre, escribir):
    #Funcion que cuenta las lineas y palabras de un archivo (mensaje)
    #Contamos el número de líneas (aquí solo será 1, ya que no hay saltos de línea en el mensaje)
    num_lineas = mensaje_padre.count('\n') + 1  # Le sumo 1 porque si no hay saltos de línea, solamente habrá 1

    #Contamos el número de "palabras", usando split() para separar por espacios
    num_palabras = len(mensaje_padre.split())

    #Envia el resultado al padre
    os.write(escribir, f"Líneas: {num_lineas}, Palabras: {num_palabras}".encode('utf-8'))

def proceso_padre():
    #Creo de pipes
    tuberia= os.pipe()
    leer=tuberia[0]
    escribir=tuberia[1]

    tuberia2=os.pipe()
    leer2=tuberia2[0]
    escribir2=tuberia2[1]

    #Creo el proceso hijo
    pid = os.fork()

    if pid == 0:
        #Proceso del hijo
        modificar_mensaje(leer, escribir2)
        os._exit(0)
    else:
        #Proceso del padre
        mensaje = "Hola hijo, ¿cómo estás?\n¿Todo bien?"
        os.write(escribir, mensaje.encode('utf-8'))

        print(f"Mensaje original enviado al hijo: {mensaje}")

        #El padre recibe el mensaje, lo lee y sale por pantalla
        mensaje_modificado = os.read(leer2, 1024).decode('utf-8')
        print(f"Mensaje recibido del hijo en mayúsculas: {mensaje_modificado}")

        #Espera a que el hijo termine
        os.waitpid(pid, 0)

        # Crear el proceso hijo para contar las líneas y palabras del mensaje
        pid = os.fork()

        if pid == 0:
            # Proceso hijo para contar las líneas y palabras del mensaje
            contar_lineas_y_palabras(mensaje, escribir)
            os._exit(0)
        else:
            # Proceso padre
            resultado = os.read(leer, 1024).decode('utf-8')
            print(f"Resultado del mensaje: {resultado}")

            os.waitpid(pid, 0)


if __name__ == "__main__":
    proceso_padre()
