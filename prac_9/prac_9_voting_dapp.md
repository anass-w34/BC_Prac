
Creating a decentralized voting application on Ethereum is a great way to explore blockchain development. We'll use Truffle for smart contract development, Ganache for a local blockchain environment, and Visual Studio Code (VSCode) as our IDE. In this tutorial, I'll guide you step-by-step to create a basic voting Dapp where users can vote on pre-defined candidates.

Overview of the Voting Dapp
This Dapp will:

Allow the administrator to add candidates.
Allow users to vote for a candidate.
Track and display the votes for each candidate.
Prevent double voting by individual users.
Requirements
Ensure you have the following tools installed:

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


Download and install Ganache for creating a local Ethereum blockchain.
Create a New Truffle Project:
Open VSCode, then create a new project folder and navigate into it in the terminal:
bash
mkdir VotingDapp
cd VotingDapp

Initialize a Truffle project:
bash
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

Explanation:
addCandidate: Allows the administrator to add new candidates.
vote: Allows a user to vote for a candidate. It checks if the user has already voted and prevents double voting.
getVotes: Retrieves the total votes for a given candidate.

---------------------------------------------------------------------------------------------------------------

Step 4: Compile and Deploy the Smart Contract
Compile the Contract:

In the terminal, compile the contract:
bash
truffle compile

This generates the contract’s ABI and bytecode.

Deploy the Contract:
In the migrations folder, create a new file 2_deploy_contracts.js:

javascript: 
const Voting = artifacts.require("Voting");
module.exports = function (deployer) {
  deployer.deploy(Voting);
};


Deploy the contract to the Ganache network:
bash
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

Run the Tests:
bash 
truffle test

If the tests pass, the contract works as expected.

-------------------------------------------------------------------------------------------------------------

Step 6: Build the Front-End Interface
Install Web3.js:
In the project folder, install Web3.js:
bash
npm install web3

Create the Front-End Files:
Create an index.html file in the root of the project:
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

Create the JavaScript Interaction (app.js):
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
Steps to Create and Add index.html and app.js
Create the client folder:
Inside the root of your VotingDapp project, create a new folder named client.
This folder will contain your front-end files.
Add index.html:

Inside the client folder, create a file named index.html. This file will be your main HTML page.
Add app.js:
Inside the client folder, create a file named app.js. This JavaScript file will contain the code to interact with the Ethereum smart contract using Web3.
Move Static Assets (if needed):

If you have any CSS files, images, or other assets, you can create a subfolder within client, like client/assets or client/css, to store these files.
Example Code for index.html and app.js
Place the following code in index.html and app.js as mentioned in the previous instructions:

client/index.html
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

    <!-- Include Web3.js -->
    <script src="https://cdn.jsdelivr.net/gh/ethereum/web3.js@1.3.4/dist/web3.min.js"></script>
    <script src="app.js"></script>
</body>
</html>
_________________________________________________________________________________________________________
client/app.js

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

************ Notes:***********************************************************
Replace 'YOUR_CONTRACT_ADDRESS' with the actual contract address from the Truffle deployment on Ganache.
The contractABI array should be copied from the build/contracts/Voting.json file generated by Truffle.


-------------------------------------------------------------------------------------------------------

To run your Dapp locally, you'll need to serve index.html using a local server. 
This is necessary because some browsers block JavaScript from interacting with files directly on your computer, especially when working with Web3 and MetaMask. 
Here’s a step-by-step guide on how to do this using a couple of different methods.

Option 1: Using http-server (Node.js)
Install http-server:
In your terminal, navigate to the VotingDapp project directory.
Install http-server globally via npm if you haven’t already:
bash
npm install -g http-server

Serve the client Folder:
Inside your project, navigate to the client folder (where index.html is located):
bash
cd client

Start the server with the following command:
bash
http-server -c-1

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




