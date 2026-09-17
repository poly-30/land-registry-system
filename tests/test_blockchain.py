"""
Automated Unit and Integration Tests for Land Registry Blockchain.
"""

import os
import unittest
from blockchain.wallet import Wallet
from blockchain.merkle import MerkleTree
from blockchain.transaction import (
    Transaction,
    TransactionType,
    PropertyRegistrationData,
)
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.land_registry import LandRegistry


class TestLandRegistryBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain(difficulty=2)
        self.registry = LandRegistry(self.blockchain)
        self.authority = Wallet()
        self.alice = Wallet()  # Owner
        self.bob = Wallet()    # Buyer
        self.charlie = Wallet() # Investor
        self.registry.register_authority(self.authority)

    def test_wallet_and_signatures(self):
        """Tests ECDSA key generation, address derivation, and signature verification."""
        self.assertTrue(self.alice.address.startswith("0x"))
        self.assertEqual(len(self.alice.address), 42)

        data = b"Land Registry Deed Authorization"
        signature = self.alice.sign(data)
        self.assertTrue(isinstance(signature, str))
        self.assertTrue(len(signature) > 0)

        # Valid verification
        valid = Wallet.verify(self.alice.public_key_pem, data, signature)
        self.assertTrue(valid)

        # Invalid verification (wrong message or wrong key)
        self.assertFalse(Wallet.verify(self.alice.public_key_pem, b"Tampered Message", signature))
        self.assertFalse(Wallet.verify(self.bob.public_key_pem, data, signature))

    def test_merkle_tree(self):
        """Tests Merkle tree root calculation and audit proofs."""
        leaves = ["hash1", "hash2", "hash3", "hash4"]
        tree = MerkleTree(leaves)
        self.assertIsNotNone(tree.root)
        self.assertEqual(len(tree.root), 64)

        # Proof generation for leaf 2
        proof = tree.get_proof(2)
        self.assertTrue(MerkleTree.verify_proof("hash3", proof, tree.root))

    def test_multi_layer_verification_and_mining(self):
        """Tests Layer 1 (document hash), Layer 2 (authority signing), Layer 3 (mining block)."""
        doc_content = b"Official Land Deed: Plot 42, Civil Lines, Kanpur. Survey: 104/A."
        prop_id = "PROP-KNP-001"

        # Alice submits registration (Layer 1)
        reg_tx = self.registry.submit_property_registration(
            owner_wallet=self.alice,
            property_id=prop_id,
            survey_number="104/A",
            location={"city": "Kanpur", "state": "UP", "zone": "Civil Lines"},
            area_sqft=2400.0,
            market_value=12000000.0,
            document_bytes=doc_content,
            document_name="deed_plot42.pdf",
            owner_name="Alice Sharma",
        )
        self.assertTrue(reg_tx.is_valid())

        # Authority verifies property (Layer 2)
        verif_tx = self.registry.verify_property(
            registrar_wallet=self.authority,
            property_id=prop_id,
            registrar_name="Kanpur Municipal Registrar",
            document_bytes=doc_content,
            approve=True,
        )
        self.assertTrue(verif_tx.is_valid())
        self.assertTrue(verif_tx.payload["layer_1_doc_verified"])
        self.assertTrue(verif_tx.payload["layer_2_authority_verified"])

        # Mine block (Layer 3)
        miner = Wallet()
        block = self.registry.mine_block(miner.address)
        self.assertIsNotNone(block)
        self.assertEqual(block.index, 1)
        self.assertTrue(block.hash.startswith("00"))

        # Verify property state on ledger
        prop = self.registry.get_property(prop_id)
        self.assertIsNotNone(prop)
        self.assertEqual(prop["verification_status"], "VERIFIED")
        self.assertEqual(prop["owner_address"], self.alice.address)

        # Entire chain must be valid
        is_valid, msg = self.blockchain.is_chain_valid()
        self.assertTrue(is_valid, msg)

    def test_fractional_tokenization_and_rent(self):
        """Tests tokenizing property, trading fractional tokens, and dividend distribution."""
        doc_content = b"Commercial Complex Deed, Mall Road, Kanpur"
        prop_id = "COMM-KNP-002"

        # Register and verify
        self.registry.submit_property_registration(
            owner_wallet=self.alice,
            property_id=prop_id,
            survey_number="55/B",
            location={"city": "Kanpur", "district": "Mall Road"},
            area_sqft=5000.0,
            market_value=50000000.0,
            document_bytes=doc_content,
            document_name="deed_mall_road.pdf",
            owner_name="Alice",
        )
        self.registry.verify_property(
            registrar_wallet=self.authority,
            property_id=prop_id,
            registrar_name="Mall Road Registrar",
            document_bytes=doc_content,
            approve=True,
        )
        self.registry.mine_block(self.authority.address)

        # Alice tokenizes into 100 shares
        self.registry.tokenize_property(
            owner_wallet=self.alice,
            property_id=prop_id,
            total_tokens=100,
            token_symbol="KNP-MALL",
            price_per_token=500000.0,
        )
        self.registry.mine_block(self.authority.address)

        prop = self.registry.get_property(prop_id)
        self.assertTrue(prop["tokenized"])
        self.assertEqual(prop["token_holders"][self.alice.address], 100)

        # Alice sells 30 tokens to Charlie
        self.registry.transfer_tokens(
            seller_wallet=self.alice,
            property_id=prop_id,
            buyer_address=self.charlie.address,
            token_count=30,
            total_amount=15000000.0,
        )
        self.registry.mine_block(self.authority.address)

        prop = self.registry.get_property(prop_id)
        self.assertEqual(prop["token_holders"][self.alice.address], 70)
        self.assertEqual(prop["token_holders"][self.charlie.address], 30)

        # Distribute rental yield of 100,000 INR
        self.registry.distribute_rent(
            payer_wallet=self.alice,
            property_id=prop_id,
            total_rent_amount=100000.0,
            period="March 2026",
        )
        self.registry.mine_block(self.authority.address)

        # Check Charlie's portfolio
        charlie_port = self.registry.get_user_portfolio(self.charlie.address)
        self.assertEqual(len(charlie_port["fractional_investments"]), 1)
        self.assertEqual(charlie_port["fractional_investments"][0]["tokens_held"], 30)
        self.assertEqual(charlie_port["fractional_investments"][0]["share_percentage"], "30.0%")

        # Ensure chain remains cryptographically sound
        is_valid, msg = self.blockchain.is_chain_valid()
        self.assertTrue(is_valid, msg)

    def test_tamper_detection(self):
        """Tests that any malicious alteration of a past block is instantly detected."""
        doc = b"Deed for Plot 99"
        prop_id = "PLOT-99"

        self.registry.submit_property_registration(
            owner_wallet=self.alice,
            property_id=prop_id,
            survey_number="99",
            location={"city": "Kanpur"},
            area_sqft=1000,
            market_value=1000000,
            document_bytes=doc,
            document_name="deed.pdf",
            owner_name="Alice",
        )
        self.registry.verify_property(self.authority, prop_id, "Registrar", doc, True)
        self.registry.mine_block(self.authority.address)

        is_valid, _ = self.blockchain.is_chain_valid()
        self.assertTrue(is_valid)

        # Attacker attempts to change the owner in block 1 transaction payload
        block_1 = self.blockchain.chain[1]
        attacker = Wallet()
        block_1.transactions[0].payload["owner_name"] = "Attacker Mallory"
        block_1.transactions[0].sender_address = attacker.address

        # Check chain validity: Merkle root mismatch or signature or hash mismatch must trigger failure
        is_valid, msg = self.blockchain.is_chain_valid()
        self.assertFalse(is_valid)
        self.assertTrue("Merkle Root mismatch" in msg or "signature" in msg or "mismatch" in msg)

    def test_persistence_save_and_load(self):
        """Tests blockchain persistence to disk and state reconstruction."""
        doc = b"Deed for Plot 100"
        prop_id = "PLOT-100"

        self.registry.submit_property_registration(
            owner_wallet=self.alice,
            property_id=prop_id,
            survey_number="100",
            location={"city": "Kanpur"},
            area_sqft=1500,
            market_value=2000000,
            document_bytes=doc,
            document_name="deed.pdf",
            owner_name="Alice",
        )
        self.registry.verify_property(self.authority, prop_id, "Registrar", doc, True)
        self.registry.mine_block(self.authority.address)

        test_file = "e:/Land-registry-system/data/test_ledger.json"
        self.blockchain.save_to_file(test_file)
        self.assertTrue(os.path.exists(test_file))

        # Load back
        loaded_bc = Blockchain.load_from_file(test_file)
        self.assertEqual(len(loaded_bc.chain), len(self.blockchain.chain))
        self.assertIn(prop_id, loaded_bc.state.properties)
        self.assertEqual(loaded_bc.state.properties[prop_id]["verification_status"], "VERIFIED")

        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
