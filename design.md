# Alumni Platform — Style Reference
> a quiet university library at golden hour — warm cream paper, deep forest-green ink, and a single terracotta bookmark. The brand lives in that calm contrast: cream is the paper, white is the page, green is the ink, terracotta is the margin note.

**Theme:** light

Values below are taken from the CSS currently shipped in `app/templates/`. Roles and recommendations are interpreted. HTML examples are reconstructions, not source components. For the short brand summary see [brand.md](brand.md).

Alumni Platform is an academic and career network for graduates, students, and institutions. It renders in a warm, editorial, light-only system: a cream page canvas carries flat white cards with hairline sand borders, set in a Playfair Display serif for headings and Plus Jakarta Sans for every UI surface. Deep Forest Green is the single filled action color; Warm Terracotta is a quiet accent for links, section labels, and secondary highlights. The nav is a plain white bar with a bottom border, not a floating pill. Components are softly rounded (6–12px), never pill-shaped except badges and filter chips. Pages should read as roughly 70% typography on flat surfaces, 20% bordered cards and tables, 10% accent color.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Deep Forest Green | `#1B4332` | `--color-primary` | The only filled action color: primary buttons, active nav text, focus ring, avatar fill, stat numbers, brand wordmark. |
| Forest Green Hover | `#143325` | `--color-primary-hover` | Hover/pressed state of primary buttons only. |
| Warm Terracotta | `#C2410C` | `--color-accent` | Secondary accent: text links, section labels, company names, "pending" status, panel links. Never a filled surface behind long text. |
| Terracotta Hover | `#9A3412` | `--color-accent-hover` | Hover state of terracotta-filled buttons (used on the homepage hero CTA). |
| Warm Cream | `#FAF8F5` | `--color-bg` | Page background, table header fill, footer bars inside cards, inset blocks (cover letter, hero summary). |
| Pure White | `#FFFFFF` | `--color-surface` | Cards, tables, form fields, and the top navigation bar. |
| Charcoal | `#1C1917` | `--color-text` | Headings and body copy. |
| Stone Muted | `#57534E` | `--color-muted` | Secondary text, helper hints, inactive nav links, meta rows. |
| Soft Sand | `#E7E5E4` | `--color-border` | Every 1px hairline: card borders, table row dividers, input borders, nav bottom border. |
| Crimson Error | `#B91C1C` | `--color-error` | Error messages, required-field asterisks, delete buttons, "rejected" and "closed" status text. |
| Sage Tint | `#E8F0EC` | — (inline) | Soft green surface: active nav item, "Database Connected" chip, alumni and active badges. |
| Sage Border | `#C5D9CE` | — (inline) | Border for Sage Tint chips and badges. |
| Error Tint | `#FEF2F2` | — (inline) | Background of error boxes, delete buttons, and rejected/closed badges. |
| Error Border | `#FECACA` | — (inline) | Border paired with Error Tint. |
| Terracotta Tint | `#FFF7ED` | — (inline) | Background of "student" and "pending" badges. |
| Terracotta Border | `#FED7AA` | — (inline) | Border for the pending badge. |

## Tokens — Typography

### Playfair Display — Headings and wordmark only. A high-contrast serif that gives the platform its academic, editorial voice. · `--font-heading`
- **Source:** Google Fonts
- **Weights:** 600, 700 (700 is used in practice)
- **Sizes:** 16px, 18px, 20px, 22px, 24px, 28px, 34px, 38px, 46px
- **Role:** `h1`–`h4`, the navbar `.brand`, job titles, candidate names, large stat numbers, form titles, and the `404` badge. Never used for body copy, labels, table cells, or buttons.

### Plus Jakarta Sans — Workhorse for every UI surface: body, nav links, tables, forms, buttons, badges. · `--font-body`
- **Source:** Google Fonts
- **Weights:** 400, 500, 600, 700
- **Sizes:** 11px, 12px, 13px, 14px, 15px, 16px
- **Role:** 400 for body and descriptions, 500 for nav links and secondary labels, 600 for buttons, form labels, and badges, 700 for emphasized numbers and small uppercase section labels.

### Font loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale

| Role | Family | Weight | Size | Line Height | Where used |
|------|--------|--------|------|-------------|------------|
| label-xs | Plus Jakarta Sans | 700 | 11px | normal | Uppercase section titles in forms (letter-spacing 0.8px, terracotta) |
| caption | Plus Jakarta Sans | 400–600 | 12px | 1.5 | Meta text, badges, table headers (uppercase, 0.5px tracking) |
| body-sm | Plus Jakarta Sans | 400–500 | 13px | 1.5 | Form labels, helper text, meta rows, small buttons |
| body | Plus Jakarta Sans | 400 | 14px | 1.6 | Default body, table cells, inputs |
| body-md | Plus Jakarta Sans | 400 | 15–16px | 1.6 | Hero paragraph, subtitles |
| heading-xs | Playfair Display | 700 | 16px | 1.3 | Feed item and announcement titles |
| heading-sm | Playfair Display | 700 | 18–20px | 1.3 | Card titles, job titles, panel titles |
| heading | Playfair Display | 700 | 22–24px | 1.3 | Navbar brand, form titles, section titles |
| heading-lg | Playfair Display | 700 | 28px | 1.3 | Page `h1` on list pages |
| display | Playfair Display | 700 | 34–38px | 1.2 | Homepage stat values and hero headline |

