import hashlib
import json
from time import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import websockets

HTTP_PORT = 3001
P2P_PORT = 6001
INITIAL_PEERS = []

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = str(previous_hash)
        self.timestamp = timestamp
        self.data = data
        self.hash = str(hash)

sockets = []

class MessageType:
    QUERY_LATEST = 0
    QUERY_ALL = 1
    RESPONSE_BLOCKCHAIN = 2

def get_genesis_block():
    return Block(0, "0", 1465154705, "my genesis block!!", "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7")

blockchain = [get_genesis_block()]

app = Flask(__name__)
CORS(app)

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([block.__dict__ for block in blockchain])

@app.route('/mineBlock', methods=['POST'])
def mine_block():
    new_block = generate_next_block(request.json['data'])
    add_block(new_block)
    broadcast(response_latest_msg())
    print(f'block added: {json.dumps(new_block.__dict__)}')
    return '', 204

@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify([f"{ws.remote_address[0]}:{ws.remote_address[1]}" for ws in sockets])

@app.route('/addPeer', methods=['POST'])
def add_peer():
    connect_to_peers([request.json['peer']])
    return '', 204

def init_http_server():
    app.run(port=HTTP_PORT)

async def init_connection(websocket, path):
    sockets.append(websocket)
    await init_message_handler(websocket)
    await websocket.send(json.dumps(query_chain_length_msg()))

async def init_message_handler(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f'Received message {json.dumps(data)}')
            if data['type'] == MessageType.QUERY_LATEST:
                await websocket.send(json.dumps(response_latest_msg()))
            elif data['type'] == MessageType.QUERY_ALL:
                await websocket.send(json.dumps(response_chain_msg()))
            elif data['type'] == MessageType.RESPONSE_BLOCKCHAIN:
                await handle_blockchain_response(data)
    except websockets.exceptions.ConnectionClosed:
        sockets.remove(websocket)

def generate_next_block(block_data):
    previous_block = get_latest_block()
    next_index = previous_block.index + 1
    next_timestamp = int(time())
    next_hash = calculate_hash(next_index, previous_block.hash, next_timestamp, block_data)
    return Block(next_index, previous_block.hash, next_timestamp, block_data, next_hash)

def calculate_hash_for_block(block):
    return calculate_hash(block.index, block.previous_hash, block.timestamp, block.data)

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def add_block(new_block):
    if is_valid_new_block(new_block, get_latest_block()):
        blockchain.append(new_block)

def is_valid_new_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        print('invalid index')
        return False
    elif previous_block.hash != new_block.previous_hash:
        print('invalid previoushash')
        return False
    elif calculate_hash_for_block(new_block) != new_block.hash:
        print(f'invalid hash: {calculate_hash_for_block(new_block)} {new_block.hash}')
        return False
    return True

async def connect_to_peers(new_peers):
    for peer in new_peers:
        try:
            async with websockets.connect(peer) as websocket:
                await init_connection(websocket, None)
        except:
            print('connection failed')

async def handle_blockchain_response(message):
    received_blocks = sorted(json.loads(message['data']), key=lambda k: k['index'])
    latest_block_received = received_blocks[-1]
    latest_block_held = get_latest_block()

    if latest_block_received['index'] > latest_block_held.index:
        print(f'blockchain possibly behind. We got: {latest_block_held.index} Peer got: {latest_block_received["index"]}')
        if latest_block_held.hash == latest_block_received['previousHash']:
            print("We can append the received block to our chain")
            blockchain.append(Block(**latest_block_received))
            await broadcast(response_latest_msg())
        elif len(received_blocks) == 1:
            print("We have to query the chain from our peer")
            await broadcast(query_all_msg())
        else:
            print("Received blockchain is longer than current blockchain")
            replace_chain(received_blocks)
    else:
        print('received blockchain is not longer than current blockchain. Do nothing')

def replace_chain(new_blocks):
    if is_valid_chain(new_blocks) and len(new_blocks) > len(blockchain):
        print('Received blockchain is valid. Replacing current blockchain with received blockchain')
        blockchain[:] = [Block(**block) for block in new_blocks]
        broadcast(response_latest_msg())
    else:
        print('Received blockchain invalid')

def is_valid_chain(blockchain_to_validate):
    if json.dumps(blockchain_to_validate[0]) != json.dumps(get_genesis_block().__dict__):
        return False
    temp_blocks = [blockchain_to_validate[0]]
    for i in range(1, len(blockchain_to_validate)):
        if is_valid_new_block(Block(**blockchain_to_validate[i]), Block(**temp_blocks[i - 1])):
            temp_blocks.append(blockchain_to_validate[i])
        else:
            return False
    return True

def get_latest_block():
    return blockchain[-1]

def query_chain_length_msg():
    return {'type': MessageType.QUERY_LATEST}

def query_all_msg():
    return {'type': MessageType.QUERY_ALL}

def response_chain_msg():
    return {
        'type': MessageType.RESPONSE_BLOCKCHAIN, 
        'data': json.dumps([block.__dict__ for block in blockchain])
    }

def response_latest_msg():
    return {
        'type': MessageType.RESPONSE_BLOCKCHAIN,
        'data': json.dumps([get_latest_block().__dict__])
    }

async def broadcast(message):
    await asyncio.gather(*[ws.send(json.dumps(message)) for ws in sockets])

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(connect_to_peers(INITIAL_PEERS))
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(init_connection, 'localhost', P2P_PORT))
    print(f'listening websocket p2p port on: {P2P_PORT}')
    init_http_server()