# Email Infrastructure Setup - Weekly Meta Intel Freebie

Cilj: pripremiti `info@aleksaadvision.com` za broadcast i nurture iz GHL-a, sa inbox placement >85% pre prvog real send-a. Cela faza je **bez ijednog send-a na realne subscribere** dok checklist nije zelena.

---

## 1. DNS records (postavi na DNS provider-u za `aleksaadvision.com`)

GHL koristi šared sender pool by default. Da bi `info@aleksaadvision.com` bio prepoznat kao legit sender (a ne forwarded preko GHL-a), moraš postaviti SPF / DKIM / DMARC.

### 1.1 SPF (TXT record)
- **Host**: `@` (root domain)
- **Value**: `v=spf1 include:mailgun.org include:_spf.google.com ~all`
- **Note**: GHL u 2026 koristi Mailgun za outbound. Ako u GHL UI vidiš drugačiji include domain, koristi taj. Google se dodaje da info@ ostane funkcionalan u Gmail interfejsu.

Provera: `dig TXT aleksaadvision.com +short` treba da vrati liniju koja sadrži `v=spf1`.

### 1.2 DKIM (CNAME records - GHL generiše ključeve)
- U GHL UI: **Settings > Email Services > Dedicated Domain & IP > Add Domain**
- GHL će generisati 2-3 CNAME-a (npr. `mail._domainkey`, `pic._domainkey`, `s1._domainkey`)
- Dodaj svaki CNAME na DNS provider tačno kako GHL kaže (host i value)
- Vrati se u GHL UI i klikni **Verify Domain** - treba zelena kvačica

### 1.3 DMARC (TXT record)
- **Host**: `_dmarc`
- **Value (start safe)**: `v=DMARC1; p=none; rua=mailto:info@aleksaadvision.com; pct=100; sp=none`
- Kad inbox placement bude stabilan (~2 nedelje), prebaci na `p=quarantine`, kasnije na `p=reject`

### 1.4 MX record (samo ako želiš da info@ prima emailove)
- Već postoji u Google Workspace verovatno. Ne diraj ako Aleksa već koristi Gmail za info@.

---

## 2. GHL Email Service activation

U GHL subaccountu `cHKLqGf6siPAG5tl6B6m`:

1. **Settings > Email Services > LC Email** - proveri da je aktivirano (default je da, ali bilo je slučajeva da subaccount nema)
2. Ako je deactivated - aktiviraj na **Settings > Subscription** ili kontaktiraj GHL support
3. **Settings > Business Profile**:
   - Business Name: `AdVision`
   - From Name: `Aleksa from AdVision`
   - From Email: `info@aleksaadvision.com`
   - Reply-To: `info@aleksaadvision.com`
4. **Settings > Email Services > Sender Email** - dodaj i verifikuj `info@aleksaadvision.com`

---

## 3. Sender domain verification

U GHL: **Settings > Email Services > Domain Authentication**

- Klikni **Authenticate Domain** > unesi `aleksaadvision.com`
- GHL daje 3 CNAME-a (DKIM) - postavi na DNS (već gore u 1.2)
- Klikni **Verify** dok ne dobiješ zelenu kvačicu na sve 3
- **Compliance**: u **Settings > Business Profile > Compliance** dodaj fizičku adresu kompanije (CAN-SPAM/GDPR - obavezno u footer-u svakog emaila)

---

## 4. Footer sa unsubscribe (ovo se mora pojaviti u SVAKOM emailu)

GHL automatski dodaje `{{unsubscribe_link}}` ako je **Email Compliance** enabled. Verifikuj:

```
AdVision · Belgrade, Serbia
You're receiving this because you opted in at aleksaadvision.com/intel
Unsubscribe: {{unsubscribe_link}}
```

Bez ovoga inbox provideri šalju u spam, plus zakonski problem (CAN-SPAM, GDPR).

---

## 5. Warming protokol - `info@aleksaadvision.com`

**Pravilo**: novi domain mora poslati ~30 emaila dnevno kroz 2-3 nedelje pre nego što se može slati u stotine. Pokušaj da pošalješ broadcast 200+ ljudi prvi dan = guaranteed spam folder.

### Faza 1 - Manual seed (Dani 1-3)
- Pošalji 5-10 emaila/dan iz `info@aleksaadvision.com` ka **realnim adresama koje će otvoriti i odgovoriti**:
  - Tvojim ličnim Gmail/Outlook/Yahoo adresama (3-4 adrese)
  - 2-3 prijatelja kojima ćeš reći "klikni Reply, kucaj 'thanks'"
