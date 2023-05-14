from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2, schemas
from app.database import get_db
from app.models import Account, User
from app.repositories import AccountRepository


async def create(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account_repository = AccountRepository(db)
    account = Account(**account_create.dict(), user=current_user)

    return await account_repository.create(account)


async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Gets a user account"""

    account_repository = AccountRepository(db)
    account = await account_repository.get_account_by_id(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    return account


async def get_all_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> list[schemas.Account]:
    """Gets all user account"""

    account_repository = AccountRepository(db)

    return await account_repository.get_all_accounts(current_user.id)


async def update(
    account_id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Updates user account"""

    account_repository = AccountRepository(db)
    account = await account_repository.get_account_by_id(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return await account_repository.update(account_id, account_update)


async def delete(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Deletes user account"""

    account_repository = AccountRepository(db)
    account = await account_repository.get_account_by_id(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return await account_repository.delete(account)
