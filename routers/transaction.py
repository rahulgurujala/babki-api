from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Transaction]:
    """Get all user transactions"""

    transactions = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == current_user.id)
        .all()
    )

    return transactions


@router.get("", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK, include_in_schema=False)
def get_account_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Transaction]:
    """Get all account transactions"""

    account = db.query(models.Account).filter(models.Account.id == account_id).first()

    if not account:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Account does not exist.")

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    transactions = (
        db.query(models.Transaction)
        .filter(models.Transaction.account_id == account_id)
        .all()
    )

    return transactions


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_transaction(
    transaction_create: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Transaction:
    """Create transcation"""

    if transaction_create.user_id != current_user.id:
        raise HTTPException(403, detail="Not authorized to perform action.")

    account = (
        db.query(models.Account)
        .filter(models.Account.id == transaction_create.account_id)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with id: {transaction_create.account_id} for this user does not exist.",
        )

    transaction = models.Transaction(**transaction_create.dict())

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Delete account transaction"""

    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
    transaction = transaction_query.first()

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    if transaction.user_id != current_user.id:
        raise HTTPException(403, detail="Not authorized to perform action.")

    transaction_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_transaction(
    id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.user = Depends(oauth2.get_current_user),
) -> schemas.Transaction:
    """Update account transaction"""

    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
    transaction = transaction_query.first()

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    if transaction.user_id != current_user.id:
        raise HTTPException(403, detail="Not authorized to perform action.")

    transaction_query.update(
        transaction_update.dict(exclude_unset=True), synchronize_session=False
    )
    db.commit()

    return transaction_query.first()
