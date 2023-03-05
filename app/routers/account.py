from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models, oauth2, schemas

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Account])
def get_accounts(user_id: int, db: Session = Depends(get_db)):
    """Returns all user accounts"""

    accounts = db.query(models.Account).filter(models.Account.user_id == user_id).all()

    return accounts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Account)
def get_account(id: int, db: Session = Depends(get_db)):
    """Return single user account"""

    account = db.query(models.Account).filter(models.Account.id == id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account does not exist."
        )

    return account


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Account)
def create_account(
    Account: schemas.AccountCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    """Creates user account"""

    user = db.query(models.User).filter(models.User.id == Account.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    account = models.Account(**Account.dict(), owner=user)
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Account)
def update_account(
    id: int, account: schemas.AccountUpdate, db: Session = Depends(get_db)
):
    """Updates account"""

    post_query = db.query(models.Account).filter(models.User.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    post_query.update(account.dict(exclude_unset=True), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(id: int, db: Session = Depends(get_db)):
    """Deletes user account"""

    post_query = db.query(models.Account).filter(models.User.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
