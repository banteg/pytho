import json

from brownie import MerkleDistributor, Pytho, accounts, rpc


def main():
    tree = json.load(open("snapshot/02-merkle.json"))
    user = accounts[0] if rpc.is_active() else accounts.load(input("account: "))
    pytho = Pytho.deploy("Pytho", "PYTHO", tree["tokenTotal"], {"from": user})
    distributor = MerkleDistributor.deploy(pytho, tree["merkleRoot"], {"from": user})
    pytho.transfer(distributor, pytho.balanceOf(user))
