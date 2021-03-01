import time
from hashlib import sha256
import json

# define block objects
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for the block class.
        :param index: unique block ID
        :param transactions: list of transactions
        :param timestamp: timestamp of the block.
        :param previous_hash: hash of the previous block, used for chaining them together
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        """
        decodes json into python string, __dict__ gets all the (writable)varibles related to the object
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        hash = sha256(block_string.encode()).hexdigest()
        return hash
    

# chain the blocks
class BlockChain:
    def __init__(self):
        """
        constructor method
        """
        self.chain = []
        self.generate_gensis_block()
    
    def generate_gensis_block(self):
        """
        function that generates the genesis block, called on init
        """
        genesis_block = Block(0,[],time.time(),"0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        returns last block in the chain
        """
        return self.chain[-1]
    
    __difficulty = 2

    def proof_of_work(self, block):
        """
        a proof of work is needed so it takes a time to recompute all the hash values in the chain.
        it tries out different values of the nonce to get a hash that satisfies the difficulty 
        criteria. It works by adding a value to the block and computing the hash until the condition
        is met. 
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*BlockChain.__difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    
    def add_block(self, block, proof):
        """
        A function that adds a block to the chain after verification.
        """
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash :
            return False
        if not self.is_valid_proof(block=block,block_hash=proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
        
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0'* BlockChain.__difficulty) and block_hash == block.compute_hash())
