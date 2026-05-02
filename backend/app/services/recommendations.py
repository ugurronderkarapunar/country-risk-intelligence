def trade_logistics_recommendations(
    *,
    risk_level: str,
    conflict_effective: float,
    political_stability: float,
    economic_risk: float,
    logistics_friction: float,
) -> list[str]:
    """Lojistik ve dış ticaret odaklı, Türkçe operasyonel öneriler."""
    recs: list[str] = []

    if risk_level in ("HIGH", "EXTREME"):
        recs.append(
            "Yüksek ülke riski: öncelikle teminat mektubu / akreditif ve nakit akışı kısıtlarını gözden geçirin; "
            "alternatif tedarik veya transit ülke senaryoları tanımlayın."
        )

    if conflict_effective >= 6.5:
        recs.append(
            "Çatışma / güvenlik baskısı yüksek: kara konvoylarında güvenlik protokolü ve canlı izleme zorunlu sayılmalı; "
            "mümkünse deniz veya hava çıkış limanına kaydırın."
        )
    elif conflict_effective >= 4.5:
        recs.append(
            "Orta düzey güvenlik riski: rota çeşitlendirme, depo bölge seçimi ve gecikme tamponu (lead time) ekleyin."
        )

    if political_stability < 4.0:
        recs.append(
            "Politik belirsizlik: gümrük / kota / yaptırım değişimlerine karşı sözleşmelerde force majeure ve "
            "yeniden fiyatlama maddeleri önerilir."
        )

    if economic_risk >= 6.5:
        recs.append(
            "Ekonomik ve kur riski: yerel para ödemelerinde hedge veya döviz endeksli sözleşme; "
            "kredi sigortası limitlerini güncelleyin."
        )

    if logistics_friction >= 6.5:
        recs.append(
            "Lojistik sürtünme yüksek: liman dolulukları, iç nakliye kapasitesi ve belge süreçlerini ön denetimden geçirin; "
            "3PL yerel ortak due diligence yapın."
        )

    if not recs:
        recs.append(
            "Risk profili makul seviyede: standart Incoterms, sigorta ve KYC süreçleri ile operasyon sürdürülebilir."
        )

    return recs
