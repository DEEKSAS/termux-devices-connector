Remote Device Code Runner Prototype

Bu prototip, yetkili kullanıcıların güvenli, imzalanmış kod paketlerini sahip oldukları cihazlarda (ör. Android TV içinde Termux veya Linux tabanlı cihazlarda) çalıştırabilmesi için örnek bir mimari, sunucu ve uç ajan sağlar.

Özellikler:
- Yönetim API (Flask) — imzalanmış kod paketlerini kabul eder ve saklar.
- İmza araçları — RSA ile paket imzalama örneği.
- Uç ajan (Termux için bash) — sunucudan imzalı paketleri çeker, imzayı doğrular, izole bir ortamda çalıştırır.

Güvenlik uyarısı:
- Bu araç yalnızca sahip olduğunuz ve fiziksel erişiminiz olan cihazlarda kullanılmalıdır.
- Donanım etkisine sahip işlemler için ek el ile onay ve sınırlandırma mekanizmaları uygulayın.

Hızlı başlatma (sunucu için):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r prototype/server/requirements.txt
python prototype/server/app.py
```

Uç ajan kurulumu (Termux):

1. Termux içinde gerekli paketleri kurun:

```bash
pkg update && pkg install proot openssl curl python unzip
```

2. Ajanı cihazınıza kopyalayın:

```bash
# host'ta
scp prototype/agent/agent.sh prototype/agent/verify_signature.py user@device:/data/data/com.termux/files/home/
ssh user@device
cd /data/data/com.termux/files/home
chmod +x agent.sh
```

3. Public anahtarı cihazınıza kopyalayın veya `RDCR_PUBKEY_URL` ile sunucudan indirme ayarlayın.

4. Ajan kullanım örnekleri:

```bash
# signature doğrulama
./agent.sh verify bundle.zip

# doğrula ve çalıştır
./agent.sh run bundle.zip

# sunucuya yükle
RDCR_JWT=... ./agent.sh upload bundle.zip
```

5. Örnek paket: `prototype/sample_app/run.sh` — bu paket testi için kullanabilirsiniz. Paketleyip imzalamak için `prototype/signing/sign_and_package.py` scriptini kullanın.

Daha fazla detay için `prototype/docs` klasörüne bakın.
