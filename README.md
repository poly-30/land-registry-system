# Blockchain-Based Secure Land Registry System with Multi-Layer Verification

An immutable, cryptographically secure blockchain engine developed in Python specifically tailored for decentralized land registry management, fractional real estate tokenization, and multi-layer title verification — with a full-stack web application (React + Express.js) and an interactive CLI demo.

**B.Tech (Computer Science & Engineering — Cyber Security)**
**Pranveer Singh Institute of Technology (PSIT), Kanpur**

---

## 📋 Table of Contents

- [System Architecture](#-system-architecture--multi-layer-verification)
- [Technology Stack](#-technology-stack)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [How to Access & Run](#-how-to-access--run)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Modules Mapped to Synopsis](#-modules-mapped-to-synopsis)

---

## 🏗️ System Architecture & Multi-Layer Verification

The system enforces a **3-Layer Verification Model** to prevent fraudulent entries, duplicate property sales, and fake ownership claims:

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

### Full-Stack Architecture

```
┌─────────────────────────────────┐
│   React + Vite Frontend         │  http://localhost:5173
│   (Tailwind CSS, Lucide Icons)  │
└──────────────┬──────────────────┘
               │  REST API (Vite dev proxy → /api)
┌──────────────▼──────────────────┐
│   Express.js Backend            │  http://localhost:8000
│   (JWT Auth, MongoDB, CORS)     │
└──────────────┬──────────────────┘
               │  child_process.spawn (JSON over stdout)
┌──────────────▼──────────────────┐
│   Python Blockchain Engine      │  api_bridge.py
│   (ECDSA, Merkle, PoW, State)  │
└─────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Blockchain Core (Python)

| Technology | Version | Purpose |
|:---|:---|:---|
| **Python** | 3.10+ | Core language for blockchain engine |
| **cryptography** | ≥ 41.0.0 | ECDSA SECP256K1 elliptic curve key pairs, digital signatures (DER), AES-256-CBC / PKCS#8 password encryption |
| **hashlib (stdlib)** | — | SHA-256 hashing for block headers, Merkle trees, transaction hashes, and address derivation |
| **rich** | ≥ 13.0.0 | Terminal formatting, tables, and panels for the interactive CLI demo |

### Backend (Node.js)

| Technology | Version | Purpose |
|:---|:---|:---|
| **Node.js** | 18+ | JavaScript runtime for the REST API server |
| **Express.js** | ^4.19.2 | Web framework for REST API routing |
| **MongoDB** | 6+ | NoSQL database for user accounts and authentication |
| **Mongoose** | ^8.4.0 | MongoDB ODM for schema definitions and queries |
| **JSON Web Token (jsonwebtoken)** | ^9.0.2 | JWT-based stateless authentication |
| **bcrypt** | ^5.1.0 | Secure password hashing with salt rounds |
| **cors** | ^2.8.5 | Cross-Origin Resource Sharing middleware |
| **dotenv** | ^16.4.5 | Environment variable management |
| **nodemon** | ^3.1.4 | Dev server auto-restart on file changes |

### Frontend (React)

| Technology | Version | Purpose |
|:---|:---|:---|
| **React** | ^18.3.1 | Component-based UI library |
| **React Router DOM** | ^6.23.1 | Client-side routing (Home, Dashboard, Properties, Marketplace) |
| **Vite** | ^5.4.1 | Next-gen frontend build tool and dev server with HMR |
| **Tailwind CSS** | ^3.4.10 | Utility-first CSS framework for responsive styling |
| **PostCSS** | ^8.4.41 | CSS transformation pipeline (used with Tailwind) |
| **Autoprefixer** | ^10.4.20 | Automatic vendor prefixing for CSS |
| **Axios** | ^1.7.2 | HTTP client for API calls |
| **Lucide React** | ^0.378.0 | Modern icon library (Shield, Lock, Globe, etc.) |
| **ESLint** | ^9.9.0 | JavaScript/React code linting |

### Cryptographic Standards

| Standard | Usage |
|:---|:---|
| **ECDSA SECP256K1** | Asymmetric key pairs and digital signatures (same curve as Bitcoin & Ethereum) |
| **SHA-256** | Block hashing, Merkle tree construction, transaction hashing, address derivation |
| **AES-256-CBC** | Private key encryption at rest (via PKCS#8) |
| **PKCS#8** | Private key serialization format (with optional password encryption) |
| **DER Encoding** | Digital signature binary format |
| **PEM Encoding** | Public/private key interchange format |

---

## 🚀 Key Features

1. **Cryptographic Wallets & Identity** — Asymmetric ECDSA SECP256K1 key pairs with `0x…` Ethereum-styled addresses.
2. **Tamper-Proof Merkle Trees** — Binary Merkle trees with SHA-256, inclusion proofs, and root integrity verification.
3. **Multi-Layer Property Registration** — `REGISTER_PROPERTY` captures GIS coordinates, cadastral survey numbers, area, market value, and IPFS document hashes.
4. **Government Authority Verification** — `VERIFY_PROPERTY` enforces registrar digital signature before any trade or tokenization.
5. **Fractional Real Estate Tokenization** — `TOKENIZE_PROPERTY` splits equity into fractional shares (e.g., 100 tokens).
6. **Token Trading** — `TRANSFER_TOKENS` enables fractional retail investment in high-value properties.
7. **Automated Rent Distribution** — `DISTRIBUTE_RENT` disburses rental yields proportionally across all token holders.
8. **Chain Audit & Tamper Detection** — Re-verifies hash links, PoW difficulty, Merkle roots, and transaction signatures.
9. **Password-Protected Keystore** — AES-256-CBC / PKCS#8 encrypted wallet files in `wallets/`.
10. **Ledger Persistence** — Blockchain state serialized to JSON on disk.
11. **Web Dashboard & Marketplace** — React-based UI for property browsing, statistics, and ownership transfers.
12. **JWT Authentication** — Secure user registration and login with bcrypt password hashing.

---

## 📁 Project Structure

```
Land-registry-system/
│
├── blockchain/                          # Python Blockchain Engine
│   ├── __init__.py                      # Package exports
│   ├── wallet.py                        # SECP256K1 ECDSA wallet, addresses & signatures
│   ├── keystore.py                      # AES-256 password-encrypted keystore manager
│   ├── merkle.py                        # Binary Merkle Tree & audit proofs
│   ├── transaction.py                   # Domain transaction models & digital signatures
│   ├── block.py                         # Block structure & Proof-of-Work mining
│   ├── blockchain.py                    # Core blockchain engine, mempool & state machine
│   └── land_registry.py                 # 3-Layer Verification & tokenization controller
│
├── backend/                             # Node.js Express API Server
│   ├── src/
│   │   ├── index.js                     # Express app entry point
│   │   ├── middleware/
│   │   │   └── auth.js                  # JWT authentication middleware
│   │   ├── models/
│   │   │   └── User.js                  # Mongoose user schema (email, password, role, wallet)
│   │   ├── routes/
│   │   │   ├── auth.js                  # POST /api/auth/register, POST /api/auth/login
│   │   │   ├── properties.js            # GET /api/properties, POST /api/properties/register
│   │   │   ├── transactions.js          # POST /api/transactions/transfer
│   │   │   ├── blockchain.js            # GET /api/blockchain/chain
│   │   │   └── dashboard.js             # GET /api/dashboard/stats
│   │   └── utils/
│   │       └── pythonBridge.js          # Spawns Python blockchain bridge as child process
│   ├── python_bridge/
│   │   └── api_bridge.py                # Python CLI that executes blockchain actions
│   ├── .env                             # Environment variables (ports, MongoDB URI, JWT secret)
│   ├── package.json                     # Node.js dependencies
│   └── requirements.txt                 # Python dependencies for backend bridge
│
├── frontend/                            # React + Vite Frontend
│   ├── src/
│   │   ├── main.jsx                     # React app entry point with BrowserRouter
│   │   ├── App.jsx                      # Root component with navbar & route definitions
│   │   ├── index.css                    # Global styles (Tailwind directives)
│   │   └── pages/
│   │       ├── Home.jsx                 # Landing page with hero section & feature cards
│   │       ├── Dashboard.jsx            # Blockchain stats dashboard (blocks, transactions, users)
│   │       ├── Properties.jsx           # Registered property listing with search
│   │       └── Marketplace.jsx          # Buy/sell property transfer forms
│   ├── index.html                       # HTML entry point
│   ├── vite.config.js                   # Vite config with API proxy to backend
│   ├── tailwind.config.js               # Tailwind CSS configuration
│   ├── postcss.config.js                # PostCSS plugins
│   └── package.json                     # Frontend dependencies
│
├── data/
│   └── land_registry_ledger.json        # Persisted blockchain ledger (auto-generated)
│
├── wallets/                             # Encrypted participant keystore files
│   ├── alice_owner.json                 # Alice's AES-256 encrypted wallet
│   ├── bob_buyer.json                   # Bob's AES-256 encrypted wallet
│   └── registrar_authority.json         # Registrar's AES-256 encrypted wallet
│
├── tests/
│   ├── test_blockchain.py               # 6 unit tests (blockchain, verification, tokenization)
│   └── test_keystore.py                 # 5 unit tests (keystore encryption & management)
│
├── demo.py                              # End-to-end interactive CLI demonstration
├── requirements.txt                     # Python dependencies (cryptography, rich)
├── PROJECT_SUMMARY.txt                  # Comprehensive project documentation
└── README.md                            # This file
```

---

## ✅ Prerequisites

Before running the project, ensure the following are installed on your machine:

| Software | Required Version | Download |
|:---|:---|:---|
| **Python** | 3.10 or higher | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18 or higher | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ (bundled with Node.js) | Included with Node.js |
| **MongoDB** | 6.0 or higher | [mongodb.com](https://www.mongodb.com/try/download/community) |
| **Git** | Any recent version | [git-scm.com](https://git-scm.com/) |

> **Windows Users:** Ensure Python and Node.js are added to your system `PATH` during installation.

---

## 📦 Installation & Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/your-username/Land-registry-system.git
cd Land-registry-system
```

### 2. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `cryptography` — ECDSA SECP256K1 keys, AES-256 encryption
- `rich` — Terminal formatting for the CLI demo

### 3. Install Backend Dependencies

```powershell
cd backend
npm install
cd ..
```

### 4. Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

### 5. Configure Environment Variables

The backend ships with a pre-configured `.env` file at `backend/.env`:

```env
PORT=8000
MONGODB_URI=mongodb://localhost:27017/land_registry
JWT_SECRET=supersecretkey
JWT_EXPIRES_IN=30m
FRONTEND_URL=http://localhost:5173
PYTHON_BRIDGE_PATH=../python_bridge/api_bridge.py
```

> **Important:** Ensure MongoDB is running on `localhost:27017` before starting the backend. Update `MONGODB_URI` if your MongoDB instance uses a different host or port.

### 6. Start MongoDB

```powershell
# If MongoDB is installed as a Windows service, it starts automatically.
# Otherwise, start it manually:
mongod --dbpath "C:\data\db"
```

---

## 🖥️ How to Access & Run

### Option A: Run the Full Web Application (Frontend + Backend + Blockchain)

Open **three separate terminals** from the project root:

**Terminal 1 — Start the Backend API Server (Port 8000):**

```powershell
cd backend
npm run dev
```

You should see:
```
MongoDB connected
Server running on port 8000
```

**Terminal 2 — Start the Frontend Dev Server (Port 5173):**

```powershell
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
```

**Terminal 3 — (Optional) Run the CLI Demo:**

```powershell
python demo.py
```

**Access the Web Application:**

| Page | URL | Description |
|:---|:---|:---|
| **Home** | [http://localhost:5173/](http://localhost:5173/) | Landing page with hero section and feature overview |
| **Dashboard** | [http://localhost:5173/dashboard](http://localhost:5173/dashboard) | Blockchain statistics (total blocks, transactions, properties, users) |
| **Properties** | [http://localhost:5173/properties](http://localhost:5173/properties) | Browse all registered properties on the blockchain |
| **Marketplace** | [http://localhost:5173/marketplace](http://localhost:5173/marketplace) | Buy properties or transfer ownership to another address |
| **Login** | [http://localhost:5173/login](http://localhost:5173/login) | User authentication (register/login) |

### Option B: Run Only the Python Blockchain (CLI Demo)

No MongoDB, Node.js, or frontend required — just Python:

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Run the full interactive demonstration
python demo.py
```

The demo walks through all 11 phases:
1. Blockchain initialization with Genesis Block
2. Cryptographic wallet generation & AES-256 keystore encryption
3. Property registration with IPFS document hashing (Layer 1)
4. Government registrar verification and signing (Layer 2)
5. Proof-of-Work mining into immutable blocks (Layer 3)
6. Real estate tokenization into 100 fractional shares
7. Fractional token trading between investors
8. Automated proportional rent/dividend distribution
9. Full cryptographic chain audit
10. Malicious tamper-detection simulation (and recovery)
11. Ledger persistence to `data/land_registry_ledger.json`

### Option C: Inspect Persisted Data

After running the demo or the web app, you can inspect the saved state:

```powershell
# View the persisted blockchain ledger (JSON)
notepad data\land_registry_ledger.json

# View encrypted wallet keystore files
notepad wallets\alice_owner.json
notepad wallets\bob_buyer.json
notepad wallets\registrar_authority.json
```

---

## 🔌 API Endpoints

The Express.js backend exposes the following REST endpoints (all prefixed with `/api`):

### Authentication

| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `POST` | `/api/auth/register` | — | Register a new user (`email`, `password`) |
| `POST` | `/api/auth/login` | — | Login and receive a JWT (`email`, `password`) |

### Properties

| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/properties` | — | List all registered properties from the blockchain |
| `POST` | `/api/properties/register` | JWT | Register a new property (`property_id`, `details`) |

### Transactions

| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `POST` | `/api/transactions/transfer` | — | Transfer property ownership (`property_id`, `to_address`, `sale_price`) |

### Blockchain

| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/blockchain/chain` | — | Fetch the full blockchain (all blocks and transactions) |

### Dashboard

| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/dashboard/stats` | — | Get blockchain statistics (blocks, transactions, properties, users) |

> **Authentication:** Protected endpoints require a JWT token in the `Authorization: Bearer <token>` header, obtained from the login endpoint.

---

## 🧪 Testing

### Run All Tests

```powershell
python -m unittest discover -s tests -v
```

### Expected Output (11/11 passing)

```
test_wallet_and_signatures ... ok
test_merkle_tree ... ok
test_multi_layer_verification_and_mining ... ok
test_fractional_tokenization_and_rent ... ok
test_tamper_detection ... ok
test_persistence_save_and_load ... ok
test_save_and_load_unencrypted_wallet ... ok
test_save_and_load_password_encrypted_wallet ... ok
test_load_encrypted_wallet_wrong_or_missing_password ... ok
test_public_profile_without_password ... ok
test_list_and_delete_wallets ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.191s

OK
```

### What the Tests Cover

| Test File | Tests | Coverage |
|:---|:---|:---|
| `tests/test_blockchain.py` | 6 | Wallet crypto, Merkle trees, 3-layer verification, tokenization, rent distribution, tamper detection, ledger persistence |
| `tests/test_keystore.py` | 5 | Unencrypted wallet save/load, AES-256 encrypted wallet, wrong/missing password rejection, public profile access, wallet listing & deletion |

---

## 📊 Modules Mapped to Synopsis

| Module from Synopsis | Implementation Reference |
|:---|:---|
| **User Authentication** | `blockchain/wallet.py` (ECDSA key pairs & addresses) + `backend/src/routes/auth.js` (JWT login) |
| **Property Registration** | `blockchain/transaction.py` (`REGISTER_PROPERTY` with IPFS hash) |
| **Ownership Verification** | `blockchain/land_registry.py` (Layer 1 doc check + Layer 2 registrar signature) |
| **Blockchain Consensus** | `blockchain/block.py`, `blockchain/blockchain.py` (PoW mining & Merkle trees) |
| **Tokenization** | `blockchain/transaction.py` (`TOKENIZE_PROPERTY` fractional equity shares) |
| **Investment System** | `blockchain/land_registry.py` (`TRANSFER_TOKENS` portfolio management) |
| **Rent Distribution** | `blockchain/transaction.py` (`DISTRIBUTE_RENT` proportional yield payouts) |
| **Web Interface** | `frontend/src/pages/` (React components for Dashboard, Properties, Marketplace) |
| **REST API** | `backend/src/routes/` (Express.js endpoints bridging to Python blockchain) |
| **User Management** | `backend/src/models/User.js` (MongoDB schema with bcrypt password hashing) |

---

## 📄 License

This project was developed as an academic capstone project at **Pranveer Singh Institute of Technology (PSIT), Kanpur** for the **B.Tech CSE (Cyber Security)** program.

---

© 2026 Land Registry Blockchain System. All rights reserved.
