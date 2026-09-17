"""
Keystore and Key Management Service for Land Registry Blockchain.
Manages local persistence, password encryption (AES-256 / PKCS#8),
and recovery of participant cryptographic identities.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from .wallet import Wallet


class Keystore:
    """
    Manages local storage, password protection, and retrieval of participant wallets.
    Stores public keys, addresses, and encrypted private keys on disk.
    """

    def __init__(self, keystore_dir: str = "wallets"):
        self.keystore_dir = keystore_dir
        os.makedirs(self.keystore_dir, exist_ok=True)

    def _get_wallet_path(self, label: str) -> str:
        # Sanitize label for safe filename
        safe_name = "".join(c for c in label if c.isalnum() or c in ("-", "_")).lower()
        return os.path.join(self.keystore_dir, f"{safe_name}.json")

    def save_wallet(
        self,
        wallet: Wallet,
        label: str,
        password: Optional[str] = None,
    ) -> str:
        """
        Saves a wallet to a local JSON keystore file.
        If a password is provided, the private key is strongly encrypted (AES-256 via PKCS#8).
        """
        filepath = self._get_wallet_path(label)
        is_encrypted = bool(password)

        private_key_pem = wallet.export_private_key_pem(password=password)

        keystore_record = {
            "label": label,
            "address": wallet.address,
            "public_key_pem": wallet.public_key_pem,
            "public_key_hex": wallet.public_key_hex,
            "is_encrypted": is_encrypted,
            "crypto_algorithm": "AES-256-CBC / PKCS#8" if is_encrypted else "Plain PKCS#8",
            "created_at": time.time(),
            "private_key_pem": private_key_pem,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(keystore_record, f, indent=2)

        return filepath

    def load_wallet(
        self,
        label: str,
        password: Optional[str] = None,
    ) -> Wallet:
        """
        Loads and decrypts a wallet from the keystore using its label or filepath.
        Raises ValueError if password is required but missing/invalid.
        """
        if os.path.isfile(label):
            filepath = label
        else:
            filepath = self._get_wallet_path(label)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Keystore file not found for label/path: '{label}'")

        with open(filepath, "r", encoding="utf-8") as f:
            record = json.load(f)

        if record.get("is_encrypted") and not password:
            raise ValueError(f"Wallet '{record.get('label')}' is password-protected. Password is required.")

        try:
            wallet = Wallet.from_private_key_pem(
                record["private_key_pem"],
                password=password,
            )
            # Verify derived address matches recorded address
            if wallet.address != record["address"]:
                raise ValueError("Address mismatch after private key decryption.")
            return wallet
        except Exception as e:
            if "bad decrypt" in str(e).lower() or "password" in str(e).lower() or isinstance(e, ValueError):
                raise ValueError("Incorrect password or corrupted keystore.") from e
            raise e

    def get_public_profile(self, label: str) -> Dict[str, Any]:
        """
        Retrieves the public address and public key without requiring a password.
        Safe for public registry lookup.
        """
        if os.path.isfile(label):
            filepath = label
        else:
            filepath = self._get_wallet_path(label)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Keystore file not found for label/path: '{label}'")

        with open(filepath, "r", encoding="utf-8") as f:
            record = json.load(f)

        return {
            "label": record["label"],
            "address": record["address"],
            "public_key_pem": record["public_key_pem"],
            "public_key_hex": record["public_key_hex"],
            "is_encrypted": record["is_encrypted"],
            "created_at": record["created_at"],
        }

    def list_wallets(self) -> List[Dict[str, Any]]:
        """
        Lists all wallets stored in the keystore directory with their public metadata.
        """
        wallets = []
        for filename in os.listdir(self.keystore_dir):
            if filename.endswith(".json"):
                full_path = os.path.join(self.keystore_dir, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        wallets.append({
                            "label": data.get("label", filename[:-5]),
                            "address": data.get("address"),
                            "is_encrypted": data.get("is_encrypted", False),
                            "file": filename,
                            "created_at": data.get("created_at"),
                        })
                except Exception:
                    continue
        return wallets

    def delete_wallet(self, label: str) -> bool:
        """Deletes a wallet from the keystore."""
        filepath = self._get_wallet_path(label)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
