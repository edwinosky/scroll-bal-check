import requests

# Configura la URL base de la API y tu clave API
URL_BASE_API = "https://api.scrollscan.com/api"
API_KEY = "YourAPIKEY"

# Función para leer las direcciones de un archivo
def leer_direcciones(archivo_entrada):
    with open(archivo_entrada, 'r') as file:
        return [line.strip() for line in file]

# Función para guardar las direcciones con balance en un archivo
def guardar_direcciones(direcciones, archivo_salida):
    with open(archivo_salida, 'w') as file:
        for direccion in direcciones:
            file.write(direccion + '\n')

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
            return True
        else:
            print(f"La wallet {wallet} no tiene balance.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error al verificar la wallet {wallet}: {e}")
        return False

# Archivos de entrada y salida
archivo_entrada = 'wallets.txt'
archivo_salida = 'wallets_with_balance.txt'

# Leer las direcciones del archivo de entrada
wallets = leer_direcciones(archivo_entrada)

# Lista para guardar las direcciones con balance
wallets_con_balance = []

# Verificar cada wallet en la lista
for wallet in wallets:
    if verificar_balance(wallet):
        wallets_con_balance.append(wallet)

# Guardar las direcciones con balance en el archivo de salida
guardar_direcciones(wallets_con_balance, archivo_salida)
