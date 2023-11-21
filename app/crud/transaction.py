from sqlalchemy.orm import Session

from app.crud.account import AccountCRUD
from app.models import Transaction
from app.schemas import TransactionUpdate


class TransactionCRUD:
    def create(self, db: Session, transaction: Transaction) -> Transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    def get_transaction_by_id(
        self, db: Session, transaction_id: int, user_id: int
    ) -> Transaction:
        return (
            db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
        )

    def get_account_transactions(
        self, db: Session, account_id: int, sorted: bool = False, skip: int = 0
    ) -> list[Transaction]:
        if sorted:
            return (
                db.query(Transaction)
                .filter_by(account_id=account_id)
                .order_by(Transaction.created_at.desc())
                .offset(skip)
            )
        return db.query(Transaction).filter_by(account_id=account_id).offset(skip).all()

    def get_all_transactions(self, db: Session, user_id: int) -> list[Transaction]:
        return db.query(Transaction).filter_by(user_id=user_id).all()

    def update(
        self, db: Session, transaction_id: int, transaction_update: TransactionUpdate
    ) -> Transaction:
        query = db.query(Transaction).filter_by(id=transaction_id)
        query.update(
            transaction_update.dict(exclude_unset=True), synchronize_session=False
        )
        transaction = query.first()
        db.commit()
        db.refresh(transaction)

        return transaction

    def delete(self, db: Session, transaction: Transaction):
        db.delete(transaction)
        db.commit()


transaction_crud = TransactionCRUD()
