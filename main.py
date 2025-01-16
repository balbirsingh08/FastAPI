from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
from exceptions import CustomHTTPException
from schema import CreateBookRequest, GetBookResponse, UpdateBookRequest, DeleteBookResponse
import os
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

# In-memory database for books
books: List[dict] = [
    {"id": 1, "title": "1984", "author": "George Orwell", "description": "Dystopian novel about surveillance."},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "description": "Novel about racial injustice."},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "description": "Romantic novel set in the 19th century."},
    {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "description": "Novel about the American dream."},
    {"id": 5, "title": "Moby Dick", "author": "Herman Melville", "description": "A story of a captain's obsession with a whale."},
    {"id": 6, "title": "War and Peace", "author": "Leo Tolstoy", "description": "Historical novel about Napoleonic wars."},
    {"id": 7, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "description": "A story about teenage rebellion."},
    {"id": 8, "title": "The Hobbit", "author": "J.R.R. Tolkien", "description": "Fantasy novel about a hobbit's journey."},
    {"id": 9, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "description": "A young wizard's adventure begins."},
    {"id": 10, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "description": "Epic fantasy about the fight against evil."},
]
# Directory to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# POST /upload - Upload a file
@app.post("/upload", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file.

    Args:
    - file (UploadFile): The file being uploaded.

    Returns:
    - dict: A success message with the file name.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file to the server
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    return {"message": f"File '{file.filename}' uploaded successfully."}

# GET /files - List all uploaded files
@app.get("/files", response_model=List[str])
async def list_files():
    """
    Endpoint to list all uploaded files.

    Returns:
    - List[str]: A list of file names in the upload directory.
    """
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=404, detail="No files found")
    return files

# GET /files/{filename} - Download a specific file
@app.get("/files/{filename}")
async def download_file(filename: str):
    """
    Endpoint to download a specific file.

    Args:
    - filename (str): The name of the file to download.

    Returns:
    - FileResponse: The file for download.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    
# POST /books - Add a new book
@app.post("/books", status_code=201, response_model=GetBookResponse)
def create_book(book: CreateBookRequest):
    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {"id": new_id, **book.dict()}
    books.append(new_book)
    return new_book

# GET /books - Retrieve all books
@app.get("/books", response_model=List[GetBookResponse])
def get_books():
    if not books:
        raise CustomHTTPException(
            status_code=404, 
            detail="No books found", 
            error_code="BOOKS_NOT_FOUND"
        )
    return books

# GET /books/{id} - Get details of a specific book
@app.get("/books/{id}", response_model=GetBookResponse)
def get_book(id: int):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        raise CustomHTTPException(
            status_code=404, 
            detail=f"Booooook with ID {id} not found", 
            error_code="BOOK_NOT_FOUND"
        )
    return book

@app.put("/books/{id}", response_model=GetBookResponse)
def update_book(id: int, updated_book: UpdateBookRequest):
    # Validate that the ID in the path matches the ID in the body, if provided
    if updated_book.id != id:
        raise CustomHTTPException(
            status_code=400,
            detail="ID in path and body must match",
            error_code="ID_MISMATCH"
        )
    
    # Find the book to update
    for book in books:
        if book["id"] == id:
            # Update only fields provided in the request payload
            if updated_book.title is not None:
                book["title"] = updated_book.title
            if updated_book.author is not None:
                book["author"] = updated_book.author
            if updated_book.description is not None:
                book["description"] = updated_book.description
            return book
    
    # Raise error if the book is not found
    raise CustomHTTPException(
        status_code=404,
        detail=f"Book with ID {id} not found",
        error_code="BOOK_NOT_FOUND"
    )


# DELETE /books/{id} - Delete a book
@app.delete("/books/{id}", response_model=DeleteBookResponse)
def delete_book(id: int):
    global books
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        raise CustomHTTPException(
            status_code=404, 
            detail=f"Book with ID {id} not found", 
            error_code="BOOK_NOT_FOUND"
        )
    books = [b for b in books if b["id"] != id]
    return {"message": f"Book with ID {id} deleted successfully"}