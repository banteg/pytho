# @version 0.2.8
from vyper.interfaces import ERC20

implements: ERC20


event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Redeemed:
    receiver: indexed(address)
    pytho: uint256
    dai: uint256


name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)
dai: ERC20


@external
def __init__(name: String[64], symbol: String[32], supply: uint256):
    self.name = name
    self.symbol = symbol
    self.decimals = 18
    self.balanceOf[msg.sender] = supply
    self.totalSupply = supply
    self.dai = ERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F)
    log Transfer(ZERO_ADDRESS, msg.sender, supply)


@internal
def _transfer(sender: address, receiver: address, amount: uint256):
    assert receiver not in [self, ZERO_ADDRESS]
    self.balanceOf[sender] -= amount
    self.balanceOf[receiver] += amount
    log Transfer(sender, receiver, amount)


@external
def transfer(receiver: address, amount: uint256) -> bool:
    self._transfer(msg.sender, receiver, amount)
    return True


@external
def transferFrom(sender: address, receiver: address, amount: uint256) -> bool:
    if msg.sender != sender and self.allowance[sender][msg.sender] != MAX_UINT256:
        self.allowance[sender][msg.sender] -= amount
        log Approval(sender, msg.sender, self.allowance[sender][msg.sender])
    self._transfer(sender, receiver, amount)
    return True


@external
def approve(spender: address, amount: uint256) -> bool:
    self.allowance[msg.sender][spender] = amount
    log Approval(msg.sender, spender, amount)
    return True


@view
@internal
def _rate(amount: uint256) -> uint256:
    if self.totalSupply == 0:
        return 0
    return amount * self.dai.balanceOf(self) / self.totalSupply


@view
@external
def rate() -> uint256:
    return self._rate(10 ** self.decimals)


@view
@external
def redeemable(account: address) -> uint256:
    return self._rate(self.balanceOf[account])


@external
def burn(_amount: uint256 = MAX_UINT256):
    amount: uint256 = min(_amount, self.balanceOf[msg.sender])
    redeemed: uint256 = self._rate(amount)
    self.dai.transfer(msg.sender, redeemed)
    self.totalSupply -= amount
    self.balanceOf[msg.sender] -= amount
    log Redeemed(msg.sender, amount, redeemed)
    log Transfer(msg.sender, ZERO_ADDRESS, amount)
