from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/my_chats", response_model=List[schemas.ChatOut])
def get_user_chats(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    try:
        chats = (
            db.query(models.Chat)
            .filter(
                (models.Chat.user1_id == current_user.id)
                | (models.Chat.user2_id == current_user.id)
            )
            .order_by(models.Chat.created_at.desc())
            .all()
        )

        return [schemas.ChatOut.model_validate(chat) for chat in chats]

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
