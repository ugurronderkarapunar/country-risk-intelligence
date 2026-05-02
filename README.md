# Country Risk Intelligence

Lojistik ve dış ticaret odaklı ülke risk paneli: bileşik risk skoru, ReliefWeb RSS ile çatışma sinyalleri ve Türkçe operasyonel öneriler.

## Yerel kurulum (Windows)

### 1) Backend (Python 3.11+)

```powershell
cd "C:\Users\Windows 11\Desktop\country-risk-intelligence\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

İsteğe bağlı: `backend\.env.example` dosyasını `.env` olarak kopyalayın.

Sunucuyu başlatın:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API: `http://127.0.0.1:8000/docs`
- Çatışma akışı her gün **12:00 Türkiye saati (Europe/Istanbul)** için zamanlanır; ilk veri için panele gidip **“Çatışma akışını şimdi güncelle”** veya `POST http://127.0.0.1:8000/api/sync` kullanın.

### 2) Frontend (Node.js 20+)

[Node.js LTS](https://nodejs.org/) kurulu olmalı (`npm` PATH’te görünür).

```powershell
cd "C:\Users\Windows 11\Desktop\country-risk-intelligence\frontend"
npm install
npm run dev
```

Arayüz: `http://127.0.0.1:5173` (Vite, `/api` isteklerini backend’e yönlendirir).

## GitHub

Proje kökünde (bu klasörde):

```powershell
cd "C:\Users\Windows 11\Desktop\country-risk-intelligence"
& "C:\Program Files\Git\bin\git.exe" init
& "C:\Program Files\Git\bin\git.exe" add .
& "C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: Country Risk Intelligence"
& "C:\Program Files\Git\bin\git.exe" branch -M main
& "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/KULLANICI_ADINIZ/country-risk-intelligence.git
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

`KULLANICI_ADINIZ` ve repo adını GitHub’da oluşturduğunuz repo ile değiştirin. İlk push’ta tarayıcı veya Personal Access Token ile giriş istenebilir.

## Canlıya alma (Render.com + Docker)

Repoyu GitHub’a ittikten sonra:

1. [Render](https://render.com) → **New** → **Blueprint** (veya **Web Service**).
2. Repo’yu bağlayın; kökteki `Dockerfile` ile deploy edin (`render.yaml` Blueprint için kullanılabilir).
3. Servis ayakta olduktan sonra tek URL hem arayüzü hem `/api` uçlarını sunar (`/api/health` ile kontrol).

**Not:** Render free web uyku moduna geçebilir; iç zamanlayıcı her zaman çalışmayabilir. Üretimde günlük senkron için Render **Cron Job** ile `POST https://SIZIN-URL/api/sync` veya harici cron önerilir. SQLite dosyası konteyner diskindedir; kalıcı DB için managed PostgreSQL’e geçmek gerekir.

## Mimari özeti

- **Backend:** FastAPI, **senkron** SQLAlchemy + SQLite (`backend/data/risk_intel.db`), APScheduler (Europe/Istanbul cron). Async/greenlet gerektirmez; kurumsal Windows ortamlarında daha sorunsuz çalışır.
- **Veri:** Ülke temel metrikleri seed; ReliefWeb RSS metninden anahtar kelime → ISO2 eşlemesi; son 14 gün olay sayısı çatışma bileşenine sınırlı boost uygular.
- **Frontend:** React + Vite + TypeScript + Tailwind + Recharts.

## Yasal not

Panel bilgilendirme amaçlıdır; ticari ve hukuki kararlar için uzman görüşü gereklidir.