## Tokens — Spacing & Shapes

**Base unit:** 4px steps (mostly 8px multiples)

**Density:** comfortable

### Spacing Scale

| Name | Value | Typical use |
|------|-------|-------------|
| 4 | 4px | Badge vertical padding, icon nudges |
| 8 | 8px | Gap between nav links, filter chips, card footer buttons |
| 12 | 12px | Input padding, small gaps |
| 16 | 16px | Element gap, card list gap |
| 24 | 24px | Card padding (list cards), section gap inside forms |
| 28–36 | 28–36px | Form card padding, navbar side padding (36px) |
| 40–48 | 40–48px | Hero padding, page top padding |
| 60–64 | 60–64px | Page bottom padding |

### Border Radius

| Element | Value |
|---------|-------|
| buttons | 6px |
| inputs and selects | 6px |
| tables and list cards | 10px |
| hero and error cards | 12px |
| nav link hover/active | 6px |
| badges and filter chips | 20px (full pill) |
| avatar | 50% |

### Layout

- **Navbar height:** 68px, full-width, side padding 36px
- **Page max-width:** 1120px (homepage), 1100px (job postings), 1080px (users), 960px (announcements, applications)
- **Form page max-width:** 620–720px, single centered card
- **Page padding:** 24px sides, 36–40px top, 60–64px bottom
- **Card padding:** 22–30px (list cards), 26–28px (panels and forms)
- **Element gap:** 8–18px

## Components

### Top Navigation Bar
**Role:** Primary site navigation, present on every page

White (`#FFFFFF`) bar, 68px tall, 1px `#E7E5E4` bottom border, no shadow, 36px side padding. Left: Playfair Display 22px 700 wordmark "Alumni Platform" in Deep Forest Green, followed by links (Home, Users, Announcements, Job Postings, Applications, Swagger API) in Plus Jakarta Sans 14px 500 Stone Muted. Link padding 8px 14px, 6px radius. Hover: text turns green, background Warm Cream. Active: text green 600, background Sage Tint `#E8F0EC`. List and homepage views add a right-aligned "Database Connected" chip; the homepage nav is `position: sticky; top: 0`.

### Database Connected Chip
**Role:** Status badge in nav

Sage Tint fill, 1px Sage Border, Deep Forest Green text, 12px 600, padding 6px 14px, 20px radius, preceded by an 8px solid green dot.

### Primary Button
**Role:** Highest-emphasis action

Deep Forest Green fill, white text, Plus Jakarta Sans 13–14px 600, padding 10–11px 18–22px, 6px radius, no shadow. Hover: `#143325`. Used for "+ Create", "Submit", "Save", "Apply Now", "Explore Job Board".

### Accent Button
**Role:** Secondary conversion action, homepage hero only

Warm Terracotta fill, white text, same dimensions as the primary button. Hover: `#9A3412`. At most one per viewport next to a primary button.

### Outline / Secondary Button
**Role:** Lower-emphasis action (Edit, Cancel, Browse)

White fill, 1px Soft Sand border, Charcoal text 13px 600 (Cancel is Stone Muted 500). Hover: border and text turn Deep Forest Green (Cancel hovers to Charcoal).

### Danger Button
**Role:** Delete

Error Tint fill, 1px Error Border, Crimson text, 12–13px 600, 6px radius. Hover: slightly darker tint (`#FEE2E2`). Always paired with a `confirm()` dialog.

### Card
**Role:** Default container for content

White surface, 1px Soft Sand border, 10px radius, 22–30px padding, no shadow. A card header (when present) is separated from its body by a 1px Soft Sand rule. Card footers use Warm Cream fill with a top hairline.

### Table
**Role:** Users registry

White card wrapper with 10px radius and `overflow: hidden`. Header row on Warm Cream, 12px 600 uppercase Stone Muted text, 0.5px tracking. Cells 14px with 16px 20px padding and a 1px Soft Sand bottom border (none on the last row). Row hover: `#FDFCFB`. Empty state is a single centered cell in Stone Muted.

### Status Badge
**Role:** Inline category or state tag

Pill (20px radius), 12px 600, padding 4px 10px. Variants:

