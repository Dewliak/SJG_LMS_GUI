from typing import Dict, Literal

translations = {
    "en": {
        # --- Main Page ---
        "All books": "All books",
        "Unique books": "Unique books",
        "Late books": "Late books",
        "Late book lends": "Late book lends",
        "ID": "ID",
        "NAME": "NAME",
        "CLASS": "CLASS",
        "EMAIL": "EMAIL",
        "BOOK_ID": "BOOK_ID",
        "END_DATE": "END_DATE",
        "STATUS": "STATUS",
        "Submit": "Submit",

        # --- CRUD Page ---
        "Author": "Author",
        "Title": "Title",
        "Quantity": "Quantity",
        "start typing": "start typing",
        "Update book": "Update book",
        "The book was edited successfully": "The book was edited successfully",
        "There was an error while editing the book": "There was an error while editing the book",
        "AUTHOR": "AUTHOR",
        "TITLE": "TITLE",
        "ISBN": "ISBN",
        "QUANTITY": "QUANTITY",
        "USED": "USED",
        "You can only delete books when there is 0 in usage.":"You can only delete books when there is 0 in usage.",
        "The book was deleted successfully!":"The book was deleted successfully!",
        "The was an error deleting the book!":"The was an error deleting the book!",
        "Do you want to delete it?": "Do you want to delete it?",
        
        # --- Book Return Page ---
        "Book returnal": "Return book",
        "Book return": "Book returned",
        "Book not found": "Book not found",
        "No lender was select": "No lender was selected",

        # --- QR Page ---
        "Print": "Print",
        "Print Amount": "Print Amount",
        "The QR-code document is being downloaded": "The QR-code document is being downloaded",

        # --- Header ---
        "Home": "Home",
        "Books": "Books",
        "Return book": "Return book",
        "Add book": "Add book",
        "QR Codes": "QR Codes",
        "Info": "Info",
    },
    "hu": {
        # --- Main Page ---
        "All books": "Összes könyv",
        "Unique books": "Egyedi könyvek",
        "Late books": "Késedelmes könyvek",
        "Late book lends": "Késedelmes kölcsönzések",
        "ID": "Azonosító",
        "NAME": "Név",
        "CLASS": "Osztály",
        "EMAIL": "E-mail",
        "BOOK_ID": "Könyv ID",
        "END_DATE": "Visszahozás dátuma",
        "STATUS": "Állapot", 
        "Submit": "Hozzáad",

        # --- CRUD Page ---
        "Author": "Szerző",
        "Title": "Cím",
        "Quantity": "Mennyiség",
        "start typing": "írd be",
        "Update book": "Könyv frissítése",
        "The book was edited successfully": "A könyv sikeresen frissítve",
        "There was an error while editing the book": "Hiba történt a könyv szerkesztése során",
        "AUTHOR": "Szerző",
        "TITLE": "Cím",
        "ISBN": "ISBN",
        "QUANTITY": "Mennyiség",
        "USED": "Használatban",
        "You can only delete books when there is 0 in usage.":"Csak olyan könyveket használhatsz, amik nincsenek használatban (USAGE=0)",
        "The book was deleted successfully!":"A könyv sikeresen törölve lett!",
        "The was an error deleting the book!":"Hiba történt a könyv törlése közben!",
        "Do you want to delete it?": "Biztosan ki akarod törölni?",
        # --- Book Return Page ---
        "Book returnal": "Könyvek visszahozása",
        "Book return": "A könyv visszahozva",
        "Book not found": "A könyvet nem találta",
        "No lender was select": "Nem lett kiválasztva kölcsönző",

        # --- QR Page ---
        "Print": "Nyomtatás",
        "Print Amount": "Példányszám",
        "The QR-code document is being downloaded": "A QR-kód dokumentum letöltése folyamatban",
        
        # --- Header
        "Home": "Otthon",
        "Books": "Könyvek",
        "Return book": "Könyv visszavétele",
        "Add book": "Könyv hozzáadása",
        "QR Codes": "QR kódok",
        "Info": "Információk",

    }
}

class Translator:
    dictionary: Dict[str, Dict[str, str]] = translations
    language: Literal['hu', 'en'] = 'hu'
    available_languages = ('en', ' hu')
    
    @classmethod
    def translate(cls, text: str):
        return Translator.dictionary[Translator.language][text]
    
    @classmethod
    def __class_getitem__(cls, key: str) ->str :
        return Translator.translate(key)



