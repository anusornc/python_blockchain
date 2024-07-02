# Python Blockchain

This project implements a simple blockchain in Python, featuring both HTTP and P2P interfaces. It's designed for educational purposes to demonstrate basic blockchain concepts. Inspired from https://github.com/lhartikk/naivechain

## Features

- Simple proof-of-work blockchain implementation
- HTTP API for interacting with the blockchain
- P2P network capabilities for node communication
- Block mining functionality

## Prerequisites

- Python 3.7 or later

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-blockchain.git
   cd python-blockchain
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install flask flask-cors websockets
   ```

## Usage

1. Start the blockchain node:
   ```
   python blockchain.py
   ```
   This will start both the HTTP server (default port 3001) and the P2P server (default port 6001).

2. Interact with the blockchain using HTTP requests:

   - Get the current blockchain:
     ```
     curl http://localhost:3001/blocks
     ```

   - Mine a new block:
     ```
     curl -X POST -H "Content-Type: application/json" -d '{"data":"Some block data"}' http://localhost:3001/mineBlock
     ```

   - Get the list of peers:
     ```
     curl http://localhost:3001/peers
     ```

   - Add a new peer:
     ```
     curl -X POST -H "Content-Type: application/json" -d '{"peer":"ws://localhost:6001"}' http://localhost:3001/addPeer
     ```

## Running Multiple Nodes

To create a network of multiple nodes:

1. Start the first node with default settings:
   ```
   python blockchain.py
   ```

2. Start additional nodes in new terminal windows, specifying different ports and peers:
   ```
   HTTP_PORT=3002 P2P_PORT=6002 PEERS=ws://localhost:6001 python blockchain.py
   ```
   ```
   HTTP_PORT=3003 P2P_PORT=6003 PEERS=ws://localhost:6001,ws://localhost:6002 python blockchain.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This blockchain implementation is for educational purposes only and is not suitable for production use without significant enhancements.