from fastapi import FastAPI, Body

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

app = FastAPI()

# GET


@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello World"}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{dynamic_param}")
async def read_book(dynamic_param: str):
    # return {"dynamic_param": dynamic_param}
    for book in BOOKS:
        if book.get("title").casefold() == dynamic_param.casefold():
            return book
    return {"message": "Book not found"}


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_autho_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            if book.get("category").casefold() == category.casefold():
                books_to_return.append(book)
    return books_to_return


# POST


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# PUT


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
