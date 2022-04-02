from brownie import accounts, config, network, FundMe, MockV3Aggregator

def main():
    if network.show_active() == 'development':
        contract = deploy_ganache()
    else:
        contract = deploy_rinkeby()

    print(f"Contract address: {contract.address}")
    print(f"Eth price: {contract.getEthPriceInWei()}")

def deploy_ganache():
    account = accounts[0]

    if len(MockV3Aggregator) < 1:
        MockV3Aggregator.deploy(8, 3000_00000000, {"from": account})

    return FundMe.deploy(MockV3Aggregator[0].address, {"from": account})

def deploy_rinkeby():
    account = accounts.add(config["wallets"]["from_key"])
    return FundMe.deploy(config["networks"]["rinkeby"]["eth_usd_feed"], {"from": account})