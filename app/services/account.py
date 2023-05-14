from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2, schemas, utils
from app.database import get_db
from app.models import Account
from app.repositories import AccountRepository


async def create_account(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: Account = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account = Account(**account_create.dict(), user_id=current_user.id)
