from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithdaddy",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2026,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithdaddy", "A very nice book!", 5, 2001),
    Book(2, "Be Fast with FastAPI", "codingwithdaddy", "A great book!", 5, 1970),
    Book(3, "Master Endpoints", "codingwithdaddy", "An awesome book!", 5, 1971),
    Book(4, "HP1", "Author 1", "Book Description", 2, 1972),
    Book(5, "HP2", "Author 2", "Book Description", 3, 1973),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


def print_pairs(**kwargs):
    result = ", ".join(f"{k}: {v}" for k, v in kwargs.items())
    print(result)


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(book_published_date: int = Query(gt=0)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    # print(type(book_request))
    # print(book_request.model_dump())  # dict
    print_pairs(**book_request.model_dump())  # key value pairs
    # new_book = Book(**book_request.dict())
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update_books", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            # If we used `BOOKS[i] = book`, we would replace a Book object
            # with a BookRequest model instance. That would mix types in BOOKS
            # and could break later code that expects actual Book objects.
            # BOOKS[i] = book
            # print(f"Updated book with id {book.id}")
            updated_book = Book(**book.model_dump())
            BOOKS[i] = updated_book
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail=f"Book with id {book.id} not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
