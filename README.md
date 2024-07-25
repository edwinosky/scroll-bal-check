# scroll-bal-check
python script to check if a list of addresses "wallets.txt" has balance on the scroll blockchain

## Instructions:  
1: pip install requests

2: Input file: Make sure the wallets.txt file contains one wallet address per line.

3: Run the script: Save the script to a Python file (e.g. check_bal.py) and run it. It will read the addresses from wallets.txt, check the balance of each one using the Scroll API, print the result to the console and save the addresses with balance in a file wallets_with_balance.txt.

===================================

Make sure the API key (API_KEY) is correct. You can get it by registering at: https://scrollscan.com/register

Balance conditions: The script considers that if the result of the API (data['result']) is greater than 0, the wallet has balance.

Error Handling: The script handles request exceptions to catch possible errors while querying the API.
