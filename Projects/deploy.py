from solcx import compile_standard, install_solc
import json
from web3 import Web3

install_solc('0.6.0')

with open("./SimpleStorage.sol", "r") as file:
    file_contents = file.read()

compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": file_contents
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)

with open("./compiled.json", "w") as file:
    json.dump(compiled, file)

bytecode = compiled["contracts"]["SimpleStorage.sol"]["Storage"]["evm"]["bytecode"]["object"]
abi = compiled["contracts"]["SimpleStorage.sol"]["Storage"]["abi"]


# Infura para deploy en testnet
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
chain_id = 1337
address = ""
key = ""
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(address)
txn = SimpleStorage.constructor().buildTransaction({
    "gasPrice": 3000,
    "chainId": chain_id,
    "from": address,
    "nonce": nonce
})
signed_txn = w3.eth.account.sign_transaction(txn, private_key=key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# interacting
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

txn = simple_storage.functions.store(69).buildTransaction({
    "gasPrice": 3000, # TODO: check this out
    "chainId": chain_id,
    "from": address,
    "nonce": nonce + 1
})
signed_txn = w3.eth.account.sign_transaction(txn, private_key=key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print(simple_storage.functions.retrieve().call())