# Brand & Design System — Alumni Platform

Bu doküman, **Alumni Tracking & Networking Platform** arayüzlerinde kullanılacak renk paleti, tipografi kuralları ve bileşen tasarım standartlarını tanımlar.

> Ayrıca bkz: [README.md](README.md) — proje özeti ve mimari · [ddd.md](ddd.md) — veri sözlüğü ve API referansı · [design.md](design.md) — token'lar, bileşen spesifikasyonları ve Do's/Don'ts içeren tam stil referansı.

---

## 1. Renk Paleti (Color Palette)

| Rol / Token | Renk Adı | Hex Kodu | CSS Değişkeni | Kullanım Alanı |
|---|---|---|---|---|
| **Primary** | Deep Forest Green | `#1B4332` | `--color-primary` | Ana aksiyon butonları (CTA), aktif navigasyon vurguları, marka ana rengi |
| **Accent** | Warm Terracotta | `#C2410C` | `--color-accent` | İkincil vurgular, rozetler (badges), önemli bildirim/aksiyon linkleri |
| **Background** | Warm Cream | `#FAF8F5` | `--color-bg` | Sayfa ana arka plan zemini (`<body>`) |
| **Surface** | Pure White | `#FFFFFF` | `--color-surface` | Kartlar, tablolar, form kutuları ve üst navigasyon yüzeyi |
| **Text** | Charcoal | `#1C1917` | `--color-text` | Başlıklar, gövde metinleri ve tablo içerikleri |
| **Border** | Soft Sand | `#E7E5E4` | `--color-border` | Kart çerçeveleri, tablo satır ayraçları ve form input kenarlıkları |
| **Error** | Crimson Red | `#B91C1C` | `--color-error` | Hata mesajları, silme (delete) butonları ve doğrulama uyarıları |

### CSS Değişken Tanımı (`:root`)

```css
:root {
    --color-primary: #1B4332;
    --color-accent: #C2410C;
    --color-bg: #FAF8F5;
    --color-surface: #FFFFFF;
    --color-text: #1C1917;
    --color-border: #E7E5E4;
    --color-error: #B91C1C;
}
```

---

## 2. Tipografi (Typography)

- **Başlıklar (`h1`, `h2`, `h3`, `.brand`):** `'Playfair Display'` (serif) — akademik, kurumsal ve prestijli bir görünüm sağlar.
- **Gövde, Tablo ve Form Metinleri (`body`, `table`, `input`, `select`, `textarea`, `button`):** `'Plus Jakarta Sans'` (sans-serif) — yüksek okunabilirlik ve modern arayüz netliği sağlar.

### Google Fonts Entegrasyonu

Tüm HTML şablonlarının `<head>` bölümüne aşağıdaki Google Fonts bağlantısı eklenmelidir:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Temel Tipografi CSS Kuralları

```css
body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #FAF8F5;
    color: #1C1917;
}

h1, h2, h3, h4, .brand {
    font-family: 'Playfair Display', Georgia, serif;
    color: #1C1917;
}
```

---

## 3. Bileşen Stili (Component Guidelines)

- **Zemin ve Kartlar:** Sıcak krem (`#FAF8F5`) sayfa zemini üzerinde, ince taş rengi çerçeveli (`1px solid #E7E5E4`) saf beyaz (`#FFFFFF`) kartlar kullanılır. Ağır gölgeler yerine zarif kenarlıklar tercih edilir.
- **Ana Butonlar (Primary Buttons):** Koyu orman yeşili (`#1B4332`) arka plan ve beyaz (`#FFFFFF`) metin; ikincil/vurgu aksiyonlarda sıcak terakota (`#C2410C`) kullanılır.
- **Tablolar:** Ferah satır aralıkları (`padding: 14px 18px`), taş rengi (`#E7E5E4`) satır ayraçları ve okunaklı `'Plus Jakarta Sans'` tipografisi.
- **Üst Navigasyon Çubuğu (Navbar):** Sade, temiz yüzey (`#FFFFFF` veya koyu yeşil `#1B4332` varyasyonu), `'Playfair Display'` ile yazılmış marka başlığı ve ince alt çerçeve (`1px solid #E7E5E4`).
