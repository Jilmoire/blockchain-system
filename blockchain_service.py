import time
import json
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from modules.hasher import hash_block

app = Flask(__name__)
CORS(app)

class BlockChain:
    def __init__(self): # allows to call the BlockChain class using the self param
        self.chainlist =[
            {
                "index": 0,
                "timestamp": 123456789,
                "data": [
                    {
                        "data1": 54321,
                        "data2": 2344323443,
                    }
                ],
                "previous_hash": "0",
                "hash": ""
            }
        ]
    def gblock_hash(self): # creates the hash for the genesis block
        genesis_block = self.chainlist[0]
        genesis_block["hash"] = hash_block(genesis_block)
        
    def validate_block(self, unverified_block): # validates any newly added block to the chain
        # passed block's hash is removed for recalculation before comparison
        temp_block = unverified_block.copy()
        temp_block["hash"] = ""
        if unverified_block["hash"] != hash_block(temp_block):
            print("Change in the original hash detected. Not continuing.")
            return False
        return True
      
    def validate_chain(self): # uses the same function as validate_block() but for the whole list
        for i in range(1, len(self.chainlist)):
            current_block = self.chainlist[i]
            previous_block = self.chainlist[i - 1]
            temp_block = previous_block.copy()
            temp_block["hash"] = ""
            if current_block["previous_hash"] != hash_block(temp_block):
                print("Change in the previous hash detected. Not continuing.")
                return False
        return True
         
    def block_adder(self, data): # adds a new block to the list
        previous_block = self.chainlist[-1]
        indexer = previous_block["index"] + 1
        timestamp = int(time.time())
        new_block = {
            "index": indexer,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_block["hash"],
            "hash": ""
        }
        new_block["hash"] = hash_block(new_block)   
         
        if previous_block["hash"] == new_block["previous_hash"] and self.validate_block(new_block): # verification purposes
            self.chainlist.append(new_block)
            return new_block
        else:
            print("Previous hash was not the same. Chain is compromised.")
            return None

@app.route("/add_block", methods = ["POST"])
def add_block():
    data = request.json.get("data")
    if data:
        new_block = blockchain.block_adder(data)
        return jsonify(new_block)
    return jsonify({"error": "Missing input"}), 400

@app.route("/getchain", methods = ["GET"])
def get_chain():
    return jsonify(blockchain.chainlist)


blockchain = BlockChain()
blockchain.gblock_hash()
blockchain.block_adder({"data1": 1111, "data2": 2222})
blockchain.block_adder({"data1": 3333, "data2": 4444})
blockchain.validate_chain()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
