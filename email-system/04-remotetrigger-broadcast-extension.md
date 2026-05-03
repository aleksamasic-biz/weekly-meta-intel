# RemoteTrigger PHASE 4 - Auto Broadcast (Disabled by Default)

Cilj: kad Issue N publish-uje na sajtu (PHASE 2 OK), trigger automatski:
1. Update-uje GHL Custom Fields na svim `trend-subscriber` kontaktima sa this week's hooks
2. Pokrene GHL Webhook workflow koji šalje broadcast email

**Stanje sad: DISABLED**. Ne dirati trigger prompt dok Aleksa ne kaže "uključi broadcast" posle završenog warming-a.

---

## Zašto je disabled

GHL email warming nije završen. Slanje 100+ emaila bez warming-a = direktno u spam folder + dugotrajno oštećenje sender reputation-a.

Aktivacija PHASE 4 zahteva:
- ✅ DNS records postavljeni (SPF/DKIM/DMARC) - vidi `01-warming-and-dns.md`
- ✅ GHL sender domain authenticated (zelena kvačica na DKIM CNAMEs)
- ✅ Faza 1-3 warming protokol završeni (~21 dan)
- ✅ Open rate >25% u Fazi 3
- ✅ GHL `Weekly Broadcast · Triggered by API` workflow setup-ovan i testiran sa fake webhook
- ✅ Aleksa eksplicitna komanda "go live broadcast"

---

## Kako se aktivira (kad bude vreme)

### Korak 1 - Create GHL Webhook
U GHL workflow `Weekly Broadcast · Triggered by API`:
- Trigger: **Webhook**
- GHL će ti dati webhook URL u formi: `https://services.leadconnectorhq.com/hooks/{location_id}/webhook-trigger/{webhook_id}`
- Copy ovaj URL - biće potreban u trigger prompt-u kao `{{GHL_WEBHOOK_URL}}`

### Korak 2 - Test webhook ručno
```bash
curl -sk -X POST "{{GHL_WEBHOOK_URL}}" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_num": 999,
    "headline": "test broadcast - ignore",
    "teaser_line": "this is a webhook test",
    "brief_theme": "testing the webhook",
    "hook_1": "test hook 1",
    "hook_2": "test hook 2",
    "hook_3": "test hook 3",
    "tag_filter": "test-only-tag"
  }'
```

GHL bi trebalo da pošalje email samo na kontakte sa tag-om `test-only-tag` (kreiraj 1 test contact sa tim tagom). Verify deliverability na test inbox.

### Korak 3 - Update RemoteTrigger prompt

U trigger `trig_01SKamL3i6MfJzUbeF8gmtV4`, dodaj na kraj postojećeg prompt-a (posle FINAL NOTES sekcije) sledeći blok:

