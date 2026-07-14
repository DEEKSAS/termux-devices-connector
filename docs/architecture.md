# Mimari Özeti

- Yönetim Sunucusu: İmzalı paketlerin alındığı ve saklandığı REST API.
- İmza Araçları: Paketleyip RSA ile imzalayan yardımcı script.
- Uç Ajan: Cihaz üzerinde çalışan, paketleri doğrulayan ve izole şekilde çalıştıran küçük daemon/cron/manuel ajan.

İletişim:
- TLS + JWT (veya mTLS) ile yetkilendirme.
- Paketlerin bütünlüğü RSA-SHA256 ile doğrulanır.

Sandboxing:
- Termux için `proot`/`proot-distro` önerilir.
- Diğer Linux cihazlarda `user namespaces`, `containers` veya `firejail` gibi araçlar kullanılmalıdır.
