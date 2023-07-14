from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas import TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def get_transaction_by_id(self, transaction_id: int, user_id: int) -> Transaction:
        return (
            self.db.query(Transaction)
            .filter_by(id=transaction_id, user_id=user_id)
            .first()
        )

    def get_account_transactions(self, account_id: int) -> list[Transaction]:
        return self.db.query(Transaction).filter_by(account_id=account_id).all()

    def get_all_transactions(self, user_id: int) -> list[Transaction]:
        return self.db.query(Transaction).filter_by(user_id=user_id).all()

    def update(
        self, transaction_id: int, transaction_update: TransactionUpdate
    ) -> Transaction:
        query = self.db.query(Transaction).filter_by(id=transaction_id)
        query.update(
            transaction_update.dict(exclude_unset=True), synchronize_session=False
        )
        transaction = query.first()
        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def delete(self, transaction: Transaction):
        self.db.delete(transaction)
        self.db.commit()
