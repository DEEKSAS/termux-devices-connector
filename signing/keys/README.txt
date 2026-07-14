Generate a keypair for signing (on a secure machine):

```
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out private.pem
openssl rsa -in private.pem -pubout -out public.pem
```

Place `private.pem` on your signing machine and `public.pem` in `prototype/signing/keys/` and also copy to the server's `signing/keys/` directory.
