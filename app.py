from flask import Flask, jsonify
from flasgger import Swagger
import json
import copy
import datetime

app = Flask(__name__)

swagger = Swagger(app)

@app.route("/lunch", methods=("GET",))
def lunch():
    """
    Reads recipes and ingredients data and returns JSON with available recipes.
    Ingredients past their use-by are excluded. Recipes with ingredients before 
    their use-by but past their best-before are placed at the bottom of the list.
    ---

    definitions: 
        Recipe:
            type: object
            properties:
                title:
                    type: string
                ingredients:
                    type: array
                    items:
                        type: string

    responses:
        200:
            description: A list of available recipes
            schema:
                recipes:
                    type: array
                    items:
                        $ref: '#/definitions/Recipe'

    """
    #Read json data
    ingreds = json.load(open("./data/ingredients.json"))["ingredients"]
    recipes = json.load(open("./data/recipes.json"))["recipes"]

    #Filter recipes
    d = datetime.datetime.now()
    filtered = filter_recipes(recipes,ingreds,d)

    #Return filtered recipe list

    return jsonify({"recipes":filtered})

def filter_recipes(recipes,ingredients,test_date):
    """
    Filter recipes by ingredient use-by and order by ingredient best-before

    Args:
        recipes (list): List of recipe dicts.
        ingredients (list): List of ingredient dicts.
        test_date (datetime): Datetime object of date to compare useby/best-before with.

    Returns:
        list: List of filtered and ordered recipe dicts.
    """

    #Convert recipes and ingredients to dicts
    r_d = {r["title"]:r["ingredients"] for r in recipes}
    i_d = {i["title"]:{"use-by":i["use-by"],"best-before":i["best-before"]} for i in ingredients}

    recipe_cp = copy.deepcopy(recipes)

    #Classify recipes as past their best-before
    for r in recipe_cp:
        past_bb = False
        for ing in r["ingredients"]:
            if (ing in i_d) and test_date > datetime.datetime.strptime(i_d[ing]["best-before"],"%Y-%m-%d"):
                past_bb = True
        r["past_bb"] = past_bb

    #Create new filtered recipe list
    l1 = [] #For recipes not past best before
    l2 = [] #For recipes past best before

    for r in recipe_cp:
        past_bb = False
        available = True
        for ing in r["ingredients"]:
            if (ing in i_d) and (test_date <= datetime.datetime.strptime(i_d[ing]["use-by"],"%Y-%m-%d")):
                if r["past_bb"]:
                    past_bb = True
            else:
                available = False
        if available:
            if not past_bb:
                l1.append(r)
            else:
                l2.append(r)

    res = l1 + l2
    for r in res:
        r.pop("past_bb",None)
    return res


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
