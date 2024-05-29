// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EscrowERC20 {
    IERC20 public token;
    address public payer;
    address public payee;
    address public arbiter;
    uint public amount;
    bool public isLocked;
    bool public isConfirmed;

    constructor(address _token, address _payee, address _arbiter, uint _amount) {
        token = IERC20(_token);
        payer = msg.sender;
        payee = _payee;
        arbiter = _arbiter;
        amount = _amount;
        isLocked = false;
        isConfirmed = false;
    }

    function lock() public {
        require(msg.sender == payer, "Only payer can lock funds");
        require(token.transferFrom(payer, address(this), amount), "Token transfer failed");
        isLocked = true;
    }

    function confirm() public {
        require(msg.sender == arbiter, "Only arbiter can confirm");
        require(isLocked, "Funds are not locked yet");
        isConfirmed = true;
    }

    function commit() public {
        require(isConfirmed, "Transaction not confirmed yet");
        require(token.transfer(payee, amount), "Token transfer failed");
        reset();
    }

    function rollback() public {
        require(msg.sender == payer || msg.sender == arbiter, "Only payer or arbiter can rollback");
        require(!isConfirmed, "Transaction already confirmed");
        require(token.transfer(payer, amount), "Token transfer failed");
        reset();
    }

    function reset() internal {
        isLocked = false;
        isConfirmed = false;
    }
}
