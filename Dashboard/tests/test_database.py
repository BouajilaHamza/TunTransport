from unittest.mock import MagicMock

import pytest

from Dashboard.utils.database import (  # Adjust the import based on your file structure
    get_dests_from_mongo,
)


@pytest.fixture
def mock_mongo(mocker):
    # Mock MongoDB client and collection
    mock_client = mocker.patch("pymongo.MongoClient")
    mock_collection = MagicMock()
    mock_client.return_value["Transport"]["Destinations"] = mock_collection
    return mock_collection


@pytest.fixture
def mock_redis(mocker):
    # Mock Redis connection
    mock_redis_instance = mocker.patch("redis.Redis")
    return mock_redis_instance


def test_get_dests_from_mongo(mock_mongo):
    # Set up the return value for clean_filter
    mock_mongo.find.return_value = [{"_id": "1", "Name": "Destination A"}]

    selected_departure = {"Name": "Departure A", "Id": "1", "Company": "Company A"}
    mongo_filter = {"Company": {"$in": ["Company A"]}}

    _, clean_dests = get_dests_from_mongo(mock_mongo, selected_departure, mongo_filter)
    assert len(clean_dests) == 1
    assert clean_dests[0] == "Destination A"


# def test_get_dests_from_redis(mock_redis):
#     # Mock the search method of Redisearch
#     mock_redis.ft.return_value.search.return_value.docs = [
#         {"json": json.dumps({"Name": "Destination B", "Id": 2, "Company": "Company B"})}
#     ]

#     results = get_dests_from_redis(company="Company B")

#     assert len(results) == 1
#     assert json.loads(results[0]["json"])["Name"] == "Destination B"


# def test_get_data(mock_mongo, mock_redis):
#     # Mock Redis to return no results initially
#     mock_redis.ft.return_value.search.return_value.docs = []

#     # Mock MongoDB response
#     mock_mongo.find.return_value = [{"_id": "2", "Name": "Destination C", "Id": 2}]

#     selected_departure = {"Name": "Departure B", "Id": "2", "Company": "Company B"}
#     search_filter = {"Company": {"$in": ["Company B"]}, "Depart": None}

#     raw_dests, _ = get_data(mock_mongo, selected_departure, search_filter)

#     assert len(raw_dests) == 1
#     assert raw_dests[0] == "Destination C"

#     # Ensure that the data is cached in Redis after fetching from MongoDB
#     mock_redis.json().set.assert_called_once()
#     args, kwargs = mock_redis.json().set.call_args
#     assert args[0] == f"destination:{str(raw_dests[0]['_id'])}"
#     assert json.loads(args[1]) == raw_dests[0]
