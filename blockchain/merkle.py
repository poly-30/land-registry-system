"""
Merkle Tree implementation for transaction integrity validation in blocks.
"""

import hashlib
from typing import List, Tuple, Optional


def sha256d(data: bytes) -> str:
    """Computes SHA-256 hash of byte data and returns hex string."""
    return hashlib.sha256(data).hexdigest()


class MerkleTree:
    """
    Constructs a binary Merkle Tree over a list of transaction hashes.
    Ensures cryptographic tamper-proof validation of transactions inside a block.
    """

    def __init__(self, leaves: Optional[List[str]] = None):
        self.leaves: List[str] = leaves or []
        self.levels: List[List[str]] = []
        if self.leaves:
            self._build_tree()

    def _build_tree(self) -> None:
        """Constructs the Merkle tree levels from leaves to root."""
        current_level = self.leaves[:]
        self.levels = [current_level]

        while len(current_level) > 1:
            next_level: List[str] = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # Duplicate last element if odd number of nodes
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = left + right
                parent = sha256d(combined.encode("utf-8"))
                next_level.append(parent)
            self.levels.append(next_level)
            current_level = next_level

    @property
    def root(self) -> str:
        """Returns the Merkle root hash, or 64 zeros if tree is empty."""
        if not self.levels or not self.levels[-1]:
            return "0" * 64
        return self.levels[-1][0]

    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """
        Generates an audit proof for a leaf at the given index.
        Returns list of (sibling_hash, 'left'|'right').
        """
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise IndexError("Leaf index out of bounds")

        proof = []
        idx = leaf_index
        for level in self.levels[:-1]:
            is_right_child = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right_child else idx + 1
            if sibling_idx >= len(level):
                sibling_idx = idx  # Paired with itself

            sibling_hash = level[sibling_idx]
            position = "left" if is_right_child else "right"
            proof.append((sibling_hash, position))
            idx //= 2
        return proof

    @staticmethod
    def verify_proof(leaf_hash: str, proof: List[Tuple[str, str]], root: str) -> bool:
        """
        Verifies whether a leaf_hash belongs to the Merkle tree with the given root.
        """
        current = leaf_hash
        for sibling_hash, position in proof:
            if position == "left":
                combined = sibling_hash + current
            else:
                combined = current + sibling_hash
            current = sha256d(combined.encode("utf-8"))
        return current == root
