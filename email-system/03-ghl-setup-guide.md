# GHL Setup Guide - Nurture Workflow + Weekly Broadcast

Klik-by-klik instrukcije za podizanje 2 pipeline-a u GHL subaccountu `cHKLqGf6siPAG5tl6B6m`. Pretpostavka: već si prošao file `01-warming-and-dns.md` (DNS verified, sender authenticated, kompliance footer postavljen).

---

## STEP 1 - Kreiraj 12 email template-a

GHL: **Marketing > Emails > Templates > New Template**

Za svaki od 12 emailova iz `02-email-copy.md`:

1. **Template Name**: `Intel Nurture · E{N} · {Topic}` (npr. `Intel Nurture · E01 · Welcome`)
2. **Builder**: izaberi **Plain Text Editor** (ne Drag-n-Drop). Za nurture sequence plain-text dramatično bolje deliverability.
3. **From Name**: `Aleksa from AdVision`
4. **From Email**: `info@aleksaadvision.com`
5. **Reply-To**: `info@aleksaadvision.com`
6. **Subject**: paste subject iz `02-email-copy.md`
7. **Preview Text** (preheader): paste iz `02-email-copy.md`
8. **Body**: paste body. Sačuvaj `{{first_name}}` i `{{unsubscribe_link}}` merge tags.
9. Klikni **Save Template**

Ponovi 12 puta. Pre nego krenes na sledeći korak, idi u **Templates** lista i provjeri da svih 12 ima ispravne subject linije.

---

## STEP 2 - Kreiraj Custom Fields za broadcast

GHL: **Settings > Custom Fields > Add Field**

Kreiraj 8 polja sa tipovima iz tabele:

| Name | Field Type | Placeholder/Default |
|---|---|---|
| `issue_num` | Number | (leave empty) |
| `headline` | Single Line Text | (leave empty) |
| `teaser_line` | Single Line Text | (leave empty) |
| `brief_theme` | Single Line Text | (leave empty) |
| `hook_1` | Single Line Text | (leave empty) |
| `hook_2` | Single Line Text | (leave empty) |
| `hook_3` | Single Line Text | (leave empty) |
| `archive_url` | URL | `https://aleksaadvision.com/intel-access-granted` |

**Bitno**: ova polja će se nalaziti u kontaktu, ali će se **ažurirati programski** od strane RemoteTrigger pre svakog ponedeljaka. Detalji u `04-remotetrigger-extension.md`.

Alternativno (V1 manual): u GHL Email Composer možeš direktno upisati subject+body svake nedelje bez dynamic fields.

---

## STEP 3 - Nurture Workflow (12-email drip)

GHL: **Automation > Workflows > Create Workflow**

### Workflow basic info
- **Workflow Name**: `Intel Nurture · 12-email · 6-week soft drip`
- **Status**: KEEP DRAFT (ne Active dok warming nije gotov)

### Trigger
- **Add Trigger** → **Contact Tag** → **Tag Added**
- **Select Tag**: `trend-subscriber`
- (Opciono) Filter: `niche-fitness` - ako želiš samo fitness opt-ins, ne sve

### Steps (po redosledu)

