def test_dai_amount(distributor, tree, pytho):
    assert pytho.balanceOf(distributor) == tree["tokenTotal"]


def test_tree_total(tree):
    claim_total = sum(v["amount"] for v in tree["claims"].values())
    assert claim_total == int(tree["tokenTotal"])
