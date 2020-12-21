import json

import click
from brownie import MerkleDistributor, Pytho, Wei, accounts, rpc

PYTHO = ...
DISTRIBUTOR = ...


def get_user():
    if rpc.is_active():
        return accounts.at("0x5E38b802525de11A54506801B296D2Aa93d033EF", force=True)
    else:
        return accounts.load(
            click.prompt("Account", type=click.Choice(accounts.load()))
        )


def main():
    tree = json.load(open("snapshot/04-merkle.json"))
    user = get_user()
    dist = MerkleDistributor.at(DISTRIBUTOR, owner=user)
    if user not in tree["claims"]:
        return click.secho(f"{user} is not included in the distribution", fg="red")
    claim = tree["claims"][user]
    if dist.isClaimed(claim["index"]):
        return click.secho(f"{user} has already claimed", fg="yellow")

    amount = Wei(claim["amount"]).to("ether")
    _amount = click.style(f"{amount:,.2f} PYTHO", fg="green", bold=True)
    print(f"Claimable amount: {_amount}")
    dist.claim(claim["index"], user, claim["amount"], claim["proof"])


def burn():
    user = get_user()
    pytho = Pytho.at(PYTHO, owner=user)
    balance = pytho.balanceOf(user).to("ether")
    rate = pytho.rate().to("ether")
    _pytho = click.style(f"{balance:,.2f} PYTHO", fg="green", bold=True)
    _dai = click.style(f"{balance * rate:,.2f} DAI", fg="green", bold=True)
    _rate = click.style(f"{rate:,.5%}", fg="green", bold=True)
    _burn = click.style("burn", fg="red", bold=True)
    print(f"You have {_pytho}, which can be burned for {_dai} at a rate of {_rate}")
    if click.confirm(f"Do you want to {_burn} PYTHO for DAI?"):
        pytho.burn()