```
=========================================
PHASE 4: BROADCAST EMAIL (NEW)
=========================================

Trigger broadcast email to all contacts tagged trend-subscriber via GHL webhook.

CONFIG:
- GHL_WEBHOOK_URL: <PASTE WEBHOOK URL FROM GHL HERE>
- BROADCAST_ENABLED: true

If BROADCAST_ENABLED is false, skip this entire phase.

STEP 4.1: Construct broadcast payload from the issue data you just published.

Compute these from the JSON object you pushed in PHASE 2:
- ISSUE_NUM = NEW.num
- HEADLINE = NEW.title (use as is, max 40 chars - if longer, shorten with judgment)
- TEASER_LINE = NEW.summary (use as is, max 90 chars)
- BRIEF_THEME = 1-line summary derived from NEW.featuredDesc (strip HTML, take core message)
- HOOK_1, HOOK_2, HOOK_3 = the first 3 hooks from NEW.contentHtml Winning Hooks section. Extract just the hook label/category (one line each, under 80 chars). Example: "Specific Numerical hooks (e.g. 'I lost 22 lbs without giving up wine')"

STEP 4.2: POST to GHL webhook:

```bash
WEBHOOK_PAYLOAD=$(python3 -c "
import json
payload = {
    'issue_num': $ISSUE_NUM,
    'headline': '''$HEADLINE''',
    'teaser_line': '''$TEASER_LINE''',
    'brief_theme': '''$BRIEF_THEME''',
    'hook_1': '''$HOOK_1''',
    'hook_2': '''$HOOK_2''',
    'hook_3': '''$HOOK_3''',
    'tag_filter': 'trend-subscriber'
}
print(json.dumps(payload))
")

curl -sk --ssl-no-revoke -X POST "$GHL_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$WEBHOOK_PAYLOAD" > /tmp/broadcast_resp.json

cat /tmp/broadcast_resp.json
```

STEP 4.3: Verify webhook accepted

Webhook should return HTTP 200 with `{"status":"received"}` or similar. If response indicates error (4xx/5xx), capture the error and add to PHASE 3 confirmation email body so Aleksa knows broadcast didn't go.

STEP 4.4: Update PHASE 3 confirmation email

Add new section to the [AUTO-PUBLISHED] email body, before === META ===:

```
=== BROADCAST STATUS ===

Broadcast triggered: YES
Sent to tag: trend-subscriber
Webhook response: <paste response from STEP 4.3>
Estimated reach: <count of contacts with tag trend-subscriber, fetch via GHL API GET /contacts/search>
```

If broadcast disabled (BROADCAST_ENABLED=false), the section reads:
```
=== BROADCAST STATUS ===

Broadcast: DISABLED (BROADCAST_ENABLED flag is off)
To enable: edit RemoteTrigger trig_01SKamL3i6MfJzUbeF8gmtV4 and set BROADCAST_ENABLED=true
```

ERROR HANDLING:
- If webhook fails: send error to email body, do NOT retry (one shot, manual intervention if fail)
- If hooks extraction fails: skip with note "hooks could not be parsed from contentHtml"
```

### Korak 4 - Test PHASE 4 end-to-end

- Sa BROADCAST_ENABLED=false, reci Claude-u u session-u: "Test broadcast PHASE 4 sa fake webhook URL https://webhook.site/abc"
- Webhook.site će ti pokazati šta je trigger poslao
- Verify: payload struktura ispravna, sva polja popunjena

Tek kad je test prošao, prebaci na pravi GHL webhook URL i flip BROADCAST_ENABLED=true.

---

## Sledeći ponedeljak posle aktivacije

- **07:00 UTC**: PHASE 1-2 publish-uje Issue N (kao i sad)
- **07:01 UTC**: PHASE 3 šalje confirmation Gmail draft Aleksi
- **07:02 UTC**: PHASE 4 zove GHL webhook → workflow okida → email šalje subscriberima
- **~07:05 UTC**: Subscriberi primaju "issue N: {headline}" email u inbox
- **07:30 UTC**: Aleksa otvara confirmation Gmail draft, vidi BROADCAST STATUS sekciju, potvrdi reach broj

---

## Rollback (ako broadcast ne radi)

Ako vidiš u confirmation emailu da broadcast pukao 2 nedelje zaredom:

1. Edit RemoteTrigger prompt → set `BROADCAST_ENABLED: false`
2. Update prompt
3. Sledeći ponedeljak PHASE 4 se preskače
4. Reci Claude-u u session-u "debug broadcast PHASE 4" - proveriće webhook, GHL workflow status, recent email logs

---

## Cost note

GHL ne naplaćuje per-email u Pro+ planu. Webhook trigger je free. Custom field updates su free.

Email service cost: 0 incremental.

Token cost po PHASE 4 run-u: ~500-1000 tokena (parse contentHtml, extract hooks, POST). Zanemarljivo.

---

## Status check

Trenutno stanje (2026-05-03):
- PHASE 4 NIJE DODATA u trigger prompt
- BROADCAST_ENABLED flag NE POSTOJI
- Trigger trenutno kompletan PHASE 1-3 setup, broadcast = manual u GHL UI

Da bi se aktivirao, neko (Aleksa ili Claude u budućoj session-i) treba:
1. Završiti email warming (vidi `01-warming-and-dns.md`)
2. Setup-ovati GHL `Weekly Broadcast` workflow + email template (vidi `03-ghl-setup-guide.md` STEP 4 Option B)
3. Dodati PHASE 4 blok u trigger prompt po instrukcijama gore
4. Set BROADCAST_ENABLED=true
