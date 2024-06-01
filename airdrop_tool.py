import requests

# Function to fetch ordinals for a given wallet address
def fetch_ordinals(wallet_address):
    ordinals_endpoint = f"https://ordinals.gorillapool.io/api/wallet/{wallet_address}/ordinals"
    print(f"Fetching ordinals from: {ordinals_endpoint}")  # Debugging info
    response = requests.get(ordinals_endpoint)
    if response.status_code == 200:
        print(f"Successfully fetched ordinals for wallet: {wallet_address}")  # Debugging info
        return response.json()["ordinals"]
    else:
        raise Exception("Failed to fetch ordinals")

# Function to transfer an ordinal from sender to recipient
def transfer_ordinal(sender_wallet, recipient_wallet, ordinal_id):
    transfer_endpoint = "https://ordinals.gorillapool.io/api/ordinals/transfer"
    payload = {
        "sender_wallet": sender_wallet,
        "ordinal_id": ordinal_id,
        "recipient_wallet": recipient_wallet
    }
    print(f"Transferring ordinal {ordinal_id} from {sender_wallet} to {recipient_wallet}")  # Debugging info
    response = requests.post(transfer_endpoint, json=payload)
    if response.status_code == 200:
        print(f"Successfully transferred ordinal {ordinal_id} to {recipient_wallet}")  # Debugging info
        return response.json()
    else:
        raise Exception("Failed to transfer ordinal")

# Function to airdrop ordinals to a list of recipients
def airdrop_ordinals(wallet_address, recipients):
    print(f"Starting airdrop from wallet: {wallet_address} to recipients")  # Debugging info
    ordinals = fetch_ordinals(wallet_address)
    
    for recipient in recipients:
        try:
            transfer_ordinal(wallet_address, recipient["wallet_address"], recipient["ordinal_id"])
            print(f"Successfully transferred ordinal {recipient['ordinal_id']} to {recipient['wallet_address']}")  # Debugging info
        except Exception as e:
            print(f"Failed to transfer ordinal {recipient['ordinal_id']} to {recipient['wallet_address']}: {str(e)}")  # Debugging info

# Example usage
wallet_address = "user_wallet_address"
recipients = [
    {"wallet_address": "recipient_wallet_1", "ordinal_id": "ordinal_id_1"},
    {"wallet_address": "recipient_wallet_2", "ordinal_id": "ordinal_id_2"}
]

airdrop_ordinals(wallet_address, recipients)
