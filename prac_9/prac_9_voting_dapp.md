
Node.js and npm
Truffle
Ganache
MetaMask (for browser interaction)
Visual Studio Code (VSCode)


Step-by-Step Guide
Step 1: Set Up the Development Environment
Install Truffle and Ganache:

Install Truffle globally:
bash
npm install -g truffle

Create a New Truffle Project:
Open VSCode, then create a new project folder and navigate into it in the terminal:
create VotingDapp folder 
open vscode in that folder


Initialize a Truffle project:
terminal

truffle init
------------------------------------------------------------------------------------------------------
Step 2: Configure Ganache
Start Ganache:

Open Ganache and either create a new workspace or start a quickstart instance. Note the RPC server URL (usually http://127.0.0.1:7545) and port number.
Configure Truffle to Connect to Ganache:

Open truffle-config.js in your project folder and configure the development network to connect to Ganache:
javascript

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545, // Port for Ganache
      network_id: "*", // Match any network id
    },
  },
  compilers: {
    solc: {
      version: "0.8.0", // Solidity version
    },
  },
};

--------------------------------------------------------------------------------------------------------------------

Step 3: Write the Voting Smart Contract
Create a Smart Contract File:

In the contracts folder, create a new file named Voting.sol.
Write the Solidity Code:

Add the following code:
solidity
code: 
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    // Structure to represent a candidate
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Mappings to store candidates and to track whether an address has voted
    mapping(uint => Candidate) public candidates;
    mapping(address => bool) public hasVoted;

    uint public candidatesCount;  // Number of candidates

    // Event emitted when a vote is cast
    event VoteCast(uint indexed candidateId);

    // Function to add a candidate (only admin can call this in real-world apps)
    function addCandidate(string memory name) public {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, name, 0);
    }

    // Function to vote for a candidate
    function vote(uint candidateId) public {
        require(!hasVoted[msg.sender], "You have already voted.");
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate ID.");

        hasVoted[msg.sender] = true;
        candidates[candidateId].voteCount++;

        emit VoteCast(candidateId);
    }

    // Function to get total votes of a candidate
    function getVotes(uint candidateId) public view returns (uint) {
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate ID.");
        return candidates[candidateId].voteCount;
    }
}


Step 4: in terminal
truffle compile

This generates the contract’s ABI and bytecode.

Deploy the Contract:
In the migrations folder, create a new file 2_deploy_contracts.js:

javascript: 
const Voting = artifacts.require("Voting");
module.exports = function (deployer) {
  deployer.deploy(Voting);
};



IN TERMINAL

truffle migrate --network development

Once deployed, copy the contract’s address from the console.


----------------------------------------------------------------------------------------------------------

Step 5: Test the Smart Contract
Create a Test File:
In the test folder, create a new file named Voting.test.js:
javascript
Copy code: 
const Voting = artifacts.require("Voting");

contract("Voting", (accounts) => {
  it("should add a candidate", async () => {
    const instance = await Voting.deployed();
    await instance.addCandidate("Alice");

    const candidate = await instance.candidates(1);
    assert.equal(candidate.name, "Alice", "Candidate name should be Alice.");
  });

  it("should allow voting", async () => {
    const instance = await Voting.deployed();
    await instance.vote(1, { from: accounts[1] });

    const candidate = await instance.candidates(1);
    assert.equal(candidate.voteCount, 1, "Vote count should be 1.");
  });

  it("should prevent double voting", async () => {
    const instance = await Voting.deployed();
    try {
      await instance.vote(1, { from: accounts[1] });
    } catch (error) {
      assert(error, "Expected an error but did not get one");
    }
  });
});

Run the Tests: IN TERMINAL
truffle test

If the tests pass, the contract works as expected.

-------------------------------------------------------------------------------------------------------------

Step 6: 

In the project folder, install Web3.js:
IN TERMINAL
npm install web3

