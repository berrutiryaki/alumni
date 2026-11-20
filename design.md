# Alumni Platform — Style Reference
> a botanical courtyard at dusk — Warm Dusty Rose blossom pierces the deep forest-green canvas and warm cream beds below. The brand lives in that contrast: the dark forest is the soil, the warm cream is the bench, the dusty rose is the bloom.

**Theme:** mixed (alternating `#14281D` dark forest and `#FFFFFF` / `#FAF8F5` warm light bands)

All pages share [`static/css/theme.css`](static/css/theme.css) and the partials in `app/templates/partials/` (`head.html`, `nav.html`, `footer.html`). For the short Turkish summary see [brand.md](brand.md).

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Forest Depths | `#14281D` | `--color-forest-depths` | Dark hero, dark feature bands, and footer canvas |
| Deep Forest Green | `#1B4332` | `--color-moss-shadow` | Selected nav pill state and atmospheric orb gradient |
| Lichen Sage | `#9BA89E` | `--color-lichen-sage` | Secondary muted text, captions, and pill borders on dark |
| Pale Fern | `#CBD5CD` | `--color-pale-fern` | Supporting body copy and nav links on dark surfaces |
| Warm Dusty Rose | `#F497AE` | `--color-electric-sprout` | Primary filled CTA buttons, active accent words on dark, and Hiring tag |
| Deep Rose | `#C85A78` | `--color-deep-verdant` | Accent words and company highlights on light surfaces, input focus border |
| Soft Rose Blush | `#FCEEF2` | `--color-sprout-wash` | Soft pink badge fill and focus ring halo |
| Rose Mist | `#F5D6DF` | `--color-mist-green` | Subtle rose border for destructive/alert chips |
| Charcoal | `#1C1917` | `--color-onyx-olive` | Primary text on light surfaces and 1px structural card borders |
| Pure White | `#FFFFFF` | `--color-pure-white` | Light band canvas, text on dark surfaces, and floating hero mockup cards |
| Warm Cream | `#FAF8F5` | `--color-bone-white` | Elevated card, table, and form container surface on light bands |
| Soft Sand | `#E7E5E4` | `--color-soft-mist` | Table row dividers, filter pill borders, and inner card hairlines |
| Cool Stone | `#D6D3D1` | `--color-cool-stone` | Muted/archived badge surface |

## Tokens — Typography

- **Display (`--font-display`):** `'Boldonse'`, 400 weight, `clamp(36px, 7vw, 72px)` for hero display (`line-height: 1.25`) and `clamp(26px, 3.8vw, 44px)` for section headings (`line-height: 1.3`). One key word per heading switches to `.accent` (`#F497AE` on dark, `#C85A78` on light).
- **UI Workhorse (`--font-ui`):** `'Inter'`, weights 400, 500, 600, 700 — carries navigation, body copy, tables, form controls, badges, and buttons.
- **Editorial Accent (`--font-serif`):** `'Instrument Serif'`, 400 weight — used for section eyebrows (`.eyebrow`), graduation cohort labels, and announcement/application timestamps.

## Components

- **Floating Pill Navigation (`partials/nav.html`):** Fixed at top (`top: 24px`), `max-width: 1200px`, translucent dark pill (`rgba(48, 50, 42, 0.9)` with `backdrop-filter: blur(12px)`), `28px` border-radius, containing the `alumni` wordmark + dusty-pink `Hiring` tag, module links, outlined `Swagger API` button, and filled dusty-pink `Post a job` pill CTA.
- **Inner Page Hero (`.page-hero`):** Dark forest canvas with atmospheric `.orb`, Instrument Serif eyebrow, Boldonse display heading with one dusty-pink accent word, KPI badge strip, and primary dusty-pink pill CTA on the right.
- **Filter & Search Toolbar (`.toolbar`):** Pill filter buttons (`.filter-pill`, active state in `#14281D` with `#F497AE` text) paired with a live client-side `.search-input` (`24px` pill radius).
- **Directory Table & Cards (`.dir-card`, `.card-light`, `.card-dark`):** `20px` border-radius, `1px solid #1C1917` structural frame, Warm Cream `#FAF8F5` surface on light bands.
- **Form Shell (`.form-shell`):** Centered `680px` Warm Cream card (`24px` radius) with `24px`-radius pill inputs (`.input-pill`, `.select-pill`) and `18px`-radius textareas (`.textarea-pill`).
