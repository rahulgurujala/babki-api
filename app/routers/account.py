from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models
from ..schemas import *

router = APIRouter(prefix="/user", tags=["Accounts"])


@router.post("/account", status_code=status.HTTP_201_CREATED)
def create_account(Account: AccountIn, db: Session = Depends(get_db)):
    """Creates user account"""

    user = db.query(models.User).filter(models.User.id == Account.user_id).first()
    print(dir(user))

    user.accounts.append(models.Account(**Account.dict()))
    db.add(user)
    db.commit()
    db.refresh(user)
    # print(user)

    # accounts = models.Account(owner=user, **Account.dict())
    # db.add(accounts)
    # db.commit()
    # db.refresh(accounts)

    return {"data": user}


@router.get("/accounts", status_code=status.HTTP_200_OK)
def get_accounts(db: Session = Depends(get_db)):
    """Gets all user accounts"""

    accounts = db.query(models.Account).all()

    return accounts
