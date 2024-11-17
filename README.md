# Naslovna strana

**Naziv projekta**: PyPC Manager  
**Autori**: Emir Kusundžija, Faris Milić, Daris Pružan  
**Datum izrade**: 28.10.2024

---

# Sadržaj

- [Kratak opis projekta](#kratak-opis-projekta)
- [Postupak razvoja softvera](#postupak-razvoja-softvera)
  - [Izabrana metodologija](#izabrana-metodologija)
  - [Detaljan plan projekta](#detaljan-plan-projekta)
- [Analiza zahtjeva](#analiza-zahtjeva)
- [Projektovanje sistema](#projektovanje-sistema)
- [Implementacija softvera](#implementacija-softvera)
- [Testiranje softvera](#testiranje-softvera)
  - [Rezultati testiranja](#rezultati-testiranja)
- [Isporuka softvera](#isporuka-softvera)
- [Predrekvizite](#predrekvizite)

---

## Kratak opis projekta

PyPC Manager je projekat koji omogućava praćenje osnovnih informacija o računarskom sistemu, uključujući upotrebu CPU-a, RAM-a i diska. Alat pruža uvid u performanse sistema u stvarnom vremenu, što je korisno za optimizaciju resursa i identifikaciju potencijalnih problema.

---

## Postupak razvoja softvera

### Izabrana metodologija

Za razvoj softverskog rješenja koristićemo **kaskadni model** razvoja. Ovaj model je odabran zbog svoje jednostavnosti i jasno definisanih faza razvoja, što omogućava lakše praćenje napretka i obezbjeđuje kvalitetnu dokumentaciju kroz sve faze.

### Detaljan plan projekta

- **Kritične tačke (milestones)**:
  1. **Početak projekta**: Postavljanje osnova projekta, inicijalizacija repozitorijuma, i instalacija predrekvizita (Datum: 28.10.2024)
  2. **Razrada funkcionalnosti**: Implementacija osnovnih funkcionalnosti za praćenje CPU, RAM i diska (Datum: 05.11.2024)
  3. **Testiranje modula**: Jedinično testiranje svakog modula sistema (Datum: 14.11.2024)
  4. **Finalna verzija i isporuka**: Finalno testiranje i priprema dokumentacije (Datum: 14.11.2024)

- **Uloge članova tima**:
  - **Emir Kusundžija**: Implementacija korisničkog interfejsa i povezivanje sa backend logikom.
  - **Faris Milić**: Razvoj funkcionalnosti za praćenje i prikazivanje podataka o sistemskim resursima.
  - **Daris Pružan**: Pisanje korisničke dokumentacije.

---

## Analiza zahtjeva

Specifikacija softverskih zahtjeva obuhvata sledeće:

- **Funkcionalni zahtjevi**:
  1. Sistem mora omogućiti praćenje osnovnih parametara računarskog sistema (CPU, RAM, disk).
  2. Podaci moraju biti ažurirani u stvarnom vremenu.
  3. Korisnički interfejs mora biti jednostavan i intuitivan.

- **Zahtjevi za veze sa okruženjem**:
  1. Sistem mora raditi na svim platformama koje podržavaju Python i biblioteke `nicegui`.
  2. Podaci treba da budu prikupljeni direktno sa sistema putem dostupnih API-ja.

- **Zahtjevi za performanse**:
  1. Ažuriranje podataka ne smije biti sporije od 1 sekunde.
  2. Minimalna upotreba resursa kako bi se omogućila nesmetana radnja na svim računarima.

---

## Projektovanje sistema

Arhitektura sistema je modularna, gdje su glavni moduli:

1. **Backend modul**: Služi za prikupljanje podataka o CPU, RAM-u i disku.
2. **Frontend modul**: Koristi `nicegui` za prikazivanje podataka korisnicima.
3. **Testiranje i integracija**: Modul za testiranje i validaciju podataka i funkcionalnosti.

Izabrani programski jezik je **Python**, jer omogućava brz razvoj i široku podršku za biblioteke kao što je `psutil` za praćenje resursa i `nicegui` za izradu korisničkog interfejsa.

---

## Implementacija softvera

Programski kôd je napisan u Pythonu i koristi sledeće biblioteke:

- `psutil` za praćenje sistemskih resursa.
- `nicegui` za korisnički interfejs.

Svi moduli su dobro dokumentovani i komentarisani kako bi olakšali dalji razvoj i održavanje.

---

## Testiranje softvera

- **Jedinično testiranje** je sprovedeno za svaki od modula: praćenje CPU-a, RAM-a i diska.
- **Integraciono testiranje** je obuhvatilo povezivanje svih modula u jednu cjelinu i provjeru ispravnosti funkcionalnosti.

### Rezultati testiranja

![Uspješni testovi](images/testiranje.png)

---

## Isporuka softvera

### Predrekvizite

Za instalaciju i upotrebu ovog projekta, potrebno je imati sledeće alate:

1. **[uv](https://github.com/astral-sh/uv)** – Python package manager koji omogućava lako upravljanje Python okruženjem kao i Python verzijama.
2. **[nicegui](https://nicegui.io/)** – Biblioteka za izradu korisničkog interfejsa.

### Instalacija `uv` package i Python managera

#### Na Windows-u:

Otvorite PowerShell i pokrenite sljedeću komandu:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Na macOS i Linux-u:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
