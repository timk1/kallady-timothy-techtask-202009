from flask import Flask, jsonify
from flasgger import Swagger
import json

app = Flask(__name__)

swagger = Swagger(app)

@app.route('/lunch', methods=('GET',))
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

    #Filter recipes

    #Return recipe list

    return jsonify({"recipes":[]})

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

    #Remove ingredients past their use-by

    #Determine what recipes can be made, and whether they are past best before date

    return []


if __name__ == "__main__":
    app.run(debug=True)
