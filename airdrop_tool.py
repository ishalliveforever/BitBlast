import requests

def fetch_ordinals(wallet_address):
    ordinals_endpoint = f"https://ordinals.gorillapool.io/api/wallet/{wallet_address}/ordinals"
    response = requests.get(ordinals_endpoint)
    if response.status_code == 200:
        return response.json()["ordinals"]
    else:
        raise Exception("Failed to fetch ordinals")

def transfer_ordinal(sender_wallet, recipient_wallet, ordinal_id):
    transfer_endpoint = "https://ordinals.gorillapool.io/api/ordinals/transfer"
    payload = {
        "sender_wallet": sender_wallet,
        "ordinal_id": ordinal_id,
        "recipient_wallet": recipient_wallet
    }
    response = requests.post(transfer_endpoint, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to transfer ordinal")

def airdrop_ordinals(wallet_address, recipients):
    ordinals = fetch_ordinals(wallet_address)
    
    for recipient in recipients:
        try:
            transfer_ordinal(wallet_address, recipient["wallet_address"], recipient["ordinal_id"])
            print(f"Successfully transferred ordinal {recipient['ordinal_id']} to {recipient['wallet_address']}")
        except Exception as e:
            print(f"Failed to transfer ordinal {recipient['ordinal_id']} to {recipient['wallet_address']}: {str(e)}")

# Example usage
wallet_address = "user_wallet_address"
recipients = [
    {"wallet_address": "recipient_wallet_1", "ordinal_id": "ordinal_id_1"},
    {"wallet_address": "recipient_wallet_2", "ordinal_id": "ordinal_id_2"}
]

airdrop_ordinals(wallet_address, recipients)
