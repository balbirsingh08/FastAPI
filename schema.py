from pydantic import BaseModel, StrictInt, StrictStr
from typing import Optional


# POST Request Model
class CreateBookRequest(BaseModel):
    title: StrictStr
    author: StrictStr
    description: Optional[StrictStr] = None


# GET Response Model
class GetBookResponse(BaseModel):
    id: StrictInt
    title: StrictStr
    author: StrictStr
    description: Optional[StrictStr] = None


# PUT Request Model
class UpdateBookRequest(BaseModel):
    id: StrictInt  # The ID is still required to identify the book to update.
    title: Optional[StrictStr] = None
    author: Optional[StrictStr] = None
    description: Optional[StrictStr] = None


# DELETE Response Model
class DeleteBookResponse(BaseModel):
    message: StrictStr
