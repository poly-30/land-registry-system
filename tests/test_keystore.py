"""
Unit tests for Keystore and Key Management Module.
"""

import os
import shutil
import unittest
from blockchain.wallet import Wallet
from blockchain.keystore import Keystore


class TestKeystore(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests/test_wallets"
        self.keystore = Keystore(keystore_dir=self.test_dir)
        self.wallet = Wallet()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_unencrypted_wallet(self):
        """Tests saving and loading an unencrypted wallet."""
        label = "test_unencrypted"
        filepath = self.keystore.save_wallet(self.wallet, label)
        self.assertTrue(os.path.exists(filepath))

        loaded = self.keystore.load_wallet(label)
        self.assertEqual(loaded.address, self.wallet.address)
        self.assertEqual(loaded.public_key_hex, self.wallet.public_key_hex)

    def test_save_and_load_password_encrypted_wallet(self):
        """Tests saving and loading a wallet encrypted with AES-256 / PKCS#8 password."""
        label = "alice_secure"
        password = "SuperSecretPassword123!"

        filepath = self.keystore.save_wallet(self.wallet, label, password=password)
        self.assertTrue(os.path.exists(filepath))

        # Successfully load with correct password
        loaded = self.keystore.load_wallet(label, password=password)
        self.assertEqual(loaded.address, self.wallet.address)
        self.assertEqual(loaded.public_key_hex, self.wallet.public_key_hex)

        # Signing with decrypted wallet works identically
        data = b"Verify deed signature"
        sig1 = self.wallet.sign(data)
        sig2 = loaded.sign(data)
        self.assertTrue(Wallet.verify(loaded.public_key_pem, data, sig1))
        self.assertTrue(Wallet.verify(self.wallet.public_key_pem, data, sig2))

    def test_load_encrypted_wallet_wrong_or_missing_password(self):
        """Tests that loading with missing or wrong password fails securely."""
        label = "bob_secure"
        password = "CorrectPassword456"
        self.keystore.save_wallet(self.wallet, label, password=password)

        # Missing password
        with self.assertRaises(ValueError):
            self.keystore.load_wallet(label)

        # Wrong password
        with self.assertRaises(ValueError):
            self.keystore.load_wallet(label, password="WrongPassword!")

    def test_public_profile_without_password(self):
        """Tests that public info (address & public key) can be read without password."""
        label = "registrar_public"
        self.keystore.save_wallet(self.wallet, label, password="SecretPassword")

        profile = self.keystore.get_public_profile(label)
        self.assertEqual(profile["address"], self.wallet.address)
        self.assertEqual(profile["public_key_pem"], self.wallet.public_key_pem)
        self.assertTrue(profile["is_encrypted"])

    def test_list_and_delete_wallets(self):
        """Tests listing available wallets and deleting one."""
        self.keystore.save_wallet(Wallet(), "wallet_1")
        self.keystore.save_wallet(Wallet(), "wallet_2", password="pwd")

        wallets = self.keystore.list_wallets()
        self.assertEqual(len(wallets), 2)
        labels = [w["label"] for w in wallets]
        self.assertIn("wallet_1", labels)
        self.assertIn("wallet_2", labels)

        # Delete wallet_1
        self.assertTrue(self.keystore.delete_wallet("wallet_1"))
        self.assertEqual(len(self.keystore.list_wallets()), 1)


if __name__ == "__main__":
    unittest.main()
