import re

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from html2text import html2text

from worker import send

# Create the FastAPI app
app = FastAPI()


# Use pydantic to keep track of the input request payload
class Message(BaseModel):
    to: EmailStr
    to_name: str
    from_addr: EmailStr = Field(None, alias='from')
    from_name: str
    subject: str
    body: str


@app.post('/email')
def enqueue_add(msg: Message):

    # Convert message HTML into Markdown-like text
    msg.body = html2text(msg.body)

    # Enqueue task using celery's delay method
    send.delay(msg.dict())
