# scroll-bal-check
python script to check if a list of addresses "wallets.txt" has balance on the scroll blockchain

## Instructions:  
1: pip install requests multiprocessing

2: Input file: Make sure the wallets.txt file contains one wallet address per line.

3: Run the script: Save the script to a Python file (e.g. check_bal.py) and run it. It will read the addresses from wallets.txt, check the balance of each one using the Scroll API, print the result to the console and save the addresses with balance in a file wallets_con_balance.txt.

===================================

Make sure the API key (API_KEY) is correct. You can get it by registering at: https://scrollscan.com/register

Balance conditions: The script considers that if the result of the API (data['result']) is greater than 0, the wallet has balance.

Error Handling: The script handles request exceptions to catch possible errors while querying the API.

### UPDATE 1

Número de procesos: El número de procesos (num_procesos) se puede ajustar según la capacidad de tu máquina.
Tamaño de los lotes: El tamaño de los lotes se calcula dividiendo el número total de wallets restantes entre el número de procesos.
Bloqueo: El bloqueo asegura que solo un proceso a la vez puede escribir en los archivos compartidos.

### UPDATE 2

Guardado del progreso: El script guarda el índice de la última wallet verificada en un archivo progreso.txt. Esto permite reanudar desde donde se dejó si el script se interrumpe.
Manejo de errores de conexión: Si hay un error de conexión, el script espera 5 segundos (time.sleep(5)) antes de reintentar.
Lectura del progreso: Al inicio, el script lee el progreso desde progreso.txt y comienza la verificación desde el último índice exitoso.
Modo append en el archivo de salida: El archivo wallets_con_balance.txt se abre en modo de adición ('a') para agregar nuevas direcciones sin sobrescribir las anteriores.
