const Web3 = require('web3');
const MyToken = require('./build/contracts/MyToken.json');
const EscrowERC20 = require('./build/contracts/EscrowERC20.json');

const web3 = new Web3('http://localhost:8545');

const main = async () => {
  const accounts = await web3.eth.getAccounts();
  const payer = accounts[0];
  const payee = accounts[1];
  const arbiter = accounts[2];

  const networkId = await web3.eth.net.getId();
  const myTokenNetwork = MyToken.networks[networkId];
  const escrowNetwork = EscrowERC20.networks[networkId];

  const token = new web3.eth.Contract(MyToken.abi, myTokenNetwork.address);
  const escrow = new web3.eth.Contract(EscrowERC20.abi, escrowNetwork.address);

  const amountToLock = web3.utils.toWei('10', 'ether');

  // 批准Escrow合约转移代币
  console.log('Approving tokens...');
  await token.methods.approve(escrow.options.address, amountToLock).send({ from: payer });

  // 锁定资金
  console.log('Locking funds...');
  await escrow.methods.lock().send({ from: payer });

  // 仲裁者确认交易
  console.log('Confirming transaction...');
  await escrow.methods.confirm().send({ from: arbiter });

  // 提交交易
  console.log('Committing transaction...');
  await escrow.methods.commit().send({ from: payer });

  console.log('Transaction completed!');
};

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
