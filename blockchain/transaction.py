"""
Transaction models for the Secure Land Registry System.
Handles land title registration, multi-layer verification, ownership transfers,
tokenization for fractional investments, and rental yields.
"""

import json
import time
import hashlib
from enum import Enum
from typing import Dict, Any, Optional
from .wallet import Wallet


class TransactionType(str, Enum):
    REGISTER_PROPERTY = "REGISTER_PROPERTY"
    VERIFY_PROPERTY = "VERIFY_PROPERTY"
    TRANSFER_OWNERSHIP = "TRANSFER_OWNERSHIP"
    TOKENIZE_PROPERTY = "TOKENIZE_PROPERTY"
    TRANSFER_TOKENS = "TRANSFER_TOKENS"
    DISTRIBUTE_RENT = "DISTRIBUTE_RENT"
    GENESIS = "GENESIS"


class PropertyRegistrationData:
    def __init__(
        self,
        property_id: str,
        survey_number: str,
        location: Dict[str, Any],
        area_sqft: float,
        market_value: float,
        ipfs_document_hash: str,
        owner_name: str,
    ):
        self.property_id = property_id
        self.survey_number = survey_number
        self.location = location
        self.area_sqft = area_sqft
        self.market_value = market_value
        self.ipfs_document_hash = ipfs_document_hash
        self.owner_name = owner_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "survey_number": self.survey_number,
            "location": self.location,
            "area_sqft": self.area_sqft,
            "market_value": self.market_value,
            "ipfs_document_hash": self.ipfs_document_hash,
            "owner_name": self.owner_name,
            "layer_1_document_hash_verified": True,
        }


class PropertyVerificationData:
    def __init__(
        self,
        property_id: str,
        registrar_name: str,
        layer_1_doc_verified: bool,
        layer_2_authority_verified: bool,
        remarks: str = "Verified and Approved by Land Records Authority",
    ):
        self.property_id = property_id
        self.registrar_name = registrar_name
        self.layer_1_doc_verified = layer_1_doc_verified
        self.layer_2_authority_verified = layer_2_authority_verified
        self.remarks = remarks

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "registrar_name": self.registrar_name,
            "layer_1_doc_verified": self.layer_1_doc_verified,
            "layer_2_authority_verified": self.layer_2_authority_verified,
            "remarks": self.remarks,
        }


class OwnershipTransferData:
    def __init__(
        self,
        property_id: str,
        from_address: str,
        to_address: str,
        sale_price: float,
        deed_ipfs_hash: Optional[str] = None,
    ):
        self.property_id = property_id
        self.from_address = from_address
        self.to_address = to_address
        self.sale_price = sale_price
        self.deed_ipfs_hash = deed_ipfs_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "sale_price": self.sale_price,
            "deed_ipfs_hash": self.deed_ipfs_hash,
        }


class TokenizePropertyData:
    def __init__(
        self,
        property_id: str,
        total_tokens: int,
        token_symbol: str,
        price_per_token: float,
    ):
        self.property_id = property_id
        self.total_tokens = total_tokens
        self.token_symbol = token_symbol
        self.price_per_token = price_per_token

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "total_tokens": self.total_tokens,
            "token_symbol": self.token_symbol,
            "price_per_token": self.price_per_token,
        }


class TransferTokensData:
    def __init__(
        self,
        property_id: str,
        from_address: str,
        to_address: str,
        token_count: int,
        total_amount: float,
    ):
        self.property_id = property_id
        self.from_address = from_address
        self.to_address = to_address
        self.token_count = token_count
        self.total_amount = total_amount

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "token_count": self.token_count,
            "total_amount": self.total_amount,
        }


class DistributeRentData:
    def __init__(
        self,
        property_id: str,
        total_rent_amount: float,
        period: str,
    ):
        self.property_id = property_id
        self.total_rent_amount = total_rent_amount
        self.period = period

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "total_rent_amount": self.total_rent_amount,
            "period": self.period,
        }


class Transaction:
    """
    Cryptographically signed land registry transaction.
    """

    def __init__(
        self,
        tx_type: TransactionType,
        sender_address: str,
        sender_public_key_pem: str,
        payload: Dict[str, Any],
        timestamp: Optional[float] = None,
        signature: Optional[str] = None,
        tx_hash: Optional[str] = None,
    ):
        self.tx_type = tx_type
        self.sender_address = sender_address
        self.sender_public_key_pem = sender_public_key_pem
        self.payload = payload
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.signature = signature
        self.tx_hash = tx_hash or self.calculate_hash()

    def get_signing_data(self) -> bytes:
        """Returns deterministic JSON bytes of transaction contents for signing/hashing."""
        content = {
            "tx_type": self.tx_type.value if isinstance(self.tx_type, TransactionType) else str(self.tx_type),
            "sender_address": self.sender_address,
            "timestamp": round(self.timestamp, 4),
            "payload": self.payload,
        }
        return json.dumps(content, sort_keys=True).encode("utf-8")

    def calculate_hash(self) -> str:
        """Computes SHA-256 hash of transaction content."""
        return hashlib.sha256(self.get_signing_data()).hexdigest()

    def sign(self, wallet: Wallet) -> None:
        """Signs the transaction using the sender's wallet."""
        if wallet.address != self.sender_address:
            raise ValueError(
                f"Signer wallet address ({wallet.address}) does not match sender address ({self.sender_address})"
            )
        self.signature = wallet.sign(self.get_signing_data())
        self.tx_hash = self.calculate_hash()

    def is_valid(self) -> bool:
        """
        Validates transaction integrity:
        1. Hash matches calculated hash.
        2. Genesis transactions are automatically valid if address is 0x0.
        3. Signature is present and validly signed by sender_public_key_pem.
        """
        if self.tx_type == TransactionType.GENESIS:
            return True

        if not self.signature:
            return False

        if not self.sender_public_key_pem:
            return False

        # Verify signature against signing data
        return Wallet.verify(
            public_key_pem=self.sender_public_key_pem,
            message=self.get_signing_data(),
            signature_hex=self.signature,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_hash": self.tx_hash,
            "tx_type": self.tx_type.value if isinstance(self.tx_type, TransactionType) else str(self.tx_type),
            "sender_address": self.sender_address,
            "sender_public_key_pem": self.sender_public_key_pem,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        return cls(
            tx_type=TransactionType(data["tx_type"]),
            sender_address=data["sender_address"],
            sender_public_key_pem=data["sender_public_key_pem"],
            payload=data["payload"],
            timestamp=data["timestamp"],
            signature=data.get("signature"),
            tx_hash=data.get("tx_hash"),
        )
