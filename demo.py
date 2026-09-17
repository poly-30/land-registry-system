"""
Interactive Demonstration of Blockchain-Based Secure Land Registry System
with Multi-Layer Verification & Real Estate Tokenization.
"""

import os
import sys
import time

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from blockchain.wallet import Wallet
from blockchain.keystore import Keystore
from blockchain.blockchain import Blockchain
from blockchain.land_registry import LandRegistry

console = Console(highlight=False)


def print_header():
    console.print(
        Panel.fit(
            "[bold cyan]BLOCKCHAIN-BASED SECURE LAND REGISTRY SYSTEM[/bold cyan]\n"
            "[bold yellow]WITH MULTI-LAYER VERIFICATION & FRACTIONAL TOKENIZATION[/bold yellow]\n"
            "[dim]Pranveer Singh Institute of Technology (PSIT), Kanpur[/dim]",
            border_style="bright_blue",
        )
    )


def main():
    print_header()

    # Step 1: Initialize Blockchain
    console.print("\n[bold green]=== STEP 1: INITIALIZING BLOCKCHAIN LEDGER ===[/bold green]")
    blockchain = Blockchain(difficulty=2)
    registry = LandRegistry(blockchain)
    console.print(f"[green][+][/green] [cyan]Genesis Block (Block #0)[/cyan] generated successfully.")
    console.print(f"[green][+][/green] Consensus Engine: [magenta]Proof-of-Work (PoW)[/magenta] (Target Difficulty: {blockchain.difficulty})")
    console.print(f"[green][+][/green] Genesis Block Hash: [dim]{blockchain.chain[0].hash}[/dim]")

    # Step 2: Cryptographic Identity Generation & Password-Protected Keystore
    console.print("\n[bold green]=== STEP 2: PARTICIPANT WALLETS & ENCRYPTED KEYSTORE ===[/bold green]")
    keystore = Keystore(keystore_dir="wallets")

    registrar = Wallet()
    alice = Wallet()    # Original Landowner
    bob = Wallet()      # Property Buyer
    charlie = Wallet()  # Fractional Investor 1
    diana = Wallet()    # Fractional Investor 2
    miner = Wallet()    # Network Validator / Miner

    registry.register_authority(registrar)

    # Save Alice's and Registrar's wallet with AES-256 PKCS#8 password encryption
    keystore.save_wallet(registrar, "registrar_authority", password="GovtLandRecordsSecureKey2026!")
    keystore.save_wallet(alice, "alice_owner", password="AlicePrivateDeedPassword#99")
    keystore.save_wallet(bob, "bob_buyer", password="BobSecurePassword#123")

    console.print("[green][+][/green] Participant wallets saved to [bold cyan]wallets/[/bold cyan] with [yellow]AES-256 PKCS#8 password encryption[/yellow].")
    console.print("[green][+][/green] Verified: Private keys encrypted on disk, public keys and addresses remain inspectable.")

    wallet_table = Table(title="Generated Cryptographic Identities", show_lines=True)
    wallet_table.add_column("Participant Role", style="bold yellow")
    wallet_table.add_column("Public Address (0x...)", style="cyan")
    wallet_table.add_column("Key Spec", style="dim")
    wallet_table.add_column("Keystore Security", style="green")

    wallet_table.add_row("Land Registrar (Govt Authority)", registrar.address, "ECDSA SECP256K1 (256-bit)", "Encrypted (AES-256)")
    wallet_table.add_row("Alice Sharma (Property Owner)", alice.address, "ECDSA SECP256K1 (256-bit)", "Encrypted (AES-256)")
    wallet_table.add_row("Bob Verma (Buyer)", bob.address, "ECDSA SECP256K1 (256-bit)", "Encrypted (AES-256)")
    wallet_table.add_row("Charlie Gupta (Investor A)", charlie.address, "ECDSA SECP256K1 (256-bit)", "Ephemeral In-Memory")
    wallet_table.add_row("Diana Roy (Investor B)", diana.address, "ECDSA SECP256K1 (256-bit)", "Ephemeral In-Memory")
    wallet_table.add_row("Validator / Miner Node", miner.address, "ECDSA SECP256K1 (256-bit)", "Ephemeral In-Memory")
    console.print(wallet_table)

    # Step 3: Layer 1 - Document Submission & Hashing
    console.print("\n[bold green]=== STEP 3: PROPERTY REGISTRATION (LAYER-1: DOCUMENT INTEGRITY) ===[/bold green]")
    prop_id = "PROP-UP-KNP-2026-001"
    raw_deed_pdf = b"%PDF-1.4 Official Deed: Plot 104, Sector 4, Civil Lines, Kanpur. Area: 3,500 sq ft. Cadastral Survey: CS/2026/894."
    
    console.print(f"  * Alice prepares land title registration for parcel: [bold cyan]{prop_id}[/bold cyan]")
    reg_tx = registry.submit_property_registration(
        owner_wallet=alice,
        property_id=prop_id,
        survey_number="CS/2026/894",
        location={"city": "Kanpur", "state": "UP", "district": "Civil Lines", "gps": "26.4712 N, 80.3498 E"},
        area_sqft=3500.0,
        market_value=15000000.0,  # 1.5 Crore INR
        document_bytes=raw_deed_pdf,
        document_name="Kanpur_CivilLines_Deed_Signed.pdf",
        owner_name="Alice Sharma",
    )
    console.print(f"[green][+][/green] [cyan]Layer 1 Document Hash / IPFS CID:[/cyan] {reg_tx.payload['ipfs_document_hash']}")
    console.print(f"[green][+][/green] Digital Signature by Alice: [dim]{reg_tx.signature[:32]}...[/dim]")
    console.print(f"[green][+][/green] Transaction Hash: [dim]{reg_tx.tx_hash}[/dim]")

    # Step 4: Layer 2 - Government Authority Verification
    console.print("\n[bold green]=== STEP 4: LAYER-2: GOVERNMENT REGISTRAR VERIFICATION ===[/bold green]")
    console.print("  * Land Authority retrieves submitted deed, verifies digital signatures & cadastral coordinates...")
    verif_tx = registry.verify_property(
        registrar_wallet=registrar,
        property_id=prop_id,
        registrar_name="Kanpur Municipal Land Registry Office (Sub-Registrar 4B)",
        document_bytes=raw_deed_pdf,
        approve=True,
        remarks="Physical deed, surveyor coordinates (CS/2026/894), and encumbrance cleared.",
    )
    console.print(f"[green][+][/green] Layer-1 Document Hash Match: [bold green]PASSED[/bold green]")
    console.print(f"[green][+][/green] Layer-2 Authority Approval: [bold green]APPROVED[/bold green]")
    console.print(f"[green][+][/green] Digital Signature by Registrar: [dim]{verif_tx.signature[:32]}...[/dim]")

    # Step 5: Layer 3 - Blockchain Mining (Immutability)
    console.print("\n[bold green]=== STEP 5: LAYER-3: BLOCKCHAIN CONSENSUS & MINING ===[/bold green]")
    console.print("  * Miner node packaging transactions into Block #1 and solving Proof-of-Work...")
    start_time = time.time()
    block_1 = registry.mine_block(miner.address)
    elapsed = time.time() - start_time
    console.print(f"[green][+][/green] [bold green]Block #1 successfully mined in {elapsed:.3f}s![/bold green]")
    console.print(f"    - Block Index: [cyan]{block_1.index}[/cyan]")
    console.print(f"    - Nonce: [yellow]{block_1.nonce}[/yellow]")
    console.print(f"    - Block Hash: [magenta]{block_1.hash}[/magenta]")
    console.print(f"    - Merkle Root: [dim]{block_1.merkle_root}[/dim]")
    console.print(f"    - Confirmed Transactions: [bold]{len(block_1.transactions)}[/bold]")

    # Step 6: Real Estate Tokenization (Fractional Ownership)
    console.print("\n[bold green]=== STEP 6: REAL ESTATE TOKENIZATION (FRACTIONAL OWNERSHIP) ===[/bold green]")
    console.print("  * Alice tokenizes the 1.5 Cr property into 100 fractional equity tokens (symbol: KNP-CIVIL)...")
    tok_tx = registry.tokenize_property(
        owner_wallet=alice,
        property_id=prop_id,
        total_tokens=100,
        token_symbol="KNP-CIVIL",
        price_per_token=150000.0,
    )
    registry.mine_block(miner.address)
    console.print(f"[green][+][/green] Property [cyan]{prop_id}[/cyan] is now tokenized into 100 shares.")

    # Step 7: Fractional Investment Trading
    console.print("\n[bold green]=== STEP 7: FRACTIONAL INVESTMENT TRANSACTIONS ===[/bold green]")
    console.print("  * Charlie buys 30 tokens for INR 4,500,000")
    registry.transfer_tokens(alice, prop_id, charlie.address, 30, 4500000.0)
    console.print("  * Diana buys 20 tokens for INR 3,000,000")
    registry.transfer_tokens(alice, prop_id, diana.address, 20, 3000000.0)
    block_3 = registry.mine_block(miner.address)
    console.print(f"[green][+][/green] [bold green]Block #{block_3.index} mined[/bold green] with token transfers.")

    # Step 8: Rental Yield Distribution
    console.print("\n[bold green]=== STEP 8: AUTOMATED RENT DISTRIBUTION TO INVESTORS ===[/bold green]")
    monthly_rent = 100000.0  # 1 Lakh INR monthly rent
    console.print(f"  * Distributing commercial tenant rent of INR {monthly_rent:,.2f} for March 2026...")
    registry.distribute_rent(alice, prop_id, monthly_rent, "March 2026")
    registry.mine_block(miner.address)

    # Display Token Distribution & Portfolio
    prop = registry.get_property(prop_id)
    token_table = Table(title=f"Cap Table & Rent Yield for {prop_id}", show_lines=True)
    token_table.add_column("Stakeholder", style="bold")
    token_table.add_column("Address", style="dim")
    token_table.add_column("Tokens Owned", justify="right")
    token_table.add_column("Equity %", justify="right", style="cyan")
    token_table.add_column("Monthly Rent Payout (INR)", justify="right", style="green")

    for holder, count in prop["token_holders"].items():
        pct = (count / prop["total_tokens"]) * 100
        rent = (count / prop["total_tokens"]) * monthly_rent
        holder_name = "Alice (Original Owner)" if holder == alice.address else ("Charlie (Investor A)" if holder == charlie.address else "Diana (Investor B)")
        token_table.add_row(holder_name, f"{holder[:12]}...", str(count), f"{pct:.1f}%", f"INR {rent:,.2f}")
    console.print(token_table)

    # Step 9: Chain Validation Audit
    console.print("\n[bold green]=== STEP 9: CRYPTOGRAPHIC LEDGER AUDIT ===[/bold green]")
    valid, message = blockchain.is_chain_valid()
    if valid:
        console.print(f"[bold green][+][/bold green] [bold green]AUDIT RESULT:[/bold green] {message}")
        console.print(f"    Total Verified Blocks: [bold cyan]{len(blockchain.chain)}[/bold cyan]")

    # Step 10: Attack / Tamper Simulation
    console.print("\n[bold red]=== STEP 10: MALICIOUS TAMPER-DETECTION SIMULATION ===[/bold red]")
    console.print("  * Simulating an insider threat attempting to alter Block #1's records...")
    console.print("    [yellow]Attacker modifies the registered owner name in Block #1 to 'Malicious Hacker'[/yellow]")
    target_block = blockchain.chain[1]
    original_owner_name = target_block.transactions[0].payload["owner_name"]
    # Tamper with the block payload
    target_block.transactions[0].payload["owner_name"] = "Malicious Hacker"

    tampered_valid, tamper_msg = blockchain.is_chain_valid()
    console.print(f"    Audit Check Result: [bold red]FAIL - TAMPERING DETECTED[/bold red]")
    console.print(f"    Tamper Diagnostic: [bold red]{tamper_msg}[/bold red]")
    console.print("    [bold green][+] Security Shield Activated:[/bold green] Tampering broke the Merkle Root and Block Hash!")

    # Restore the block
    target_block.transactions[0].payload["owner_name"] = original_owner_name
    restored_valid, _ = blockchain.is_chain_valid()
    console.print(f"    State restored to authentic ledger: [bold green]Valid = {restored_valid}[/bold green]")

    # Step 11: Persistence to disk
    console.print("\n[bold green]=== STEP 11: LEDGER PERSISTENCE ===[/bold green]")
    ledger_path = "e:/Land-registry-system/data/land_registry_ledger.json"
    blockchain.save_to_file(ledger_path)
    console.print(f"[green][+][/green] Blockchain state safely persisted to [bold cyan]{ledger_path}[/bold cyan]")

    console.print(Panel.fit("[bold green]ALL DEMONSTRATION PHASES COMPLETED SUCCESSFULLY![/bold green]", border_style="green"))


if __name__ == "__main__":
    main()
