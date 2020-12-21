from random import randrange

import brownie


def test_claim(distributor, tree, pytho):
    idx = randrange(len(tree["claims"]))
    account = sorted(tree["claims"])[idx]
    claim = tree["claims"][account]

    initial_balance = pytho.balanceOf(account)
    distributor.claim(
        claim["index"],
        account,
        claim["amount"],
        claim["proof"],
        {"from": account},
    )

    assert pytho.balanceOf(account) == initial_balance + claim["amount"]


def test_claim_via_different_account(distributor, tree, pytho):
    idx = randrange(len(tree["claims"]))
    account = sorted(tree["claims"])[idx]
    claim = tree["claims"][account]

    initial_balance = pytho.balanceOf(account)
    distributor.claim(claim["index"], account, claim["amount"], claim["proof"])

    assert pytho.balanceOf(account) == initial_balance + claim["amount"]


def test_claim_twice(distributor, tree):
    idx = randrange(len(tree["claims"]))
    account = sorted(tree["claims"])[idx]
    claim = tree["claims"][account]

    distributor.claim(claim["index"], account, claim["amount"], claim["proof"])

    with brownie.reverts("MerkleDistributor: Drop already claimed."):
        distributor.claim(claim["index"], account, claim["amount"], claim["proof"])