| State | Background | Text | Border |
|-------|-----------|------|--------|
| alumni / active / accepted | `#E8F0EC` | `#1B4332` | `#C5D9CE` |
| student / pending | `#FFF7ED` | `#C2410C` | `#FED7AA` |
| reviewed / employment type | `#FAF8F5` | `#1C1917` | `#E7E5E4` |
| inactive / closed / rejected | `#FEF2F2` | `#B91C1C` | `#FECACA` |

Application and job badges use 11px uppercase with 0.3–0.4px tracking.

### Filter Chips
**Role:** Client-side list filtering on Job Postings and Applications

Pill (20px radius), 13px 500, padding 6px 14px, white fill, 1px Soft Sand border, Stone Muted text. Hover and active: Deep Forest Green fill and border, white text.

### Form Field
**Role:** Text input, select, textarea

White fill, 1px Soft Sand border, 6px radius, padding 10–11px 12–13px, Plus Jakarta Sans 14px, Charcoal text. Focus: border turns Deep Forest Green with a `0 0 0 3px rgba(27,67,50,0.12)` ring. Labels are 13px 600 Charcoal; required markers use Crimson `*`; hints are 12px 400 Stone Muted.

### Form Card
**Role:** Create and edit pages

Single centered white card (max-width 620–720px) with a header (Playfair 24px title plus 13px Stone Muted subtitle), a body split into sections, and a Warm Cream footer holding the primary submit button and an outline Cancel. Section titles are 11px 700 uppercase terracotta with a bottom hairline. Edit pages add a small ID chip (`#12`) on the right of the header. A breadcrumb above the card uses terracotta 600 links.

### Job Card
**Role:** Job Postings list item

White card in an auto-fill grid (min 460px). Top row: 42px company initial tile (Warm Cream, 1px border, Playfair green initial) on the left, type and status badges on the right. Then Playfair 20px job title, terracotta 14px 600 company name, 13px Stone Muted meta row (city, salary, posted by), 14px description, and a footer row with a green "Apply Now" button, an outline Edit, and a red Delete. Inactive postings render at 72% opacity.

### Application Card
**Role:** Applications list item

White card with a header row: 42px green avatar circle with the candidate initial, Playfair 18px candidate name, a "Applied for **Title** at Company" line (company in terracotta), and a status badge on the right. An optional cover-letter block sits on Warm Cream with a 1px border and 6px radius. Footer on Warm Cream with submitted time, "View CV" (terracotta), Edit, and Delete.

### Homepage Hero
**Role:** Landing statement

White card, 12px radius, 48px 44px padding. Left: small uppercase terracotta tag, Playfair 38px headline, 16px Stone Muted paragraph, and a row of three buttons (primary, accent, outline). Right: a Warm Cream summary box with three label/value rows (values in Playfair 22px green).

### Stat Card
**Role:** Homepage KPI tiles

White card, 10px radius, 22px 24px padding. 13px 600 uppercase Stone Muted label, Playfair 34px green value, 13px meta line (terracotta for the highlighted count). Hover: border turns green. Four across, collapsing to two and one.

### Error Page Card
**Role:** 404 and 5xx pages

Centered white card, 12px radius, with a large Playfair status badge (Error Tint fill, Crimson text), an H1, a Warm Cream reason box with a 4px Crimson left border, optional "Did you mean" suggestions, and navigation buttons.

## Do's and Don'ts

### Do
- Use Deep Forest Green `#1B4332` as the only filled action color; every primary button, active nav state, focus ring, and avatar runs through it.
- Use Warm Terracotta `#C2410C` for text accents only: links, company names, section labels, pending state.
- Set every heading in Playfair Display 700 and every other piece of text in Plus Jakarta Sans.
- Keep surfaces flat: white card, 1px Soft Sand border, Warm Cream page behind it.
- Use 6px radius for buttons and inputs, 10px for cards and tables, 12px for hero and error cards, and a full pill only for badges and chips.
- Pair every destructive action with Crimson on an Error Tint fill and a confirmation dialog.
- Put the Warm Cream fill on anything "inset" inside a white card (table header, card footer, quote block).
- Provide a visible keyboard focus state (green border plus 3px ring) on every form control.

### Don't
- Don't add a second filled accent color. If green is unavailable, use the outline button, never a new hue.
- Don't use terracotta as a large background or as a button fill outside the homepage hero.
- Don't put drop shadows on cards, tables, badges, or buttons; elevation is not part of this system.
- Don't set Playfair Display on body copy, table cells, labels, or buttons.
- Don't use pure black `#000`; the darkest text is Charcoal `#1C1917`.
- Don't use gradients; every surface and button is a flat fill.
- Don't use emoji as icons in new components; earlier mockups did, the current templates do not (map pins and similar in the job card meta row are the only remaining exception).
- Don't use the legacy blue/indigo palette (`#0d6efd`, `#667eea`) anywhere; it was replaced by this system.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Warm Cream page | `#FAF8F5` | Body background |
| 1 | Pure White card | `#FFFFFF` | Cards, tables, nav, form fields |
| 2 | Cream inset | `#FAF8F5` | Table header, card footer, quote and summary blocks |
| 3 | Sage Tint chip | `#E8F0EC` | Active nav item, positive status badge |
| 4 | Terracotta Tint chip | `#FFF7ED` | Pending and student badge |
| 5 | Error Tint | `#FEF2F2` | Error boxes, delete buttons, negative badges |
| 6 | Deep Forest Green | `#1B4332` | Primary action fill and avatar |

