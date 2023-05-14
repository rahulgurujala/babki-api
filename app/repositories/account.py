from sqlalchemy.orm import Session

from app.models import Account
from app.schemas import AccountUpdate


class AccountRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_account(self, account: Account) -> Account:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account

    async def get_account_by_id(self, account_id: int) -> Account:
        return self.db.query(Account).filter_by(id=account_id).first()

    async def get_all_accounts(self, user_id: int) -> list[Account]:
        return self.db.query(Account).filter_by(user_id=user_id).all()

    async def update_account(
        self, account_id: int, account_update: AccountUpdate
    ) -> Account:
        query = self.db.query(Account).filter_by(id=account_id)
        account = query.first()
        query.update(account_update.dict(exclude_unset=True), synchronize_session=False)
        self.db.commit()
        self.db.refresh(account)

        return account

    async def delete_account(self, account: Account):
        self.db.delete(account)
        self.db.commit()
