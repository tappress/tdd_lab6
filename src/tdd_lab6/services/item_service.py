import logging

from beanie import PydanticObjectId

from tdd_lab6.exceptions.errors import ResourceNotFound
from tdd_lab6.models import Item
from tdd_lab6.repositories import ItemRepository
from tdd_lab6.schemas.item import CreateItem

logger = logging.getLogger(__name__)


class ItemService:
    def __init__(self, repository: ItemRepository):
        self._repository = repository

    async def get_all(self) -> list[Item]:
        logger.info(" --------------  GET ALL ------------------")

        return await self._repository.find_all()

    async def get_by_id(self, id_: PydanticObjectId) -> Item:
        logger.info(f"request for id = {id_}")

        item = await self._repository.find_by_id(id_)

        if not item:
            raise ResourceNotFound(f"Item with id = {id_} not found")

        return item

    async def create(self, item: CreateItem) -> Item:
        logger.info(f"request for creation = {item}")

        db_item = Item.model_validate(item, from_attributes=True)
        return await self._repository.save(db_item)

    async def delete(self, id_: PydanticObjectId) -> None:
        logger.info(f"delete id = {id_}")

        item = await self._repository.find_by_id(id_)

        if not item:
            raise ResourceNotFound(f"Item with id = {id_} not found")

        await self._repository.delete_by_id(id_)
