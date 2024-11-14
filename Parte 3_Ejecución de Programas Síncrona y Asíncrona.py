import subprocess
import time

def ejecutar_sincrono():
    #Ejecutamos Notepad de forma síncrona (bloqueante), esperando a que se cierre.
    print("Ejecutando Notepad de forma síncrona...")
    start_time = time.time()

    #Ejecutamos Notepad
    subprocess.run(["notepad.exe"])

    end_time = time.time()
    return end_time - start_time  #Calculamos el tiempo desde que se abre hasta que se cierra

def ejecutar_asincrono():
    #Ejecutamos notepad de forma asíncrona (no bloqueante), sin esperar a que se cierre.
    print("Ejecutando Notepad de forma asíncrona...")
    start_time = time.time()

    #Ejecutamos Notepad
    proceso = subprocess.Popen(["notepad.exe"])

    end_time = time.time()
    return end_time - start_time  #Calculamos el tiempo que va ser menor porque no espera a que el notepad se cierre

def main():
    print("Elige el tipo de ejecución:")
    print("1. Ejecución Síncrona (Bloqueante)")
    print("2. Ejecución Asíncrona (No Bloqueante)")
    print("3. Salir")

    opcion = input("Ingresa 1 para síncrono o 2 para asíncrono: ")

    if opcion == '1':
        tiempo = ejecutar_sincrono()
        print(f"Tiempo de ejecución síncrona: {tiempo:.4f} segundos")
    elif opcion == '2':
        tiempo = ejecutar_asincrono()
        print(f"Tiempo de ejecución asíncrona: {tiempo:.4f} segundos")
    elif opcion == '3':
        print("Programa finalizado")
    else:
        print("Opción no válida, elige 1 o 2")

if __name__ == "__main__":
    main()