## 📘 Felhasználói kézikönyv — SJG LMS

### 🖥 Alkalmazás leírása
Ez az alkalmazás egy könyvkezelő rendszer grafikus felülettel, amely a következőket teszi lehetővé:

- Könyvek nyilvántartása, hozzáadása, módosítása és törlése  
- Könyvek kölcsönzése és visszavétele  
- Könyvek azonosítása QR-kóddal  
- A könyvek és felhasználók adatainak kezelése (pl. `pandas` segítségével táblázatos formában)

A program a grafikus felületet a `NiceGUI` könyvtár segítségével jeleníti meg.

---

### 📦 Rendszerkövetelmények

- Windows 10 vagy újabb operációs rendszer
- Internetkapcsolat (a Google API használatához, ha engedélyezve van)
- A program mappájában a következő fájloknak kell lenniük:
  - `main.exe`
  - `credentials.json`
  - `secrets.json`

> ⚠️ A `credentials.json` és `secrets.json` fájlok **nélkül a program nem tud csatlakozni a távoli adatforráshoz**.

---

### 📁 Mappa szerkezete

Amikor megkapod a programot, az így fog kinézni:

Amikor megkapod a programot, az így fog kinézni:

Konyvkezelo/
│
├── main.exe
├── credentials.json
└── secrets.json


---

### ▶️ A program indítása

1. Másold a teljes mappát (`Konyvkezelo`) a számítógépedre.
2. Dupla kattintás a `main.exe` fájlra.
3. Az alkalmazás elindul, és megnyitja a grafikus felületet a böngésződben vagy beágyazott ablakban.

---

### 📋 Használati útmutató

Miután a program elindul, a felület bal oldalán megjelennek a fő menüpontok. Az egyes oldalak funkciói a következők:

#### 🏠 Főoldal (`main_page`)
- Ez az alkalmazás kezdőoldala, ahová belépés után érkezel.
- Itt általános információkat és statisztikákat láthatsz a könyvtár adatbázisáról.
- Gyors gombokkal elérhetők a legfontosabb funkciók (pl. új könyv hozzáadása, kölcsönzés, visszavétel).

#### 📚 Könyvkezelés (CRUD oldal) (`crud_page`)
- Ezen az oldalon tudod a meglévő könyveket **listázni, szerkeszteni vagy törölni**.
- A könyvek táblázatos formában jelennek meg (`pandas` adatszerkezetekből töltve).
- Lehetőség van a könyvek adatait frissíteni (cím, szerző, kiadó, ISBN stb.)
- Egy kattintással törölhetsz is egy könyvet az adatbázisból.

#### ➕ Új könyv hozzáadása (`add_book_page`)
- Itt új könyveket vihetsz fel az adatbázisba.
- Kitölthető mezők például: **cím, szerző, ISBN, példányszám, kiadás éve, polc helye**.
- A mentés után a könyv automatikusan megjelenik a BOOKS listában is.
- A rendszer automatikusan hozzárendel egy azonosítót (ID-t) az új könyvhöz.

#### 📷 QR-kód generálás (`qr_page`)
- Ki választasz egy (vagy több könyvet), majd megadodd, hogy az adott könyvből mennyi qr-kódot szeretnél generálni, majd ezeket egy .docx fájlba generálja le.

#### 📥 Könyv visszavétele (Return book)
- Ez az oldal a kölcsönzött könyvek visszavételére szolgál.
- A visszavétel történhet:
  - könyv kiválasztásával a listából, majd a 'Return book' gomb megnyomásával a könyv visszavettnek tekintett
- A visszavétel után a könyv státusza frissül az adatbázisban (újra kölcsönözhető lesz).

---

### 💡 Tippek a felhasználóknak
- A navigáció egyszerű: a fenti menüből válaszd ki a kívánt oldalt.
- A változtatások automatikusan mentésre kerülnek.
- Ha új könyvet adsz hozzá, frissítsd a CRUD oldalt, hogy azonnal megjelenjen a listában.

---

### ⚠️ Fontos tudnivalók

- **Ne töröld a `credentials.json` és `secrets.json` fájlokat.** Ezek nélkül a rendszer nem tud hitelesíteni és adatokat elérni.
- Az adatok módosítása automatikusan mentésre kerül a háttérrendszerben.
- A program használatához aktív internetkapcsolat szükséges, ha a távoli adatbázist használja.

---

### ❓ Hibaelhárítás

| Hibaüzenet                          | Lehetséges ok                             | Megoldás                                |
|------------------------------------|-------------------------------------------|------------------------------------------|
| „credentials.json nem található”   | Hiányzik a fájl                           | Másold a fájlt a `main.exe` mellé         |
| „ModuleNotFoundError”               | Hiányzik egy modul a buildből             | Töltsd újra a legfrissebb `.exe` fájlt    |
| Nem tölt be a felület               | Nincs internetkapcsolat                   | Csatlakozz az internetre és próbáld újra |

---

### 📧 Kapcsolat

Ha problémát tapasztalsz a használat során, fordulj a fejlesztőhöz.
