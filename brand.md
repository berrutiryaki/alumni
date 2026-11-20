# Brand & Design System — Alumni Platform

Bu doküman, **Alumni Tracking & Networking Platform** arayüzlerinde kullanılan renk paleti, tipografi kuralları ve bileşen tasarım standartlarını özetler.

> Ayrıca bkz: [README.md](README.md) — proje özeti ve mimari · [ddd.md](ddd.md) — veri sözlüğü ve API referansı · [design.md](design.md) — token'lar, bileşen spesifikasyonları ve Do's/Don'ts içeren tam stil referansı.

---

## 1. Renk Paleti (Color Palette)

| Rol / Token | Renk Adı | Hex Kodu | CSS Değişkeni | Kullanım Alanı |
|---|---|---|---|---|
| **Dark Canvas** | Forest Depths | `#14281D` | `--color-forest-depths` | Hero bölümleri, koyu bantlar ve footer arka planı |
| **Primary Forest** | Deep Forest Green | `#1B4332` | `--color-moss-shadow` | Seçili navigasyon durumu, atmosferik küre (orb) geçişleri |
| **Primary Accent (CTA)** | Warm Dusty Rose | `#F497AE` | `--color-electric-sprout` | Ana aksiyon butonları (pill CTA), koyu zemin üzerindeki vurgu kelimeleri |
| **Light Accent** | Deep Rose | `#C85A78` | `--color-deep-verdant` | Açık zemin üzerindeki başlık/şirket vurguları ve odak (focus) kenarlığı |
| **Badge Wash** | Soft Rose Blush | `#FCEEF2` | `--color-sprout-wash` | Durum rozetleri (badges) ve odak halkası (focus ring) arka planı |
| **Elevated Card** | Warm Cream | `#FAF8F5` | `--color-bone-white` | Açık bölümlerdeki kart, tablo ve form kutusu yüzeyi |
| **Light Surface** | Pure White | `#FFFFFF` | `--color-pure-white` | Açık bölüm arka planı, koyu zemin metinleri ve yüzen mockup kartları |
| **Primary Text** | Charcoal | `#1C1917` | `--color-onyx-olive` | Açık zemin üzerindeki metinler ve 1px kart kenarlıkları |
| **Border** | Soft Sand | `#E7E5E4` | `--color-soft-mist` | Tablo satır ayraçları ve kart içi ince çizgiler |

---

## 2. Tipografi (Typography)

- **Display Başlıklar (`h1`, `h2`):** `'Boldonse'` (`--font-display`) — hero ve bölüm ana başlıklarında güçlü, sıkı istiflenmiş editoryal görünüm.
- **Arayüz, Tablo ve Form Metinleri:** `'Inter'` (`--font-ui`) — navigasyon, gövde metinleri, butonlar, tablolar ve form alanları.
- **Editoryal Vurgu (`eyebrow`, tarih/yazar satırları):** `'Instrument Serif'` (`--font-serif`) — bölüm üst başlıkları ve meta satırlarında organik serif dokunuşu.

### Ortak Stil Dosyası ve Parçalar (Partials)

Tüm sayfalar ortak olarak [`static/css/theme.css`](static/css/theme.css) dosyasını ve `app/templates/partials/` altındaki şablon parçalarını (`head.html`, `nav.html`, `footer.html`) kullanır.
