import requests
import time
import os
import multiprocessing

# Configura la URL base de la API y tu clave API
URL_BASE_API = "https://api.scrollscan.com/api"
API_KEY = "YourAPIKEY"

# Archivos de entrada y salida
archivo_entrada = 'wallets.txt'
archivo_salida = 'wallets_con_balance.txt'
archivo_progreso = 'progreso.txt'

# Función para leer las direcciones de un archivo
def leer_direcciones(archivo_entrada):
    with open(archivo_entrada, 'r') as file:
        return [line.strip() for line in file]

# Función para guardar las direcciones con balance en un archivo
def guardar_direcciones(direcciones, archivo_salida):
    with open(archivo_salida, 'a') as file:  # Append mode
        for direccion in direcciones:
            file.write(direccion + '\n')

# Función para leer el progreso desde un archivo
def leer_progreso(archivo_progreso):
    if os.path.exists(archivo_progreso):
        with open(archivo_progreso, 'r') as file:
            return int(file.readline().strip())
    return 0

# Función para guardar el progreso en un archivo
def guardar_progreso(indice, archivo_progreso):
    with open(archivo_progreso, 'w') as file:
        file.write(str(indice))

# Función para verificar si una wallet tiene balance en la blockchain de Scroll
def verificar_balance(wallet):
    # Construye la URL con los parámetros necesarios
    url = f"{URL_BASE_API}?module=account&action=balance&address={wallet}&tag=latest&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Verifica si hay balance
        if data.get('result') and int(data['result']) > 0:
            print(f"La wallet {wallet} tiene un balance de {data['result']}.")
            return wallet, True
        else:
            print(f"La wallet {wallet} no tiene balance.")
            return wallet, False
    
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar la wallet {wallet}: {e}")
        return wallet, None

# Función para procesar wallets en un rango de índices
def procesar_wallets(wallets, inicio, fin, indice_progreso, lock):
    wallets_con_balance = []
    
    for i in range(inicio, fin):
        wallet = wallets[i]
        resultado = verificar_balance(wallet)
        
        # Si la verificación tuvo éxito, guardar el progreso y la dirección si tiene balance
        if resultado[1] is not None:
            with lock:
                guardar_progreso(indice_progreso + i, archivo_progreso)
                if resultado[1]:
                    wallets_con_balance.append(wallet)
                    guardar_direcciones([wallet], archivo_salida)
        else:
            # Si hay un error de conexión, espera un momento antes de reintentar
            time.sleep(5)

    return wallets_con_balance

# Función principal
def main():
    # Leer las direcciones del archivo de entrada
    wallets = leer_direcciones(archivo_entrada)

    # Leer el progreso desde el archivo de progreso
    ultimo_indice_exitoso = leer_progreso(archivo_progreso)
    
    # Definir el número de procesos
    num_procesos = 4  # Puedes ajustar esto según tus necesidades
    tamano_lote = (len(wallets) - ultimo_indice_exitoso) // num_procesos
    procesos = []
    lock = multiprocessing.Lock()
    
    # Crear procesos para verificar las wallets en paralelo
    for i in range(num_procesos):
        inicio = ultimo_indice_exitoso + i * tamano_lote
        fin = inicio + tamano_lote if i != num_procesos - 1 else len(wallets)
        p = multiprocessing.Process(target=procesar_wallets, args=(wallets, inicio, fin, ultimo_indice_exitoso, lock))
        procesos.append(p)
        p.start()
    
    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()

    print("Verificación completada.")

if __name__ == "__main__":
    main()
