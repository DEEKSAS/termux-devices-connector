# Threat model and security notes

- Hedef: yalnızca cihaz sahibi tarafından yetkilendirilmiş kod çalıştırılması.
- Tehditler: yetkisiz erişim, imzalanmamış kod çalıştırma, man-in-the-middle, anahtar sızıntısı.

Önlemler:
- Tüm paketler sunucuda imzalanmalı; cihazda imza doğrulanmadan çalıştırılmamalı.
- İstemci ve sunucu arasında TLS zorunlu olmalı (server için HTTPS ters proxy önerilir).
- Özel anahtar offline veya HSM içinde tutulmalı.
- Donanım etkisi olan komutlar için ek onay (manuel) gereklidir.
- Audit logları ve sürüm kontrolleri zorunlu.
