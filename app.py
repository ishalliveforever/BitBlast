from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

def fetch_ordinals(wallet_address):
    ordinals_endpoint = f"https://ordinals.gorillapool.io/api/wallet/{wallet_address}/ordinals"
    response = requests.get(ordinals_endpoint)
    if response.status_code == 200:
        return response.json()["ordinals"]
    else:
        raise Exception("Failed to fetch ordinals")

def fetch_ordinals_by_collection(collection_id):
    ordinals_endpoint = f"https://ordinals.gorillapool.io/api/collections/{collection_id}/holders"
    logging.debug(f"Fetching ordinals from: {ordinals_endpoint}")
    response = requests.get(ordinals_endpoint)
    logging.debug(f"Response status code: {response.status_code}")
    logging.debug(f"Response content: {response.content}")
    if response.status_code == 200:
        return response.json()["holders"]
    else:
        raise Exception(f"Failed to fetch ordinals by collection ID: {response.content}")

def transfer_ordinal(sender_wallet, recipient_wallet, ordinal_id, password):
    transfer_endpoint = "https://ordinals.gorillapool.io/api/ordinals/transfer"
    payload = {
        "sender_wallet": sender_wallet,
        "ordinal_id": ordinal_id,
        "recipient_wallet": recipient_wallet,
        "password": password  # Include the password in the payload
    }
    response = requests.post(transfer_endpoint, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to transfer ordinal")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_ordinals', methods=['GET'])
def fetch_ordinals_route():
    collection_id = request.args.get('collection_id')
    try:
        ordinals = fetch_ordinals_by_collection(collection_id)
        return jsonify(ordinals), 200
    except Exception as e:
        logging.error(f"Error fetching ordinals: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/airdrop', methods=['POST'])
def airdrop_ordinals():
    data = request.json
    wallet_address = data['wallet_address']
    recipients = data['recipients']
    password = data['password']  # Receive the password from the request
    
    for recipient in recipients:
        try:
            transfer_ordinal(wallet_address, recipient["wallet_address"], recipient["ordinal_id"], password)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
