"""
Wallet & Cryptographic Identity Module for Land Registry Blockchain.
Uses ECDSA (curve SECP256K1) for key generation, digital signatures, and address derivation.
"""

import hashlib
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Represents a participant's cryptographic identity in the Land Registry System.
    Provides SECP256K1 key pairs, digital signing, and address generation.
    """

    def __init__(self, private_key: Optional[ec.EllipticCurvePrivateKey] = None):
        if private_key is None:
            self._private_key = ec.generate_private_key(ec.SECP256K1())
        else:
            self._private_key = private_key
        self._public_key = self._private_key.public_key()

    @property
    def public_key(self) -> ec.EllipticCurvePublicKey:
        return self._public_key

    @property
    def public_key_pem(self) -> str:
        """Export public key as PEM encoded string."""
        pem_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem_bytes.decode("utf-8")

    @property
    def public_key_hex(self) -> str:
        """Export raw uncompressed public key bytes as hex string."""
        raw_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        return raw_bytes.hex()

    @property
    def private_key_pem(self) -> str:
        """Export private key as PEM string."""
        pem_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem_bytes.decode("utf-8")

    @property
    def address(self) -> str:
        """
        Derives an Ethereum-styled public address:
        0x + first 40 hex chars of SHA-256(public_key_raw_bytes).
        """
        raw_pub = self._public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        digest = hashlib.sha256(raw_pub).hexdigest()
        return f"0x{digest[:40]}"

    def sign(self, message: bytes) -> str:
        """
        Signs the given message bytes using ECDSA with SHA-256.
        Returns the hex-encoded DER signature.
        """
        signature = self._private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256()),
        )
        return signature.hex()

    @staticmethod
    def verify(public_key_pem: str, message: bytes, signature_hex: str) -> bool:
        """
        Verifies a DER hex signature against the message and PEM public key.
        """
        try:
            pub_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
            signature = bytes.fromhex(signature_hex)
            pub_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            return True
        except (InvalidSignature, ValueError, Exception):
            return False

    def export_private_key_pem(self, password: Optional[str] = None) -> str:
        """Export private key as PEM, optionally encrypted with a password."""
        if password:
            enc = serialization.BestAvailableEncryption(password.encode("utf-8"))
        else:
            enc = serialization.NoEncryption()
        pem_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=enc,
        )
        return pem_bytes.decode("utf-8")

    @classmethod
    def from_private_key_pem(cls, pem_str: str, password: Optional[str] = None) -> "Wallet":
        """Reconstructs a Wallet instance from a PEM encoded private key (with optional password)."""
        priv_key = serialization.load_pem_private_key(
            pem_str.encode("utf-8"),
            password=password.encode("utf-8") if password else None,
        )
        return cls(private_key=priv_key)
