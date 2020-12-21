import json

import pytest


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    # enable function isolation
    pass


@pytest.fixture(scope="module")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def pytho(Pytho, tree, deployer):
    return Pytho.deploy("Pytho", "PYTHO", tree["tokenTotal"], {"from": deployer})


@pytest.fixture(scope="module")
def tree():
    with open("snapshot/02-merkle.json") as fp:
        claim_data = json.load(fp)
    for value in claim_data["claims"].values():
        value["amount"] = int(value["amount"])

    return claim_data


@pytest.fixture(scope="module")
def distributor(MerkleDistributor, tree, pytho, deployer):
    contract = MerkleDistributor.deploy(pytho, tree["merkleRoot"], {"from": deployer})
    pytho.transfer(contract, tree["tokenTotal"])
    return contract
