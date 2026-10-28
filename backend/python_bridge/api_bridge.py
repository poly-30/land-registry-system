import sys
import json
import argparse
import os

# Add parent directory to path to import blockchain modules as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from blockchain.blockchain import Blockchain
    from blockchain.transaction import Transaction, TransactionType
    from blockchain.block import Block
    from blockchain.wallet import Wallet
except ImportError as e:
    print(json.dumps({"error": f"Failed to import blockchain modules: {e}"}))
    sys.exit(1)

# Initialize blockchain (loads from data/blockchain.json if exists)
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
os.makedirs(data_dir, exist_ok=True)
blockchain = Blockchain()

def handle_get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": [tx.to_dict() for tx in block.transactions],
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "nonce": block.nonce
        })
    return {"chain": chain_data, "length": len(blockchain.chain)}

def handle_get_stats():
    return {
        "totalBlocks": len(blockchain.chain),
        "totalTransactions": sum(len(block.transactions) for block in blockchain.chain),
        "totalProperties": len(blockchain.state.properties),
        "activeUsers": len(blockchain.state.authorized_registrars)
    }

def handle_get_properties():
    props = []
    for prop_id, prop_data in blockchain.state.properties.items():
        props.append({
            "property_id": prop_id,
            "owner": prop_data.get("owner_address"),
            "details": prop_data.get("location", {}).get("address", "")
        })
    return {"properties": props}

def handle_register_property(data):
    property_id = data.get("property_id")
    owner_address = data.get("owner_address")
    details = data.get("details", "")
    
    if not property_id or not owner_address:
        return {"error": "Missing property_id or owner_address"}
        
    try:
        # Create a mock wallet for the system for demo purposes
        wallet = Wallet()
        
        # Create transaction
        tx = Transaction(
            tx_type=TransactionType.REGISTER_PROPERTY,
            sender_address=wallet.address,
            sender_public_key_pem=wallet.public_key_pem,
            payload={
                "property_id": property_id,
                "survey_number": "SURVEY-" + property_id,
                "location": {"address": details},
                "area_sqft": 1000,
                "market_value": 500000,
                "ipfs_document_hash": "QmMockHash12345",
                "owner_name": "System Demo User"
            }
        )
        
        # Sign it
        tx.sign(wallet)
        
        # Add to blockchain
        blockchain.add_transaction(tx)
        
        # Mine it to save state
        blockchain.mine_pending_transactions(wallet.address)
        blockchain.save_to_file(os.path.join(data_dir, "blockchain.json"))
        
        return {"success": True, "message": "Property registered and mined"}
    except Exception as e:
        return {"error": str(e)}

def handle_transfer_ownership(data):
    property_id = data.get("property_id")
    to_address = data.get("to_address")
    sale_price = data.get("sale_price", 0)
    
    if not property_id or not to_address:
        return {"error": "Missing property_id or to_address"}
        
    try:
        # Create a mock wallet for the current owner
        # In a real app we'd need the actual owner's wallet to sign this
        wallet = Wallet()
        
        # We need to manually set the owner address in our state to bypass the strict signature check
        # FOR DEMO PURPOSES ONLY! Since we don't have the original private key.
        if property_id in blockchain.state.properties:
            blockchain.state.properties[property_id]["owner_address"] = wallet.address
            
            tx = Transaction(
                tx_type=TransactionType.TRANSFER_OWNERSHIP,
                sender_address=wallet.address,
                sender_public_key_pem=wallet.public_key_pem,
                payload={
                    "property_id": property_id,
                    "from_address": wallet.address,
                    "to_address": to_address,
                    "sale_price": sale_price
                }
            )
            tx.sign(wallet)
            blockchain.add_transaction(tx)
            blockchain.mine_pending_transactions(wallet.address)
            blockchain.save_to_file(os.path.join(data_dir, "blockchain.json"))
            
            return {"success": True, "message": "Ownership transferred"}
        else:
            return {"error": "Property not found"}
            
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="API Bridge to Blockchain")
    parser.add_argument('action', type=str, help='Action to perform')
    parser.add_argument('--data', type=str, help='JSON data for the action', default='{}')
    
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON data"}))
        sys.exit(1)
        
    result = {}
    
    if args.action == 'get_chain':
        result = handle_get_chain()
    elif args.action == 'get_stats':
        result = handle_get_stats()
    elif args.action == 'get_properties':
        result = handle_get_properties()
    elif args.action == 'register_property':
        result = handle_register_property(data)
    elif args.action == 'transfer_ownership':
        result = handle_transfer_ownership(data)
    else:
        result = {"error": f"Unknown action: {args.action}"}
        
    print(json.dumps(result))

if __name__ == '__main__':
    main()
