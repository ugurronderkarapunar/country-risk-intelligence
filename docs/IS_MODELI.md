# İş modeli ve ürün kararı (Country Risk Intelligence)

## Karar: hibrit gelir — önce SaaS panel, API ikinci gelir kaynağı

**Neden tam API değil?**  
Lojistik ve dış ticaret şirketlerinde karar verenler (operasyon, gümrük, finans) çoğunlukla **panel, rapor ve uyarı** ister. Saf API, satış döngüsünü uzatır ve teknik alıcı (CTO) dışında değeri anlatmak zordur.

**Neden API yine de var?**  
Orta ve büyük filolarda **TMS / WMS / ERP** entegrasyonu kaçınılmazdır. API, **Pro ve Enterprise** paketlerde “kilit özellik” olarak konumlandırılır; böylece hem **koltuk başı SaaS** hem **entegrasyon ücreti** mümkün olur.

Özet tablo:

| Kanal | Hedef müşteri | Fiyatlandırma fikri |
|--------|-----------------|---------------------|
| **SaaS panel** | Operasyon müdürü, rota planlama, ticaret | Aylık koltuk / düşük bilet Starter |
| **REST API** | IT + entegratör, TMS | Pro+ paket veya çağrı başına üst sınır |
| **Enterprise** | Holding, banka, sigorta ortaklığı | Yıllık lisans, SLA, özel veri |

## Ürün paketleri (kod ile uyumlu)

- **Starter:** Panel + sınırlı aylık **koridor analizi** kotası; API yok.
- **Pro:** Yüksek koridor kotası + **API anahtarı** (`X-API-Key`) + `GET/POST /api/v1/...`.
- **Enterprise:** Fiilen sınırsız kota (üst sınır), sözleşme, özelleştirme alanı.

Kota ve plan alanları `organizations.subscription_tier` üzerinden yönetilir. Stripe / ödeme kurumu entegrasyonu bir sonraki adımdır (şu an `demo_upgrade_secret` ile test yükseltmesi).

## API uçları (Pro+)

- `POST /api/v1/corridor` — gövde: `{ "legs": ["DE","PL","UA"] }`
- `GET /api/v1/countries` — skor listesi
- `GET /api/v1/countries/{iso2}` — detay + öneriler

Kimlik: `X-API-Key: crik_...` (JWT değil).

## Yasal ve güven

Risk skorları ve haber eşlemesi **bilgilendirme** amaçlıdır; müşteri sözleşmesinde mutlaka **feragat**, **veri kaynağı** ve **yükümlülük sınırı** tanımlanmalıdır.

## Sonraki gelir adımları (teknik olmayan)

1. Stripe Checkout + Customer Portal (plan yükseltme).  
2. Fatura (Türkiye için uyumlu muhasebe entegrasyonu veya manuel).  
3. Kurumsal demo ve **pilot ücreti**.  
4. Beyaz etiket (müşteri domain + logo) ücreti.
