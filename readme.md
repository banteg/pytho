# Pytho

Akropolis token claimable by exploit victims.

Snapshot is provided by Akropolis team, token design is based on [Cornichon](https://github.com/banteg/cornichon).

Technical writeup on the hack [can be found here](https://www.rekt.news/akropolis-rekt/).

## Mainnet deployment

MerkleDistributor deployed at: TBD

Pytho deployed at: TBD

## Deploy

To deploy the distributor and the token on the mainnet:

```
brownie run snapshot deploy --network mainnet
```

## Claim

To claim the distribution:
```
brownie accounts import alias keystore.json
brownie run claim --network mainnet
```

To burn PYTHO for DAI:
```
brownie run claim burn --network mainnet
```

## Tests

All testing is performed in a forked mainnet environment.

To run end to end claim and burn test:

```
brownie run distribution
```

To run the unit tests:

```
brownie test
```
