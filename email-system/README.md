# Email System - Weekly Meta Intel Freebie

Kompletan email setup za Advision freebie subscribere. Dva pipeline-a:
1. **Welcome / Long Nurture** - 12 emailova preko 6 nedelja, soft value-first, no hard pitch
2. **Weekly Broadcast** - svaki ponedeljak posle Issue publish-a

**Status: SETUP MODE.** Sve spremno za implementaciju, ali NE šaljemo emailove dok GHL warming nije završen.

---

## Kako koristiti ovaj folder

Idi redom kroz fajlove:

| # | Fajl | Šta radiš |
|---|---|---|
| 1 | [`01-warming-and-dns.md`](./01-warming-and-dns.md) | DNS records (SPF/DKIM/DMARC), GHL sender setup, 4-faze warming protokol (~21 dan) |
| 2 | [`02-email-copy.md`](./02-email-copy.md) | 12 nurture email copies + weekly broadcast template, copy-paste ready |
| 3 | [`03-ghl-setup-guide.md`](./03-ghl-setup-guide.md) | Klik-by-klik GHL UI: kreiraj 12 templatesa + 8 custom fields + 2 workflow-a |
| 4 | [`04-remotetrigger-broadcast-extension.md`](./04-remotetrigger-broadcast-extension.md) | RemoteTrigger PHASE 4 dodatak (DISABLED dok warming nije gotov) |

---

## Brzi pregled - šta je kreirano

### Pipeline 1: Long Nurture (12 emailova / 42 dana)

| # | Day | Topic | Pitch |
|---|---|---|---|
| 1 | 0 | Welcome | None |
| 2 | 2 | Hook specificity ("Sarah beats real results") | None |
| 3 | 5 | 2 hero ads is the trap (creative volume) | None |
| 4 | 8 | What changed in March (Andromeda explainer) | None |
| 5 | 12 | The Pack System breakdown | None |
| 6 | 16 | 4 hooks that work in 2026 | None |
| 7 | 20 | Why ads die in 7 days (creative fatigue) | None |
| 8 | 24 | Mini case study (anonymized e-com) | None |
| 9 | 28 | What the algo wants now (Andromeda signals) | None |
| 10 | 32 | How I think about audits | SOFT (mention) |
| 11 | 36 | What an audit looks like (sample) | SOFT (demo) |
| 12 | 42 | If you ever want a look (reply AUDIT) | SOFT (close) |

**Tonal rule:** E1-E9 = zero ask, pure value. E10-E12 = soft "no pressure" mention with reply trigger.

### Pipeline 2: Weekly Broadcast (1 template + dynamic content)

Šalje se svaki ponedeljak ~09:00 UTC (07:00 publish + 2h buffer).

Subject: `issue {{ISSUE_NUM}}: {{HEADLINE}}`
Body: 80-150 reči sa 3 hook teasera + link na archive.

Dynamic content dolazi iz this week's published issue (RemoteTrigger PHASE 4 update-uje GHL custom fields pre slanja). V1 može da se radi i ručno u GHL Email Composer-u.

---

## Aktivacija - redosled koraka

```
[ ] 1. DNS setup (SPF + DKIM + DMARC) - vidi 01-warming-and-dns.md
    └─ DKIM 3 CNAME-a iz GHL UI
    └─ SPF: v=spf1 include:mailgun.org ~all
    └─ DMARC: v=DMARC1; p=none; rua=mailto:info@aleksaadvision.com

[ ] 2. GHL sender authentication
    └─ Settings > Email Services > Domain Authentication > verify

[ ] 3. GHL Business Profile + Compliance (CAN-SPAM)
    └─ Settings > Business Profile > add address + sender info

[ ] 4. Kreiraj 12 email templates (02-email-copy.md → 03-ghl-setup-guide.md STEP 1)

[ ] 5. Kreiraj 8 custom fields (03-ghl-setup-guide.md STEP 2)

[ ] 6. Kreiraj Nurture workflow (DRAFT mode) (03-ghl-setup-guide.md STEP 3)

[ ] 7. Kreiraj Broadcast workflow (DRAFT mode, Option A ili B) (03-ghl-setup-guide.md STEP 4)

[ ] 8. Test send svim test contact-ima (03-ghl-setup-guide.md STEP 5)

═══ WARMING (21 dan) ═══

[ ] 9. Faza 1 (Days 1-3): Manual seed sends - 5-10 emaila/dan ka svojim test inboxima
    └─ Mora open + reply na svaki

[ ] 10. Faza 2 (Days 4-10): GHL test sends - 2-3/dan ka 5-10 test inboxa

[ ] 11. Faza 3 (Days 11-21): Aktiviraj Nurture workflow za nove opt-ins SAMO
    └─ Monitor open rate u GHL Email Stats - target >25%

[ ] 12. Faza 4 (Day 22+): Aktiviraj Weekly Broadcast workflow

═══ AUTOMATION ═══

[ ] 13. (Opciono) Aktiviraj RemoteTrigger PHASE 4 (zero-touch broadcast)
    └─ Vidi 04-remotetrigger-broadcast-extension.md
    └─ Postavi GHL_WEBHOOK_URL u trigger prompt
    └─ Set BROADCAST_ENABLED=true

[ ] 14. Monitor weekly: open >25%, click >3%, unsubscribe <0.5%
```

---

## Trenutno stanje (2026-05-03)

- ✅ Copy generisan (email-copywriter agent, banned-word audit prošao)
- ✅ DNS / warming guide napisan
- ✅ GHL UI setup guide napisan
- ✅ RemoteTrigger PHASE 4 dokumentovan (NE aktiviran)
- ⏳ DNS records - nisu postavljeni (Aleksa korak)
- ⏳ GHL templates / workflows - nisu kreirani (Aleksa korak)
- ⏳ Warming - nije počet (Aleksa korak)
- ⏳ PHASE 4 - DISABLED u trigger-u (Aleksa korak posle warming-a)

---

## Procenjeno vreme

- DNS setup: 30 min (jednom)
- GHL templates + workflows: 2-3h (jednom)
- Warming: 21 dan kalendarski, ~10 min/dan rad
- PHASE 4 aktivacija: 30 min (jednom, posle warming-a)

**Total active rad: ~6h preko 25 dana, posle čega sistem radi sam svake nedelje.**

---

## Resume komande za buduće session-e

- **"Resume - pomozi mi da postavim DNS za freebie email sistem"** → idi kroz 01-warming-and-dns.md sa Aleksom
- **"Resume - kreiramo email templates u GHL"** → 03-ghl-setup-guide.md STEP 1
- **"Resume - gotov sam sa warming-om, aktiviraj PHASE 4"** → 04-remotetrigger-broadcast-extension.md aktivacija
- **"Resume - broadcast pukao, debug"** → fetch RemoteTrigger logs + GHL email stats + rollback ako treba

---

## Bitno - što NIJE u ovom sistemu (a možda treba)

- **Re-engagement sequence** za subscribere koji nisu otvorili 4+ nedelje zaredom (sleeper wake-up)
- **Audit booking confirmation** sequence (kad neko bookuje audit, šta dobija pre poziva?)
- **Onboarding sequence za audit attendees** (posle calla, da li ide u nurture za "not yet bought"?)
- **Re-broadcast za missed weekly emailove** (ako neko ne otvori issue 5, da li dobija reminder?)

Ovo je V1 - namerno simple. Ako V1 radi (>25% open na Issue Drop emails posle 4 nedelje), V2 dodaje gore navedene petlje.
