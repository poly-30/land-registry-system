"""
Core Blockchain Engine and Land Registry State Machine.
Manages chain validation, consensus mining, state transitions, and ledger persistence.
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from .block import Block
from .transaction import Transaction, TransactionType


class RegistryState:
    """
    In-memory state engine maintained by applying verified transactions from mined blocks.
    Tracks properties, ownership, verification status, and fractional token holdings.
    """

    def __init__(self):
        # property_id -> property record dict
        self.properties: Dict[str, Dict[str, Any]] = {}
        # authorized registrar addresses
        self.authorized_registrars: set = set()

    def add_registrar(self, address: str) -> None:
        self.authorized_registrars.add(address)

    def is_authorized_registrar(self, address: str) -> bool:
        return address in self.authorized_registrars

    def apply_transaction(self, tx: Transaction) -> None:
        """Applies a confirmed transaction to update the registry state."""
        tx_type = tx.tx_type
        p = tx.payload

        if tx_type == TransactionType.REGISTER_PROPERTY:
            prop_id = p["property_id"]
            self.properties[prop_id] = {
                "property_id": prop_id,
                "survey_number": p["survey_number"],
                "location": p["location"],
                "area_sqft": p["area_sqft"],
                "market_value": p["market_value"],
                "ipfs_document_hash": p["ipfs_document_hash"],
                "owner_address": tx.sender_address,
                "owner_name": p["owner_name"],
                "layer_1_document_hash_verified": p.get("layer_1_document_hash_verified", True),
                "layer_2_authority_verified": False,
                "verification_status": "PENDING_VERIFICATION",
                "registrar_address": None,
                "tokenized": False,
                "total_tokens": 0,
                "token_symbol": None,
                "price_per_token": 0.0,
                "token_holders": {},  # address -> token count
                "history": [
                    {
                        "action": "REGISTERED",
                        "by": tx.sender_address,
                        "timestamp": tx.timestamp,
                        "tx_hash": tx.tx_hash,
                    }
                ],
            }

        elif tx_type == TransactionType.VERIFY_PROPERTY:
            prop_id = p["property_id"]
            if prop_id in self.properties:
                prop = self.properties[prop_id]
                prop["layer_2_authority_verified"] = p["layer_2_authority_verified"]
                prop["verification_status"] = "VERIFIED" if p["layer_2_authority_verified"] else "REJECTED"
                prop["registrar_address"] = tx.sender_address
                prop["history"].append({
                    "action": f"VERIFICATION_{prop['verification_status']}",
                    "registrar": tx.sender_address,
                    "registrar_name": p["registrar_name"],
                    "remarks": p["remarks"],
                    "timestamp": tx.timestamp,
                    "tx_hash": tx.tx_hash,
                })

        elif tx_type == TransactionType.TRANSFER_OWNERSHIP:
            prop_id = p["property_id"]
            if prop_id in self.properties:
                prop = self.properties[prop_id]
                old_owner = prop["owner_address"]
                new_owner = p["to_address"]
                prop["owner_address"] = new_owner
                if p.get("deed_ipfs_hash"):
                    prop["ipfs_document_hash"] = p["deed_ipfs_hash"]
                prop["history"].append({
                    "action": "OWNERSHIP_TRANSFERRED",
                    "from": old_owner,
                    "to": new_owner,
                    "sale_price": p["sale_price"],
                    "timestamp": tx.timestamp,
                    "tx_hash": tx.tx_hash,
                })

        elif tx_type == TransactionType.TOKENIZE_PROPERTY:
            prop_id = p["property_id"]
            if prop_id in self.properties:
                prop = self.properties[prop_id]
                prop["tokenized"] = True
                prop["total_tokens"] = p["total_tokens"]
                prop["token_symbol"] = p["token_symbol"]
                prop["price_per_token"] = p["price_per_token"]
                # Initially, all tokens belong to the original owner
                prop["token_holders"] = {tx.sender_address: p["total_tokens"]}
                prop["history"].append({
                    "action": "PROPERTY_TOKENIZED",
                    "total_tokens": p["total_tokens"],
                    "token_symbol": p["token_symbol"],
                    "price_per_token": p["price_per_token"],
                    "timestamp": tx.timestamp,
                    "tx_hash": tx.tx_hash,
                })

        elif tx_type == TransactionType.TRANSFER_TOKENS:
            prop_id = p["property_id"]
            if prop_id in self.properties:
                prop = self.properties[prop_id]
                from_addr = p["from_address"]
                to_addr = p["to_address"]
                count = p["token_count"]

                holders = prop["token_holders"]
                holders[from_addr] = holders.get(from_addr, 0) - count
                holders[to_addr] = holders.get(to_addr, 0) + count

                prop["history"].append({
                    "action": "TOKENS_TRANSFERRED",
                    "from": from_addr,
                    "to": to_addr,
                    "count": count,
                    "total_amount": p["total_amount"],
                    "timestamp": tx.timestamp,
                    "tx_hash": tx.tx_hash,
                })

        elif tx_type == TransactionType.DISTRIBUTE_RENT:
            prop_id = p["property_id"]
            if prop_id in self.properties:
                prop = self.properties[prop_id]
                total_rent = p["total_rent_amount"]
                period = p["period"]
                total_tokens = prop["total_tokens"]

                distributions = {}
                for holder, count in prop["token_holders"].items():
                    share = (count / total_tokens) * total_rent if total_tokens > 0 else 0
                    distributions[holder] = round(share, 2)

                prop["history"].append({
                    "action": "RENT_DISTRIBUTED",
                    "total_rent": total_rent,
                    "period": period,
                    "distributions": distributions,
                    "timestamp": tx.timestamp,
                    "tx_hash": tx.tx_hash,
                })


class Blockchain:
    """
    Blockchain ledger implementation for Land Registry.
    Maintains consensus, cryptographic validity, state transitions, and persistent storage.
    """

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.pending_transactions: List[Transaction] = []
        self.state: RegistryState = RegistryState()

        # Initialize with genesis block
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Generates the initial immutable Genesis Block (Block #0)."""
        genesis_tx = Transaction(
            tx_type=TransactionType.GENESIS,
            sender_address="0x0000000000000000000000000000000000000000",
            sender_public_key_pem="",
            payload={"message": "Genesis Block - Secure Land Registry Ledger Initialized"},
            timestamp=0.0,
            signature="GENESIS_SIGNATURE",
            tx_hash="0" * 64,
        )
        genesis_block = Block(
            index=0,
            transactions=[genesis_tx],
            previous_hash="0" * 64,
            timestamp=0.0,
            nonce=0,
        )
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def authorize_registrar(self, address: str) -> None:
        """Grants an address Government Land Authority status."""
        self.state.add_registrar(address)

    def validate_transaction_against_state(self, tx: Transaction) -> bool:
        """
        Enforces domain rules before accepting a transaction into the mempool.
        """
        # Cryptographic check
        if not tx.is_valid():
            raise ValueError("Cryptographic signature verification failed.")

        p = tx.payload
        tx_type = tx.tx_type

        if tx_type == TransactionType.REGISTER_PROPERTY:
            prop_id = p.get("property_id")
            if not prop_id:
                raise ValueError("Property ID is required.")
            in_pending = any(
                ptx.tx_type == TransactionType.REGISTER_PROPERTY and ptx.payload.get("property_id") == prop_id
                for ptx in self.pending_transactions
            )
            if prop_id in self.state.properties or in_pending:
                raise ValueError(f"Property '{prop_id}' is already registered or pending registration on this ledger.")
            if not p.get("ipfs_document_hash"):
                raise ValueError("Layer-1 document IPFS hash is required.")

        elif tx_type == TransactionType.VERIFY_PROPERTY:
            prop_id = p.get("property_id")
            in_pending = any(
                ptx.tx_type == TransactionType.REGISTER_PROPERTY and ptx.payload.get("property_id") == prop_id
                for ptx in self.pending_transactions
            )
            if prop_id not in self.state.properties and not in_pending:
                raise ValueError(f"Property '{prop_id}' does not exist.")
            if not self.state.is_authorized_registrar(tx.sender_address):
                raise ValueError(f"Sender {tx.sender_address} is not an authorized Land Registry Authority.")

        elif tx_type == TransactionType.TRANSFER_OWNERSHIP:
            prop_id = p.get("property_id")
            if prop_id not in self.state.properties:
                raise ValueError(f"Property '{prop_id}' does not exist.")
            prop = self.state.properties[prop_id]
            if prop["verification_status"] != "VERIFIED":
                raise ValueError(f"Property '{prop_id}' must be VERIFIED before transferring ownership.")
            if prop["owner_address"] != tx.sender_address:
                raise ValueError("Only the registered owner can initiate full ownership transfer.")
            if prop["tokenized"]:
                # If tokenized, seller must hold 100% of tokens to transfer full title
                seller_tokens = prop["token_holders"].get(tx.sender_address, 0)
                if seller_tokens != prop["total_tokens"]:
                    raise ValueError("Cannot transfer title directly; property is fractionalized among token holders.")

        elif tx_type == TransactionType.TOKENIZE_PROPERTY:
            prop_id = p.get("property_id")
            if prop_id not in self.state.properties:
                raise ValueError(f"Property '{prop_id}' does not exist.")
            prop = self.state.properties[prop_id]
            if prop["verification_status"] != "VERIFIED":
                raise ValueError(f"Property '{prop_id}' must be verified by authority before tokenization.")
            if prop["owner_address"] != tx.sender_address:
                raise ValueError("Only the registered owner can tokenize the property.")
            if prop["tokenized"]:
                raise ValueError(f"Property '{prop_id}' has already been tokenized.")
            if p.get("total_tokens", 0) <= 0:
                raise ValueError("Total tokens must be greater than zero.")

        elif tx_type == TransactionType.TRANSFER_TOKENS:
            prop_id = p.get("property_id")
            if prop_id not in self.state.properties:
                raise ValueError(f"Property '{prop_id}' does not exist.")
            prop = self.state.properties[prop_id]
            if not prop["tokenized"]:
                raise ValueError(f"Property '{prop_id}' is not tokenized.")
            sender_balance = prop["token_holders"].get(tx.sender_address, 0)
            if sender_balance < p["token_count"]:
                raise ValueError(
                    f"Insufficient token balance. Available: {sender_balance}, Requested: {p['token_count']}"
                )

        elif tx_type == TransactionType.DISTRIBUTE_RENT:
            prop_id = p.get("property_id")
            if prop_id not in self.state.properties:
                raise ValueError(f"Property '{prop_id}' does not exist.")
            prop = self.state.properties[prop_id]
            if not prop["tokenized"]:
                raise ValueError(f"Property '{prop_id}' is not tokenized for rental distribution.")
            if p.get("total_rent_amount", 0) <= 0:
                raise ValueError("Rent distribution amount must be greater than zero.")

        return True

    def add_transaction(self, tx: Transaction) -> bool:
        """Validates and queues a transaction into pending transactions mempool."""
        self.validate_transaction_against_state(tx)
        self.pending_transactions.append(tx)
        return True

    def mine_pending_transactions(self, miner_address: str) -> Optional[Block]:
        """
        Packages pending transactions into a new block, mines it using Proof of Work,
        updates the ledger state, and commits the block to the chain.
        """
        if not self.pending_transactions:
            return None

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions[:],
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
        )

        new_block.mine(self.difficulty)

        # Apply transactions to state machine
        for tx in new_block.transactions:
            self.state.apply_transaction(tx)

        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self) -> (bool, str):
        """
        Cryptographic integrity check for the entire blockchain:
        1. Checks block header hashes against calculated SHA-256 hashes.
        2. Checks Proof-of-Work difficulty fulfillment.
        3. Checks previous_hash chaining links.
        4. Re-computes and checks Merkle Root for all transaction sets.
        5. Verifies all transaction signatures.
        """
        target_prefix = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify previous hash link
            if current.previous_hash != previous.hash:
                return False, f"Broken chain link at Block #{current.index}: previous_hash mismatch."

            # 2. Verify Merkle root matches transactions
            calculated_merkle = current.calculate_merkle_root()
            if current.merkle_root != calculated_merkle:
                return False, f"Tampered transactions at Block #{current.index}: Merkle Root mismatch."

            # 3. Verify block hash calculation
            calculated_hash = current.calculate_hash()
            if current.hash != calculated_hash:
                return False, f"Tampered block header at Block #{current.index}: Hash mismatch."

            # 4. Verify Proof of Work
            if not current.hash.startswith(target_prefix):
                return False, f"Proof of Work invalid at Block #{current.index}: Insufficient difficulty."

            # 5. Verify transaction signatures
            for tx in current.transactions:
                if not tx.is_valid():
                    return False, f"Invalid transaction signature in Block #{current.index}, Tx: {tx.tx_hash}"

        return True, "Blockchain integrity verified: 100% valid."

    def save_to_file(self, file_path: str) -> None:
        """Persists the blockchain to a JSON file."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        data = {
            "difficulty": self.difficulty,
            "authorized_registrars": list(self.state.authorized_registrars),
            "chain": [block.to_dict() for block in self.chain],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: str) -> "Blockchain":
        """Loads and reconstructs a verified blockchain from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        blockchain = cls(difficulty=data.get("difficulty", 2))
        blockchain.chain = [Block.from_dict(b) for b in data["chain"]]
        blockchain.state = RegistryState()

        for reg in data.get("authorized_registrars", []):
            blockchain.authorize_registrar(reg)

        # Replay transactions to reconstruct consistent state
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.tx_type != TransactionType.GENESIS:
                    blockchain.state.apply_transaction(tx)

        valid, msg = blockchain.is_chain_valid()
        if not valid:
            raise ValueError(f"Loaded blockchain failed integrity check: {msg}")

        return blockchain
