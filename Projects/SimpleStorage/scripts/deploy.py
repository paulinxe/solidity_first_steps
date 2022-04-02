from brownie import Storage

def main():
    contract = deploy()
    print(getNumber(contract))
    txn = changeNumber(contract, 69)
    txn.wait(1)
    print(getNumber(contract))

def deploy():
    return Storage.deploy({
        "from": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    })

def getNumber(contract):
    return contract.retrieve()

def changeNumber(contract, number):
    return contract.store(number, {"from": "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"})