import pytest
import datetime
import json
from app import filter_recipes
from .conftest import client

ingreds = json.load(open('./data/ingredients.json'))["ingredients"]
recipes = json.load(open('./data/recipes.json'))["recipes"]

def test_filter():
    """
    Test whether the filter correctly removes ingredients past their useby date
    """

    #With useby date in the past
    d1 = datetime.datetime(2000,1,1,12,0)

    assert filter_recipes(recipes,ingreds,d1) == [] #all recipes are filtered

    #With useby in future
    d2 = datetime.datetime(2030,1,1,12,0)

    filtered = filter_recipes(recipes,ingreds,d2)

    #no recipes are filtered
    for r in recipes:
        assert r in filtered

    #With use-by in between
    d3 = datetime.datetime(2018,3,20,12,0)

    filtered = filter_recipes(recipes,ingreds,d3)

    check_ub(filtered,d3)

def test_best_before():
    """
    Test whether recipes with ingredients past their best-before date are placed last
    """

    d4 = datetime.datetime(2018,3,20,12,0)

    filtered = filter_recipes(recipes,ingreds,d4)

    check_bb(filtered,d4)


def test_get_request(client):
    """
    Integration test of GET /lunch
    """
    
    res = client.get('/lunch')

    filtered = res.get_json()["recipes"]

    d5 = datetime.datetime.now()

    check_ub(filtered,d5)
    check_bb(filtered,d5)


def check_bb(filtered, date):
    """
    Check recipes past best-before are put last in filtered list
    """

    ingred_d = {i["title"]:i["best-before"] for i in ingreds} #convert ingred list to best-before dict

    #Classifiy each recipe as past best-before or not
    for r in filtered:
        past_bb = False
        for ingred in r["ingredients"]:
            best_before = datetime.datetime.strptime(ingred_d[ing], "%Y-%m-%d")
            if date > best_before:
                past_bb = True
        r["past_bb"] = past_bb
        
    #Compare all recipes with each other
    for i1, r1 in enumerate(filtered):
        for i2, r2 in enumerate(filtered): 
            if r1["past_bb"] and not r2["past_bb"]:
                assert i1 > i2 #the past bb result should come after (index should be higher)


def check_ub(filtered,date):
    """
    Loop through each recipe. If any of its ingredients are past useby or unavailable, it should not be in filtered results, otherwise it should be.
    """

    ingred_d = {i["title"]:i["use-by"] for i in ingreds} #convert ingred list to use-by dict

    for recipe in recipes:
        excluded = False
        for ing in recipe["ingredients"]:
            if ing in ingred_d:
                use_by = datetime.datetime.strptime(ingred_d[ing], "%Y-%m-%d")
                if date > use_by:
                    excluded = True
            else:
                excluded = True
        if excluded:
            assert recipe not in filtered
        else:
            assert recipe in filtered