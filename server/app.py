from flask import Flask, request, jsonify
import os
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

APP_SECRET = 'change-me-for-prod'
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), '..', 'signing', 'keys', 'public.pem')
RECEIVE_DIR = os.path.join(os.path.dirname(__file__), 'received')

os.makedirs(RECEIVE_DIR, exist_ok=True)

app = Flask(__name__)

def load_public_key(path=PUBLIC_KEY_PATH):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())

@app.route('/submit', methods=['POST'])
def submit_bundle():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return jsonify({'error':'missing auth'}), 401
    token = auth.split(' ',1)[1]
    try:
        jwt.decode(token, APP_SECRET, algorithms=['HS256'])
    except Exception as e:
        return jsonify({'error':'invalid token', 'detail': str(e)}), 401

    if 'bundle' not in request.files or 'signature' not in request.form:
        return jsonify({'error':'missing bundle or signature'}), 400

    bundle = request.files['bundle'].read()
    signature = bytes.fromhex(request.form['signature'])

    pub = load_public_key()
    try:
        pub.verify(
            signature,
            bundle,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception as e:
        return jsonify({'error':'signature invalid', 'detail': str(e)}), 400

    # Save bundle
    idx = len(os.listdir(RECEIVE_DIR)) + 1
    path = os.path.join(RECEIVE_DIR, f'bundle_{idx}.zip')
    with open(path, 'wb') as f:
        f.write(bundle)

    return jsonify({'status':'accepted', 'path': path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
