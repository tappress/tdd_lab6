from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from beanie import PydanticObjectId

from tdd_lab6.exceptions.errors import ResourceNotFound
from tdd_lab6.models import Item
from tdd_lab6.repositories import ItemRepository
from tdd_lab6.schemas.item import CreateItem
from tdd_lab6.services import ItemService


@pytest.fixture
def mock_repository() -> AsyncMock:
    mock = AsyncMock(ItemRepository)
    return mock


@pytest_asyncio.fixture
async def item_service(mock_repository: AsyncMock) -> ItemService:
    return ItemService(repository=mock_repository)


@pytest.mark.asyncio
async def test_get_all_returns_items(
    item_service: ItemService, mock_repository: AsyncMock, test_items: list[Item]
) -> None:
    mock_repository.find_all.return_value = test_items
    items = await item_service.get_all()

    assert len(items) == len(test_items)
    mock_repository.find_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_returns_item(
    item_service: ItemService, mock_repository: AsyncMock, test_items: list[Item]
) -> None:
    test_item = test_items[0]
    mock_repository.find_by_id.return_value = test_item
    found_item = await item_service.get_by_id(test_item.id)

    assert found_item.id == test_item.id
    mock_repository.find_by_id.assert_called_once_with(test_item.id)


@pytest.mark.asyncio
async def test_get_by_non_existing_id_raises_error(
    item_service: ItemService, mock_repository: AsyncMock
) -> None:
    mock_repository.find_by_id.side_effect = ResourceNotFound("Item not found")

    with pytest.raises(ResourceNotFound):
        await item_service.get_by_id(PydanticObjectId())


@pytest.mark.asyncio
async def test_create_saves_new_item(
    item_service: ItemService, mock_repository: AsyncMock
) -> None:
    new_item_data = {
        "name": "Tablet",
        "code": "TB001",
        "description": "A powerful tablet.",
    }

    new_item = Item(**new_item_data)
    mock_repository.save.return_value = new_item

    await item_service.create(CreateItem(**new_item_data))

    # arguments are automatically captured, check if they are correctly passed to repository
    args, kwargs = mock_repository.save.call_args
    assert args[0].name == new_item_data["name"]
    assert args[0].code == new_item_data["code"]
    assert args[0].description == new_item_data["description"]

    mock_repository.save.assert_called_once_with(new_item)
