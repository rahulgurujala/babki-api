from sqlalchemy.orm import Session

from app.models import Account
from app.schemas import AccountUpdate


class AccountRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, account: Account) -> Account:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account

    def get_account(self, account_id: int, user_id: int) -> Account:
        return self.db.query(Account).filter_by(id=account_id, user_id=user_id).first()

    def get_all_accounts(self, user_id: int) -> list[Account]:
        return self.db.query(Account).filter_by(user_id=user_id).all()

    def get_balance(self, account_id: int, user_id: int) -> float:
        return (
            self.db.query(Account.balance)
            .filter_by(id=account_id, user_id=user_id)
            .scalar()
        )

    def set_balance(self, account_id: int, balance: float) -> float:
        account = self.db.query(Account).filter_by(id=account_id).first()
        account.balance = balance
        self.db.commit()

        return account.balance

    def update(self, account_id: int, account_update: AccountUpdate) -> Account:
        query = self.db.query(Account).filter_by(id=account_id)
        query.update(account_update.dict(exclude_unset=True), synchronize_session=False)
        account = query.first()
        self.db.commit()
        self.db.refresh(account)

        return account

    def delete(self, account: Account):
        self.db.delete(account)
        self.db.commit()
