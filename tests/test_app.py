import pytest
from app import filter_recipes
from .conftest import client

def test_filter():
    """
    Test whether the filter correctly removes ingredients past their useby date
    """

    #With useby date in the past

    #With useby in future

    #With useby in between


    assert False


def test_best_before():
    """
    Test whether recipes with ingredients past their best-before date are placed last
    """
    assert False


def test_get_request(client):
    """
    Integration test of GET /lunch
    """
    assert False