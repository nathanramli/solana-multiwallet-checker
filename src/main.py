import time

from solana.rpc.api import Client
from solana.rpc.types import RPCResponse, TokenAccountOpts

# Solana mainnet
http_client = Client("https://api.mainnet-beta.solana.com")

print("Input token mint address: ", end="")
mint_address = input()

# Open file
'''
    IMPORTANT:
    Use this format for wallet_address.txt

    Name1 walletaddress2
    Name2 walletaddress2

    Example:
    John 4Scm3Jgk8JGh8jpYnZ5Xt535DP1cQTfJLTYQixWfGY3M
    Dodo 6Scm3Jgk8FMh8DpBnZ5Xt535AA1cQTfJLTYQixWfGY3M
'''
with open("wallet_address.txt") as f:
    lines = f.readlines()
    for line in lines:
        word = line.strip().split()

        result = RPCResponse(http_client.get_token_accounts_by_owner(word[1], TokenAccountOpts(mint=mint_address, encoding="jsonParsed")))
        if len(result["result"]["value"]) == 0:
            amount = 0
        else:
            amount = result["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
        if amount == 0:
            print(word[0] + f" : \033[31mNo token\033[0m")
        else:
            print(f"{word[0]} : \033[92m{str(amount)}\033[0m")
        time.sleep(0.1)