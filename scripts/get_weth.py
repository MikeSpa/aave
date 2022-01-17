from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def get_weth(amount=0.1):
    """
    Mints WETH by deposing ETH.
    """
    account = get_account()
    # interact with wETH contract:
    # ABI (copy interface (tho only need function we wanna use)) +
    # Address of the contract (copy in config)
    # weth is the WETH contract
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    deposit_tx = weth.deposit({"from": account, "value": amount * 10 ** 18})
    deposit_tx.wait(1)
    print(f"Received {amount} WETH")
    return deposit_tx


def get_eth(amount=0.1):
    account = get_account()
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    withdraw_tx = weth.withdraw(amount * 10 ** 18, {"from": account})
    withdraw_tx.wait(1)
    print(f"Received {amount} ETH")
    return withdraw_tx


def main():
    get_weth()
