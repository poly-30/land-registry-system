# Blockchain-Based Secure Land Registry System with Multi-Layer Verification

An immutable, cryptographically secure blockchain engine developed in Python specifically tailored for decentralized land registry management, fractional real estate tokenization, and multi-layer title verification.

Based on the Project Synopsis for **B.Tech (Computer Science & Engineering - Cyber Security)** at **Pranveer Singh Institute of Technology (PSIT), Kanpur**.

---

## 🏗️ System Architecture & Multi-Layer Verification

The system enforces a **3-Layer Verification Model** to ensure that fraudulent entries, duplicate property sales, and fake ownership claims are prevented before and after being committed to the ledger:

```
+-----------------------------------------------------------------------------------+
|                        Layer 1: Document Integrity Verification                   |
|   - Land deed, survey coordinates, and cadastral maps hashed via SHA-256 / IPFS   |
|   - Unique Content Identifier (CID) bound to property registration request         |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                     Layer 2: Simulated Authority Verification                     |
|   - Authorized Government Land Registrar conducts physical and legal validation   |
|   - Registrar digitally signs an approval transaction using ECDSA SECP256K1       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                     Layer 3: Blockchain Immutability & Consensus                  |
|   - Transactions batched with Merkle Tree root calculation                        |
|   - Sealed via Proof-of-Work (PoW) consensus into cryptographic blocks            |
|   - Tamper-evident chaining: any past deed alteration breaks Merkle root & hash   |
+-----------------------------------------------------------------------------------+
```

---

## 🚀 Key Features

1. **Cryptographic Wallets & Identity**:
   - Asymmetric cryptography with **ECDSA SECP256K1** (the standard curve used in Bitcoin & Ethereum).
   - Generates unique public addresses (`0x...`) and digital signatures for buyers, sellers, and registrars.

2. **Tamper-Proof Merkle Trees**:
   - Computes binary Merkle trees over all transactions in each block.
   - Provides cryptographic proofs of inclusion and detects any payload alteration.

3. **Multi-Layer Property Registration**:
   - `REGISTER_PROPERTY`: Captures cadastral survey numbers, GIS coordinates, area (sq ft), market value, and IPFS document hashes.
   - `VERIFY_PROPERTY`: Enforces registrar authority digital signature before a title can be traded or tokenized.

4. **Fractional Real Estate Tokenization**:
   - Allows property owners to tokenize real estate into equity tokens (e.g., 100 shares).
   - `TRANSFER_TOKENS`: Enables fractional retail investment in high-value properties.
   - `DISTRIBUTE_RENT`: Automates dividend and rental yield distribution proportionally across token holders.

5. **Chain Audit & Tamper Detection**:
   - Re-verifies previous hash links, block header hashes, Proof-of-Work difficulty, and transaction signatures.
   - Instantly rejects blocks with corrupted or altered records.

6. **Password-Protected Keystore & Key Management**:
   - Stores user identities in `wallets/<label>.json` with **AES-256-CBC / PKCS#8** password encryption.
   - Decrypts private keys on demand for signing transactions while leaving public addresses and public keys inspectable.

7. **Ledger Persistence**:
   - Automatic save and load of blockchain ledger state to JSON disk storage (`data/land_registry_ledger.json`).

---

## 📁 Project Structure

```
Land-registry-system/
├── blockchain/
│   ├── __init__.py          # Package exports
│   ├── wallet.py            # ECDSA SECP256K1 wallet, signing & verification
│   ├── keystore.py          # Password-encrypted keystore & key persistence (AES-256)
│   ├── merkle.py            # Merkle Tree calculation & proofs
│   ├── transaction.py       # Domain transaction models & digital signatures
│   ├── block.py             # Block structure & Proof-of-Work mining
│   ├── blockchain.py        # Core blockchain engine, mempool & state machine
│   └── land_registry.py     # High-level 3-layer verification controller
├── wallets/                 # Encrypted participant keystore files
├── data/
│   └── land_registry_ledger.json # Persisted blockchain ledger
├── tests/
│   └── test_blockchain.py   # Comprehensive automated unit & integration tests
├── demo.py                  # End-to-end interactive CLI demonstration
├── requirements.txt         # Project dependencies
└── README.md                # System documentation
```

---

## 🛠️ Quick Start

### 1. Requirements & Setup

Ensure Python 3.10+ is installed. Install the dependencies:

```powershell
pip install -r requirements.txt
```

### 2. Run Automated Unit Tests

Execute the test suite covering wallet cryptography, Merkle trees, multi-layer verification, tokenization, persistence, and tamper-detection:

```powershell
python -m unittest discover -s tests
```

### 3. Run the Interactive Demonstration

Experience the full end-to-end simulation:

```powershell
python demo.py
```

---

## 📊 Modules Mapped to Synopsis

| Module from Synopsis | Python Implementation Reference |
| :--- | :--- |
| **User Authentication** | [`blockchain/wallet.py`](file:///e:/Land-registry-system/blockchain/wallet.py) (ECDSA public/private key pairs & addresses) |
| **Property Registration** | [`blockchain/transaction.py`](file:///e:/Land-registry-system/blockchain/transaction.py) (`REGISTER_PROPERTY` with IPFS hash) |
| **Ownership Verification** | [`blockchain/land_registry.py`](file:///e:/Land-registry-system/blockchain/land_registry.py) (Layer 1 doc check + Layer 2 registrar signature) |
| **Blockchain Consensus** | [`blockchain/block.py`](file:///e:/Land-registry-system/blockchain/block.py), [`blockchain/blockchain.py`](file:///e:/Land-registry-system/blockchain/blockchain.py) (PoW mining & Merkle trees) |
| **Tokenization** | [`blockchain/transaction.py`](file:///e:/Land-registry-system/blockchain/transaction.py) (`TOKENIZE_PROPERTY` fractional equity shares) |
| **Investment System** | [`blockchain/land_registry.py`](file:///e:/Land-registry-system/blockchain/land_registry.py) (`TRANSFER_TOKENS` portfolio management) |
| **Rent Distribution** | [`blockchain/transaction.py`](file:///e:/Land-registry-system/blockchain/transaction.py) (`DISTRIBUTE_RENT` proportional yield payouts) |
