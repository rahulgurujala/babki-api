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
    """Get all account transactions"""

    transactions = db.query(models.Transaction).all()

    return transactions


@router.get("/{account_id}", status_code=status.HTTP_200_OK)
def get_account_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Get all account transactions"""

    transactions = (
        db.query(models.Transaction).filter(models.Account.id == account_id).all()
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
