from sqlalchemy.orm import Session

from app.models import Account
from app.schemas import AccountUpdate


class AccountCRUD:
    def create(self, db: Session, account: Account) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    def get_account(self, db: Session, account_id: int, user_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id, user_id=user_id).first()

    def get_all_accounts(self, db: Session, user_id: int) -> list[Account]:
        return db.query(Account).filter_by(user_id=user_id).all()

    def get_balance(self, db: Session, account_id: int, user_id: int) -> float:
        return (
            db.query(Account.balance).filter_by(id=account_id, user_id=user_id).scalar()
        )

    def set_balance(self, db: Session, account_id: int, balance: float) -> float:
        account = db.query(Account).filter_by(id=account_id).first()
        account.balance = balance
        db.commit()

        return account.balance

    def update(
        self, db: Session, account_id: int, account_update: AccountUpdate
    ) -> Account:
        query = db.query(Account).filter_by(id=account_id)
        query.update(account_update.dict(exclude_unset=True), synchronize_session=False)
        account = query.first()
        db.commit()
        db.refresh(account)

        return account

    def delete(self, db: Session, account: Account):
        db.delete(account)
        db.commit()


account = AccountCRUD()
