from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models
from ..schemas import *

router = APIRouter("/{user_id}/account", tags=["Accounts"])


@router.post("/")
def create_account(user_id: int, Account: AccountIn, db: Session = Depends(get_db)):
    """Creates user account"""

    account = models.Account(**Account.dict())

    db.add(account)
    db.commit()

    return {"data": account}
