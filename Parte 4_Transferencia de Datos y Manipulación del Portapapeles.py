import subprocess
import pyperclip
import time

#Funcion para descargar el archivo donde se necesita el servidor, el archivo y las credenciales
def descargar_archivo_ftp(servidor, archivo, usuario, contrasena):
    comando_ftp = f"open {servidor}\nuser {usuario} {contrasena}\nget {archivo}\nquit\n"

    proceso_ftp = subprocess.Popen(
        ["ftp", "-n"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

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

    #Verifica el contenido del portapapeles y muestra un mensaje si ha cambiado.
    contenido_anterior = pyperclip.paste()
    print("Esperando cambios en el portapapeles...")

    while True:
        time.sleep(2)
        contenido_actual = pyperclip.paste()
        if contenido_actual != contenido_anterior:
            print("¡El contenido del portapapeles ha cambiado!")
            contenido_anterior = contenido_actual


def main():
    servidor_ftp = "ftp.gnu.org" # Cambia el servidor FTP
    archivo_ftp = "gnu/README"  # Nombre del archivo para descargar
    usuario_ftp = "anonymous"  # Usuario FTP
    contrasena_ftp = "guest"  # Contraseña FTP

    #Paso 1: Descargar el archivo
    descargar_archivo_ftp(servidor_ftp, archivo_ftp, usuario_ftp, contrasena_ftp)

    #Paso 2: Copiar el contenido del archivo
    copiar_al_portapapeles(archivo_ftp)

    #Paso 3: Verificar si el contenido del portapapeles ha cambiado
    verificar_cambio_portapapeles()

if __name__ == "__main__":
    main()
