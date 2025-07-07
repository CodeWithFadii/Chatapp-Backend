from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(tags=["Authentication"])


# Existing login route
@router.post("/login", response_model=schemas.UserAuthOut)
def login(credential: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(models.User).filter(credential.user_name == models.User.user_name).first()  # type: ignore
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )

        if not utils.verify_password(credential.password, user.password) is True:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password",
            )

        access_token = oauth2.create_access_token({"user_id": str(user.id)})

        return schemas.UserAuthOut(
            access_token=access_token,
            token_type="bearer",
            user=schemas.User.model_validate(user),
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


# Existing register route
@router.post(
    "/register", response_model=schemas.UserAuthOut, status_code=status.HTTP_200_OK
)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        existing = (
            db.query(models.User)
            .filter(models.User.user_name == user.user_name)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user name is taken",
            )

        hashed_password = utils.get_password_hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = oauth2.create_access_token({"user_id": str(new_user.id)})
        return schemas.UserAuthOut(
            access_token=access_token,
            token_type="bearer",
            user=schemas.User.model_validate(new_user),
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


# Existing change password route
@router.post("/change_password")
def change_password(request: schemas.ChangePassword, db: Session = Depends(get_db)):
    try:
        # Find the user
        existing = (
            db.query(models.User)
            .filter(models.User.user_name == request.user_name)
            .first()
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )

        # Check if old password is correct
        is_verified = utils.verify_password(request.old_password, existing.password)  # type: ignore
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password",
            )

        # Update to new hashed password
        hashed_password = utils.get_password_hash(request.new_password)
        existing.password = hashed_password  # type: ignore
        db.commit()

        return schemas.ChangePasswordOut(
            success=True, message="Password changed successfully"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


# Change name route
@router.post("/change_name", response_model=schemas.User)
def change_name(
    request: schemas.ChangeName,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    try:
        # Get current user from DB
        db_user = (
            db.query(models.User).filter(models.User.id == current_user.id).first()
        )
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )

        # Update name
        db_user.name = request.name  # type: ignore
        db.commit()
        db.refresh(db_user)

        return schemas.User.model_validate(db_user)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
