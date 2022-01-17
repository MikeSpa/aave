from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRNOMENT,
)
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRNOMENT
    ):
        get_weth()