create client folder bahar of a project and add index.html and app.js  into it
Create an index.html file in client
html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Voting Dapp</title>
</head>
<body>
    <h1>Voting Dapp</h1>
    <input type="text" id="candidateName" placeholder="Enter candidate name">
    <button onclick="addCandidate()">Add Candidate</button>
    <div id="candidates"></div>
    <script src="https://cdn.jsdelivr.net/gh/ethereum/web3.js@1.3.4/dist/web3.min.js"></script>
    <script src="app.js"></script>
</body>
</html>

Create the app.js in client:
In app.js, add code to interact with the contract:
javascript
Copy code: 

let web3;
let voting;
window.addEventListener('load', async () => {
  if (window.ethereum) {
    web3 = new Web3(window.ethereum);
    await window.ethereum.enable();
  } else {
    console.log("No Ethereum browser extension detected.");
    return;
  }

  const contractABI = [/* ABI from build/contracts/Voting.json */];
  const contractAddress = 'YOUR_CONTRACT_ADDRESS';
  voting = new web3.eth.Contract(contractABI, contractAddress);

  loadCandidates();
});

async function addCandidate() {
  const accounts = await web3.eth.getAccounts();
  const candidateName = document.getElementById("candidateName").value;
  await voting.methods.addCandidate(candidateName).send({ from: accounts[0] });
  loadCandidates();
}

async function vote(candidateId) {
  const accounts = await web3.eth.getAccounts();
  await voting.methods.vote(candidateId).send({ from: accounts[0] });
  loadCandidates();
}

async function loadCandidates() {
  const candidatesCount = await voting.methods.candidatesCount().call();
  const candidatesDiv = document.getElementById("candidates");
  candidatesDiv.innerHTML = '';

  for (let i = 1; i <= candidatesCount; i++) {
    const candidate = await voting.methods.candidates(i).call();
    candidatesDiv.innerHTML += `
      <p>
        ${candidate.name} - Votes: ${candidate.voteCount}
        <button onclick="vote(${candidate.id})">Vote</button>
      </p>
    `;
  }
}


******************************* < Replace YOUR_CONTRACT_ADDRESS with your deployed contract address, and add the ABI from build/contracts/Voting.json. > ***************************************************************

VotingDapp
├── build                 # Contains ABI and other build artifacts
├── contracts             # Contains Solidity smart contracts
│   └── Voting.sol
├── migrations            # Contains deployment scripts
│   └── 2_deploy_contracts.js
├── node_modules          # Contains Node.js dependencies
├── test                  # Contains test scripts
│   └── Voting.test.js
├── client                # New folder for front-end files
│   ├── index.html        # Front-end HTML file for the Dapp
│   └── app.js            # JavaScript file to interact with the smart contract
├── package-lock.json
├── package.json
└── truffle-config.js     # Truffle configuration file

------------------------------------------------------------------------------------
IN TERMINAL

npm install -g http-server

cd client

http-server -c-1
***********************************************************
Open the Dapp in Your Browser:
http-server will display an address like http://127.0.0.1:8080 or http://localhost:8080 in the terminal.
Open this address in your browser. You should see your Dapp's UI.

Connect MetaMask:
Ensure MetaMask is connected to your local Ganache network. Add your local network in MetaMask using the following details:
Network Name: Ganache
New RPC URL: http://127.0.0.1:7545 (or your Ganache RPC server URL)
Chain ID: 1337 (for Ganache)
After connecting, you can interact with the Dapp by adding candidates and voting.

********************************************************************************************************
Testing Your Dapp
Add a Candidate:

Use the Dapp’s input field to enter a candidate’s name and click the Add Candidate button. The transaction will be sent to Ganache.
Vote for a Candidate:

Once candidates are added, click Vote next to a candidate's name. This will trigger a MetaMask transaction.
Verify in Ganache:

Open Ganache and go to the Transactions tab. You should see transactions corresponding to your interactions on the Dapp.




