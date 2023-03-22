from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)) -> list[schemas.User]:
    """Returns all users"""

    return db.query(models.User).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)) -> schemas.User:
    """Returns single user"""

    if user := db.query(models.User).filter(models.User.id == id).first():
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    user_query = db.query(models.User).filter(models.User.email == user.email)

    if user_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken."
        )

    # Hash user's password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# @router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
# def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     """Updates user"""

#     user_query = db.query(models.User).filter(models.User.id == id)

#     if not user_query.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User does not exist.",
#         )

#     user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
#     db.commit()

#     return user_query.first()


# @router.delete("/{id}")
# def delete_user(id: int, db: Session = Depends(get_db)):
#     """Deletes user account"""

#     user_query = db.query(models.User).filter(models.User.id == id)

#     if not user_query.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User does not exist.",
#         )

#     user_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
