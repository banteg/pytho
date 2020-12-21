import csv
import json
from itertools import zip_longest

from brownie import web3
from eth_abi.packed import encode_abi_packed
from eth_utils import encode_hex, is_address, to_checksum_address


def main():
    reader = csv.reader(open("snapshot/01-delphi.csv"))
    balances = {
        to_checksum_address(address): int(balance)
        for address, balance in reader
        if is_address(address)
    }
    print("recipients:", len(balances))
    print("total supply:", sum(balances.values()) / 1e18)
    distribution = prepare_merkle_tree(balances)
    print("merkle root:", distribution["merkleRoot"])
    with open("snapshot/02-merkle.json", "wt") as f:
        json.dump(distribution, f, indent=2)


def prepare_merkle_tree(balances):
    elements = [
        (index, account, amount)
        for index, (account, amount) in enumerate(balances.items())
    ]
    nodes = [encode_abi_packed(["uint", "address", "uint"], el) for el in elements]
    tree = MerkleTree(nodes)
    distribution = {
        "merkleRoot": encode_hex(tree.root),
        "tokenTotal": str(sum(balances.values())),
        "claims": {
            user: {
                "index": index,
                "amount": str(amount),
                "proof": tree.get_proof(nodes[index]),
            }
            for index, user, amount in elements
        },
    }
    return distribution


class MerkleTree:
    def __init__(self, elements):
        self.elements = sorted(set(web3.keccak(el) for el in elements))
        self.layers = MerkleTree.get_layers(self.elements)

    @property
    def root(self):
        return self.layers[-1][0]

    def get_proof(self, el):
        el = web3.keccak(el)
        idx = self.elements.index(el)
        proof = []
        for layer in self.layers:
            pair_idx = idx + 1 if idx % 2 == 0 else idx - 1
            if pair_idx < len(layer):
                proof.append(encode_hex(layer[pair_idx]))
            idx //= 2
        return proof

    @staticmethod
    def get_layers(elements):
        layers = [elements]
        while len(layers[-1]) > 1:
            layers.append(MerkleTree.get_next_layer(layers[-1]))
        return layers

    @staticmethod
    def get_next_layer(elements):
        return [
            MerkleTree.combined_hash(a, b)
            for a, b in zip_longest(elements[::2], elements[1::2])
        ]

    @staticmethod
    def combined_hash(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return web3.keccak(b"".join(sorted([a, b])))
