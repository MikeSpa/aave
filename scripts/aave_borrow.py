from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRNOMENT,
)
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def get_lending_pool():
    # To interact with the contract we need the abi and the address
    # ABI -> ILendingPoolAddressesProvider
    # Address -> config: address of lending_pool_addresses_provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI: ILendingPool
    # Address: lending_pool_address
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    # ABI and address
    print("Approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRNOMENT
    ):
        get_weth()

    lending_pool = get_lending_pool()
    # approve sending out ERC20 tokens
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    print("Depositing...")
    deposit_tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    deposit_tx.wait(1)
    print("Deposited")
