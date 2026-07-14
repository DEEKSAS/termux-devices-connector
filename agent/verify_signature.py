from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys

def verify(pubkey_path, bundle_path, sig_path):
    with open(pubkey_path, 'rb') as f:
        pub = serialization.load_pem_public_key(f.read())
    with open(bundle_path, 'rb') as f:
        data = f.read()
    with open(sig_path, 'rb') as f:
        sig = f.read()
    try:
        pub.verify(sig, data, padding.PKCS1v15(), hashes.SHA256())
        return 0
    except Exception as e:
        print('verify failed:', e)
        return 2

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: verify_signature.py public.pem bundle.zip bundle.zip.sig')
        sys.exit(2)
    sys.exit(verify(sys.argv[1], sys.argv[2], sys.argv[3]))
