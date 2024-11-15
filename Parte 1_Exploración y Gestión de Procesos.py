import psutil

#Función para listar los procesos activos
def listar_procesos(palabra_clave=""):
    procesos_encontrados = []
    print(f"\nProcesos activos (filtrando por: '{palabra_clave}'):")

    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            nombre = proc.info['name']
            pid = proc.info['pid']
            memoria = proc.info['memory_info'].rss / (1024 * 1024)  #Esto pone la memoria en MB para que por pantalla salga bonito
            if palabra_clave.lower() in nombre.lower():
                procesos_encontrados.append({
                    'nombre': nombre,
                    'pid': pid,
                    'memoria': memoria
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not procesos_encontrados:
        print("No se encontraron procesos")
    else:
        for proceso in procesos_encontrados:
            print(f"Nombre: {proceso['nombre']}, PID: {proceso['pid']}, Memoria: {proceso['memoria']}")

    return procesos_encontrados

#Función para finalizar un proceso
def finalizar_proceso(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"Proceso con PID {pid} finalizado correctamente")
    except psutil.NoSuchProcess:
        print(f"No se encontró el proceso con PID {pid}")
    except psutil.AccessDenied:
        print(f"No tienes permisos para finalizar el proceso con PID {pid}")
    except Exception as e:
        print(f"Ocurrió un error al intentar finalizar el proceso: {e}")

def main():
    palabra_clave = input("Ingresa una palabra clave para filtrar los procesos (deja vacío para no filtrar): ")

    procesos = listar_procesos(palabra_clave)

    if procesos:
        try:
            pid_seleccionado = int(input("\nIngresa el PID del proceso que deseas finalizar (0 para salir): "))
            if pid_seleccionado == 0:
                print("Se terminó el programa")
            else:
                finalizar_proceso(pid_seleccionado)
        except ValueError:
            print("Ingresa un número válido para el PID")
    else:
        print("No se encontraron procesos para finalizar")

if __name__ == "__main__":
    main()
