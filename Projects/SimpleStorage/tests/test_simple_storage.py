from brownie import accounts, Storage

def test_initial_number_is_zero():
    contract = Storage.deploy({"from": accounts[0]})
    actualNumber = contract.retrieve()
    expected = 0

    assert actualNumber == expected

def test_updating_number():
    number = 69

    contract = Storage.deploy({"from": accounts[0]})
    contract.store(number)
    actualNumber = contract.retrieve()

    assert actualNumber == number