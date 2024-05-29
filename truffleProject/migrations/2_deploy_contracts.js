const MyToken = artifacts.require("MyToken");
const EscrowERC20 = artifacts.require("EscrowERC20");

module.exports = async function (deployer, network, accounts) {
    const initialSupply = web3.utils.toWei('1000', 'ether'); // Ensure initial supply parameter is provided
    await deployer.deploy(MyToken, initialSupply); // Pass initial supply here
    const token = await MyToken.deployed();

    const payee = accounts[1];
    const arbiter = accounts[2];
    const amountToLock = web3.utils.toWei('10', 'ether');
    await deployer.deploy(EscrowERC20, token.address, payee, arbiter, amountToLock);
    const escrow = await EscrowERC20.deployed();
};
