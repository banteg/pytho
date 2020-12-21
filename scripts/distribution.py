import json

from brownie import MerkleDistributor, Pytho, accounts, interface


def main():
    tree = json.load(open("snapshot/02-merkle.json"))
    whale = accounts.at("0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", force=True)
    dai = interface.ERC20("0x6B175474E89094C44Da98b954EedeAC495271d0F", owner=whale)
    pytho = Pytho.deploy("Pytho", "PYTHO", tree["tokenTotal"], {"from": whale})
    distributor = MerkleDistributor.deploy(pytho, tree["merkleRoot"], {"from": whale})
    pytho.transfer(distributor, tree["tokenTotal"])
    # the hacker sends everything back
    dai.transfer(pytho, tree["tokenTotal"])

    for user, claim in tree["claims"].items():
        distributor.claim(claim["index"], user, claim["amount"], claim["proof"])
        assert pytho.balanceOf(user) == claim["amount"]
        print("remaining in distributor:", pytho.balanceOf(distributor).to("ether"))
    assert pytho.balanceOf(distributor) == 0

    for user in tree["claims"]:
        user = accounts.at(user, force=True)
        amount = pytho.balanceOf(user)
        before = dai.balanceOf(user)
        assert pytho.rate() == "1 ether"
        pytho.burn(amount, {"from": user})
        assert pytho.balanceOf(user) == 0
        assert dai.balanceOf(user) == before + amount
        print("rate:", pytho.rate().to("ether"))
        print("remaining supply:", pytho.totalSupply().to("ether"))
        print("remaining dai:", dai.balanceOf(pytho).to("ether"))

    assert dai.balanceOf(pytho) == 0
    assert pytho.totalSupply() == 0
