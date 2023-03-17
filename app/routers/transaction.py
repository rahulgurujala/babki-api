from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2
from app.database import get_db

from .. import models, schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Transaction]:
    """Get all user transactions"""

    transactions = db.query(models.Transaction).all()

    return transactions


@router.get("/{account_id}", status_code=status.HTTP_200_OK)
def get_account_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Transaction]:
    """Get all account transactions"""

    account = db.query(models.Account).filter(models.Account.id == account_id).first()

    if not account:
        raise HTTPException(404, detail="Account does not exist.")

    transactions = (
        db.query(models.Transaction)
        .filter(models.Transaction.account_id == account_id)
        .all()
    )

    return transactions


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    Transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
) -> schemas.Transaction:
    """Create transcation"""

    transaction = models.Transaction(**Transaction.dict())

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

    if not transaction_query.first():
        raise HTTPException(404, detail=f"Transaction of id {id} does not exist.")

    transaction_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_transaction(
    id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.user = Depends(oauth2.get_current_user),
):
    """Update account transaction"""

    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)

    if not transaction_query.first():
        raise HTTPException(404, detail=f"Transaction of id {id} does not exist.")

    transaction_query.update(
        transaction.dict(exclude_unset=True), synchronize_session=False
    )
    db.commit()

    return transaction_query.first()
