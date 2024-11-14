import subprocess
import pyperclip
import time


def descargar_archivo_ftp(servidor, archivo, usuario, contrasena):
    #Conecta al servidor FTP y descarga el archivo utilizando subprocess.Popen.

    #Comando FTP en modo no interactivo
    comando_ftp = f"open {servidor}\nuser {usuario} {contrasena}\nget {archivo}\nquit\n"

    # Iniciar el proceso FTP
    proceso_ftp = subprocess.Popen(
        ["ftp", "-n"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Enviar los comandos FTP
    salida, error = proceso_ftp.communicate(input=comando_ftp)

    if error:
        print(f"Error al conectar al servidor FTP: {error}")
    else:
        print("Archivo descargado exitosamente.")


def copiar_al_portapapeles(archivo):
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
            pyperclip.copy(contenido)
            print("Contenido copiado al portapapeles.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")


def verificar_cambio_portapapeles():

    #Verifica periódicamente el contenido del portapapeles y muestra un mensaje si ha cambiado.

    contenido_anterior = pyperclip.paste()
    print("Esperando cambios en el portapapeles...")

    while True:
        time.sleep(2)  # Verifica cada 2 segundos
        contenido_actual = pyperclip.paste()
        if contenido_actual != contenido_anterior:
            print("¡El contenido del portapapeles ha cambiado!")
            contenido_anterior = contenido_actual  # Actualiza el contenido anterior


def main():
    servidor_ftp = "ftp.gnu.org" # Cambié el servidor FTP
    archivo_ftp = "gnu/README"  # Nombre del archivo a descargar (ajusta según lo que quieras)
    usuario_ftp = "anonymous"  # Usuario FTP
    contrasena_ftp = "guest"  # Contraseña FTP

    # Paso 1: Descargar el archivo desde el servidor FTP
    descargar_archivo_ftp(servidor_ftp, archivo_ftp, usuario_ftp, contrasena_ftp)

    # Paso 2: Copiar el contenido del archivo al portapapeles
    copiar_al_portapapeles(archivo_ftp)

    # Paso 3: Verificar periódicamente si el contenido del portapapeles ha cambiado
    verificar_cambio_portapapeles()

if __name__ == "__main__":
    main()
