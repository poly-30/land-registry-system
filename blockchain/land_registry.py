"""
Land Registry Management Service with Multi-Layer Verification.
Orchestrates high-level land registry operations, IPFS document validation,
authority approvals, tokenized fractional investments, and ownership queries.
"""

import hashlib
from typing import Dict, Any, List, Optional
from .wallet import Wallet
from .transaction import (
    Transaction,
    TransactionType,
    PropertyRegistrationData,
    PropertyVerificationData,
    OwnershipTransferData,
    TokenizePropertyData,
    TransferTokensData,
    DistributeRentData,
)
from .blockchain import Blockchain


class LandRegistry:
    """
    Land Registry System providing the 3-Layer Verification Workflow:
    - Layer 1: Document & IPFS Hash Integrity
    - Layer 2: Government Authority Cryptographic Signing
    - Layer 3: Immutable Blockchain Consensus & State Finality
    """

    def __init__(self, blockchain: Optional[Blockchain] = None):
        self.blockchain = blockchain or Blockchain(difficulty=2)

    def register_authority(self, authority_wallet: Wallet) -> None:
        """Enrolls a government land authority/registrar wallet on the ledger."""
        self.blockchain.authorize_registrar(authority_wallet.address)

    @staticmethod
    def simulate_ipfs_upload(document_bytes: bytes, filename: str) -> str:
        """
        Simulates IPFS document upload and returns a deterministic IPFS CID (Content Identifier).
        In production, this uploads to Pinata/IPFS daemon.
        """
        sha = hashlib.sha256(document_bytes).hexdigest()
        # Simulated IPFS v0 Base58-styled CID prefix 'Qm'
        return f"Qm{sha[:44]}"

    def submit_property_registration(
        self,
        owner_wallet: Wallet,
        property_id: str,
        survey_number: str,
        location: Dict[str, Any],
        area_sqft: float,
        market_value: float,
        document_bytes: bytes,
        document_name: str,
        owner_name: str,
    ) -> Transaction:
        """
        Layer 1 Submission:
        Hashes deed/surveyor documents and submits property registration transaction.
        """
        ipfs_cid = self.simulate_ipfs_upload(document_bytes, document_name)
        reg_data = PropertyRegistrationData(
            property_id=property_id,
            survey_number=survey_number,
            location=location,
            area_sqft=area_sqft,
            market_value=market_value,
            ipfs_document_hash=ipfs_cid,
            owner_name=owner_name,
        )

        tx = Transaction(
            tx_type=TransactionType.REGISTER_PROPERTY,
            sender_address=owner_wallet.address,
            sender_public_key_pem=owner_wallet.public_key_pem,
            payload=reg_data.to_dict(),
        )
        tx.sign(owner_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def verify_property(
        self,
        registrar_wallet: Wallet,
        property_id: str,
        registrar_name: str,
        document_bytes: bytes,
        approve: bool = True,
        remarks: str = "Deed and survey coordinates validated successfully.",
    ) -> Transaction:
        """
        Layer 2 Verification:
        Government registrar checks document hash against submitted document (Layer 1 verification),
        performs authority inspection, and signs the verification transaction.
        """
        # Layer 1 Document Verification Check
        recomputed_cid = self.simulate_ipfs_upload(document_bytes, "verification_check")
        pending_txs = [
            t for t in self.blockchain.pending_transactions
            if t.tx_type == TransactionType.REGISTER_PROPERTY and t.payload.get("property_id") == property_id
        ]
        registered_prop = self.blockchain.state.properties.get(property_id)

        expected_cid = None
        if pending_txs:
            expected_cid = pending_txs[0].payload.get("ipfs_document_hash")
        elif registered_prop:
            expected_cid = registered_prop.get("ipfs_document_hash")

        layer_1_valid = (expected_cid == recomputed_cid)
        layer_2_approved = approve and layer_1_valid

        verif_data = PropertyVerificationData(
            property_id=property_id,
            registrar_name=registrar_name,
            layer_1_doc_verified=layer_1_valid,
            layer_2_authority_verified=layer_2_approved,
            remarks=remarks if layer_1_valid else "Document mismatch: Layer 1 verification failed.",
        )

        tx = Transaction(
            tx_type=TransactionType.VERIFY_PROPERTY,
            sender_address=registrar_wallet.address,
            sender_public_key_pem=registrar_wallet.public_key_pem,
            payload=verif_data.to_dict(),
        )
        tx.sign(registrar_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def transfer_ownership(
        self,
        seller_wallet: Wallet,
        property_id: str,
        buyer_address: str,
        sale_price: float,
        new_deed_bytes: Optional[bytes] = None,
    ) -> Transaction:
        """Executes full legal ownership deed transfer on verified property."""
        deed_cid = (
            self.simulate_ipfs_upload(new_deed_bytes, "transfer_deed")
            if new_deed_bytes else None
        )
        transfer_data = OwnershipTransferData(
            property_id=property_id,
            from_address=seller_wallet.address,
            to_address=buyer_address,
            sale_price=sale_price,
            deed_ipfs_hash=deed_cid,
        )

        tx = Transaction(
            tx_type=TransactionType.TRANSFER_OWNERSHIP,
            sender_address=seller_wallet.address,
            sender_public_key_pem=seller_wallet.public_key_pem,
            payload=transfer_data.to_dict(),
        )
        tx.sign(seller_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def tokenize_property(
        self,
        owner_wallet: Wallet,
        property_id: str,
        total_tokens: int,
        token_symbol: str,
        price_per_token: float,
    ) -> Transaction:
        """Tokenizes real estate asset into fractional ownership shares."""
        tok_data = TokenizePropertyData(
            property_id=property_id,
            total_tokens=total_tokens,
            token_symbol=token_symbol,
            price_per_token=price_per_token,
        )
        tx = Transaction(
            tx_type=TransactionType.TOKENIZE_PROPERTY,
            sender_address=owner_wallet.address,
            sender_public_key_pem=owner_wallet.public_key_pem,
            payload=tok_data.to_dict(),
        )
        tx.sign(owner_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def transfer_tokens(
        self,
        seller_wallet: Wallet,
        property_id: str,
        buyer_address: str,
        token_count: int,
        total_amount: float,
    ) -> Transaction:
        """Transfers fractional property tokens to an investor."""
        tok_transfer_data = TransferTokensData(
            property_id=property_id,
            from_address=seller_wallet.address,
            to_address=buyer_address,
            token_count=token_count,
            total_amount=total_amount,
        )
        tx = Transaction(
            tx_type=TransactionType.TRANSFER_TOKENS,
            sender_address=seller_wallet.address,
            sender_public_key_pem=seller_wallet.public_key_pem,
            payload=tok_transfer_data.to_dict(),
        )
        tx.sign(seller_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def distribute_rent(
        self,
        payer_wallet: Wallet,
        property_id: str,
        total_rent_amount: float,
        period: str = "March 2026",
    ) -> Transaction:
        """Distributes rental yields proportionally across all fractional token holders."""
        rent_data = DistributeRentData(
            property_id=property_id,
            total_rent_amount=total_rent_amount,
            period=period,
        )
        tx = Transaction(
            tx_type=TransactionType.DISTRIBUTE_RENT,
            sender_address=payer_wallet.address,
            sender_public_key_pem=payer_wallet.public_key_pem,
            payload=rent_data.to_dict(),
        )
        tx.sign(payer_wallet)
        self.blockchain.add_transaction(tx)
        return tx

    def mine_block(self, miner_address: str):
        """Layer 3 Seal: Mines pending transactions into an immutable block."""
        return self.blockchain.mine_pending_transactions(miner_address)

    def get_property(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves current property state from the ledger."""
        return self.blockchain.state.properties.get(property_id)

    def get_user_portfolio(self, user_address: str) -> Dict[str, Any]:
        """Calculates total owned properties and fractional tokens for a user address."""
        wholly_owned = []
        fractional_holdings = []

        for prop_id, prop in self.blockchain.state.properties.items():
            if prop["owner_address"] == user_address and not prop["tokenized"]:
                wholly_owned.append(prop)
            if prop["tokenized"] and user_address in prop["token_holders"]:
                tokens = prop["token_holders"][user_address]
                if tokens > 0:
                    fractional_holdings.append({
                        "property_id": prop_id,
                        "token_symbol": prop["token_symbol"],
                        "tokens_held": tokens,
                        "total_tokens": prop["total_tokens"],
                        "share_percentage": f"{(tokens / prop['total_tokens']) * 100:.1f}%",
                        "market_value_share": (tokens / prop["total_tokens"]) * prop["market_value"],
                    })

        return {
            "user_address": user_address,
            "wholly_owned_properties": wholly_owned,
            "fractional_investments": fractional_holdings,
        }
