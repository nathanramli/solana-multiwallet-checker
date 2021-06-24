import time
from solana.rpc.api import Client
from solana.rpc.types import RPCResponse, TokenAccountOpts
from constant import CACHE_LIFETIME_SECS, REFRESH_CACHE_URL, RPC_URL, CACHE_FILENAME
from cache import Cache

# Solana mainnet
http_client = Client(RPC_URL)

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

# Open file
cache = Cache(CACHE_FILENAME, REFRESH_CACHE_URL, CACHE_LIFETIME_SECS)

token_name = "Token"
for token in cache.data["tokens"]:
    if token["address"] == mint_address:
        token_name = token["name"]

print(f"Start fetching \033[94m{token_name}\033[0m with mint address \033[93m{mint_address}\033[0m...")

with open("wallet_address.txt") as f:
    lines = f.readlines()
    for line in lines:
        word = line.strip().split()
        result = RPCResponse(http_client.get_token_accounts_by_owner(word[1], TokenAccountOpts(mint=mint_address, encoding="jsonParsed")))
        
        if "error" in result:
            print("\033[31mError\033[0m: Invalid token.")
            break

        if len(result["result"]["value"]) == 0:
            amount = 0
        else:
            amount = result["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
        if amount == 0:
            print(word[0] + f" : \033[31mNo token\033[0m")
        else:
            print(f"{word[0]} : \033[92m{str(amount)}\033[0m")
        time.sleep(0.1)