## Elevation

None. Hierarchy is carried by 1px Soft Sand borders and the white-on-cream surface step. The only non-flat effect is the 3px translucent green focus ring on form controls.

## Imagery

The platform uses no photography and no illustration. Identity comes from type and color only. People are represented by a single-letter avatar circle (green fill, white Playfair initial) and companies by a single-letter tile (Warm Cream fill, green Playfair initial). Iconography is minimal; any icon should be a thin 1.5–2px line in Deep Forest Green or Stone Muted.

## Layout

The page model is a full-width white top bar over a Warm Cream canvas, with content in a centered container (960–1120px for list pages, 620–720px for forms). List pages open with a white header card (Playfair H1, one-line description, a stats row, and the primary "+ New" button on the right), followed by an optional filter chip row, then the content as a table or a card list/grid. Form pages open with a breadcrumb, then a single card. The homepage stacks a hero card, a four-up stat grid, a two-column feed (latest jobs and announcements), and a four-up module grid. Section separation is whitespace and hairlines, never colored bands. Mobile: grids collapse at 900px and 520px, and the hero stacks at 820px.

## Agent Prompt Guide

QUICK COLOR REFERENCE
- Page background: `#FAF8F5` Warm Cream
- Card / nav / input surface: `#FFFFFF` Pure White
- Primary text: `#1C1917` Charcoal
- Secondary text: `#57534E` Stone Muted
- Border / divider: `#E7E5E4` Soft Sand
- Primary action: `#1B4332` Deep Forest Green
- Accent (text and links): `#C2410C` Warm Terracotta
- Error: `#B91C1C` Crimson

EXAMPLE COMPONENT PROMPTS
1. Primary button: background `#1B4332`, white text, Plus Jakarta Sans 14px 600, padding 10px 18px, 6px radius, no shadow, hover background `#143325`.
2. List card: white background, 1px `#E7E5E4` border, 10px radius, 24px padding, no shadow. Title in Playfair Display 20px 700 `#1C1917`, subtitle in 14px 600 `#C2410C`, body in 14px `#1C1917` at 1.6 line-height. Footer separated by a 1px `#E7E5E4` top rule.
3. Status badge: 12px 600, padding 4px 10px, 20px radius. Positive: background `#E8F0EC`, text `#1B4332`, border `#C5D9CE`. Pending: background `#FFF7ED`, text `#C2410C`, border `#FED7AA`. Negative: background `#FEF2F2`, text `#B91C1C`, border `#FECACA`.
4. Form input: white background, 1px `#E7E5E4` border, 6px radius, padding 10px 12px, 14px Plus Jakarta Sans. On focus: border `#1B4332` and `box-shadow: 0 0 0 3px rgba(27,67,50,0.12)`.
5. Page header card: white, 1px `#E7E5E4` border, 10px radius, 26px 30px padding, flex row with space-between. Left: Playfair 28px H1, 14px `#57534E` description, stats row with 15px 700 green numbers. Right: primary button.

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-primary: #1B4332;
  --color-primary-hover: #143325;
  --color-accent: #C2410C;
  --color-accent-hover: #9A3412;
  --color-bg: #FAF8F5;
  --color-surface: #FFFFFF;
  --color-text: #1C1917;
  --color-muted: #57534E;
  --color-border: #E7E5E4;
  --color-error: #B91C1C;

  /* Tints (currently inlined in templates) */
  --tint-sage: #E8F0EC;
  --tint-sage-border: #C5D9CE;
  --tint-error: #FEF2F2;
  --tint-error-border: #FECACA;
  --tint-terracotta: #FFF7ED;
  --tint-terracotta-border: #FED7AA;

  /* Typography */
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Radius */
  --radius-control: 6px;
  --radius-card: 10px;
  --radius-hero: 12px;
  --radius-pill: 20px;

  /* Layout */
  --nav-height: 68px;
  --page-max-width: 1120px;
  --form-max-width: 720px;
}
```

> Note: each template currently declares its own copy of the core color variables (primary, accent, bg, surface, text, muted, border, error) in its `<style>` block, and `--color-accent-hover` only on the homepage. The tint, font, radius, and layout variables above are recommended names for a future shared stylesheet; they do not exist in the code yet.
