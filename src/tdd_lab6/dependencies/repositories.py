from typing import Annotated

from fastapi import Depends

from tdd_lab6.repositories import ItemRepository


def get_item_repository():
    return ItemRepository()


ItemRepositoryIoC = Annotated[ItemRepository, Depends(get_item_repository)]
