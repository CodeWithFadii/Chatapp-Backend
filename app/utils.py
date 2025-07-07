import os
from fastapi import UploadFile
from passlib.context import CryptContext

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def save_uploaded_image(file: UploadFile, filename: str, folder: str = "media") -> str:
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    # Return full public URL
    return f"http://13.53.34.41/{folder}/{filename}"