| # | Action | Settings |
|---|---|---|
| 1 | **Send Email** | Template: `Intel Nurture · E01 · Welcome` |
| 2 | **Wait** | 2 days |
| 3 | **Send Email** | Template: `Intel Nurture · E02 · Hook Specificity` |
| 4 | **Wait** | 3 days |
| 5 | **Send Email** | Template: `Intel Nurture · E03 · Diversity Plateau` |
| 6 | **Wait** | 3 days |
| 7 | **Send Email** | Template: `Intel Nurture · E04 · Andromeda Explainer` |
| 8 | **Wait** | 4 days |
| 9 | **Send Email** | Template: `Intel Nurture · E05 · Pack System` |
| 10 | **Wait** | 4 days |
| 11 | **Send Email** | Template: `Intel Nurture · E06 · Hook Frameworks` |
| 12 | **Wait** | 4 days |
| 13 | **Send Email** | Template: `Intel Nurture · E07 · Fatigue Science` |
| 14 | **Wait** | 4 days |
| 15 | **Send Email** | Template: `Intel Nurture · E08 · Mini Case Study` |
| 16 | **Wait** | 4 days |
| 17 | **Send Email** | Template: `Intel Nurture · E09 · What Algo Wants` |
| 18 | **Wait** | 4 days |
| 19 | **Send Email** | Template: `Intel Nurture · E10 · Soft Audit Mention` |
| 20 | **Wait** | 4 days |
| 21 | **Send Email** | Template: `Intel Nurture · E11 · Audit Example` |
| 22 | **Wait** | 6 days |
| 23 | **Send Email** | Template: `Intel Nurture · E12 · Soft Close` |

Total: 12 emailova / 42 dana. Cadence: dense u prvih 14 dana (5 emailova), prored u poslednje 4 nedelje.

### Send-time optimization
- U GHL Workflow Settings, omogući **Send Time Optimization** ako postoji u tvojoj GHL verziji
- Ako ne, postavi Send Time: **Tuesday-Thursday 09:00-11:00 recipient timezone** (highest open rates za B2B)

### Reply branch (opciono ali korisno)
Ako neko odgovori na bilo koji email u sekvenci sa rečju "AUDIT":
- Add **Conditional Branch**: If `Reply contains "AUDIT"` (case insensitive)
- → **Add Tag**: `audit-requested`
- → **Send Internal Notification** to Aleksa (email/SMS): "AUDIT request from {{first_name}} {{last_name}} ({{email}})"
- → **End Workflow** (exit nurture)

### Save & test
- Klikni **Save** ali OSTAVI **Status: Draft**
- Test: dodaj sebe kao kontakt sa tagom `trend-subscriber` → vidi da li workflow okida na test contact-u (Workflow > Test mode)

---

## STEP 4 - Weekly Broadcast Workflow

Dva načina implementacije. Preporučujem **Option A** za V1 (jednostavnije, ne zahteva API integraciju).

### Option A: GHL native broadcast (manual ili scheduled)

GHL: **Marketing > Emails > Campaigns > Create Campaign**

- **Campaign Name**: `Weekly Intel Drop · Issue {N}` (zameni N pre svakog send-a)
- **Recipient list**: Filter contacts by tag = `trend-subscriber`
- **Template**: koristi `02-email-copy.md` Weekly Broadcast template
- **Schedule**: Monday 09:00 UTC (ili tvoja vremenska zona ekvivalent)
- **Subject + Body**: ručno popuni svake nedelje sa this week's issue title/hooks

Tradeoff: Aleksa mora svakog ponedeljka da uđe u GHL i izmeni template + send. ~5 min/nedelja, ali nije zero-touch.

### Option B: GHL API-triggered broadcast (zero-touch)

RemoteTrigger nakon PHASE 2 (publish) zove GHL API da update-uje `issue_num`, `headline`, `hook_1-3`, `teaser_line`, `brief_theme` na svim kontaktima sa tagom `trend-subscriber`, pa pokrene workflow koji šalje email.

Detalji u `04-remotetrigger-extension.md`.

Workflow setup za Option B:
- **Automation > Workflows > Create Workflow**
- **Name**: `Weekly Broadcast · Triggered by API`
- **Status**: KEEP DRAFT
- **Trigger**: **Webhook** (GHL daje URL koji RemoteTrigger zove)
- **Filter**: Contact has tag `trend-subscriber`
- **Step 1**: **Send Email** → Template: `Weekly Intel Drop · Dynamic`

Template setup za Option B:
- **Marketing > Emails > Templates > New Template**
- **Template Name**: `Weekly Intel Drop · Dynamic`
- **From / Reply-To**: kao kod nurture-a
- **Subject**: `issue {{contact.issue_num}}: {{contact.headline}}`
- **Preview Text**: `{{contact.teaser_line}}`
- **Body**: paste body iz `02-email-copy.md` Weekly Broadcast Template (sa svim {{contact.X}} merge tags)

