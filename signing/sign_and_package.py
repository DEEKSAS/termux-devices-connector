import zipfile
import argparse
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def package_dir(src_dir, out_zip):
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src_dir):
            for fn in files:
                full = os.path.join(root, fn)
                arc = os.path.relpath(full, src_dir)
                z.write(full, arc)

def sign_file(private_key_path, file_path, out_sig):
    with open(private_key_path, 'rb') as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(file_path, 'rb') as f:
        data = f.read()
    sig = priv.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    with open(out_sig, 'wb') as f:
        f.write(sig)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--src', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--key', required=True)
    args = p.parse_args()
    package_dir(args.src, args.out)
    sign_file(args.key, args.out, args.out + '.sig')
    print('Created', args.out, 'and signature', args.out + '.sig')

if __name__ == '__main__':
    main()
