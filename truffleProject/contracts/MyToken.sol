pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    mapping(address => bool) private _transferLocks;

    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1000 * 10 ** decimals()); 
    }

    function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
        require(!_transferLocks[sender], "Transfer is locked for this sender");
        _transferLocks[sender] = true;

        // 檢查餘額和授權
        uint256 currentAllowance = allowance(sender, msg.sender);
        require(currentAllowance >= amount, "ERC20: transfer amount exceeds allowance");

        _transfer(sender, recipient, amount);
        _approve(sender, msg.sender, currentAllowance - amount);

        _transferLocks[sender] = false;
        return true;
    }

     function unsafeTransferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
        // 绕过 allowance 检查
        _transfer(sender, recipient, amount);

        // 不减少 allowance 或者使用不正确的 allowance 逻辑
        //_approve(sender, msg.sender, currentAllowance - amount);

        return true;
    }

}