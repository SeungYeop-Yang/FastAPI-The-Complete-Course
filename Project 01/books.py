from fastapi import FastAPI

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

app = FastAPI()


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
        if book["title"].casefold() == dynamic_param.casefold():
            return book
    return {"message": "Book not found"}
