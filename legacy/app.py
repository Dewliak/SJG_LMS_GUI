import json
from dataclasses import dataclass
from bookmodel import Book
from BookService import BookService




def give_back_book(item_id):
    book_service = BookService()
    item_id = "1224ce6e-c784-47b9-87a3-69155326acdc"

    book = book_service.get(item_id)
    quantity = book[0]["quantity"]
    lent = book[0]["lent"]
    if lent > 0:
        book_service.update(item_id, {"quantity": quantity + 1, "lent": lent - 1})
        return "Update Succesful"
    else:
        return "No more lent book"


if __name__ == "__main__":
    book_service = BookService()
    b = Book("Fizika", "Bob", 1243, 1)
    # book_service.add_book(b)
    # print(give_back_book(2))
    print(book_service.delete("1224ce6e-c784-47b9-87a3-69155326acdc"))

