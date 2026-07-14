from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def main():
    priv = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    priv_pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()
    )
    pub_pem = priv.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('private.pem', 'wb') as f:
        f.write(priv_pem)
    with open('public.pem', 'wb') as f:
        f.write(pub_pem)
    print('Wrote private.pem and public.pem')

if __name__ == '__main__':
    main()
