"""
Gelişmiş güvenlik + lojistik + uyum önerileri (kural tabanlı playbook).
Müşteri değerini artırmak için çok katmanlı çıktı; yasal tavsiye değildir.
"""
from __future__ import annotations


def build_playbook(
    *,
    iso2: str,
    name_en: str,
    risk_level: str,
    conflict_effective: float,
    political_stability: float,
    economic_risk: float,
    logistics_friction: float,
    recent_headline_count: int = 0,
) -> dict[str, list[str]]:
    guvenlik: list[str] = []
    lojistik: list[str] = []
    gumruk_uyum: list[str] = []
    finans_sigorta: list[str] = []
    kurumsal: list[str] = []

    # —— Güvenlik & fiziksel risk ——
    if conflict_effective >= 7.5:
        guvenlik.append(
            "Kritik çatışma/güvenlik ortamı: personel ve sürücü için seyahat güvenlik brifingi, "
            "alternatif güzergâh ve gece hareket kısıtı; yerel güvenlik danışmanı veya risk servisi değerlendirin."
        )
        guvenlik.append(
            "Yük ve depo için fiziki güvenlik seviyesini artırın (GPS mühür, konvoy protokolü, güvenli park alanı vetosu)."
        )
    elif conflict_effective >= 5.5:
        guvenlik.append(
            "Orta-yüksek güvenlik baskısı: rota keşfi (route clearance), düzenli konum paylaşımı ve acil tahliye iletişim hattı tanımlayın."
        )
    elif conflict_effective >= 3.5:
        guvenlik.append(
            "Sınırdaki olaylara duyarlılık: günlük güvenlik durum özeti ve sürücü check-list (benzin, iletişim, alternatif sınır kapısı)."
        )

    if political_stability < 3.5:
        guvenlik.append(
            "Politik kırılganlık: gösteri/emniyet olaylarında tedarik zinciri kesintisi riski — kritik envanter ve yedek rota planı."
        )

    if recent_headline_count >= 4:
        guvenlik.append(
            "Son dönemde bu ülkeye düşen haber yoğunluğu yüksek: 24–48 saatlik izleme penceresini sıkılaştırın; "
            "müşteri ve sigorta tarafını proaktif bilgilendirin."
        )

    # —— Lojistik operasyon ——
    if logistics_friction >= 7.0:
        lojistik.append(
            "Lojistik sürtünme çok yüksek: liman/boşaltma randevusu, iç nakliye kapasitesi ve şoför kıtlığı için çift tedarikçi + zaman tamponu (+15–25%)."
        )
        lojistik.append(
            "Incoterms seçimini gözden geçirin (ör. DAP yerine CIF deneme); depo yeri ve son mil için yerel 3PL SLA şartı yazın."
        )
    elif logistics_friction >= 5.0:
        lojistik.append(
            "Sınır geçiş ve iç nakliye gecikmeleri olası: cut-off saatlerini öne çekin, konteyner demurra riskini modele ekleyin."
        )

    if economic_risk >= 6.0:
        lojistik.append(
            "Ekonomik baskı: yakıt ve yerel maliyet dalgalanması — navlun sözleşmesinde fuel surcharge ve GRI maddelerini netleştirin."
        )

    if risk_level in ("HIGH", "EXTREME"):
        lojistik.append(
            "Yüksek bileşik risk: stok konumunu ülke dışına veya transit hub’a kaydırmayı değerlendirin (hub & spoke)."
        )
        lojistik.append(
            "Taşıma modu çeşitlendirmesi: tek moda bağımlılığı azaltın (kara+deniz veya demiryolu bağlantısı)."
        )

    # —— Gümrük & uyum ——
    if political_stability < 5.0 or economic_risk >= 5.5:
        gumruk_uyum.append(
            "İdari değişim riski: gümrük kodları, KDV/OTV ve kota değişiklikleri için haftalık mevzuat taraması ve broker ile çift kontrol."
        )
    gumruk_uyum.append(
        f"Yaptırım / restricted party taraması: {name_en} ({iso2}) hattında müşteri, banka ve nakliyeci için güncel liste taraması (OFAC/EU listeleri — kendi hukuk danışmanınızla)."
    )
    if logistics_friction >= 6.0:
        gumruk_uyum.append(
            "Yüksek sürtünme ülkelerinde belge hataları sık karantenaya düşer: fatura-packing list-konşimento üçlü uyumunu ön denetimden geçirin."
        )

    # —— Finans & sigorta ——
    if risk_level in ("HIGH", "EXTREME"):
        finans_sigorta.append(
            "Kredi sigortası ve poliçe muafiyetleri: limit düşüşü veya ülke exclusion ihtimali için finansman öncesi onay alın."
        )
    if economic_risk >= 6.5:
        finans_sigorta.append(
            "Kur ve likidite: ödemeyi güçlü para veya LC ile bağlama; vadeli açık hesap limitlerini düşürün."
        )
    finans_sigorta.append(
        "Nakliyat sigortası: Institute Cargo Clauses (A) ve gecikme/grev teminatlarını rota riskine göre gözden geçirin."
    )

    # —— Kurumsal süreklilik ——
    kurumsal.append(
        "Tedarik zinciri görünürlüğü: bu ülke için KPI seti (OTIF, transit süresi varyansı, gümrükte bekleme) tanımlayın ve aylık yönetim özetine bağlayın."
    )
    if conflict_effective >= 5.0:
        kurumsal.append(
            "Senaryo planlaması: en kötü durumda ikinci ülke çıkışı ve müşteri bildirim şablonları hazır tutun."
        )

    # Boş kalan kategoriler için kısa teyit
    if not guvenlik:
        guvenlik.append("Güvenlik: mevcut skorlarla standart SOP ve periyodik rota risk taraması yeterli görünüyor.")
    if not lojistik:
        lojistik.append("Lojistik: mevcut kapasite ve süreçlerle operasyon sürdürülebilir; yine de KPI izlemeye devam edin.")
    if len(gumruk_uyum) == 1:
        gumruk_uyum.append("Uyum: ihracat/ithalat belgelerinde dijital arşiv ve denetim izi tutun.")
    if len(finans_sigorta) == 1:
        finans_sigorta.append("Finans: ödeme vadelerini nakit akışı stres testine tabi tutun.")

    return {
        "guvenlik": guvenlik,
        "lojistik_operasyon": lojistik,
        "gumruk_uyum": gumruk_uyum,
        "finans_sigorta": finans_sigorta,
        "kurumsal_sureklilik": kurumsal,
    }


def playbook_to_flat_summary(playbook: dict[str, list[str]], max_per: int = 2) -> list[str]:
    """Eski API uyumu için kısa birleşik liste."""
    out: list[str] = []
    labels = {
        "guvenlik": "Güvenlik",
        "lojistik_operasyon": "Lojistik",
        "gumruk_uyum": "Gümrük/uyum",
        "finans_sigorta": "Finans/sigorta",
        "kurumsal_sureklilik": "Kurumsal",
    }
    for key, title in labels.items():
        for line in playbook.get(key, [])[:max_per]:
            out.append(f"【{title}】 {line}")
    return out[:12]
