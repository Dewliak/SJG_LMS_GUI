## 📘 Felhasználói kézikönyv — SJG LMS

<br/><br/>
### 🖥 Alkalmazás leírása
Ez az alkalmazás egy könyvkezelő rendszer grafikus felülettel, amely a következőket teszi lehetővé:

- Könyvek nyilvántartása, hozzáadása, módosítása és törlése  
- Könyvek kölcsönzése és visszavétele  
- Könyvek azonosítása QR-kóddal  
- A könyvek és felhasználók adatainak kezelése (pl. `pandas` segítségével táblázatos formában)

A program a grafikus felületet a `NiceGUI` könyvtár segítségével jeleníti meg.


> ⚠️ A program bizonyos modulok miatt lassan indul, így az elindulás eltarthat 10-20 másodpercig is


---

<br/><br/>
### 📦 Rendszerkövetelmények

- Windows 10 vagy újabb operációs rendszer
- Internetkapcsolat (a Google API használatához, ha engedélyezve van)
- A program mappájában a következő fájloknak kell lenniük:
  - `sjg-lms.exe`
  - `credentials.json`
  - `secrets.json`

> ⚠️ A `credentials.json` és `secrets.json` fájlok **nélkül a program nem tud csatlakozni az adatbázishoz**.

---
<br/><br/>
### 📁 Mappa szerkezete

Amikor megkapod a programot, az így fog kinézni:

SJG-LMS/ \
│ \
├── generated_qr_images \
└── sjg-lms.exe \

Add hozzá a **credentials.json** és a **secrets.json** fájlokat

SJG-LMS/ \
│ \
├── generated_qr_images \
├── sjg-lms.exe \
├── credentials.json \ 
└── secrets.json \ 


---

<br/><br/>
### ▶️ A program indítása

1. Másold a teljes mappát (`Konyvkezelo`) a számítógépedre.
2. Dupla kattintás a `sjg-lms.exe` fájlra.
3. Az alkalmazás elindul, és megnyitja a grafikus felületet a böngésződben vagy beágyazott ablakban.

---
<br/><br/>
### 📋 Használati útmutató

Miután a program elindul, a felület tetején megjelennek a fő menüpontok. Az egyes oldalak funkciói a következők:

#### 🏠 Főoldal (`main_page`)
- Ez az alkalmazás kezdőoldala, ahová belépés után érkezel.
- Itt általános információkat és statisztikákat láthatsz a könyvtár adatbázisáról.
- Gyors gombokkal elérhetők a legfontosabb funkciók (pl. új könyv hozzáadása, kölcsönzés, visszavétel).

#### 📚 Könyvkezelés (CRUD oldal) (`Books/könyvek`)
- Ezen az oldalon tudod a meglévő könyveket **listázni, szerkeszteni vagy törölni**.
- A könyvek táblázatos formában jelennek meg (`pandas` adatszerkezetekből töltve).
- Lehetőség van a könyvek adatait frissíteni (cím, szerző, kiadó, ISBN stb.)
- a filtereknek köszönhetően egyszerűen filtrálni lehet a könyveket
- Egy kattintással törölhetsz is egy könyvet az adatbázisból.

#### ➕ Új könyv hozzáadása (`Add book/Könyv hozzáadása`)
- Itt új könyveket vihetsz fel az adatbázisba.
- Kitölthető mezők például: **cím, szerző, ISBN, példányszám**.
- A mentés után a könyv automatikusan megjelenik a Books/Könyvek listában is.
- A rendszer automatikusan hozzárendel egy azonosítót (ID-t) az új könyvhöz.

#### 📷 QR-kód generálás (`QR codes/ QR kódok`)
- Ki választasz egy (vagy több könyvet), majd megadodd, hogy az adott könyvből mennyi qr-kódot szeretnél generálni, majd ezeket egy .docx fájlba generálja le.

#### 📥 Könyv visszavétele (Return book/ Könyv visszaadása)
- Ez az oldal a kölcsönzött könyvek visszavételére szolgál.
- könyv kiválasztásával a listából, majd a 'Return book' gomb megnyomásával a könyv visszavettnek tekintett
- A visszavétel után a könyv státusza frissül az adatbázisban(a használt könyvek száma 1-el csökken)

---
<br/><br/>

### ⚠️ Fontos tudnivalók

- **Ne töröld a `credentials.json` és `secrets.json` fájlokat.** Ezek nélkül a rendszer nem tud hitelesíteni és adatokat elérni.
- Az adatok módosítása automatikusan mentésre kerül a háttérrendszerben.
- A program használatához aktív internetkapcsolat szükséges, ha a távoli adatbázist használja.

---
<br/><br/>
### ❓ Hibaelhárítás

| Hibaüzenet                          | Lehetséges ok                             | Megoldás                                |
|------------------------------------|-------------------------------------------|------------------------------------------|
| „credentials.json nem található”   | Hiányzik a fájl                           | Másold a fájlt a `main.exe` mellé         |
| „ModuleNotFoundError”               | Hiányzik egy modul a buildből             | Töltsd újra a legfrissebb `.exe` fájlt    |
| Nem tölt be a felület               | Nincs internetkapcsolat                   | Csatlakozz az internetre és próbáld újra |

---
<br/><br/>
### 📧 Kapcsolat

Ha problémát tapasztalsz a használat során, fordulj a fejlesztőhöz.
