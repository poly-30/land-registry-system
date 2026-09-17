"""
Block data structure and Proof-of-Work mining for Land Registry Blockchain.
"""

import json
import time
import hashlib
from typing import List, Dict, Any, Optional
from .transaction import Transaction
from .merkle import MerkleTree


class Block:
    """
    Represents an immutable block on the ledger.
    Contains index, timestamp, list of transactions, previous block hash,
    Merkle root, nonce, and resulting block hash.
    """

    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: Optional[float] = None,
        nonce: int = 0,
        merkle_root: Optional[str] = None,
        block_hash: Optional[str] = None,
    ):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root or self.calculate_merkle_root()
        self.hash = block_hash or self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        """Calculates Merkle root of all transactions contained in this block."""
        tx_hashes = [tx.calculate_hash() for tx in self.transactions]
        tree = MerkleTree(tx_hashes)
        return tree.root

    def get_header_bytes(self) -> bytes:
        """Serializes block header attributes for hashing."""
        header = {
            "index": self.index,
            "timestamp": round(self.timestamp, 4),
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
        }
        return json.dumps(header, sort_keys=True).encode("utf-8")

    def calculate_hash(self) -> str:
        """Computes SHA-256 hash of block header."""
        return hashlib.sha256(self.get_header_bytes()).hexdigest()

    def mine(self, difficulty: int) -> None:
        """
        Proof-of-Work consensus mechanism:
        Increments nonce until block hash starts with `difficulty` number of zeros.
        """
        target_prefix = "0" * difficulty
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0

        while True:
            current_hash = self.calculate_hash()
            if current_hash.startswith(target_prefix):
                self.hash = current_hash
                break
            self.nonce += 1

    def has_valid_transactions(self) -> bool:
        """Verifies that all transactions inside this block are cryptographically valid."""
        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Block":
        txs = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        return cls(
            index=data["index"],
            transactions=txs,
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            nonce=data["nonce"],
            merkle_root=data.get("merkle_root"),
            block_hash=data.get("hash"),
        )
