import os


def modificar_mensaje(pipe_lectura, pipe_escritura):
    """Convierte el mensaje a mayúsculas y lo envía al padre a través del pipe."""
    mensaje = os.read(pipe_lectura, 1024).decode('utf-8')  # El hijo lee el mensaje del padre
    mensaje_modificado = mensaje.upper()  # Convertir el mensaje a mayúsculas
    os.write(pipe_escritura, mensaje_modificado.encode('utf-8'))  # Enviar el mensaje modificado al padre
    os.close(pipe_lectura)
    os.close(pipe_escritura)


def contar_lineas_y_palabras(mensaje_padre, pipe_escritura):
    """Cuenta las líneas y palabras de un mensaje y envía el resultado al padre."""
    # Contamos el número de "líneas" (aquí solo será 1, ya que no hay saltos de línea en el mensaje)
    num_lineas = mensaje_padre.count('\n') + 1  # Le sumo 1 porque si no hay saltos de línea, solamente habrá 1

    # Contamos el número de "palabras", usando split() para separar por espacios
    num_palabras = len(mensaje_padre.split())

    # Enviar el resultado al padre
    os.write(pipe_escritura, f"Líneas: {num_lineas}, Palabras: {num_palabras}".encode('utf-8'))
    os.close(pipe_escritura)


def proceso_padre():
    # Crear un pipe para la comunicación entre padre e hijo (para mandar el mensaje al hijo)
    pipe_lectura, pipe_escritura = os.pipe()

    # Crear un segundo pipe para recibir la respuesta del hijo (mensaje modificado)
    pipe_lectura2, pipe_escritura2 = os.pipe()

    # Crear el proceso hijo para modificar el mensaje
    pid = os.fork()

    if pid == 0:
        # Proceso hijo: lee el mensaje, lo modifica y lo envía al padre
        os.close(pipe_escritura)  # El hijo no usa el pipe de escritura para el primer pipe
        os.close(pipe_lectura2)  # El hijo no usa el pipe de lectura para el segundo pipe
        modificar_mensaje(pipe_lectura, pipe_escritura2)  # Modificar el mensaje y enviar al padre
        os._exit(0)
    else:
        # Proceso padre: escribe el mensaje para que el hijo lo lea
        mensaje = "Hola hijo, ¿cómo estás?\n¿Todo bien?"
        os.write(pipe_escritura, mensaje.encode('utf-8'))  # El padre escribe el mensaje
        os.close(pipe_escritura)  # El padre no necesita escribir más

        # El padre ahora imprime el mensaje original
        print(f"Mensaje original enviado al hijo: {mensaje}")

        # El padre lee el mensaje modificado del hijo
        os.close(pipe_lectura)  # El padre no usa el pipe de lectura para el primer pipe
        mensaje_modificado = os.read(pipe_lectura2, 1024).decode('utf-8')
        print(f"Mensaje recibido del hijo en mayúsculas: {mensaje_modificado}")

        # Esperar que el hijo termine
        os.waitpid(pid, 0)

        # Crear un nuevo pipe para contar las líneas y palabras del mensaje
        pipe_lectura, pipe_escritura = os.pipe()

        # Crear el proceso hijo para contar las líneas y palabras del mensaje
        pid = os.fork()

        if pid == 0:
            # Proceso hijo: contar las líneas y palabras del mensaje
            contar_lineas_y_palabras(mensaje, pipe_escritura)
            os._exit(0)
        else:
            # Proceso padre: recibe el resultado del conteo
            os.close(pipe_escritura)  # El padre no necesita escribir en el pipe
            resultado = os.read(pipe_lectura, 1024).decode('utf-8')
            print(f"Resultado del mensaje: {resultado}")

            # Esperar que el hijo termine
            os.waitpid(pid, 0)


if __name__ == "__main__":
    proceso_padre()
