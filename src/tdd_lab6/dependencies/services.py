from typing import Annotated

from fastapi import Depends

from tdd_lab6.services import ItemService
from .repositories import ItemRepositoryIoC


def get_item_service(repository: ItemRepositoryIoC) -> ItemService:
    return ItemService(repository=repository)


ItemServiceIoC = Annotated[ItemService, Depends(get_item_service)]