---

## STEP 5 - Test send protokol (PRE go-live)

NE aktiviraj nijedan workflow dok ne uradiš ovaj test:

1. Kreiraj test contact u GHL: `aki.masic01@gmail.com` (ili druga adresa do koje imaš pristup)
2. Dodaj tag `trend-subscriber`
3. Workflow `Intel Nurture` → desni klik → **Run Test** → izaberi test contact
4. Otvori inbox → email treba da stigne za 1-2 minuta
5. Verifikuj:
   - From: `Aleksa from AdVision <info@aleksaadvision.com>` ✓
   - Subject ispravan ✓
   - Preview text se vidi ✓
   - `{{first_name}}` zamenjeno sa stvarnim imenom ✓
   - `{{unsubscribe_link}}` aktivan ✓
   - Footer ima fizičku adresu ✓
   - Mobile render OK (otvori na telefonu) ✓
6. Klikni unsubscribe link → vidi šta se dešava → undo unsubscribe ako treba
7. **Reply na email** → reply trebao bi otići na `info@aleksaadvision.com` (proveriš)

Posle test-a, briši test contact iz GHL ili stavi ga u test segment.

---

## STEP 6 - Activation order

Posle warming-a (Faza 4 iz `01-warming-and-dns.md`), aktiviraj redom:

1. **Day 22** (kraj warming-a) - Aktiviraj `Intel Nurture` workflow → samo NOVI opt-ins kreće u sequence
2. **Day 30** (10 dana posle nurture aktivacije, monitor metrike) - Aktiviraj `Weekly Broadcast`

NE backfill-uj postojeću listu u Nurture (one ne treba da prime E1 "you're in" jer su već subscriberi). Backfill-uj samo ako želiš da im pošalješ E10-E12 (audit pitch). Ali za V1 - ne. Samo novi opt-ins.

---

## STEP 7 - Monitoring (nedeljni check)

Posle aktivacije, svake nedelje pogledaj **GHL > Email Stats**:

| Metric | E1 (Welcome) target | E2-E9 (Value) target | E10-E12 (Soft pitch) target |
|---|---|---|---|
| Open rate | >40% | >25% | >20% |
| Click rate | >5% | >3% | >5% |
| Reply rate | >1% | >0.5% | >2% (E12 reply trigger) |
| Unsubscribe | <0.5% | <0.5% | <1% |

Ako E1 open rate <30% - GHL placement je u promotions/spam, treba dodatno warming
Ako E10-E12 unsubscribe >2% - pitch je preagresivan ili prerano u sequence-u, treba pomeriti dalje

---

## Rollback plan

Ako bilo kada deliverability počne da pada (open rate <15% za 7 dana zaredom):

1. Pause oba workflow-a
2. Stop dodavanje novih kontakata u nurture
3. Reduce volume na 5-10 emaila/dan iz testing inboxa
4. Vrati se u Faza 1 warming protokol (manual seed sa replies)
5. Wait 7 dana, monitor Postmaster Tools
6. Kad metrike vrate na zelenu, postupno reaktiviraj

---

## Quick reference

| Što treba | Gde u GHL | Akcija |
|---|---|---|
| Email templates | Marketing > Emails > Templates | 12 nurture + 1 broadcast |
| Custom fields | Settings > Custom Fields | 8 polja za broadcast (Option B) |
| Nurture workflow | Automation > Workflows | Trigger: Tag Added `trend-subscriber` |
| Broadcast workflow | Automation > Workflows | Trigger: Webhook (Option B) ili manual Campaign |
| Email service | Settings > Email Services | LC Email aktivan, sender authenticated |
| Compliance | Settings > Business Profile | Adresa + unsubscribe enabled |
| Sender verification | Settings > Email Services > Domain Auth | DKIM 3 CNAME-a verified |