- Subject: bilo šta lično ("Test from Aleksa", "Kafa sledeće sedmice?")
- **Cilj**: prvi 30-50 emaila moraju biti otvoreni + reply-ovani. To uči Google/Microsoft da `info@aleksaadvision.com` šalje human-to-human.

### Faza 2 - GHL test send-ovi (Dani 4-10)
- U GHL napravi test workflow koji šalje 1 email na 5-10 test contacta (svoje + prijatelja)
- Šalji 2-3 puta dnevno
- Svaki put: kada email stigne, otvori → scroll na dno → klikni link → reply
- **Cilj**: 50-100 inbox interakcija sa GHL-poslanog emaila

### Faza 3 - Mali real list (Dani 11-21)
- Aktiviraj nurture workflow ali **samo za nove opt-ins** (ne backfill na postojeću listu)
- Volume target: 10-30 emaila/dan iz nurture sequence
- Monitor **GHL > Email Stats**:
  - Open rate target: >25% (manje znači spam folder)
  - Bounce rate: <2%
  - Spam complaints: <0.1%

### Faza 4 - Full send (Dan 22+)
- Aktiviraj weekly broadcast za sve subscribere sa tagom `trend-subscriber`
- Sada možeš slati 100-500/nedelja bez problema

### Warming alat (preporuka, ne mora)
- **Mailwarm.com** ili **Lemwarm** - automatski šalje 20-30 emaila/dan tvojoj adresi i drugim warming inboxima koji otvaraju + odgovaraju
- ~$30-50/mes
- Ubrzava warming sa 21 dan na ~10 dana
- Aleksa: SAMO ako ćeš slati 500+ ljudi/nedelja u skoroj budućnosti. Inače skip.

---

## 6. Pre-send testing protocol

Pre svakog NOVOG emaila koji ide u sequence ili broadcast:

1. **Mail-tester.com** test
   - Pošalji email na adresu koju Mail-tester generiše
   - Score >9.0/10 = OK; <8 = popraviti
   - Najčešći problemi: spam-trigger reči, neuravnotežen text/image ratio, nedostatak unsubscribe linka

2. **GlockApps** ili **Mailmeteor inbox test**
   - Šalje na 30+ test inboxa (Gmail, Outlook, Yahoo, AOL, etc.)
   - Vidiš inbox vs spam vs promotions placement
   - Cilj: >85% inbox

3. **Banned words check** (per memory feedback)
   - NE koristi: `for you`, `all`, `call`, `money`, `off`, `won`, `open`, `offer`, `promise`, `stop`
   - Ovo je per Mailmeteor 2026 spam trigger lista
   - Audit svaki email pre nego ide u GHL

4. **Em dash check**
   - Ctrl+F za `-` (U+2014) u svakom email body-ju
   - Hard rule: nigde em dash. Hyphen, colon, period.

---

## 7. Monitoring dashboard

Posle Faze 4 (full send aktivan), proveravaj nedeljno:

| Metric | Target | Crveni alarm |
|---|---|---|
| Open rate | >25% | <15% (warming gone bad) |
| Click rate | >3% | <1% (copy ne radi) |
| Reply rate | >0.5% | 0% (signal "ne osećaju te kao realnu osobu") |
| Bounce rate | <2% | >5% (lista loša ili domain reputation pao) |
| Unsubscribe rate | <0.5% per send | >2% (preagresivan content) |
| Spam complaint | <0.1% | >0.3% (deliverability će propasti za nedelju dana) |

Gde pratiš:
- **GHL > Email Stats**: open/click/bounce/unsub po campaign-u
- **Google Postmaster Tools** (besplatno, treba domain verification): inbox placement Gmail subscriberima
- **postmaster.live.com**: za Outlook/Hotmail subscribere

---

## Quick start (kad imaš 30 min)

1. Postavi SPF + DKIM (3 CNAME-a iz GHL UI) + DMARC TXT na `aleksaadvision.com` DNS
2. U GHL: Settings > Email Services > Domain Authentication > verify
3. U GHL: Business Profile > sender info + adresa (compliance footer)
4. Pošalji 5 emaila iz GHL na 5 svojih test inboxa, otvori sve, klikni link, reply
5. Ponovi 3 dana zaredom (Faza 1)
6. Onda kreni sa nurture workflow aktivacijom za nove opt-ins (Faza 3)

**Ne aktiviraj weekly broadcast dok ne prođeš Fazu 3 sa open rate >25%.**
