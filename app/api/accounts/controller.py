from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT
from pydantic import UUID7

from .deps import provide_accounts_repo
from .repositories import AccountRepository
from .schemas import Account, AccountReadDto, AccountUpdatePartial, CreateAccount, GetAccount


class AccountController(Controller):
    """User Account Controller"""

    path = "/accounts"
    tags = ["User Accounts"]
    dependencies = {"accounts_repo": Provide(provide_accounts_repo)}
    return_dto = AccountReadDto

    @post(status_code=HTTP_201_CREATED)
    async def create_account(self, data: CreateAccount, accounts_repo: AccountRepository) -> Account:
        """Create a new account"""

        account = await accounts_repo.get_by_email(email=data.email)
        if account:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Account is already exist")

        obj = await accounts_repo.create(data=data)
        return Account.model_validate(obj)

    @post(path="/login")
    async def login(self, data: GetAccount, accounts_repo: AccountRepository) -> Account:
        """Login account"""

        account = await accounts_repo.check_email_and_password(data=data)
        if account is None:
            raise NotFoundException(detail="Account not found")

        return Account.model_validate(account)

    @get(path="/{account_id:uuid}")
    async def get_account(self, account_id: UUID7, accounts_repo: AccountRepository) -> Account:
        """Get an existing account"""

        try:
            obj = await accounts_repo.get(account_id)
            return Account.model_validate(obj)
        except NotFoundError:
            raise NotFoundException(detail=f"Account with ID {account_id} not found")

    @patch(path="/{account_id:uuid}", status_code=HTTP_201_CREATED)
    async def partial_update_account(
        self, account_id: UUID7, data: AccountUpdatePartial, accounts_repo: AccountRepository
    ) -> Account:
        """Update a account"""

        try:
            obj = await accounts_repo.update_partial(account_id=account_id, data=data)
            return Account.model_validate(obj)
        except NotFoundError:
            raise NotFoundException(detail=f"Account with ID {account_id} not found")

    @delete(path="/{account_id:uuid}")
    async def delete_account(self, account_id: UUID7, accounts_repo: AccountRepository) -> None:
        """Delete an existing account"""

        try:
            await accounts_repo.delete(account_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Account with ID {account_id} not found")
