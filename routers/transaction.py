from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.services import transaction as transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_create: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Transaction:
    """Create transaction"""

    transaction = await transaction_service.create(
        {**transaction_create.dict(), "user_id": current_user.id}, db
    )

    return transaction


@router.get("/{id}", status_code=200)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Transaction:
    """Gets an account transaction"""

    return await transaction_service.get_transaction(
        current_user.id, transaction_id, db
    )


@router.get("/", status_code=200)
async def get_all_transactions(
    account_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Transaction]:
    """Get all transactions

    Returns:
    - All transactions for an account if account_id is passed
    - All user transactions if account_id is not passed

    """

    if account_id:
        return await transaction_service.get_account_transactions(
            current_user.id, account_id, db
        )

    return await transaction_service.get_all_transactions(current_user.id, db)


@router.patch("/{id}", status_code=200)
async def update_transaction(
    id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Transaction:
    """Update account transaction"""

    transaction = await transaction_service.get_transaction(current_user.id, id, db)

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    if transaction.amount != transaction_update.amount:
        transaction = await transaction_service.update(
            current_user.id, id, transaction_update, db
        )

    return transaction


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Delete account transaction"""

    transaction = await transaction_service.get_transaction(current_user.id, id, db)

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    transaction = await transaction_service.delete(current_user.id, id, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
